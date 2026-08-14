#!/usr/bin/env python3
"""
BUGSENSE — predict the NEXT bug by finding new instances of bugs that already happened.

WHY THIS EXISTS
  Every defect in this repo was found the same way: it shipped, an eye or an ear caught
  it, and it became a lesson. That loop works but it is paid for in credits and time.
  Four of them were not craft mistakes at all — they were STRUCTURAL, decidable from the
  source code alone, before anything ran:

    2026-08-05  BLEND_AS_OVERLAP and GENERATE_AUDIO were declared in plans/crown.py to
                fix a defect list. Neither had a single reader anywhere in the repo. A
                claimed capability, committed inside the fix for a defect list.
    2026-08-06  engine.py:781 reads SOUND["hero_shot"] with a silent default of 0.
                plans/crown.py defined "hero", not "hero_shot". The one combustion sound
                in a 30s silent film would have landed at t=0.00s, 14.00s early, on a
                278cr build. No gate looked at it.
    2026-08-06  verify.py called glob.glob() at module scope but only ever imported glob
                LOCALLY as _g inside two other functions. NameError on every call,
                swallowed by a bare except, so the relight budget silently fell back to
                18.0 for every pillar forever.
    2026-08-06  verify.py CHECK 0 globbed only "LC300_*.mp4". On crown/kk/wrx/supra the
                freshness gate compared the output against nothing and always passed —
                the check that gates all fourteen others was inert on five of six
                projects.

  All four are the same shape: A DECLARATION AND ITS READER DISAGREED, AND NOTHING SAID
  SO. That is a class, not four accidents, and a class can be scanned for.

WHAT IT IS NOT
  Not a linter, not a type checker, not a judge of craft. It cannot tell you a shot is
  boring or a bed is the wrong genre. It reads source text and reports DISAGREEMENTS.
  Everything it prints is a fact about the code, with a file and a line, or it is not
  printed. It never guesses.

  It imports nothing from the pipeline and writes nothing. Run it or delete it; the repo
  behaves identically either way.

THE FOUR CLASSES
  1 UNMET CONTRACT   a pipeline file reads a plan key with a SILENT DEFAULT, and a plan
                     does not define it. The build runs and is quietly wrong.
                     (the hero_shot class — the expensive one)
  2 INERT DECLARATION a plan declares a name that NO pipeline file reads. The plan claims
                     a capability the code does not have.
                     (the BLEND_AS_OVERLAP class)
  3 NAME SHADOW      a module uses `X.` where X is only imported INSIDE some other
                     function. NameError at runtime, usually swallowed.
                     (the glob class)
  4 FOREIGN LITERAL  shared pipeline code hardcodes one project's or pillar's name, so it
                     silently does nothing for every other project.
                     (the LC300_ class)

Usage
  python3 tools/bugsense.py                 # scan everything
  python3 tools/bugsense.py --class 1       # one class only
  python3 tools/bugsense.py --plan crown    # contracts for one plan
  python3 tools/bugsense.py --json out.json

Exit codes
  0  nothing found
  1  at least one finding
  2  could not scan (bad path)
"""
import argparse, ast, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANS = os.path.join(HERE, "plans")

# The files that ARE the pipeline. A plan is data; these are the code that reads it.
PIPELINE = ["engine.py", "planqc.py", "verify.py", "clipqc.py", "board.py", "talyx.py"]

FINDINGS = []   # (cls, severity, where, what, why)


def add(cls, sev, where, what, why):
    FINDINGS.append({"class": cls, "severity": sev, "where": where,
                     "what": what, "why": why})


def _read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def _pipeline_files():
    out = []
    for f in PIPELINE:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            out.append(p)
    td = os.path.join(HERE, "tools")
    if os.path.isdir(td):
        for f in sorted(os.listdir(td)):
            if f.endswith(".py") and f != "bugsense.py":
                out.append(os.path.join(td, f))
    return out


def _plan_files(only=None):
    if not os.path.isdir(PLANS):
        return []
    out = []
    for f in sorted(os.listdir(PLANS)):
        if not f.endswith(".py") or f.startswith("__"):
            continue
        if only and f[:-3] != only:
            continue
        out.append(os.path.join(PLANS, f))
    return out


def plan_toplevel_names(path):
    """Top-level assigned names in a plan, via AST. Never imports the plan."""
    try:
        tree = ast.parse(_read(path))
    except SyntaxError as e:
        add(0, "BLOCK", f"{os.path.relpath(path, HERE)}:{e.lineno}",
            f"plan does not parse: {e.msg}",
            "planqc cannot import it; it will report 'no plan module' and exit 2, "
            "which masks the real cause.")
        return {}, {}
    names, dict_keys = {}, {}
    for node in tree.body:
        tgts = []
        if isinstance(node, ast.Assign):
            tgts = [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            tgts = [node.target.id]
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            tgts = [node.name]
        for t in tgts:
            names[t] = node.lineno
        # record dict literal keys so we can check SOUND["hero_shot"]-style contracts
        val = getattr(node, "value", None)
        if isinstance(val, ast.Dict) and len(tgts) == 1:
            ks = set()
            for k in val.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    ks.add(k.value)
            dict_keys[tgts[0]] = ks
    return names, dict_keys


# ---------------------------------------------------------------- CLASS 1
# A pipeline file reads a plan attribute or a plan-dict key WITH A DEFAULT, and the
# plan does not define it. With no default the plan would crash loudly and you would
# know. With a default it runs and is silently wrong. That asymmetry is the whole point.
RE_GETATTR = re.compile(r"getattr\(\s*P\s*,\s*[\"'](\w+)[\"']\s*,\s*([^)]+)\)")
RE_DICTGET = re.compile(
    r"(?:getattr\(\s*P\s*,\s*[\"'](\w+)[\"'][^)]*\)|P\.(\w+))"      # the dict
    r"(?:\s*or\s*\{\})?\s*\)?"
    r"\s*\.get\(\s*[\"']([\w]+)[\"']\s*,\s*([^),]+)")               # .get("key", default)


def scan_contracts(plan_only=None):
    reads_attr, reads_key = {}, {}
    for p in _pipeline_files():
        rel = os.path.relpath(p, HERE)
        for i, ln in enumerate(_read(p).splitlines(), 1):
            if ln.lstrip().startswith("#"):
                continue
            for m in RE_GETATTR.finditer(ln):
                reads_attr.setdefault(m.group(1), []).append((rel, i, m.group(2).strip()))
            for m in RE_DICTGET.finditer(ln):
                dct = m.group(1) or m.group(2)
                if not dct or not dct.isupper():
                    continue
                reads_key.setdefault((dct, m.group(3)), []).append(
                    (rel, i, m.group(4).strip()))

    for pf in _plan_files(plan_only):
        pname = os.path.basename(pf)[:-3]
        names, dkeys = plan_toplevel_names(pf)
        if not names:
            continue
        for (dct, key), sites in sorted(reads_key.items()):
            if dct not in names:
                continue                      # plan does not use that dict at all
            if key in dkeys.get(dct, set()):
                continue                      # declared: contract met
            rel, line, dflt = sites[0]
            add(1, "HIGH", f"plans/{pname}.py",
                f"{dct}[\"{key}\"] is NOT defined, but {rel}:{line} reads it "
                f"and silently defaults to {dflt}",
                "The build will run and be quietly wrong. This is the exact shape of "
                "the hero_shot bug: one missing key put the only sound in a 30s film "
                "14.00s early on a 278cr plan, and no gate could see it.")


# ---------------------------------------------------------------- CLASS 2
def scan_inert(plan_only=None):
    """A plan name that NO pipeline file mentions. The plan claims something the code
    cannot do. Compared against the WHOLE repo, so a name used only by a doc generator
    or a board still counts as read."""
    blob = {}
    for p in _pipeline_files():
        blob[os.path.relpath(p, HERE)] = _read(p)

    # names every plan carries that are read via P.<NAME> generically, plus the two
    # callables planqc requires. Listed so they are never reported as inert.
    ALWAYS = {"timeline", "cost", "PROJECT", "PILLAR"}

    for pf in _plan_files(plan_only):
        pname = os.path.basename(pf)[:-3]
        names, _ = plan_toplevel_names(pf)
        for nm, line in sorted(names.items(), key=lambda x: x[1]):
            if nm.startswith("_") or nm in ALWAYS:
                continue
            pat = re.compile(r"[\"']" + re.escape(nm) + r"[\"']|\bP\." + re.escape(nm) + r"\b")
            hit = any(pat.search(t) for t in blob.values())
            if not hit:
                add(2, "MED", f"plans/{pname}.py:{line}",
                    f"{nm} is declared but NO pipeline file reads it",
                    "Either it is a note — say so in the file — or it is a claimed "
                    "capability. BLEND_AS_OVERLAP and GENERATE_AUDIO were exactly this, "
                    "committed inside the plan written to fix a defect list.")


# ---------------------------------------------------------------- CLASS 3
RE_LOCAL_IMPORT = re.compile(r"^\s+import\s+(\w+)\s+as\s+(\w+)\s*$")
RE_TOP_IMPORT = re.compile(r"^import\s+(.+)$|^from\s+\S+\s+import\s+(.+)$")


def _imports_of(node):
    """Names bound by import statements DIRECTLY inside this scope (not nested defs)."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                out.add((al.asname or al.name).split(".")[0])
    return out


def _direct_imports(node):
    """Imports in this function's own body, excluding nested function bodies."""
    out = set()
    stack = list(node.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue                                   # nested scope: not ours
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                out.add((al.asname or al.name).split(".")[0])
        for f in ast.iter_child_nodes(n):
            stack.append(f)
    return out


def scan_name_shadow():
    """Undefined names — delegated to pyflakes, deliberately.

    HOW THIS CHECK WAS BUILT, because the process matters more than the result:
      draft 1  compared LINE NUMBERS. Six false positives — `import cv2` on the line
               above its use read as a shadow.
      draft 2  walked AST function scopes. Twelve false positives — `import cv2` inside
               a module-level `try:` is indented, and indentation is not scope.
      draft 3  fixed that and then found NOTHING, including the real glob bug, because
               `import glob as _g` binds `_g`; the undefined name is `glob`, which was
               never in the "locally imported" set at all.

    Three drafts to rediscover that correct undefined-name analysis needs a full binding
    model. pyflakes already has one, tested against the whole language. Hand-rolling it
    would have shipped a check that was confidently wrong — which is the one thing this
    repo forbids. So this shells out, and when pyflakes is absent it says NOT MEASURED
    loudly rather than printing a clean nothing.
    """
    import subprocess
    files = [os.path.relpath(p, HERE) for p in _pipeline_files()]
    files += [os.path.relpath(p, HERE) for p in _plan_files()]
    try:
        r = subprocess.run([sys.executable, "-m", "pyflakes"] + files,
                           cwd=HERE, capture_output=True, text=True, timeout=120)
    except Exception as e:
        add(3, "MED", "tools/bugsense.py",
            f"NOT MEASURED — could not run pyflakes ({e})",
            "A check that cannot run must say so. Install with: "
            "pip install pyflakes --break-system-packages")
        return
    if "No module named" in (r.stderr or ""):
        add(3, "MED", "tools/bugsense.py",
            "NOT MEASURED — pyflakes is not installed, so undefined names were NOT "
            "checked. This is the class that hid the glob bug for weeks.",
            "Install with: pip install pyflakes --break-system-packages")
        return
    for ln in (r.stdout or "").splitlines():
        m = re.match(r"^(.+?):(\d+):\d+: undefined name '(\w+)'", ln.strip())
        if not m:
            continue
        add(3, "HIGH", f"{m.group(1)}:{m.group(2)}",
            f"undefined name '{m.group(3)}' — NameError when this line runs",
            "verify.py did exactly this with glob: the NameError was swallowed by a "
            "bare except and the relight budget silently fell back to a default for "
            "every pillar, forever.")


def _dead_scan_name_shadow_unused():
    """Retired hand-rolled version, kept only so nobody rebuilds it. See above.

    The first draft of this check compared line numbers and produced six false
    positives — `import cv2` inside the very function that uses it read as a shadow.
    A predictor with false positives gets ignored, and an ignored predictor is worse
    than none, so this walks real scopes: a name is only a finding when it is used in
    a function that neither imports it nor inherits it from module scope."""
    for p in _pipeline_files():
        rel = os.path.relpath(p, HERE)
        src = _read(p)
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue

        # MODULE SCOPE = every statement not inside a def/class, at ANY indent.
        # The first version of this only read tree.body, so `import cv2` nested in a
        # module-level `try: ... except ImportError:` was invisible and produced 12
        # false positives. Indentation is not scope in Python; def/class is.
        module_names = set(_direct_imports(tree))
        stack = list(tree.body)
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                module_names.add(n.name)
                continue                          # do not descend into its scope
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        module_names.add(t.id)
            for c in ast.iter_child_nodes(n):
                stack.append(c)

        # every name imported SOMEWHERE locally in this file, but not at module scope
        local_only = _imports_of(tree) - module_names
        if not local_only:
            continue

        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            have = _direct_imports(fn) | {ar.arg for ar in fn.args.args}
            for n in ast.walk(fn):
                if not (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)):
                    continue
                mod = n.value.id
                if mod not in local_only or mod in have or mod in module_names:
                    continue
                add(3, "HIGH", f"{rel}:{n.lineno}",
                    f"`{mod}.{n.attr}` is used inside {fn.name}() at line {n.lineno}, "
                    f"but {mod} is imported only inside OTHER functions and never at "
                    f"module scope — NameError whenever {fn.name}() runs",
                    "verify.py did exactly this with glob: the NameError was swallowed "
                    "by a bare except and the relight budget silently fell back to a "
                    "default for every pillar, forever.")
                break                                  # one finding per function


# ---------------------------------------------------------------- CLASS 4
def scan_foreign_literals():
    projects = {os.path.basename(f)[:-3] for f in _plan_files()}
    pdirs = os.path.join(HERE, "projects")
    if os.path.isdir(pdirs):
        projects |= {d for d in os.listdir(pdirs) if not d.startswith("_")}
    projects = {p for p in projects if len(p) > 2}
    for p in [os.path.join(HERE, f) for f in PIPELINE if os.path.exists(os.path.join(HERE, f))]:
        rel = os.path.relpath(p, HERE)
        for i, ln in enumerate(_read(p).splitlines(), 1):
            s = ln.strip()
            if s.startswith("#") or not s:
                continue
            for proj in sorted(projects):
                # a project name inside a STRING LITERAL in shared code
                for m in re.finditer(r"[\"']([^\"']*)[\"']", ln):
                    lit = m.group(1)
                    if re.search(r"(?i)\b" + re.escape(proj) + r"[_\-]", lit) or \
                       re.fullmatch(r"(?i)" + re.escape(proj), lit):
                        if "default" in s.lower() or "fallback" in s.lower():
                            sev = "LOW"
                        else:
                            sev = "MED"
                        add(4, sev, f"{rel}:{i}",
                            f"shared pipeline code contains the literal '{lit}' "
                            f"(project '{proj}')",
                            "verify.py CHECK 0 globbed only 'LC300_*.mp4', so on five "
                            "of six projects the freshness gate measured nothing and "
                            "always passed — and it gates every other check.")
                        break
                else:
                    continue
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--class", dest="cls", type=int, choices=[1, 2, 3, 4])
    ap.add_argument("--plan")
    ap.add_argument("--json")
    a = ap.parse_args()

    if not os.path.isdir(HERE):
        print("cannot locate repo root"); return 2

    want = a.cls
    if want in (None, 1): scan_contracts(a.plan)
    if want in (None, 2): scan_inert(a.plan)
    if want in (None, 3): scan_name_shadow()
    if want in (None, 4): scan_foreign_literals()

    TITLES = {0: "PLAN DOES NOT PARSE", 1: "UNMET CONTRACT", 2: "INERT DECLARATION",
              3: "NAME SHADOW", 4: "FOREIGN LITERAL"}
    print("=" * 78)
    print("BUGSENSE — structural defects, decidable from source, before anything runs")
    print("=" * 78)
    if not FINDINGS:
        print("\n  nothing found in the four scanned classes.")
        print("  NOTE: this proves only that these four shapes are absent. It says")
        print("  nothing about craft, content, or whether anything HAPPENS.\n")
        return 0

    order = {"BLOCK": 0, "HIGH": 1, "MED": 2, "LOW": 3}
    for cls in sorted({f["class"] for f in FINDINGS}):
        rows = [f for f in FINDINGS if f["class"] == cls]
        rows.sort(key=lambda f: order.get(f["severity"], 9))
        print(f"\n  CLASS {cls} — {TITLES[cls]}   ({len(rows)} finding(s))")
        print("  " + "-" * 74)
        seen_why = set()
        for f in rows:
            print(f"    [{f['severity']:5s}] {f['where']}")
            print(f"            {f['what']}")
            if f["why"] not in seen_why:
                for ln in f["why"].split(". "):
                    if ln.strip():
                        print(f"            > {ln.strip().rstrip('.')}.")
                seen_why.add(f["why"])
    n_high = sum(1 for f in FINDINGS if f["severity"] in ("BLOCK", "HIGH"))
    print("\n" + "=" * 78)
    print(f"  {len(FINDINGS)} finding(s), {n_high} at HIGH or above")
    print("=" * 78)
    print("  Each is a fact about the source, with a file and a line. None is a")
    print("  judgement. A LOW/MED finding may be intentional — if it is, say so in")
    print("  the file, because the next session cannot tell deliberate from forgotten.\n")

    if a.json:
        json.dump(FINDINGS, open(a.json, "w"), indent=1)
        print(f"  wrote {a.json}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())

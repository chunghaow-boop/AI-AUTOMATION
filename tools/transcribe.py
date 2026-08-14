#!/usr/bin/env python3
"""
TRANSCRIBE — word-level transcript. The piece the Cowork sandbox cannot run.

Sandy Lee's stack is Claude Code + Whisper + FFmpeg + Higgsfield. This is the Whisper half.
Model weights are blocked by the Cowork proxy (openaipublic / huggingface / alphacephei all
403), so this only works on a LOCAL Claude Code install. `bash setup-local.sh` installs it.

Output JSON feeds autocut.py, edl.py and mastermind.py:
  {tier, language, duration, words:[{w,start,end}], phrases:[{text,start,end}]}

Usage:
  python3 transcribe.py VIDEO.mp4 -o transcript.json [--model base] [--lang en]
Models: tiny(39M) base(74M) small(244M) medium(769M) large-v3(1.5G).
`base` is the right default for 9:16 social; `small` if there's music under the VO.
"""
import argparse, json, os, subprocess, sys, tempfile

def extract_audio(path):
    wav = os.path.join(tempfile.gettempdir(), "tx_audio.wav")
    subprocess.run(["ffmpeg","-y","-v","error","-i",path,"-ac","1","-ar","16000",wav],
                   capture_output=True)
    return wav if os.path.exists(wav) else None

# Domain vocabulary — Whisper mis-hears Malaysian car terms ("Myvi" -> "Mivey").
# initial_prompt biases decoding toward these without retraining.
MALAY_HINT = "Myvi, Perodua, Vellfire, Alphard, Vios, recond, RM, ringgit, Puspakom."

LOCAL_MODEL_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "faster-whisper-base"),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models"),
]

def _resolve_model(name):
    """Prefer LOCAL weights in AI/models/ — the sandbox cannot download them.
    Drop model.bin + config.json + tokenizer.json + vocabulary.txt into
    AI/models/faster-whisper-base/ and this finds them automatically."""
    for d in LOCAL_MODEL_DIRS:
        if not os.path.isdir(d): continue
        # tolerate files still carrying the WHISPER_ download prefix
        import glob as _g, shutil as _sh
        for f in _g.glob(os.path.join(d, "WHISPER_*")):
            t = os.path.join(d, os.path.basename(f).replace("WHISPER_", "", 1))
            if not os.path.exists(t):
                try: _sh.move(f, t)
                except Exception: pass
        if os.path.exists(os.path.join(d, "model.bin")):
            return d, True
    return name, False

def _rebuild_phrases(words, max_gap=0.55, max_words=14):
    """Whisper's segmenter collapses when an initial_prompt is used. Word timings stay
    accurate, so rebuild sentences from punctuation + pauses instead. This keeps the
    vocabulary hint AND fine-grained phrases — autocut needs both."""
    if not words: return []
    out, cur, start = [], [], None
    for i, w in enumerate(words):
        if start is None: start = w["start"]
        cur.append(w["w"])
        ends_sentence = w["w"].rstrip().endswith((".", "?", "!"))
        big_gap = (i + 1 < len(words)) and (words[i+1]["start"] - w["end"] > max_gap)
        if ends_sentence or big_gap or len(cur) >= max_words:
            out.append({"text": " ".join(cur).strip(), "start": round(start,3),
                        "end": round(w["end"],3)})
            cur, start = [], None
    if cur:
        out.append({"text": " ".join(cur).strip(), "start": round(start,3),
                    "end": round(words[-1]["end"],3)})
    return out

def run(path, model="base", lang=None):
    wav = extract_audio(path)
    if not wav:
        return {"tier":"none","error":"no audio track","words":[],"phrases":[]}

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {"tier":"missing",
                "error":"faster-whisper not installed. Run: bash setup-local.sh  "
                        "(this tool cannot work in the Cowork sandbox — weights are blocked)",
                "words":[],"phrases":[]}

    resolved, is_local = _resolve_model(model)
    if not is_local:
        # sandbox cannot fetch weights; fail with a useful message instead of a stack trace
        try:
            m = WhisperModel(resolved, device="cpu", compute_type="int8")
        except Exception as e:
            return {"tier":"blocked","words":[],"phrases":[],
                    "error":("no local weights and the sandbox cannot download them.\n"
                             "  FIX: put model.bin + config.json + tokenizer.json + vocabulary.txt\n"
                             "       into AI/models/faster-whisper-base/  then re-run.\n"
                             f"  ({str(e)[:90]})")}
    else:
        m = WhisperModel(resolved, device="cpu", compute_type="int8")
    segs, info = m.transcribe(wav, word_timestamps=True, language=lang,
                              initial_prompt=MALAY_HINT,
                              vad_filter=True, vad_parameters={"min_silence_duration_ms":300})
    words, phrases = [], []
    for s in segs:
        phrases.append({"text": s.text.strip(), "start": round(s.start,3), "end": round(s.end,3)})
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "start": round(w.start,3),
                          "end": round(w.end,3), "prob": round(getattr(w,"probability",1.0),3)})
    # prefer rebuilt phrases when the segmenter under-splits (prompt side-effect)
    rebuilt = _rebuild_phrases(words)
    if words and len(rebuilt) > len(phrases):
        phrases = rebuilt
    return {"tier":"faster-whisper", "model":model, "weights":"local" if is_local else "hub",
            "language": getattr(info,"language",lang),
            "duration": round(getattr(info,"duration",0.0),2),
            "words": words, "phrases": phrases}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("-o", default="transcript.json")
    ap.add_argument("--model", default="base"); ap.add_argument("--lang")
    a = ap.parse_args()
    r = run(a.video, a.model, a.lang)
    json.dump(r, open(a.o,"w"), indent=2, ensure_ascii=False)
    if r.get("error"):
        print("!!", r["error"]); sys.exit(1)
    print(f"tier={r['tier']} model={r['model']} lang={r['language']} "
          f"words={len(r['words'])} phrases={len(r['phrases'])} -> {a.o}")
    for p in r["phrases"][:5]:
        print(f"  {p['start']:>6.2f}  {p['text'][:70]}")

if __name__ == "__main__":
    main()

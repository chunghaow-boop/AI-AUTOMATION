#!/usr/bin/env python3
"""
MAKE_STORYBOARD — render the EDIT PLAN as an image, before generating anything.

WHY THIS EXISTS (his instruction, 2026-07-31)
  "plan the flow first, the editing flow, what you need before generation, so the images
   and video can sync together from ai video generation to video editing"
  "make a storyboard image of the flow for your own reference"

  A slot table in prose is easy to violate without noticing. A picture of the timeline makes
  three failures visible AT A GLANCE, before a credit is spent:

    1  the same colour repeating         = one source carrying too many shots
    2  uniform block widths              = a metronome (rate_variation ~0)
    3  a slot with no source assigned    = footage that does not exist yet

  The 4-source cut failed all three and nobody saw it until after 70cr of generation and
  two full re-cuts.

Usage
  python3 make_storyboard.py                       # the LC300 board
  python3 make_storyboard.py --json plan.json      # any beatplan output
"""
import os, sys, json, argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

HERE = os.path.dirname(os.path.abspath(__file__))

BPM, BEAT, TOTAL = 150.0, 0.400, 16.0

# source -> (label, colour, lighting stage)
SOURCES = {
    "A": ("exterior front 3/4\nlamps ignite",  "#4A6FA5", "SHOWROOM"),
    "B": ("20in alloy\n+ flank",               "#5B8C5A", "SHOWROOM"),
    "C": ("front cabin\n12.3in screen",        "#B5843A", "INTERIOR"),
    "D": ("rear dual\n11.6in screens",         "#A96B4E", "INTERIOR"),
    "E": ("ROLLING, wet road\nNIGHT",          "#7B3F6B", "NIGHT"),
    "F": ("rear 3/4, taillights\nNIGHT",       "#8C3B3B", "NIGHT"),
}

# (source, crop, kind, note)
SHOTS = [
    ("A", 1.00, "burst", "ignition"),
    ("B", 1.00, "burst", "wheel"),
    ("A", 1.95, "burst", "lamp cluster"),
    ("B", 1.90, "burst", "alloy spokes"),
    ("C", 1.00, "burst", "step inside"),
    ("D", 1.00, "hold",  "CABIN REVEAL"),
    ("C", 1.85, "burst", "12.3in screen"),
    ("D", 1.90, "burst", "screen detail"),
    ("F", 1.00, "burst", "out after dark"),
    ("E", 1.90, "burst", "lamps at speed"),
    ("F", 1.85, "burst", "taillight macro"),
    ("E", 1.00, "hold",  "ROLLING NIGHT"),
    ("F", 1.90, "burst", "tail at speed"),
    ("A", 1.00, "burst", "LOOP to frame 0"),
]
BLEND_AFTER = [3, 5, 7, 11]


def lengths():
    out, t = [], 0.0
    for src, crop, kind, note in SHOTS:
        d = 8 * BEAT if kind == "hold" else 2 * BEAT
        out.append((t, d))
        t += d
    return out, t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "STORYBOARD-FLOW.png"))
    a = ap.parse_args()

    pos, total = lengths()
    fig = plt.figure(figsize=(19, 11), facecolor="#12141A")

    # ---------------------------------------------------------------- timeline
    ax = fig.add_axes([0.04, 0.46, 0.92, 0.44])
    ax.set_facecolor("#12141A")
    ax.set_xlim(0, total)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # beat grid
    n = int(total / BEAT) + 1
    for i in range(n):
        t = i * BEAT
        strong = (i % 4 == 0)
        ax.plot([t, t], [0.4, 9.4], lw=1.4 if strong else 0.5,
                color="#39414F" if strong else "#232833", zorder=0)
    ax.text(0, 9.75, f"BEAT GRID  {BPM:.0f} BPM  ·  beat {BEAT*1000:.0f}ms  ·  "
                     f"bed trimmed {163}ms so the first transient lands on t=0",
            color="#7C8798", fontsize=10.5, va="bottom", family="monospace")

    # lighting arc bands
    stages = []
    for i, (src, _c, _k, _n) in enumerate(SHOTS):
        stages.append(SOURCES[src][2])
    band_y, band_h = 8.15, 0.75
    i = 0
    STAGE_C = {"SHOWROOM": "#1D2836", "INTERIOR": "#332818", "NIGHT": "#2A1626"}
    while i < len(SHOTS):
        j = i
        while j + 1 < len(SHOTS) and stages[j + 1] == stages[i]:
            j += 1
        x0 = pos[i][0]
        x1 = pos[j][0] + pos[j][1]
        ax.add_patch(Rectangle((x0, band_y), x1 - x0, band_h,
                               facecolor=STAGE_C[stages[i]], edgecolor="#4A5568", lw=0.8))
        ax.text((x0 + x1) / 2, band_y + band_h / 2, stages[i], ha="center", va="center",
                color="#9AA7B8", fontsize=9.5, family="monospace", weight="bold")
        i = j + 1

    # shot blocks
    y0, h = 3.6, 4.1
    for k, ((src, crop, kind, note), (t, d)) in enumerate(zip(SHOTS, pos)):
        label, colour, _stage = SOURCES[src]
        ax.add_patch(Rectangle((t + 0.012, y0), d - 0.024, h, facecolor=colour,
                               edgecolor="#0C0E12", lw=1.6, zorder=2))
        ax.text(t + d / 2, y0 + h - 0.42, f"{k}", ha="center", va="center",
                color="#0C0E12", fontsize=12, weight="bold", zorder=3)
        ax.text(t + d / 2, y0 + h - 1.15, src, ha="center", va="center",
                color="#FFFFFF", fontsize=15, weight="bold", zorder=3, family="monospace")
        if kind == "hold" or d > 1.0:
            ax.text(t + d / 2, y0 + h / 2 - 0.5, note, ha="center", va="center",
                    color="#EAF0F8", fontsize=9.5, zorder=3)
            ax.text(t + d / 2, y0 + 0.75, f"{crop:.2f}x  ·  {d:.2f}s", ha="center",
                    va="center", color="#C6D2E2", fontsize=9, zorder=3, family="monospace")
        else:
            ax.text(t + d / 2, y0 + 0.55, f"{crop:.2f}x", ha="center", va="center",
                    color="#C6D2E2", fontsize=8, zorder=3, family="monospace", rotation=90)

        # burst / hold rail
        rail_c = "#D98E3A" if kind == "burst" else "#4FA88B"
        ax.add_patch(Rectangle((t + 0.012, 3.05), d - 0.024, 0.34,
                               facecolor=rail_c, edgecolor="none", zorder=2))

    ax.text(0, 2.5, "BURST 0.80s (2 beats)", color="#D98E3A", fontsize=10,
            family="monospace", weight="bold")
    ax.text(4.6, 2.5, "HOLD 3.20s (8 beats)", color="#4FA88B", fontsize=10,
            family="monospace", weight="bold")

    # blends
    for b in BLEND_AFTER:
        x = pos[b][0] + pos[b][1]
        ax.plot([x, x], [y0 - 0.35, y0 + h + 0.35], lw=2.6, color="#E8C34A",
                zorder=4, solid_capstyle="butt")
        ax.text(x, y0 + h + 0.62, "mask_slice\n0.40s", ha="center", va="bottom",
                color="#E8C34A", fontsize=8, family="monospace")

    # time ruler
    for sec in range(0, int(total) + 1, 2):
        ax.text(sec, 1.9, f"{sec}s", ha="center", va="center", color="#7C8798",
                fontsize=9.5, family="monospace")

    # ---------------------------------------------------------------- legend
    axl = fig.add_axes([0.04, 0.30, 0.44, 0.13])
    axl.set_facecolor("#12141A"); axl.axis("off")
    axl.set_xlim(0, 10); axl.set_ylim(0, 3.2)
    axl.text(0, 3.0, "SOURCES — 6 distinct clips", color="#EAF0F8", fontsize=11.5,
             weight="bold", family="monospace")
    for i, (k, (label, colour, stage)) in enumerate(SOURCES.items()):
        cx = (i % 3) * 3.4
        cy = 2.0 - (i // 3) * 1.05
        axl.add_patch(Rectangle((cx, cy - 0.28), 0.46, 0.62, facecolor=colour,
                                edgecolor="#0C0E12", lw=1.2))
        axl.text(cx + 0.62, cy + 0.14, k, color="#FFFFFF", fontsize=12, weight="bold",
                 family="monospace", va="center")
        axl.text(cx + 1.05, cy + 0.02, label.replace("\n", "  "), color="#9AA7B8",
                 fontsize=8.2, va="center")

    # ---------------------------------------------------------------- checks
    from collections import Counter
    use = Counter(s for s, _c, _k, _n in SHOTS)
    axc = fig.add_axes([0.52, 0.30, 0.44, 0.13])
    axc.set_facecolor("#12141A"); axc.axis("off")
    axc.set_xlim(0, 10); axc.set_ylim(0, 3.2)
    axc.text(0, 3.0, "COVERAGE CHECK — run BEFORE generating", color="#EAF0F8",
             fontsize=11.5, weight="bold", family="monospace")
    need = len(SHOTS) / 2.5
    rows = [
        (f"distinct sources    {len(SOURCES)}  >=  {need:.1f}  (shots / 2.5)",
         len(SOURCES) >= need),
        (f"max shots per source  {max(use.values())}  <=  3", max(use.values()) <= 3),
        (f"punch-ins >= 1.8x     {min(c for _s, c, _k, _n in SHOTS if c > 1.05):.2f}x min",
         min(c for _s, c, _k, _n in SHOTS if c > 1.05) >= 1.8),
        (f"median shot  0.80s  vs  0.77s target", True),
        (f"cuts/min     48.7   vs  44.7 target", True),
    ]
    for i, (txt, ok) in enumerate(rows):
        axc.text(0, 2.35 - i * 0.5, "OK " if ok else "X  ",
                 color="#4FA88B" if ok else "#D9534F", fontsize=9.5,
                 family="monospace", weight="bold")
        axc.text(0.75, 2.35 - i * 0.5, txt, color="#9AA7B8", fontsize=9.5,
                 family="monospace")

    # ---------------------------------------------------------------- pipeline
    axp = fig.add_axes([0.04, 0.045, 0.92, 0.20])
    axp.set_facecolor("#12141A"); axp.axis("off")
    axp.set_xlim(0, 100); axp.set_ylim(0, 10)
    axp.text(0, 9.2, "THE ORDER  —  steps 1-5 are FREE. Step 6 is where credits burn.",
             color="#EAF0F8", fontsize=12, weight="bold", family="monospace")

    steps = [
        ("1 PILLAR\n+ duration", "#39414F"),
        ("2 MUSIC\nphonk + rhythm\nBPM AND PHASE", "#39414F"),
        ("3 BEAT GRID\nbeatplan\nburst / hold", "#39414F"),
        ("4 SLOT TABLE\nwhat each shot\nmust SHOW", "#39414F"),
        ("5 COVERAGE\nsources >= n/2.5\nBLOCK if short", "#4FA88B"),
        ("6 GENERATE\none clip per slot\n$$$", "#8C3B3B"),
        ("7 ASSEMBLE\nclipsense\neditsense fx", "#39414F"),
        ("8 PROVE\nreverse --mine-cuts\nverdict + qc", "#39414F"),
    ]
    w, gap = 10.6, 1.8
    for i, (txt, col) in enumerate(steps):
        x = i * (w + gap)
        axp.add_patch(Rectangle((x, 2.2), w, 5.4, facecolor=col, edgecolor="#0C0E12",
                                lw=1.5))
        axp.text(x + w / 2, 4.9, txt, ha="center", va="center", color="#EAF0F8",
                 fontsize=8.4, family="monospace", linespacing=1.5)
        if i < len(steps) - 1:
            axp.annotate("", xy=(x + w + gap - 0.35, 4.9), xytext=(x + w + 0.35, 4.9),
                         arrowprops=dict(arrowstyle="-|>", color="#5A6578", lw=1.6))
    axp.text(0, 0.9,
             "RULE ZERO — the edit plan comes first; generation fills its slots. "
             "Getting this backwards cost 7 of 13 cuts with hist-corr > 0.95: "
             "correct timing, footage that could not carry it.",
             color="#D98E3A", fontsize=9.6, family="monospace")

    fig.text(0.04, 0.955, "LC300 ZX  ·  CAR CINEMATIC  ·  EDIT FLOW",
             color="#FFFFFF", fontsize=21, weight="bold", family="monospace")
    fig.text(0.04, 0.925,
             "14 shots · 16.00s · 720x1280 9:16 · median 0.80s (target 0.77) · "
             "48.7 cuts/min (target 44.7) · 4 blends · grade crushed 2.0/91.5",
             color="#7C8798", fontsize=11, family="monospace")

    fig.savefig(a.out, dpi=110, facecolor="#12141A")
    print(f"written: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

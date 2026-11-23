#!/usr/bin/env python3
"""Assemble AOC-002's real, rights-cleared context footage into a silent vertical film.

Produces a *regional context* opening, NOT footage of a drilling incident.
Requires local ffmpeg/ffprobe with libx264 and drawtext enabled.
No paid generation, external requests, or publication actions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "content/AOC-002/media/originals"
DEFAULT_OUTPUT = ROOT / "content/AOC-002/media/derived/aoc002-context-opening.mp4"
SHOTS = [
    ("niger-delta-esa.jpg", 5.5, "REGIONAL CONTEXT — NIGER DELTA\\nNOT THE INCIDENT SITE", "ESA | CC BY-SA 3.0 IGO", "dd4fbc7d5bd758c3beb7c76b6b13b67049d878d904862c00a323f59fb677b1bd"),
    ("forcados-river.webm", 5.5, "REGIONAL CONTEXT — FORÇADOS RIVER\\nNOT THE INCIDENT SITE", "Nobleagege | CC BY 4.0", "ec3d4c79dc199c338b8983462661b28f5cfce7b64deac989a9d1162357043fa5"),
    ("ogbelle-rig-night.jpg", 6.5, "INDUSTRY CONTEXT — RIVERS STATE\\nNOT THE INCIDENT RIG", "Julius A OBARO | CC BY-SA 4.0", "f62cc1a79e66583ce573b13aedbeeb5b6c4c46bfd5013f7b970ef8691c422d61"),
    ("brass-island-fishing.webm", 5.5, "LIVELIHOOD CONTEXT — BRASS ISLAND\\nNOT THE INCIDENT SITE", "Christopher Wonder Osariemen | CC BY-SA 4.0", "f0dc8138f677b7d1f41396a5517697f13eacddefee960e59feeb76e7a81433ab"),
    ("obodougua-rig-sunset.jpg", 6.0, "INDUSTRY CONTEXT — DELTA STATE\\nNOT THE INCIDENT RIG", "Julius A OBARO | CC BY-SA 4.0", "f4b560a0642b532437edda0551840c40f8dd690d814e2bf8fd1dad7db62831e1"),
    ("bayelsa-palm-oil.webm", 6.0, "LIVELIHOOD CONTEXT — BAYELSA STATE\\nNOT THE INCIDENT SITE", "Christopher Wonder Osariemen | CC BY-SA 4.0", "27856007bedd40df8613d33b3afb67ec0003d2e3da050d461bd536d973f60388"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for chunk in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_originals() -> None:
    for name, _, _, _, expected in SHOTS:
        source = SOURCE_DIR / name
        if not source.is_file():
            raise RuntimeError(f"Original missing: {source}")
        actual = sha256(source)
        if actual != expected:
            raise RuntimeError(f"Original SHA-256 mismatch: {name}: {actual}")


def filter_path(path: Path) -> str:
    # FFmpeg filter option parser treats :, backslash and apostrophes specially.
    value = str(path.resolve()).replace("\\", "\\\\")
    return value.replace(":", "\\:").replace("'", "\\'")


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def assemble(output: Path, width: int, height: int) -> dict:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to assemble the opening")
    if width % 2 or height % 2:
        raise ValueError("Output dimensions must be even")
    if width < 360 or height < 640:
        raise ValueError("Output too small for the rights labels")

    check_originals()
    font = next((p for p in [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
    ] if p.is_file()), None)
    if font is None:
        raise RuntimeError("No supported TTF font available for permanent on-film labels")

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="aoc002-film-") as tmp:
        temp = Path(tmp)
        segments = []
        for index, (name, duration, label, credit, _) in enumerate(SHOTS):
            source = SOURCE_DIR / name
            title_path = temp / f"title-{index:02d}.txt"
            credit_path = temp / f"credit-{index:02d}.txt"
            title_path.write_text(label.replace("\\n", "\n"), encoding="utf-8")
            credit_path.write_text(credit, encoding="utf-8")
            segment = temp / f"shot-{index:02d}.mp4"
            input_args = ["-loop", "1", "-framerate", "30"] if source.suffix.lower() in {".jpg", ".png"} else ["-stream_loop", "-1"]
            font_arg = filter_path(font)
            top_arg, bottom_arg = filter_path(title_path), filter_path(credit_path)
            filter_graph = (
                f"[0:v]split=2[background][foreground];"
                f"[background]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},boxblur=20:10[blur];"
                f"[foreground]scale={width}:{height}:force_original_aspect_ratio=decrease[full];"
                f"[blur][full]overlay=(W-w)/2:(H-h)/2,"
                f"drawbox=x=0:y=0:w=iw:h={int(height*.15)}:color=black@0.78:t=fill,"
                f"drawtext=fontfile='{font_arg}':textfile='{top_arg}':"
                f"fontcolor=white:fontsize={max(22,int(width*.038))}:x={int(width*.045)}:y={int(height*.035)}:line_spacing=10,"
                f"drawbox=x=0:y={int(height*.91)}:w=iw:h={int(height*.09)}:color=black@0.8:t=fill,"
                f"drawtext=fontfile='{font_arg}':textfile='{bottom_arg}':"
                f"fontcolor=white:fontsize={max(17,int(width*.025))}:x={int(width*.045)}:y={int(height*.945)},"
                f"fps=30,format=yuv420p[v]"
            )
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                 *input_args, "-i", str(source), "-t", str(duration), "-filter_complex", filter_graph,
                 "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "22",
                 "-r", "30", "-pix_fmt", "yuv420p", str(segment)])
            segments.append(segment)
        concat = temp / "list.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in segments), encoding="utf-8")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat",
             "-safe", "0", "-i", str(concat), "-c", "copy", "-an",
             "-movflags", "+faststart", str(output)])

    receipt = {
        "edition": "AOC-002",
        "classification": "REGIONAL CONTEXT ONLY — NOT INCIDENT FOOTAGE",
        "silent": True,
        "output": str(output),
        "sha256": sha256(output),
        "dimensions": [width, height],
        "shots": [{"file": shot[0], "duration_seconds": shot[1], "source_sha256": shot[4]}
                  for shot in SHOTS],
        "original_attribution": "content/AOC-002/media/ATTRIBUTION.md",
    }
    receipt_path = output.with_suffix(".receipt.json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate all six original checksums only")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--height", type=int, default=1280)
    options = parser.parse_args()
    if options.check:
        check_originals()
        print("Six original AOC-002 assets passed SHA-256 verification.")
        return
    print(json.dumps(assemble(options.output, options.width, options.height), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render exact-atlas previews for a v2 ChatGPT pet."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


CELL_W = 192
CELL_H = 208
STATES = [
    ("idle", 0, [280, 110, 110, 140, 140, 320]),
    ("running-right", 1, [120] * 7 + [220]),
    ("running-left", 2, [120] * 7 + [220]),
    ("waving", 3, [140, 140, 140, 280]),
    ("jumping", 4, [140, 140, 140, 140, 280]),
    ("failed", 5, [140] * 7 + [240]),
    ("waiting", 6, [150] * 5 + [260]),
    ("running", 7, [120] * 5 + [220]),
    ("review", 8, [150] * 5 + [280]),
]


def crop_cell(atlas: Image.Image, row: int, col: int) -> Image.Image:
    return atlas.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H))


def save_gif(path: Path, frames: list[Image.Image], durations: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"expected 1536x2288, got {atlas.size}")
    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)

    all_frames: list[Image.Image] = []
    all_durations: list[int] = []
    state_frames: dict[str, list[Image.Image]] = {}
    state_durations: dict[str, list[int]] = {}
    for name, row, durations in STATES:
        frames = [crop_cell(atlas, row, col) for col in range(len(durations))]
        state_frames[name] = frames
        state_durations[name] = durations
        save_gif(output / "states" / f"{name}.gif", frames, durations)
        all_frames.extend(frames)
        all_durations.extend(durations)

    save_gif(output / "all-states.gif", all_frames, all_durations)
    idle_jump = state_frames["idle"] + state_frames["jumping"] + state_frames["idle"]
    idle_jump_durations = state_durations["idle"] + state_durations["jumping"] + state_durations["idle"]
    save_gif(output / "idle-jump-idle.gif", idle_jump, idle_jump_durations)

    look_frames = [crop_cell(atlas, 9 + index // 8, index % 8) for index in range(16)]
    save_gif(output / "look-loop.gif", look_frames, [140] * 16)

    stills = {
        "idle.png": crop_cell(atlas, 0, 0),
        "wave.png": crop_cell(atlas, 3, 2),
        "jump-peak.png": crop_cell(atlas, 4, 2),
        "failed.png": crop_cell(atlas, 5, 4),
        "look-right.png": crop_cell(atlas, 9, 4),
        "look-down.png": crop_cell(atlas, 10, 0),
    }
    (output / "stills").mkdir(parents=True, exist_ok=True)
    for filename, frame in stills.items():
        frame.save(output / "stills" / filename)

    mp4_frames = output / "mp4-frames"
    mp4_frames.mkdir(parents=True, exist_ok=True)
    canvas_color = (246, 246, 246, 255)
    for index, frame in enumerate(all_frames):
        canvas = Image.new("RGBA", frame.size, canvas_color)
        canvas.alpha_composite(frame)
        canvas.convert("RGB").save(mp4_frames / f"{index:03d}.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compose a GitHub-friendly horizontal action strip from one atlas row."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


CELL_W = 192
CELL_H = 208
ATLAS_W = 1536
ATLAS_H = 2288


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas")
    parser.add_argument("output")
    parser.add_argument("--row", type=int, default=1)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--background", default="#FFFFFF")
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    if atlas.size != (ATLAS_W, ATLAS_H):
        raise SystemExit(f"expected {ATLAS_W}x{ATLAS_H}, got {atlas.size}")

    canvas_w = 2176
    canvas_h = 724
    slot_w = canvas_w / args.frames
    baseline = 552
    max_sprite_h = 365
    max_sprite_w = slot_w - 34
    canvas = Image.new("RGBA", (canvas_w, canvas_h), args.background)

    cells: list[tuple[Image.Image, tuple[int, int, int, int]]] = []
    for column in range(args.frames):
        cell = atlas.crop(
            (
                column * CELL_W,
                args.row * CELL_H,
                (column + 1) * CELL_W,
                (args.row + 1) * CELL_H,
            )
        )
        bounds = cell.getchannel("A").getbbox()
        if bounds is None:
            raise SystemExit(f"row {args.row} column {column} is empty")
        cells.append((cell.crop(bounds), bounds))

    largest_w = max(image.width for image, _ in cells)
    largest_h = max(image.height for image, _ in cells)
    scale = min(max_sprite_w / largest_w, max_sprite_h / largest_h)

    for index, (image, _) in enumerate(cells):
        width = max(1, round(image.width * scale))
        height = max(1, round(image.height * scale))
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        center_x = round((index + 0.5) * slot_w)
        left = center_x - width // 2
        top = baseline - height
        canvas.alpha_composite(resized, (left, top))

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=95)


if __name__ == "__main__":
    main()

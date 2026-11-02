#!/usr/bin/env python3
"""Render a 3x3 GitHub action overview from a final v2 pet atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_W = 192
CELL_H = 208
ATLAS_SIZE = (1536, 2288)
CANVAS_SIZE = (1200, 1320)
CARD_W = 400
CARD_H = 440

CHINESE_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
MONO_FONT = "/System/Library/Fonts/SFNSMono.ttf"

STATES = [
    ("待机", "idle", 0, 0, 6),
    ("招手", "waving", 3, 2, 4),
    ("跳跃", "jumping", 4, 2, 5),
    ("向左移动", "running-left", 2, 2, 8),
    ("执行任务", "running", 7, 3, 6),
    ("向右移动", "running-right", 1, 2, 8),
    ("等待输入", "waiting", 6, 3, 6),
    ("完成待查看", "review", 8, 1, 6),
    ("失败或阻塞", "failed", 5, 5, 8),
]


def centered_text(draw: ImageDraw.ImageDraw, center_x: int, y: int, text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    draw.text((center_x - width / 2, y), text, font=font, fill=fill)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas")
    parser.add_argument("output")
    parser.add_argument(
        "--laughing-frog",
        action="store_true",
        help="label the frog's customized interaction rows as laughing actions",
    )
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    if atlas.size != ATLAS_SIZE:
        raise SystemExit(f"expected {ATLAS_SIZE[0]}x{ATLAS_SIZE[1]}, got {atlas.size}")

    canvas = Image.new("RGB", CANVAS_SIZE, "#FFFFFF")
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(CHINESE_FONT, 34)
    code_font = ImageFont.truetype(MONO_FONT, 23)
    count_font = ImageFont.truetype(CHINESE_FONT, 23)

    states = STATES.copy()
    if args.laughing_frog:
        states[1] = ("捧腹大笑", "waving", 3, 0, 4)
        states[2] = ("笑后弯腰", "jumping", 4, 3, 5)

    for index, (title, state, atlas_row, atlas_col, frame_count) in enumerate(states):
        card_row, card_col = divmod(index, 3)
        x0 = card_col * CARD_W
        y0 = card_row * CARD_H
        x1 = x0 + CARD_W
        y1 = y0 + CARD_H

        fill = "#FFFFFF" if card_row != 1 else "#F7F9FB"
        draw.rectangle((x0, y0, x1, y1), fill=fill, outline="#D5DDE5", width=2)
        centered_text(draw, x0 + CARD_W // 2, y0 + 20, title, title_font, "#24292F")

        frame = atlas.crop(
            (
                atlas_col * CELL_W,
                atlas_row * CELL_H,
                (atlas_col + 1) * CELL_W,
                (atlas_row + 1) * CELL_H,
            )
        )
        bounds = frame.getchannel("A").getbbox()
        if bounds is None:
            raise SystemExit(f"empty frame for {state}: row {atlas_row}, column {atlas_col}")
        sprite = frame.crop(bounds)
        scale = min(320 / sprite.width, 288 / sprite.height)
        sprite = sprite.resize(
            (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))),
            Image.Resampling.LANCZOS,
        )
        sprite_left = x0 + (CARD_W - sprite.width) // 2
        sprite_top = y0 + 76 + (300 - sprite.height) // 2
        canvas.paste(sprite, (sprite_left, sprite_top), sprite)

        code_text = state
        count_text = f" · {frame_count} 帧"
        code_box = draw.textbbox((0, 0), code_text, font=code_font)
        count_box = draw.textbbox((0, 0), count_text, font=count_font)
        code_width = code_box[2] - code_box[0]
        count_width = count_box[2] - count_box[0]
        badge_width = code_width + count_width + 28
        badge_left = x0 + (CARD_W - badge_width) / 2
        badge_top = y0 + 387
        draw.rounded_rectangle(
            (badge_left, badge_top, badge_left + badge_width, badge_top + 38),
            radius=10,
            fill="#EEF1F4",
        )
        text_y = badge_top + 4
        draw.text((badge_left + 14, text_y), code_text, font=code_font, fill="#24292F")
        draw.text((badge_left + 14 + code_width, text_y), count_text, font=count_font, fill="#24292F")

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


if __name__ == "__main__":
    main()

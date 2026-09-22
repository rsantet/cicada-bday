"""Generate a simple placeholder "photo" (gradient + heart) for stages
that expect a real couple photo but none has been supplied yet in
content-drop/. Replace the output file with a real photo whenever you
want - these scripts are only re-run manually.
"""
from __future__ import annotations

import argparse
import math

from PIL import Image, ImageDraw


def make_placeholder(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height))
    top = (30, 20, 45)
    bottom = (90, 30, 60)
    for y in range(height):
        t = y / max(height - 1, 1)
        row = tuple(
            int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)
        )
        for x in range(width):
            img.putpixel((x, y), row)

    draw = ImageDraw.Draw(img)
    cx, cy = width / 2, height / 2
    scale = min(width, height) / 6
    points = []
    steps = 200
    for i in range(steps + 1):
        t = math.pi * 2 * i / steps
        hx = 16 * math.sin(t) ** 3
        hy = -(
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )
        points.append((cx + hx * scale / 16, cy + hy * scale / 16))
    draw.polygon(points, fill=(255, 111, 165))

    return img


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--width", type=int, default=900)
    parser.add_argument("--height", type=int, default=700)
    args = parser.parse_args()

    img = make_placeholder(args.width, args.height)
    img.save(args.output, quality=90)
    print(f"wrote placeholder photo to {args.output}")


if __name__ == "__main__":
    main()

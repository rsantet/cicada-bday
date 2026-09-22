from __future__ import annotations

import argparse
import hashlib
import random

import numpy as np
from PIL import Image, ImageDraw

CANVAS = (560, 420)
NUM_EPICYCLES = 45
FRAMES_PER_LOOP = 90
PATH_SAMPLES = 300


def build_skyline_path(city: str, num_buildings: int = 14) -> np.ndarray:
    seed = int(hashlib.sha256(city.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)

    total_width = 12.0
    x = -total_width / 2
    top_points = []
    widths = [total_width / num_buildings] * num_buildings
    for w in widths:
        height = rng.uniform(1.0, 5.5)
        top_points.append((x, 0.0))
        top_points.append((x, height))
        top_points.append((x + w, height))
        top_points.append((x + w, 0.0))
        x += w

    # close the path back along the baseline for a periodic contour
    closed = top_points + [(x, 0.0), (-total_width / 2, 0.0)]
    return np.array([complex(px, py) for px, py in closed])


def resample_path(points: np.ndarray, n: int) -> np.ndarray:
    seg_lengths = np.abs(np.diff(points, append=points[:1]))
    cumulative = np.concatenate([[0], np.cumsum(seg_lengths)])
    total = cumulative[-1]
    targets = np.linspace(0, total, n, endpoint=False)
    out = np.zeros(n, dtype=complex)
    for i, t in enumerate(targets):
        idx = np.searchsorted(cumulative, t, side="right") - 1
        idx = min(idx, len(points) - 1)
        seg_start_len = cumulative[idx]
        seg_total_len = seg_lengths[idx] if seg_lengths[idx] > 0 else 1e-9
        frac = (t - seg_start_len) / seg_total_len
        p0 = points[idx]
        p1 = points[(idx + 1) % len(points)]
        out[i] = p0 + (p1 - p0) * frac
    return out


def compute_epicycles(path: np.ndarray, keep: int):
    n = len(path)
    coeffs = np.fft.fft(path) / n
    freqs = np.fft.fftfreq(n, d=1.0 / n).astype(int)
    order = np.argsort(-np.abs(coeffs))[:keep]
    return [(int(freqs[i]), coeffs[i]) for i in order]


def to_canvas(
    z: complex, scale: float, offset: complex
) -> tuple[float, float]:
    w = z * scale + offset
    return (w.real, w.imag)


def render_frames(
    epicycles, path_extent, canvas=CANVAS, frames=FRAMES_PER_LOOP
):
    scale = (min(canvas) * 0.42) / max(path_extent, 1e-6)
    offset = complex(canvas[0] / 2, canvas[1] * 0.55)

    images = []
    trail: list[tuple[float, float]] = []

    for f in range(frames):
        t = f / frames
        img = Image.new("RGB", canvas, (15, 20, 32))
        draw = ImageDraw.Draw(img)

        pos = complex(0, 0)
        prev_screen = to_canvas(pos, scale, offset)
        for freq, coeff in epicycles:
            radius = abs(coeff) * scale
            pos += coeff * np.exp(2j * np.pi * freq * t)
            screen = to_canvas(pos, scale, offset)
            if radius > 1.2:
                draw.ellipse(
                    [
                        prev_screen[0] - radius,
                        prev_screen[1] - radius,
                        prev_screen[0] + radius,
                        prev_screen[1] + radius,
                    ],
                    outline=(60, 70, 95),
                )
            draw.line([prev_screen, screen], fill=(111, 214, 255), width=1)
            prev_screen = screen

        trail.append(prev_screen)
        if len(trail) > 1:
            draw.line(trail, fill=(255, 111, 165), width=3, joint="curve")
        if t < 1.0 / frames:
            trail = []

        images.append(img)

    return images


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("city")
    parser.add_argument("output")
    args = parser.parse_args()

    raw_path = build_skyline_path(args.city)
    path = resample_path(raw_path, PATH_SAMPLES)
    # center path around its own centroid so it sits nicely on canvas
    path = path - np.mean(path)
    path_extent = np.max(np.abs(path))
    epicycles = compute_epicycles(path, NUM_EPICYCLES)
    frames = render_frames(epicycles, path_extent)

    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=45,
        loop=0,
    )
    print(f"wrote {args.output} ({len(frames)} frames, city={args.city!r})")


if __name__ == "__main__":
    main()

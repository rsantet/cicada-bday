from __future__ import annotations

import argparse

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

FONT_PATH = "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Bold.ttf"
SAMPLE_RATE = 44100

FREQ_RANGE_STANDALONE = (1000.0, 8000.0)
FREQ_RANGE_OVERLAY = (9000.0, 14000.0)


def render_text_mask(word: str, width: int, height: int) -> np.ndarray:
    img = Image.new("L", (width, height), color=0)
    draw = ImageDraw.Draw(img)

    font_size = height
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), word, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    while (text_w > width * 0.94 or text_h > height * 0.8) and font_size > 4:
        font_size -= 2
        font = ImageFont.truetype(FONT_PATH, font_size)
        bbox = draw.textbbox((0, 0), word, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    x = (width - text_w) / 2 - bbox[0]
    y = (height - text_h) / 2 - bbox[1]
    draw.text((x, y), word, fill=255, font=font)

    return np.array(img) > 127


def mask_to_audio(
    mask: np.ndarray, duration: float, freq_range: tuple[float, float]
) -> np.ndarray:
    height, width = mask.shape
    freq_max, freq_min = freq_range[1], freq_range[0]
    total_samples = int(SAMPLE_RATE * duration)
    samples_per_col = max(total_samples // width, 1)
    audio = np.zeros(samples_per_col * width, dtype=np.float64)

    row_freqs = np.linspace(freq_max, freq_min, height)
    t = np.arange(samples_per_col) / SAMPLE_RATE

    for col in range(width):
        active_rows = np.where(mask[:, col])[0]
        if len(active_rows) == 0:
            continue
        chunk = np.zeros(samples_per_col)
        for row in active_rows:
            freq = row_freqs[row]
            chunk += np.sin(2 * np.pi * freq * t)
        chunk /= max(len(active_rows), 1)
        start = col * samples_per_col
        audio[start : start + samples_per_col] = chunk

    fade = min(500, len(audio) // 10)
    if fade > 0:
        audio[:fade] *= np.linspace(0, 1, fade)
        audio[-fade:] *= np.linspace(1, 0, fade)

    peak = np.max(np.abs(audio)) or 1.0
    return audio / peak


def load_source_mono(
    path: str,
    target_sr: int,
    clip_start: float | None = None,
    clip_duration: float | None = None,
) -> np.ndarray:
    data, sr = sf.read(path, dtype="float64", always_2d=False)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if sr != target_sr:
        duration = len(data) / sr
        new_len = max(int(round(duration * target_sr)), 1)
        data = np.interp(
            np.linspace(0, len(data) - 1, new_len), np.arange(len(data)), data
        )
    if clip_start is not None:
        start_sample = int(clip_start * target_sr)
        end_sample = (
            len(data)
            if clip_duration is None
            else start_sample + int(clip_duration * target_sr)
        )
        data = data[start_sample:end_sample]
    peak = np.max(np.abs(data)) or 1.0
    return data / peak * 0.85


def mix_into_song(
    song: np.ndarray, text_audio: np.ndarray, blend: float = 0.4
) -> np.ndarray:
    insert_len = len(text_audio)
    if insert_len > len(song):
        song = np.pad(song, (0, insert_len - len(song)))
    start = (len(song) - insert_len) // 2
    mixed = song.copy()
    mixed[start : start + insert_len] += text_audio * blend
    peak = np.max(np.abs(mixed)) or 1.0
    if peak > 0.98:
        mixed = mixed / peak * 0.95
    return mixed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("word")
    parser.add_argument("output")
    parser.add_argument("--source-audio", default=None)
    parser.add_argument("--clip-start", type=float, default=None)
    parser.add_argument("--clip-duration", type=float, default=None)
    parser.add_argument("--duration", type=float, default=6.0)
    parser.add_argument("--img-width", type=int, default=220)
    parser.add_argument("--img-height", type=int, default=90)
    args = parser.parse_args()

    mask = render_text_mask(args.word.upper(), args.img_width, args.img_height)

    if args.source_audio:
        song = load_source_mono(
            args.source_audio, SAMPLE_RATE, args.clip_start, args.clip_duration
        )
        text_audio = mask_to_audio(mask, args.duration, FREQ_RANGE_OVERLAY)
        mixed = mix_into_song(song, text_audio, blend=0.4)
        pcm = (mixed * 32767).astype(np.int16)
        wavfile.write(args.output, SAMPLE_RATE, pcm)
        print(
            f"wrote {args.output} (song altered, {len(mixed) / SAMPLE_RATE:.1f}s, "
            f"word={args.word!r} in {FREQ_RANGE_OVERLAY} Hz band)"
        )
    else:
        audio = mask_to_audio(mask, args.duration, FREQ_RANGE_STANDALONE)
        pcm = (audio * 0.9 * 32767).astype(np.int16)
        wavfile.write(args.output, SAMPLE_RATE, pcm)
        print(
            f"wrote {args.output} ({args.duration}s, word={args.word!r}, synthesized)"
        )


if __name__ == "__main__":
    main()

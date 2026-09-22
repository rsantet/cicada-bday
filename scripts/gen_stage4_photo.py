from __future__ import annotations

import argparse
import os
import subprocess
import sys

import piexif
import piexif.helper
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def ensure_source_photo(source: str, fallback: str) -> str:
    if os.path.exists(source):
        return source
    subprocess.run(
        [
            sys.executable,
            os.path.join(HERE, "gen_placeholder_photo.py"),
            fallback,
        ],
        check=True,
    )
    return fallback


def embed_message(src_path: str, dst_path: str, message: str) -> None:
    img = Image.open(src_path).convert("RGB")
    exif_dict = {
        "0th": {},
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }

    user_comment = piexif.helper.UserComment.dump(message, encoding="unicode")
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment

    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = message.encode(
        "utf-8"
    )

    xp_comment = message.encode("utf-16-le") + b"\x00\x00"
    exif_dict["0th"][piexif.ImageIFD.XPComment] = list(xp_comment)

    exif_bytes = piexif.dump(exif_dict)
    img.save(dst_path, "jpeg", quality=92, exif=exif_bytes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="content-drop/couple-photo.jpg")
    parser.add_argument(
        "--fallback", default="content-drop/.generated-stage4-source.jpg"
    )
    parser.add_argument("--output", default="assets/stage4-photo.jpg")
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    source = ensure_source_photo(args.source, args.fallback)
    embed_message(source, args.output, args.message)
    print(
        f"wrote {args.output} with hidden metadata (XPComment/ImageDescription/UserComment)"
    )


if __name__ == "__main__":
    main()

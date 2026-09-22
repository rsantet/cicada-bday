from __future__ import annotations

import argparse
import math

import numpy as np
from PIL import Image, ImageDraw

CANVAS = (640, 560)
NUM_EPICYCLES = 50
FRAMES_PER_LOOP = 100
PATH_SAMPLES = 300

# Real current commune border (lon, lat), geo.api.gouv.fr INSEE 94018.
CHARENTON_BORDER = [
    (2.419759, 48.816867),
    (2.418693, 48.816757),
    (2.418153, 48.816671),
    (2.416271, 48.816307),
    (2.415925, 48.816248),
    (2.415669, 48.816222),
    (2.414799, 48.816183),
    (2.413576, 48.816202),
    (2.412114, 48.816287),
    (2.410701, 48.816397),
    (2.409731, 48.816509),
    (2.4094, 48.816557),
    (2.409007, 48.816872),
    (2.408554, 48.817141),
    (2.408122, 48.81734),
    (2.407645, 48.817501),
    (2.406906, 48.817698),
    (2.405798, 48.81801),
    (2.405003, 48.818262),
    (2.403732, 48.818688),
    (2.402006, 48.819233),
    (2.400406, 48.819771),
    (2.399073, 48.820258),
    (2.397956, 48.820691),
    (2.397526, 48.820894),
    (2.3968, 48.821266),
    (2.395524, 48.822001),
    (2.394949, 48.822374),
    (2.393395, 48.823426),
    (2.390072, 48.825692),
    (2.391022, 48.826117),
    (2.392762, 48.826855),
    (2.393993, 48.827401),
    (2.39434, 48.827539),
    (2.395179, 48.827645),
    (2.395707, 48.827727),
    (2.396843, 48.828054),
    (2.397894, 48.828329),
    (2.399205, 48.828626),
    (2.399775, 48.828791),
    (2.400679, 48.829095),
    (2.402237, 48.82959),
    (2.402871, 48.829415),
    (2.403551, 48.829175),
    (2.403814, 48.82906),
    (2.404994, 48.828403),
    (2.405376, 48.828134),
    (2.405816, 48.827797),
    (2.40655, 48.827191),
    (2.407589, 48.82643),
    (2.408085, 48.826112),
    (2.408675, 48.825767),
    (2.409175, 48.825502),
    (2.409955, 48.825183),
    (2.41027, 48.825087),
    (2.410907, 48.82494),
    (2.411757, 48.824803),
    (2.412623, 48.824737),
    (2.413111, 48.824718),
    (2.413785, 48.824723),
    (2.415083, 48.824782),
    (2.415976, 48.824777),
    (2.416513, 48.824736),
    (2.417131, 48.824649),
    (2.417763, 48.824531),
    (2.418603, 48.824312),
    (2.419387, 48.824156),
    (2.419963, 48.82408),
    (2.419905, 48.822883),
    (2.419778, 48.821114),
    (2.419775, 48.820775),
    (2.419737, 48.820109),
    (2.419685, 48.819786),
    (2.419664, 48.819368),
    (2.419676, 48.819142),
    (2.419637, 48.818542),
    (2.419679, 48.818342),
    (2.419715, 48.81746),
    (2.419759, 48.816867),
]

# Bois de Vincennes, simplified (lon, lat), via Nominatim.
BOIS_DE_VINCENNES = [
    (2.3997573, 48.8306659),
    (2.4010262, 48.829852),
    (2.4036629, 48.8291808),
    (2.4072826, 48.8267646),
    (2.4112922, 48.824967),
    (2.4156614, 48.8248575),
    (2.4193274, 48.8242486),
    (2.4239785, 48.8242592),
    (2.4289466, 48.8237863),
    (2.4305491, 48.8230771),
    (2.4343025, 48.8201561),
    (2.4359635, 48.8196002),
    (2.4395917, 48.818363),
    (2.4496376, 48.8179621),
    (2.4581662, 48.8170927),
    (2.4598131, 48.8178257),
    (2.4624925, 48.8191422),
    (2.4648248, 48.8237131),
    (2.4653136, 48.8247569),
    (2.4657352, 48.8258316),
    (2.4636012, 48.8257746),
    (2.4644451, 48.8287291),
    (2.4656414, 48.8318532),
    (2.4690901, 48.8342407),
    (2.4696743, 48.8362634),
    (2.4662904, 48.8401268),
    (2.4510186, 48.8443969),
    (2.4407662, 48.8459165),
    (2.4260848, 48.8415865),
    (2.3997573, 48.8306659),
]

# Seine, real segment near Charenton, roughly south to north (lon, lat).
SEINE = [
    (2.4094696, 48.8054344),
    (2.4093243, 48.8057037),
    (2.4089992, 48.8065351),
    (2.4088144, 48.8074733),
    (2.4088439, 48.8085036),
    (2.4089604, 48.8092883),
    (2.4089823, 48.8093613),
    (2.4097277, 48.8118469),
    (2.4102418, 48.8139333),
    (2.4102403, 48.8152295),
    (2.4101291, 48.8157023),
    (2.4099078, 48.8160728),
    (2.4097601, 48.8162242),
    (2.4093608, 48.8166335),
    (2.4076180, 48.8173953),
    (2.4051718, 48.8181865),
    (2.4018073, 48.8193281),
    (2.3990779, 48.8203340),
    (2.3963742, 48.8215491),
    (2.3937564, 48.8233178),
    (2.3909926, 48.8251148),
    (2.3905972, 48.8254348),
    (2.3902559, 48.8257262),
]


def project(points_lonlat, lon0, lat0, meters_per_deg=111_320.0):
    coslat = math.cos(math.radians(lat0))
    out = []
    for lon, lat in points_lonlat:
        x = (lon - lon0) * coslat * meters_per_deg
        y = -(lat - lat0) * meters_per_deg
        out.append(complex(x, y))
    return np.array(out)


def resample_closed(points: np.ndarray, n: int) -> np.ndarray:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()

    lons = [p[0] for p in CHARENTON_BORDER]
    lats = [p[1] for p in CHARENTON_BORDER]
    lon0, lat0 = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2

    border = project(CHARENTON_BORDER, lon0, lat0)
    vincennes = project(BOIS_DE_VINCENNES, lon0, lat0)
    seine = project(SEINE, lon0, lat0)

    centroid = np.mean(border)
    border -= centroid
    vincennes -= centroid
    seine -= centroid

    path = resample_closed(border, PATH_SAMPLES)
    epicycles = compute_epicycles(path, NUM_EPICYCLES)

    fit_pts = np.concatenate([border, vincennes])
    extent = np.max(np.abs(fit_pts))
    scale = (min(CANVAS) * 0.75) / extent
    offset = complex(CANVAS[0] / 2, CANVAS[1] / 2)

    def screen(pts):
        return [to_canvas(p, scale, offset) for p in pts]

    vincennes_screen = screen(vincennes)
    seine_screen = screen(seine)

    frames = []
    trail: list[tuple[float, float]] = []

    for f in range(FRAMES_PER_LOOP):
        t = f / FRAMES_PER_LOOP
        img = Image.new("RGB", CANVAS, (245, 242, 235))
        draw = ImageDraw.Draw(img)

        draw.polygon(vincennes_screen, fill=(206, 227, 199))
        draw.line(seine_screen, fill=(110, 170, 220), width=4, joint="curve")

        pos = complex(0, 0)
        prev_screen = to_canvas(pos, scale, offset)
        for freq, coeff in epicycles:
            radius = abs(coeff) * scale
            pos += coeff * np.exp(2j * np.pi * freq * t)
            pt_screen = to_canvas(pos, scale, offset)
            if radius > 1.2:
                draw.ellipse(
                    [
                        prev_screen[0] - radius,
                        prev_screen[1] - radius,
                        prev_screen[0] + radius,
                        prev_screen[1] + radius,
                    ],
                    outline=(190, 190, 200),
                )
            draw.line([prev_screen, pt_screen], fill=(120, 140, 200), width=1)
            prev_screen = pt_screen

        trail.append(prev_screen)
        if len(trail) > 1:
            draw.line(trail, fill=(20, 20, 20), width=3, joint="curve")
        if t < 1.0 / FRAMES_PER_LOOP:
            trail = []

        frames.append(img)

    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=45,
        loop=0,
    )
    print(f"wrote {args.output} ({len(frames)} frames)")


if __name__ == "__main__":
    main()

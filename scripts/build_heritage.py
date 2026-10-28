"""Preserve the supplied heritage composition and add native-pixel blossom motion."""

import math
from dataclasses import dataclass

from PIL import Image, ImageChops, ImageDraw

from build_profile import ASSETS


OUTPUT = ASSETS / "heritage"
SOURCE = ASSETS / "Designer.png"
SIZE = (1536, 1024)
FRAMES = 144
DURATION = 100
TEXT_REGIONS = (
    (40, 18, 330, 203), (1270, 42, 1536, 222),
    (20, 472, 86, 665), (1438, 438, 1510, 650),
    (1408, 650, 1536, 795), (0, 892, 1536, 1024),
)
PROTECTED_REGIONS = TEXT_REGIONS + (
    (500, 100, 1030, 585),  # Flag fusion and its fine rim lighting.
    (1290, 255, 1440, 646),  # Liberty silhouette and torch.
)
PETAL_COLORS = (
    (113, 62, 119), (180, 91, 151), (235, 145, 192), (255, 199, 218),
)
PETAL_SHAPES = (
    ("01100", "12320", "01210", "00100"),
    ("0010", "0120", "1230", "0100"),
    ("00000", "01210", "12320", "01000"),
    ("0100", "1230", "0120", "0010"),
)
DIVIDER_PETALS = {
    "near": ((130, 2, 2), (198, 15, 1), (280, 1, 1), (356, 14, 2),
             (443, 2, 1), (598, 15, 1), (1042, 1, 1)),
    "middle": ((275, 2, 1), (425, 15, 1), (1138, 2, 1)),
    "far": ((1108, 15, 1),),
}
FOOTER_PETALS = (
    (1056, 208, 1), (1092, 206, 2), (1104, 209, 1),
    (1130, 207, 2), (1139, 209, 1), (1150, 208, 1),
    (1178, 208, 1), (1220, 207, 1), (1282, 209, 1),
)


@dataclass(frozen=True)
class Petal:
    x: int
    y: int
    drift: int
    phase: float
    scale: int
    opacity: float


# Origins follow visible blossom-bearing branches, not a screen-wide emitter.
PETALS = (
    Petal(131, 265, 125, 0.00, 1, 0.65),
    Petal(420, 233, 110, 0.19, 1, 0.55),
    Petal(549, 244, 145, 0.42, 1, 0.58),
    Petal(455, 276, 110, 0.71, 1, 0.62),
    Petal(180, 470, 92, 0.12, 2, 0.82),
    Petal(281, 583, 150, 0.61, 2, 0.78),
    Petal(523, 430, 195, 0.32, 1, 0.70),
    Petal(615, 456, 220, 0.86, 1, 0.54),
    Petal(334, 663, 120, 0.51, 2, 0.88),
    Petal(244, 636, 170, 0.93, 1, 0.68),
    Petal(478, 788, 150, 0.24, 2, 0.84),
    Petal(661, 488, 205, 0.05, 1, 0.50),
)


def protected_mask(regions):
    mask = Image.new("L", SIZE)
    draw = ImageDraw.Draw(mask)
    for left, top, right, bottom in regions:
        draw.rectangle((left, top, right - 1, bottom - 1), fill=255)
    return mask


def pixel_treatment(source):
    if source.size != SIZE:
        raise ValueError(f"Expected original artwork at {SIZE}; got {source.size}. No resizing applied.")
    original = source.convert("RGB")
    result = original.copy()
    pixels = result.load()
    protected = protected_mask(PROTECTED_REGIONS)
    # Only settle near-identical 2x2 colors. Edges, lights and chromatic detail
    # remain native-resolution; there is no downsample or global palette clamp.
    for y in range(0, SIZE[1], 2):
        for x in range(0, SIZE[0], 2):
            if protected.crop((x, y, x + 2, y + 2)).getbbox():
                continue
            cell = [original.getpixel((x + dx, y + dy))
                    for dy in range(2) for dx in range(2)]
            if max(max(color) for color in cell) >= 150:
                continue
            if any(max(c[channel] for c in cell) - min(c[channel] for c in cell) > 18
                   for channel in range(3)):
                continue
            mean = tuple(sum(c[channel] for c in cell) / 4 for channel in range(3))
            representative = min(cell, key=lambda c: sum((c[i] - mean[i]) ** 2 for i in range(3)))
            for dy in range(2):
                for dx in range(2):
                    pixels[x + dx, y + dy] = representative
    return result


def petal_sprite(state, scale=1, opacity=1.0):
    rows = PETAL_SHAPES[state % len(PETAL_SHAPES)]
    sprite = Image.new("RGBA", (len(rows[0]), len(rows)))
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            if value != "0":
                sprite.putpixel((x, y), (*PETAL_COLORS[int(value)], round(255 * opacity)))
    if scale != 1:
        sprite = sprite.resize((sprite.width * scale, sprite.height * scale),
                               Image.Resampling.NEAREST)
    return sprite


def petal_position(petal, frame):
    life = (frame % FRAMES / FRAMES + petal.phase) % 1
    x = petal.x + petal.drift * life + 12 * math.sin(life * math.tau)
    y = petal.y + (894 - petal.y) * life
    fade = min(1, life / 0.08, (1 - life) / 0.16)
    state = int(life * 8) % 4
    return round(x), round(y), fade * petal.opacity, state


def blossom_layer(frame):
    layer = Image.new("RGBA", SIZE)
    for petal in PETALS:
        x, y, opacity, state = petal_position(petal, frame)
        layer.alpha_composite(petal_sprite(state, petal.scale, opacity), (x, y))
    layer.putalpha(ImageChops.subtract(layer.getchannel("A"), protected_mask(TEXT_REGIONS)))
    return layer


def palette_for(still):
    palette = still.quantize(colors=248, method=Image.Quantize.MEDIANCUT,
                             dither=Image.Dither.NONE)
    colors = palette.getpalette()[:248 * 3]
    colors += [channel for color in PETAL_COLORS for channel in color]
    colors += [0] * (768 - len(colors))
    palette.putpalette(colors)
    return palette


def animation_frame(base, palette, frame):
    layer = blossom_layer(frame)
    result = base.copy()
    bounds = layer.getbbox()
    if bounds:
        patch = Image.alpha_composite(base.convert("RGBA").crop(bounds), layer.crop(bounds))
        painted = layer.getchannel("A").crop(bounds).point(lambda alpha: 255 if alpha else 0)
        result.paste(patch.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE),
                     bounds[:2], painted)
    return result


def divider(level):
    with Image.open(ASSETS / "ascii-dividers/bunker-divider.png") as source:
        image = source.convert("RGBA")
    for index, (x, y, scale) in enumerate(DIVIDER_PETALS[level]):
        image.alpha_composite(petal_sprite(index, scale, 0.68), (x, y))
    return image.convert("RGB")


def footer():
    with Image.open(ASSETS / "opensuse/opensuse-pixel.png") as source:
        image = source.convert("RGBA")
    for x, y, scale in FOOTER_PETALS:
        image.alpha_composite(petal_sprite(2, scale, 0.62), (x, y))
    return image.convert("RGB")


def main():
    with Image.open(SOURCE) as source:
        still = pixel_treatment(source)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    still.save(OUTPUT / "korean-american-heritage-still.png", optimize=True)
    palette = palette_for(still)
    base = still.quantize(palette=palette, dither=Image.Dither.NONE)
    frames = [animation_frame(base, palette, frame) for frame in range(FRAMES)]
    frames[0].save(OUTPUT / "korean-american-heritage.gif", save_all=True,
                   append_images=frames[1:], duration=DURATION, loop=0,
                   disposal=1, optimize=True)
    for level in DIVIDER_PETALS:
        divider(level).save(OUTPUT / f"petal-divider-{level}.png", optimize=True)
    footer().save(OUTPUT / "opensuse-petal-footer.png", optimize=True)
    print(f"Built {FRAMES} frames at {DURATION} ms; full-resolution heritage assets in {OUTPUT}")


if __name__ == "__main__":
    main()

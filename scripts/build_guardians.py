"""Build pixel-art guardian totems and framed derivatives of unchanged project cards."""

from PIL import Image, ImageDraw

from build_profile import ASSETS


OUTPUT = ASSETS / "guardians"
SCALE = 2
TOTEM_SIZE = (50, 400)
CARD_SIZE = (800, 400)
PANEL_SIZE = (900, 400)
CARDS = (
    ("f1", "left", 0), ("geome", "right", 0),
    ("pulse", "left", 1), ("spratforge", "right", 1),
)
INK = "#0c0b18"
PALETTES = {
    "left": {"edge": "#46838c", "light": "#68b9bd", "deep": "#24505d",
             "accent": "#79567f", "soft": "#3e636d"},
    "right": {"edge": "#8f5b88", "light": "#bd7aad", "deep": "#553454",
              "accent": "#4c898b", "soft": "#704a70"},
}
GOLD = "#b59864"


def guardian(side):
    p = PALETTES[side]
    image = Image.new("RGB", TOTEM_SIZE, INK)
    d = ImageDraw.Draw(image)

    # Central load-bearing shaft and offset plinth: matching but not mirrored.
    d.polygon([(7, 57), (12, 46), (38, 46), (43, 57), (43, 344),
               (47, 352), (47, 391), (3, 391), (3, 352), (7, 344)],
              fill="#211e2c", outline="#625268")
    d.rectangle((10, 59, 39, 347), fill="#171724", outline="#3d3449")
    d.rectangle((13, 64, 36, 342), fill="#20202e", outline="#4a3d50")
    d.line((8, 63, 8, 336), fill=p["deep"])
    d.line((41, 63, 41, 336), fill="#685268")
    d.line((10, 64, 10, 334), fill=p["edge"])

    # Tiered Korean-style eaves: upswept ends, ridge, tiles, and corbels.
    for y, inset in ((2, 4), (19, 1), (35, 4)):
        d.polygon([(inset, y + 3), (inset + 4, y + 7), (15, y + 7),
                   (20, y + 3), (24, y), (29, y + 3), (35, y + 7),
                   (45 - inset, y + 7), (49 - inset, y + 3),
                   (46 - inset, y + 14), (3 + inset, y + 14)],
                  fill="#292636", outline="#706076")
        d.line((inset + 2, y + 6, inset + 5, y + 10, 45 - inset, y + 10,
                47 - inset, y + 6), fill=p["edge"])
        d.line((inset + 5, y + 14, 44 - inset, y + 14), fill="#100f1a")
        for x in range(10, 41, 6):
            d.line((x, y + 11, x, y + 13), fill="#55475d")
    d.rectangle((5, 50, 44, 58), fill="#332736", outline="#7b6274")
    d.line((7, 54, 42, 54), fill=p["soft"])
    for x in (9, 17, 25, 33, 41):
        d.polygon([(x, 51), (x + 2, 54), (x, 57), (x - 2, 54)],
                  fill=p["deep"], outline=p["edge"])
    d.polygon([(8, 60), (41, 60), (38, 65), (34, 65), (31, 70),
               (18, 70), (15, 65), (11, 65)], fill="#3c2c3b", outline="#76566b")
    d.line((11, 61, 38, 61), fill=GOLD)
    d.rectangle((17, 69, 32, 75), fill="#2b2838", outline=p["soft"])

    # Carved guardian masks become angular panel geometry in successive bays.
    for index, (top, bottom) in enumerate(((77, 132), (137, 195),
                                           (200, 257), (262, 323))):
        d.rectangle((12, top, 37, bottom), fill="#292737", outline="#695368")
        d.rectangle((15, top + 3, 34, bottom - 4), fill="#171a28", outline=p["deep"])
        d.polygon([(16, top + 6), (19, top + 3), (30, top + 3),
                   (33, top + 6), (31, top + 10), (18, top + 10)],
                  fill="#403043", outline=p["soft"])
        if index < 3:
            d.line((17, top + 15, 21, top + 17, 23, top + 15), fill=p["edge"], width=2)
            d.line((27, top + 15, 29, top + 17, 33, top + 15), fill=p["edge"], width=2)
            d.polygon([(22, top + 19), (25, top + 22), (28, top + 19),
                       (27, top + 26), (23, top + 26)], fill="#574152")
            d.line((19, top + 31, 23, top + 34, 27, top + 34, 31, top + 31),
                   fill=p["soft"], width=2)
            d.line((21, top + 37, 29, top + 37), fill="#875f78")
        else:
            d.rectangle((18, top + 14, 31, top + 37), fill="#121522", outline=p["soft"])
            for y in range(top + 18, top + 34, 4):
                d.line((20, y, 27, y), fill="#4d5367")
                d.point((29, y), fill=p["light"])
        d.line((12, bottom - 1, 37, bottom - 1), fill="#100f1a", width=2)
        d.rectangle((9, bottom + 1, 40, bottom + 4), fill="#3b3042", outline="#6f536b")
        d.line((13, bottom + 2, 36, bottom + 2), fill=p["edge"])

        # Traces grow from the carved trim through the increasingly technical bays.
        start = top + 10
        length = (5, 20, 33, 45)[index]
        x = 10 if (index + (side == "right")) % 2 == 0 else 39
        inward = 4 if x == 10 else -4
        d.line((x, start, x, start + length // 2, x + inward, start + length // 2 + 4,
                x + inward, start + length), fill=p["edge"])
        if index >= 1:
            d.rectangle((x - 1, start + length - 1, x + 1, start + length + 1),
                        fill=p["light"])
            d.line((16, bottom - 8, 20, bottom - 8, 23, bottom - 11),
                   fill=p["accent"])
        if index >= 2:
            d.line((34, start + 4, 34, start + 12, 31, start + 15,
                    31, start + 23), fill=p["accent"])
            for y in range(top + 39, bottom - 6, 4):
                d.line((18, y, 25, y), fill=p["deep"])

    # Lower bay is visibly hardware: recessed ports, bundled traces and feet.
    d.rectangle((8, 329, 41, 359), fill="#242333", outline="#6e576b")
    d.rectangle((12, 332, 37, 354), fill="#111622", outline=p["soft"])
    for y in (336, 343, 350):
        d.line((15, y, 29, y), fill="#515269", width=2)
        d.rectangle((33, y - 1, 35, y + 1), fill=p["light"])
    for x in (15, 21, 28, 34):
        d.line((x, 360, x, 370, x - 3 if x < 25 else x + 3, 373,
                x - 3 if x < 25 else x + 3, 380), fill=p["edge"], width=2)
    d.polygon([(5, 371), (13, 371), (15, 378), (34, 378), (36, 371), (44, 371),
               (47, 386), (43, 393), (6, 393), (2, 386)], fill="#2a2939",
              outline="#766077")
    d.rectangle((7, 384, 42, 390), fill="#171a27", outline=p["edge"])
    d.line((10, 387, 39, 387), fill=p["soft"])
    for x in (8, 40):
        d.rectangle((x, 375, x + 1, 376), fill=GOLD)
    d.rectangle((21, 382, 28, 389), fill="#252c38", outline=p["light"])

    if side == "left":
        d.line((1, 116, 5, 107, 6, 94, 10, 85, 15, 77), fill="#77536c", width=2)
        d.line((6, 98, 3, 94, 2, 90), fill="#77536c")
        for x, y in ((4, 93), (9, 84), (14, 78)):
            d.line((x - 2, y, x + 2, y), fill="#c981a5", width=2)
            d.line((x, y - 2, x, y + 2), fill="#c981a5", width=2)
            d.point((x, y), fill="#f3bdc9")
    else:
        d.line((39, 76, 43, 76, 43, 96, 40, 100), fill=p["accent"], width=2)
        d.rectangle((41, 99, 43, 101), fill=p["accent"])
    return image.resize((TOTEM_SIZE[0] * SCALE, TOTEM_SIZE[1] * SCALE),
                        Image.Resampling.NEAREST)


def framed_card(name, side, row):
    with Image.open(ASSETS / f"ui-elements/project-{name}.png") as source:
        if source.size != CARD_SIZE:
            raise ValueError(f"{name} must be {CARD_SIZE}, got {source.size}")
        card = source.convert("RGB")
    totem = guardian(side).crop((0, row * CARD_SIZE[1],
                                TOTEM_SIZE[0] * SCALE, (row + 1) * CARD_SIZE[1]))
    result = Image.new("RGB", PANEL_SIZE, INK)
    if side == "left":
        result.paste(totem, (0, 0))
        result.paste(card, (totem.width, 0))
    else:
        result.paste(card, (0, 0))
        result.paste(totem, (card.width, 0))
    return result


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for side in PALETTES:
        guardian(side).save(OUTPUT / f"project-guardian-{side}.png", optimize=True)
    for name, side, row in CARDS:
        framed_card(name, side, row).save(OUTPUT / f"framed-{name}.png", optimize=True)
    print("Built two continuous totems and four desktop frame derivatives.")


if __name__ == "__main__":
    main()

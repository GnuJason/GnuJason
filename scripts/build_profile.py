"""Render original, reproducible pixel artwork for the GitHub profile."""

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CYAN = "#65f5ee"
PINK = "#ff65b8"
PURPLE = "#ab85ef"
WHITE = "#e7e5fa"
MUTED = "#9691b4"
INK = "#0c0b18"
FRAMES = 40
DURATION = 100
GLYPHS = {
    "A": "01110/10001/10001/11111/10001/10001/10001",
    "B": "11110/10001/10001/11110/10001/10001/11110",
    "C": "01111/10000/10000/10000/10000/10000/01111",
    "D": "11110/10001/10001/10001/10001/10001/11110",
    "E": "11111/10000/10000/11110/10000/10000/11111",
    "F": "11111/10000/10000/11110/10000/10000/10000",
    "G": "01111/10000/10000/10111/10001/10001/01111",
    "H": "10001/10001/10001/11111/10001/10001/10001",
    "I": "11111/00100/00100/00100/00100/00100/11111",
    "J": "00111/00010/00010/00010/10010/10010/01100",
    "K": "10001/10010/10100/11000/10100/10010/10001",
    "L": "10000/10000/10000/10000/10000/10000/11111",
    "M": "10001/11011/10101/10101/10001/10001/10001",
    "N": "10001/11001/11001/10101/10011/10011/10001",
    "O": "01110/10001/10001/10001/10001/10001/01110",
    "P": "11110/10001/10001/11110/10000/10000/10000",
    "Q": "01110/10001/10001/10001/10101/10010/01101",
    "R": "11110/10001/10001/11110/10100/10010/10001",
    "S": "01111/10000/10000/01110/00001/00001/11110",
    "T": "11111/00100/00100/00100/00100/00100/00100",
    "U": "10001/10001/10001/10001/10001/10001/01110",
    "V": "10001/10001/10001/10001/10001/01010/00100",
    "W": "10001/10001/10001/10101/10101/10101/01010",
    "X": "10001/10001/01010/00100/01010/10001/10001",
    "Y": "10001/10001/01010/00100/00100/00100/00100",
    "Z": "11111/00001/00010/00100/01000/10000/11111",
    "0": "01110/10001/10011/10101/11001/10001/01110",
    "1": "00100/01100/00100/00100/00100/00100/01110",
    "2": "01110/10001/00001/00010/00100/01000/11111",
    "3": "11110/00001/00001/01110/00001/00001/11110",
    "4": "00010/00110/01010/10010/11111/00010/00010",
    "5": "11111/10000/10000/11110/00001/00001/11110",
    "6": "01110/10000/10000/11110/10001/10001/01110",
    "7": "11111/00001/00010/00100/01000/01000/01000",
    "8": "01110/10001/10001/01110/10001/10001/01110",
    "9": "01110/10001/10001/01111/00001/00001/01110",
    ".": "00000/00000/00000/00000/00000/00110/00110",
    ",": "00000/00000/00000/00000/00110/00100/01000",
    ":": "00000/00110/00110/00000/00110/00110/00000",
    "/": "00001/00001/00010/00100/01000/10000/10000",
    "-": "00000/00000/00000/11111/00000/00000/00000",
    "_": "00000/00000/00000/00000/00000/00000/11111",
    ">": "10000/01000/00100/00010/00100/01000/10000",
    "+": "00000/00100/00100/11111/00100/00100/00000",
    "[": "01110/01000/01000/01000/01000/01000/01110",
    "]": "01110/00010/00010/00010/00010/00010/01110",
    "|": "00100/00100/00100/00100/00100/00100/00100",
    "\u2022": "00000/00000/00100/01110/00100/00000/00000",
    " ": "00000/00000/00000/00000/00000/00000/00000",
    "n": "00000/00000/11110/10001/10001/10001/10001",
    "u": "00000/00000/10001/10001/10001/10001/01111",
    "a": "00000/00000/01110/00001/01111/10001/01111",
    "s": "00000/00000/01111/10000/01110/00001/11110",
    "o": "00000/00000/01110/10001/10001/10001/01110",
}


def text(draw, position, value, color=WHITE, scale=1, mixed=False):
    left, top = position
    for index, character in enumerate(value if mixed else value.upper()):
        rows = GLYPHS[character].split("/")
        for row, pixels in enumerate(rows):
            for column, pixel in enumerate(pixels):
                if pixel == "1":
                    x_coord = left + (index * 6 + column) * scale
                    y_coord = top + row * scale
                    draw.rectangle((x_coord, y_coord, x_coord + scale - 1,
                                    y_coord + scale - 1), fill=color)


def bloom(image, lights, strength=0.45):
    haze = lights.filter(ImageFilter.GaussianBlur(5))
    image = ImageChops.add(image, haze, scale=1)
    return ImageChops.add(image, lights.point(lambda value: int(value * strength)))


def background():
    image = Image.new("RGB", (750, 250), INK)
    draw = ImageDraw.Draw(image)
    rng = random.Random(7)
    draw.rectangle((0, 0, 749, 203), fill="#171326")
    for top in range(18, 204, 46):
        for left in range(-25, 750, 104):
            draw.rectangle((left, top, left + 98, top + 42), fill="#1b172c", outline="#292037")
            for offset in (4, 93):
                draw.point((left + offset, top + 4), fill="#53405e")
                draw.point((left + offset, top + 38), fill="#100f1e")
    for _ in range(6500):
        left, top = rng.randrange(750), rng.randrange(203)
        draw.point((left, top), fill=rng.choice(("#211a30", "#171426", "#261c33")))
    draw.rectangle((0, 0, 749, 13), fill="#0d0d19")
    draw.line((0, 15, 750, 15), fill="#624569", width=2)
    draw.line((0, 20, 749, 20), fill="#30273f", width=3)
    draw.line((380, 0, 380, 186, 430, 204), fill="#100e1c", width=12)
    draw.line((378, 0, 378, 184, 429, 202), fill="#4e3757", width=3)
    for top in (32, 76, 124, 170):
        draw.rectangle((371, top, 387, top + 5), fill="#32283e", outline="#594366")
    draw.rectangle((416, 31, 652, 99), fill="#060c19", outline="#594363", width=3)
    draw.rectangle((422, 36, 646, 92), fill="#292047")
    for left in range(425, 645, 13):
        roof = rng.randrange(43, 74)
        draw.rectangle((left, roof, left + 11, 91), fill=rng.choice(("#111329", "#16152e", "#201936")))
        draw.line((left + 5, roof - 5, left + 5, roof), fill="#504571")
        for row in range(roof + 5, 87, 6):
            for column in range(left + 2, left + 10, 4):
                if rng.random() < 0.55:
                    draw.rectangle((column, row, column + 1, row + 2), fill=rng.choice(("#566989", "#785380", "#439fae")))
    draw.rectangle((543, 52, 548, 80), fill="#9e497e")
    draw.rectangle((544, 56, 546, 73), fill=PINK)
    draw.line((421, 96, 649, 96), fill="#728299", width=2)
    draw.line((489, 35, 489, 94), fill="#191a2c", width=4)
    draw.line((591, 35, 591, 94), fill="#191a2c", width=4)
    draw.rectangle((663, 29, 727, 48), fill="#10121e", outline="#3b3049")
    for left in range(669, 723, 5):
        draw.line((left, 33, left, 44), fill="#655069", width=2)
    for rack_left in (405, 675, 711):
        draw.rectangle((rack_left, 107, rack_left + 29, 201), fill="#0b101c", outline="#46324f", width=2)
        for top in range(113, 196, 13):
            draw.rectangle((rack_left + 4, top, rack_left + 25, top + 9), fill="#1d2032", outline="#373347")
            draw.line((rack_left + 7, top + 3, rack_left + 17, top + 3), fill="#565269")
    draw.polygon(((0, 204), (749, 204), (749, 249), (0, 249)), fill="#100f1e")
    for left in range(-400, 1200, 90):
        draw.line((510 + (left - 510) // 4, 204, left, 249), fill="#292033")
    for top in (213, 230, 247):
        draw.line((0, top, 749, top), fill="#2d2136")
    for left in range(425, 745, 24):
        draw.line((left, 210, left + 9, 210), fill="#483447")
    text(draw, (33, 48), "UNDERGROUND / INDEPENDENT", MUTED)
    text(draw, (34, 142), "SOFTWARE ENGINEER", WHITE, 2)
    text(draw, (34, 168), "CODE. AUTOMATE. REPEAT.", MUTED)
    text(draw, (31, 192), "07", "#594465", 2)
    text(draw, (83, 196), "NO SIGNAL LOST", "#756182")
    text(draw, (677, 63), "B-07", "#a171a6")
    draw.line((682, 80, 690, 73, 700, 84, 708, 76, 718, 81), fill="#604065", width=2)
    return image


def workstation(draw, lights, phase):
    glow = ImageDraw.Draw(lights)
    for column in range(29):
        left = 448 + column * 7
        height = 5 + int(26 * (0.5 + 0.5 * math.sin(phase + column * 0.67)))
        for top in range(130 - height, 132, 4):
            color = "#7651a3" if top > 116 else "#bb4e9b"
            draw.rectangle((left, top, left + 3, top + 1), fill=color)
            glow.rectangle((left, top, left + 3, top + 1), fill=color)
    for rack_left in (405, 675, 711):
        for index, top in enumerate(range(113, 196, 13)):
            color = CYAN if math.sin(phase + index * 2 + rack_left) > -0.3 else "#316168"
            draw.point((rack_left + 22, top + 4), fill=color)
            glow.rectangle((rack_left + 21, top + 3, rack_left + 23, top + 5), fill=color)
            draw.point((rack_left + 19, top + 7), fill=PINK)
    draw.polygon(((440, 165), (647, 165), (664, 176), (427, 176)), fill="#383048")
    draw.line((429, 176, 664, 176), fill=CYAN)
    glow.line((429, 177, 664, 177), fill="#337d89", width=3)
    draw.rectangle((430, 178, 662, 184), fill="#141322")
    draw.rectangle((443, 184, 449, 218), fill="#47304b")
    draw.rectangle((643, 184, 649, 218), fill="#47304b")
    for left, top, width, height, color in ((446, 126, 49, 35, PURPLE), (503, 112, 82, 49, CYAN), (594, 126, 57, 35, PINK)):
        draw.rectangle((left - 2, top - 2, left + width + 2, top + height + 2), fill="#070c16", outline="#585066")
        draw.rectangle((left, top, left + width, top + height), fill="#102532", outline=color)
        glow.rectangle((left, top, left + width, top + height), outline=color, width=2)
        draw.rectangle((left + width // 2 - 2, top + height + 3, left + width // 2 + 2, 167), fill="#777084")
        draw.line((left + width // 2 - 10, 168, left + width // 2 + 10, 168), fill="#726075", width=2)
        for row in range(top + 6, top + height - 4, 5):
            draw.rectangle((left + 4, row, left + 7, row + 1), fill="#56808b")
            line_length = 9 + ((row * 7) % (width - 20))
            draw.line((left + 11, row, left + 11 + line_length, row), fill=color if row % 3 else "#467787")
        for row in range(top + 2, top + height, 3):
            draw.line((left + 1, row, left + width - 1, row),
                      fill=(20, 35 + int(3 * math.sin(phase * 2)), 47))
    if math.sin(phase * 2) > 0:
        draw.rectangle((511, 149, 515, 151), fill=CYAN)
    draw.polygon(((484, 171), (531, 171), (536, 174), (480, 174)), fill="#698088")
    for left in range(485, 531, 4):
        draw.point((left, 172), fill=INK)
    draw.rectangle((624, 160, 631, 170), fill="#8a6688")
    draw.rectangle((631, 161, 634, 166), outline="#8a6688")
    draw.line((466, 184, 466, 210, 484, 216, 484, 225, 460, 230), fill="#5c4167", width=2)
    draw.line((618, 184, 618, 215, 638, 225, 683, 225), fill="#306c76", width=2)
    draw.polygon(((542, 155), (528, 163), (518, 185), (538, 196), (576, 192), (582, 168), (566, 155)), fill="#090d18")
    draw.line((541, 157, 531, 164, 522, 179), fill="#57818b", width=2)
    draw.line((567, 158, 577, 165, 580, 178), fill="#89517d", width=2)
    draw.polygon(((544, 128), (560, 126), (568, 135), (567, 149), (561, 159), (546, 156), (539, 145), (539, 135)), fill="#080d17")
    draw.line((542, 133, 547, 129, 560, 129), fill="#59858d", width=2)
    draw.line((566, 134, 568, 141, 566, 148), fill="#ab5b9a", width=2)
    draw.rectangle((538, 137, 541, 148), fill="#293847")
    draw.line((532, 173, 518, 170, 508, 173), fill="#4f596a", width=3)
    draw.line((578, 173, 592, 172, 600, 170), fill="#744760", width=3)
    draw.polygon(((533, 176), (568, 176), (573, 182), (569, 205), (536, 205), (530, 181)), fill="#222134", outline="#45425b")
    draw.line((536, 181, 565, 181), fill="#625575")
    draw.rectangle((549, 205, 554, 226), fill="#555368")
    draw.line((530, 230, 551, 224, 575, 231), fill="#767084", width=3)
    for left in (529, 551, 574):
        draw.rectangle((left, 230, left + 4, 233), fill="#090c15")
    draw.rectangle((685, 207, 726, 225), fill="#4d2846", outline="#946483")
    draw.rectangle((698, 203, 713, 207), outline="#ac7696")
    draw.line((686, 213, 725, 213), fill="#c481a8")
    draw.rectangle((704, 211, 708, 216), fill="#c8ac97")
    draw.rectangle((460, 191, 483, 222), fill="#171a28", outline="#453b53")
    draw.rectangle((464, 195, 479, 198), fill="#30364a")
    draw.point((477, 216), fill=CYAN)


def banner_frame(base, index):
    phase = math.tau * index / FRAMES
    image = base.copy()
    draw = ImageDraw.Draw(image)
    lights = Image.new("RGB", image.size)
    glow = ImageDraw.Draw(lights)
    rng = random.Random(91)
    for _ in range(58):
        left = rng.randrange(424, 646)
        top = 37 + (rng.randrange(54) + index * 3) % 54
        draw.line((left, top, left - 1, min(top + 3, 91)), fill="#567082")
    workstation(draw, lights, phase)
    pulse = int(160 + 22 * math.sin(phase))
    draw.line((453, 22, 572, 22), fill=(pulse // 2, pulse, pulse), width=2)
    glow.line((453, 22, 572, 22), fill=CYAN, width=3)
    draw.line((663, 96, 739, 96), fill=PINK)
    glow.line((663, 96, 739, 96), fill=PINK, width=2)
    text(glow, (33, 81), "GnuJason", "#735488", 6, mixed=True)
    text(draw, (35, 81), "GnuJason", "#aa437d", 6, mixed=True)
    text(draw, (32, 80), "GnuJason", "#348f9e", 6, mixed=True)
    text(draw, (33, 79), "GnuJason", WHITE, 6, mixed=True)
    draw.rectangle((326, 50, 330, 54), fill=CYAN)
    glow.rectangle((326, 50, 330, 54), fill=CYAN)
    draw.line((608, 108, 656, 108, 656, 121), fill="#48889a")
    text(draw, (611, 112), "SYS/07", "#80bfd0")
    for offset in range(5):
        left = 438 + offset * 29
        draw.line((left, 219 + offset % 3, left + 15, 219 + offset % 3), fill="#24434e")
    image = bloom(image, lights)
    draw = ImageDraw.Draw(image)
    for _ in range(35):
        left = (rng.randrange(750) + index * 2) % 750
        top = rng.randrange(22, 228)
        draw.point((left, top), fill="#393044")
    draw.rectangle((0, 237, 749, 249), fill="#0b0d17")
    text(draw, (21, 240), "CYBERPUNK BUNKER ENGINEER", CYAN)
    text(draw, (168, 240), "\u2022", PINK)
    text(draw, (187, 240), "DISTRIBUTED SYSTEMS", WHITE)
    text(draw, (305, 240), "\u2022", PINK)
    text(draw, (323, 240), "AUTOMATION ARCHITECT", WHITE)
    text(draw, (625, 240), "GNUJASON / 07", MUTED)
    return image


def save_gif(frames, path, size=None, duration=DURATION):
    palette = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    if size:
        indexed = [frame.resize(size, Image.Resampling.NEAREST) for frame in indexed]
    path.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(path, save_all=True, append_images=indexed[1:],
                    duration=duration, loop=0, optimize=True, disposal=1)
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size / 1024:.0f} KiB")


def build_banner(still=False):
    base = background()
    frames = [banner_frame(base, index) for index in range(1 if still else FRAMES)]
    destination = ASSETS / "banners"
    destination.mkdir(parents=True, exist_ok=True)
    frames[0].resize((3000, 1000), Image.Resampling.NEAREST).save(destination / "bunker-engineer.png")
    if not still:
        save_gif(frames, destination / "bunker-engineer.gif", (3000, 1000))


def save_pixel(image, relative_path, factor=2):
    path = ASSETS / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    image.resize((image.width * factor, image.height * factor), Image.Resampling.NEAREST).save(path)


def icon(draw, position, kind, color, scale=1):
    shapes = {
        "terminal": ("11111111111", "10000000001", "10100000001", "10010000001", "10100111001", "10000000001", "11111111111"),
        "chip": ("010101010", "111111111", "010000010", "110111011", "010101010", "110111011", "010000010", "111111111", "010101010"),
        "signal": ("00000100000", "00100100100", "00100100100", "00100100100", "10100100101", "10100100101", "10100100101"),
        "globe": ("000111000", "011010110", "010010010", "111111111", "100010001", "111111111", "010010010", "011010110", "000111000"),
    }
    left, top = position
    for row, pixels in enumerate(shapes[kind]):
        for column, pixel in enumerate(pixels):
            if pixel == "1":
                draw.rectangle((left + column * scale, top + row * scale,
                                left + (column + 1) * scale - 1,
                                top + (row + 1) * scale - 1), fill=color)


def build_interface():
    for name, kind, color in (("terminal", "terminal", CYAN), ("projects", "chip", PINK),
                              ("stack", "signal", PURPLE), ("signal", "globe", CYAN)):
        image = Image.new("RGBA", (16, 16))
        icon(ImageDraw.Draw(image), (2, 3), kind, color)
        save_pixel(image, f"icons/bunker-{name}.png", 4)
    divider = Image.new("RGB", (750, 12), INK)
    draw = ImageDraw.Draw(divider)
    draw.line((0, 5, 749, 5), fill="#463553")
    draw.line((0, 6, 250, 6), fill="#25858d")
    draw.line((500, 6, 749, 6), fill="#914775")
    for left, color in ((0, CYAN), (370, PURPLE), (744, PINK)):
        draw.rectangle((left, 3, left + 5, 8), fill=color)
    save_pixel(divider, "ascii-dividers/bunker-divider.png")
    for label, color in (("C / C++", CYAN), ("PYTHON", PINK), ("TYPESCRIPT", PURPLE),
                         ("REACT", CYAN), ("FASTAPI", PINK), ("D3.JS", PURPLE),
                         ("LINUX", CYAN), ("GIT", PINK)):
        width = len(label) * 12 + 40
        image = Image.new("RGB", (width, 34), INK)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width - 1, 33), outline="#51405e")
        draw.rectangle((0, 0, 3, 33), fill=color)
        draw.rectangle((13, 14, 17, 18), fill=color)
        text(draw, (26, 10), label, color, 2)
        slug = label.lower().replace(" / ", "-").replace("+", "p").replace(".", "-")
        save_pixel(image, f"ui-elements/badge-{slug}.png")


def project_art(draw, kind, color):
    if kind == "signal":
        for offset in range(0, 340, 12):
            height = 5 + int(18 * (0.5 + 0.5 * math.sin(offset * 0.12)))
            draw.rectangle((24 + offset, 68 - height, 29 + offset, 68), fill="#26404d")
        points = [(24 + offset, 60 - int(11 * math.sin(offset * 0.06))) for offset in range(0, 342, 3)]
        draw.line(points, fill=color, width=2)
    elif kind == "globe":
        for radius in (10, 20, 30):
            draw.ellipse((198 - radius, 49 - radius // 2, 198 + radius, 49 + radius // 2), outline="#76517d")
        draw.line((30, 49, 166, 49), fill="#493349")
        draw.line((230, 49, 368, 49), fill="#493349")
        for left, top in ((40, 49), (130, 49), (198, 49), (268, 49), (353, 49)):
            draw.rectangle((left - 2, top - 2, left + 2, top + 2), fill=color)
    elif kind == "terminal":
        text(draw, (26, 40), "> GEOME --HELP", color, 2)
        draw.line((26, 64, 133, 64), fill="#465064", width=2)
        draw.line((143, 64, 208, 64), fill="#465064", width=2)
    else:
        for offset in range(4):
            left = 38 + offset * 91
            draw.rectangle((left - 8, 27, left + 36, 69), outline="#393449")
            draw.rectangle((left + 5, 32, left + 18, 42), fill=color)
            draw.rectangle((left + 2, 44, left + 22, 54), fill="#6d587c")
            draw.line((left + 4, 54, left - offset, 64), fill=color, width=4)
            draw.line((left + 19, 54, left + 23 + offset, 64), fill=color, width=4)


def build_projects():
    projects = (
        ("f1", "01 / TELEMETRY", "F1 / PIT WALL", "Real-time system telemetry.", "A dashboard at race pace.", "PYTHON / FASTAPI / REACT", "signal", CYAN),
        ("geome", "02 / NETWORK TOOLS", "GEOME", "Geolocation. Network metadata.", "Straight from the terminal.", "C / CLI / NETWORKING", "terminal", PINK),
        ("pulse", "03 / OPEN DATA", "PULSE OF HUMANITY", "Global population, in motion.", "Open data. Live simulation.", "OPEN DATA / VISUALIZATION", "globe", PURPLE),
        ("spratforge", "04 / PIXEL ENGINE", "SPRATFORGE", "From pixels to animation.", "Sprite generation + tooling.", "C++ / CMAKE / PIXEL ART", "chip", CYAN),
    )
    for slug, label, title, first, second, stack, kind, color in projects:
        image = Image.new("RGB", (400, 200), INK)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 399, 199), outline="#473450", width=2)
        draw.line((0, 0, 96, 0), fill=color, width=2)
        text(draw, (20, 12), label, color)
        text(draw, (369, 12), ">", color)
        project_art(draw, kind, color)
        text(draw, (20, 83), title, WHITE, 3 if len(title) <= 19 else 2)
        text(draw, (20, 117), first, "#b9b4cc", 2)
        text(draw, (20, 139), second, "#b9b4cc", 2)
        draw.line((20, 166, 379, 166), fill="#33293e")
        icon(draw, (20, 178), kind, color)
        text(draw, (39, 180), stack, color)
        save_pixel(image, f"ui-elements/project-{slug}.png")


def build_typing():
    phrase = "> GNUJASON / BUILDING BELOW THE SURFACE."
    frames = []
    for index in range(64):
        image = Image.new("RGB", (750, 42), INK)
        draw = ImageDraw.Draw(image)
        length = min(len(phrase), index + 1)
        text(draw, (25, 14), phrase[:length], CYAN, 2)
        if index < len(phrase) or index % 12 < 6:
            draw.rectangle((25 + length * 12, 14, 33 + length * 12, 28), fill=PINK)
        frames.append(image)
    save_gif(frames, ASSETS / "animations/bunker-typing.gif", (1500, 84), 100)
    save_pixel(frames[len(phrase)], "animations/bunker-typing.png")


def build_footer():
    image = Image.new("RGB", (750, 74), INK)
    draw = ImageDraw.Draw(image)
    rng = random.Random(17)
    for left in range(0, 750, 12):
        roof = rng.randrange(4, 29)
        draw.rectangle((left, roof, left + 9, 36), fill="#282039")
        for top in range(roof + 4, 34, 6):
            draw.point((left + 4, top), fill=rng.choice((CYAN, PINK, PURPLE)))
    draw.line((0, 37, 749, 37), fill="#4d3557")
    text(draw, (267, 49), "END OF TRANSMISSION", WHITE, 2)
    text(draw, (318, 67), "GNUJASON / BUNKER 07", MUTED)
    save_pixel(image, "banners/bunker-footer.png")


def opensuse_badge():
    with Image.open(ASSETS / "icons/openSUSW_lizard.png") as source:
        red, green, blue = source.convert("RGB").split()
        mask = ImageChops.subtract(green, red).point(lambda value: 255 if value > 25 else 0)
    bounds = mask.getbbox()
    if bounds is None:
        raise ValueError("The openSUSE source must contain a green lizard")
    top = bounds[1]
    left = mask.crop((0, top, mask.width, top + 1)).getbbox()[0]
    ImageDraw.floodfill(mask, (left, top), 128)
    mask = mask.point(lambda value: 255 if value == 128 else 0)
    mask = mask.crop(mask.getbbox())
    mask.thumbnail((132, 70), Image.Resampling.NEAREST)
    image = Image.new("RGB", (750, 112), INK)
    draw = ImageDraw.Draw(image)
    for top in range(4, 108, 4):
        draw.line((0, top, 749, top), fill="#151122")
    for left in range(12, 750, 24):
        draw.line((left, 100, left + 8, 92), fill="#30243f")
    draw.line((0, 1, 170, 1, 180, 11, 455, 11, 465, 1, 749, 1), fill="#614883")
    draw.line((0, 110, 470, 110, 480, 100, 710, 100, 720, 110, 749, 110), fill="#614883")
    draw.line((0, 1, 70, 1), fill=PURPLE, width=2)
    draw.line((680, 110, 749, 110), fill=PINK, width=2)
    for index in range(6):
        start = 22 + index * 13
        bend = 505 + index * 20
        end = 17 + index * 15
        draw.line((462, start, bend, start, bend + 14, end, 736, end),
                  fill="#614883" if index % 2 else "#39294f")
        draw.rectangle((733, end - 2, 737, end + 2), outline=PURPLE)
        pulse = 615 + index * 15
        draw.line((pulse, end, pulse + 12, end), fill=CYAN if index == 2 else PURPLE)
    draw.line((17, 28, 17, 18, 40, 18), fill=CYAN)
    draw.line((144, 88, 166, 88, 166, 78), fill=PINK)
    position = (27, (112 - mask.height) // 2)
    image.paste("#493263", (position[0] + 3, position[1] + 2), mask)
    lizard = Image.new("RGB", mask.size, PURPLE)
    lizard_draw = ImageDraw.Draw(lizard)
    for top in range(3, mask.height, 6):
        lizard_draw.line((0, top, mask.width, top), fill="#9570d4")
    image.paste(lizard, position, mask)
    text(draw, (191, 31), "OPENSUSE", "#493263", 5)
    text(draw, (188, 29), "OPENSUSE", PURPLE, 5)
    draw.line((188, 72, 260, 72), fill=CYAN)
    draw.line((267, 72, 425, 72), fill="#614883")
    text(draw, (188, 83), "BUILT IN THE OPEN", MUTED, 2)
    return image


def build_opensuse():
    save_pixel(opensuse_badge(), "opensuse/opensuse-pixel.png")


def build_heritage_stills():
    for source, destination in (
        ("animations/ILoveYouHeartGIFbyCarawrrr.gif", "icons/finger-heart.png"),
        ("animations/KoreanKickingGIFbyTomtomi.gif", "animations/korean-character-still.png"),
    ):
        with Image.open(ASSETS / source) as image:
            image.seek(0)
            image.convert("RGBA").save(ASSETS / destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--still", action="store_true", help="Render only the banner poster for a quick art check")
    parser.add_argument("--heritage-only", action="store_true", help="Extract stills from the supplied heritage GIFs")
    parser.add_argument("--opensuse-only", action="store_true", help="Render only the openSUSE dedication badge")
    args = parser.parse_args()
    if args.opensuse_only:
        build_opensuse()
        return
    if args.heritage_only:
        build_heritage_stills()
        return
    build_banner(args.still)
    if not args.still:
        build_interface()
        build_projects()
        build_typing()
        build_footer()
        build_heritage_stills()
        build_opensuse()


if __name__ == "__main__":
    main()
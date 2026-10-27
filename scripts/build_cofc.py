"""Render the Charleston courtyard-to-bunker panorama without changing other art."""

import random

from PIL import Image, ImageDraw

from build_profile import CYAN, INK, MUTED, PINK, PURPLE, WHITE, bloom, save_pixel, text, workstation


GOLD = "#d5ad62"


def montage():
    image = Image.new("RGB", (750, 250), INK)
    draw = ImageDraw.Draw(image)
    lights = Image.new("RGB", image.size)
    glow = ImageDraw.Draw(lights)
    rng = random.Random(1770)

    # One continuous night sky and courtyard, becoming the bunker floor.
    for top in range(16, 195):
        blend = (top - 16) / 179
        draw.line((0, top, 749, top),
                  fill=(23 + int(13 * blend), 19 + int(5 * blend), 41 + int(14 * blend)))
    for _ in range(100):
        x, y = rng.randrange(405), rng.randrange(44, 115)
        draw.point((x, y), fill=rng.choice(("#453553", "#56405e", "#29253f")))
    for x, height in ((0, 40), (40, 48), (88, 34), (132, 52), (351, 45), (380, 37)):
        draw.rectangle((x, 151 - height, x + 36, 193), fill="#1b192e")
        draw.line((x - 3, 151 - height, x + 18, 139 - height, x + 39, 151 - height),
                  fill="#3c2b49", width=2)
    draw.rectangle((0, 194, 749, 236), fill="#100f1e")
    for x in range(-400, 1200, 64):
        draw.line((284 + (x - 284) // 6, 191, x, 236), fill="#33263d")
    for y in (197, 205, 217, 234):
        draw.line((0, y, 749, y), fill="#32263b")

    # Charleston brick houses and shaded piazzas.
    for left, top, right in ((12, 104, 78), (84, 89, 155)):
        draw.rectangle((left, top, right, 188), fill="#392635", outline="#604052")
        for y in range(top + 4, 187, 5):
            draw.line((left + 1, y, right - 1, y), fill="#2b2132")
            for x in range(left + (y % 2) * 5 + 3, right, 12):
                draw.line((x, y - 4, x, y), fill="#4a3041")
        draw.polygon(((left - 4, top), (left + 10, top - 13),
                      (right - 10, top - 13), (right + 5, top)), fill="#161626")
        draw.line((left - 3, top, right + 4, top), fill="#856079", width=2)
        draw.rectangle((right - 17, top - 19, right - 11, top - 8), fill="#503344")
        for y in (top + 12, top + 44):
            for x in range(left + 8, right - 8, 24):
                draw.rectangle((x - 3, y - 2, x + 13, y + 22), fill="#171a28")
                draw.rectangle((x, y, x + 10, y + 19), fill="#70513e", outline="#a17c54")
                draw.rectangle((x + 2, y + 2, x + 8, y + 17), fill=GOLD)
                glow.rectangle((x + 2, y + 2, x + 8, y + 17), fill="#543716")
                draw.line((x + 5, y, x + 5, y + 19), fill="#3b2934")
                draw.line((x, y + 9, x + 10, y + 9), fill="#3b2934")
        for y in (top + 38, 182):
            draw.line((left - 2, y, right + 3, y), fill="#877083", width=2)
        for x in range(left + 2, right, 18):
            draw.line((x, top + 39, x, 182), fill="#635268", width=2)
        for x in range(left + 4, right, 5):
            draw.line((x, 174, x, 181), fill="#847080")
        draw.line((left, 173, right, 173), fill="#a28a96")

    # Randolph Hall-inspired portico and paired stairs, not a seal or logo.
    draw.rectangle((176, 97, 382, 180), fill="#422b3e", outline="#674256")
    for y in range(101, 180, 5):
        draw.line((177, y, 381, y), fill="#302236")
        for x in range(179 + (y % 2) * 6, 380, 13):
            draw.line((x, y - 3, x, y), fill="#563449")
    draw.polygon(((170, 97), (188, 80), (367, 80), (389, 97)), fill="#232033")
    draw.line((174, 96, 386, 96), fill="#836176", width=2)
    for x in (186, 209, 338, 361):
        for y in (108, 139):
            draw.rectangle((x, y, x + 12, y + 22), fill="#161827", outline="#7f6071")
            draw.rectangle((x + 3, y + 3, x + 9, y + 19), fill="#b68e53")
            glow.rectangle((x + 4, y + 4, x + 8, y + 18), fill="#4d331a")
            draw.line((x + 6, y + 1, x + 6, y + 21), fill="#493743")
            draw.line((x + 1, y + 10, x + 11, y + 10), fill="#493743")
    draw.rectangle((235, 107, 324, 171), fill="#252032")
    for x in (250, 276, 302):
        draw.rectangle((x, 125, x + 12, 170), fill="#0c111e", outline="#674a5e")
        draw.arc((x, 117, x + 12, 134), 180, 360, fill="#a38b92")
        draw.rectangle((x + 3, 126, x + 9, 137), fill="#aa8250")
        draw.line((x + 6, 127, x + 6, 137), fill="#3d3040")
    draw.polygon(((220, 106), (279, 65), (339, 106)), fill="#746174")
    draw.polygon(((230, 102), (279, 73), (329, 102)), fill="#342b42")
    draw.line((230, 102, 279, 73, 329, 102), fill="#a28b98")
    draw.line((220, 106, 339, 106), fill="#c6a579", width=2)
    draw.rectangle((224, 109, 334, 115), fill="#8e7c91")
    draw.line((225, 116, 333, 116), fill="#3e3048")
    for x in (230, 248, 267, 286, 305, 324):
        draw.rectangle((x, 119, x + 6, 168), fill="#82748c")
        draw.line((x + 1, 120, x + 1, 167), fill="#b1a1b3")
        draw.line((x + 5, 120, x + 5, 168), fill="#594b69")
        draw.rectangle((x - 2, 117, x + 8, 120), fill="#b19aa7")
        draw.rectangle((x - 2, 168, x + 8, 171), fill="#a18b9d")
    draw.rectangle((225, 172, 337, 177), fill="#746076")
    draw.line((225, 172, 337, 172), fill="#c1a28e")
    draw.polygon(((252, 177), (308, 177), (308, 194), (252, 194)), fill="#392b42")
    draw.arc((269, 179, 291, 206), 180, 360, fill="#9c7d91", width=2)
    draw.rectangle((271, 191, 289, 195), fill="#0d111e")
    for step in range(8):
        y = 178 + step * 2
        left, right = 225 - step * 4, 337 + step * 4
        draw.line((left, y, left + 27, y), fill="#9f879d")
        draw.line((right - 27, y, right, y), fill="#9f879d")
        draw.line((left, y + 1, left + 27, y + 1), fill="#4f3d54")
        draw.line((right - 27, y + 1, right, y + 1), fill="#4f3d54")
    draw.line((223, 172, 210, 183, 193, 189), fill="#c4a688")
    draw.line((339, 172, 352, 183, 369, 189), fill="#8d7b98")
    for x, y in ((223, 173), (211, 182), (199, 187), (340, 173), (352, 182), (364, 187)):
        draw.line((x, y, x, y + 7), fill="#958091")

    # The oak frames the campus; sparse moss and leaves retain the night palette.
    draw.polygon(((36, 198), (51, 196), (43, 157), (44, 121), (67, 87),
                  (59, 85), (38, 111), (29, 90), (18, 83), (32, 126), (33, 161)),
                 fill="#0c131d")
    draw.line((42, 187, 38, 151, 39, 119, 61, 88), fill="#38404b", width=2)
    draw.line((38, 119, 16, 101, 1, 102), fill="#0c131d", width=6)
    draw.line((42, 113, 81, 102, 106, 77, 156, 74), fill="#0c131d", width=5)
    for _ in range(180):
        x = rng.randrange(0, 172)
        y = rng.randrange(49, 88) + int(9 * (x / 172))
        width = rng.randrange(4, 17)
        draw.rectangle((x, y, x + width, y + rng.randrange(2, 7)),
                       fill=rng.choice(("#111d28", "#192633", "#22303c", "#2d3447")))
    for x, y in ((21, 88), (70, 91), (88, 96), (118, 88), (146, 86), (161, 85)):
        draw.line((x, y, x - 1, y + 12, x + 2, y + 17), fill="#47505b")
        draw.line((x + 3, y, x + 4, y + 9), fill="#313f49")
    for x in range(2, 178, 7):
        draw.line((x, 185, x, 208), fill="#0b101b", width=2)
        draw.point((x, 183), fill="#90748c")
    draw.line((0, 190, 177, 190), fill="#544158")
    draw.line((0, 203, 177, 203), fill="#544158")
    for x in (167, 382):
        draw.rectangle((x - 1, 163, x + 1, 204), fill="#625266")
        draw.rectangle((x - 5, 153, x + 5, 164), fill="#322838", outline="#99816a")
        draw.rectangle((x - 3, 155, x + 3, 161), fill=GOLD)
        glow.rectangle((x - 4, 154, x + 4, 162), fill="#735022")
        draw.line((x, 154, x, 162), fill="#554034")
        draw.polygon(((x - 7, 152), (x, 147), (x + 7, 152)), fill="#74616c")
        for y, width in ((208, 7), (214, 11), (225, 5)):
            draw.line((x - width, y, x + width, y), fill="#68503e")
    for _ in range(280):
        x, y = rng.randrange(390), rng.randrange(197, 235)
        draw.point((x, y), fill=rng.choice(("#251f33", "#37283d", "#463147")))

    # The same engineer and electronics as the hero inhabit the adjoining bay.
    draw.rectangle((399, 47, 749, 195), fill="#171326")
    for y in range(48, 194, 37):
        for x in range(403, 750, 68):
            draw.rectangle((x, y, x + 63, y + 32), fill="#1b172c", outline="#292037")
            draw.point((x + 4, y + 4), fill="#594366")
    draw.line((396, 47, 396, 182, 414, 197), fill="#0d0e19", width=9)
    draw.line((395, 47, 395, 181, 414, 198), fill="#715172", width=2)
    for y in (57, 98, 141):
        draw.rectangle((389, y, 401, y + 4), fill="#32283e", outline="#594366")
    draw.rectangle((426, 58, 657, 92), fill="#0c101c", outline="#584162")
    text(draw, (437, 67), "JASON / ENGINEERING", WHITE)
    text(draw, (437, 81), "> CAMPUS TO BUNKER_07", PURPLE)
    draw.line((431, 54, 575, 54), fill=PURPLE)
    glow.line((431, 54, 575, 54), fill="#694b9b", width=2)
    for index in range(4):
        y = 62 + index * 8
        draw.line((668, y, 690 + index * 8, y, 701 + index * 8, y + 8, 739, y + 8),
                  fill="#614883")
        draw.rectangle((736, y + 6, 740, y + 10), outline=PINK if index % 2 else PURPLE)
    for x in (405, 675, 711):
        draw.rectangle((x, 107, x + 29, 201), fill="#0b101c", outline="#46324f", width=2)
        for y in range(113, 196, 13):
            draw.rectangle((x + 4, y, x + 25, y + 9), fill="#1d2032", outline="#373347")
            draw.line((x + 7, y + 3, x + 17, y + 3), fill="#565269")
    workstation(draw, lights, 0)
    for x, color in ((280, "#776144"), (324, "#7f587f"), (370, "#815cb2"), (416, "#478a94")):
        draw.line((x, 221, x + 24, 221, x + 30, 227, x + 43, 227), fill=color)
        draw.rectangle((x, 220, x + 2, 222), fill=color)
    image = bloom(image, lights)
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 749, 43), fill=INK)
    draw.line((0, 1, 170, 1, 181, 12, 573, 12, 584, 1, 749, 1), fill="#614883")
    draw.line((0, 1, 62, 1), fill=PURPLE, width=2)
    text(draw, (20, 23), "COLLEGE OF CHARLESTON", WHITE, 2)
    text(draw, (445, 27), "CHARLESTON / SOUTH CAROLINA", MUTED)
    draw.rectangle((720, 27, 724, 31), fill=GOLD)
    draw.line((20, 42, 260, 42), fill="#735579")
    draw.rectangle((0, 237, 749, 249), fill=INK)
    text(draw, (20, 240), "SOFTWARE ENGINEERING / COMPUTER SCIENCE", MUTED)
    text(draw, (610, 240), "GNUJASON / 07", PURPLE)
    draw.rectangle((0, 0, 749, 249), outline="#463553")
    return image


if __name__ == "__main__":
    save_pixel(montage(), "cofc/cofc-montage.png", factor=4)

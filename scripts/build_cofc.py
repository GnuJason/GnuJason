"""Render the full-width Charleston campus panorama without changing other art."""

import random

from PIL import Image, ImageDraw

from build_profile import CYAN, INK, MUTED, PINK, PURPLE, bloom, save_pixel, text


GOLD = "#d5ad62"


def montage():
    image = Image.new("RGB", (750, 250), INK)
    draw = ImageDraw.Draw(image)
    lights = Image.new("RGB", image.size)
    glow = ImageDraw.Draw(lights)
    rng = random.Random(1770)

    # One continuous night sky and courtyard across the original pixel grid.
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
    # Extend the campus at its original scale, with lower roofs behind the portico.
    garden = random.Random(1772)
    for x, top, width in ((408, 113, 51), (506, 121, 67), (556, 116, 59), (699, 126, 50)):
        draw.rectangle((x, top, x + width, 188), fill="#1b192e")
        draw.polygon(((x - 3, top), (x + 12, top - 11),
                      (x + width - 9, top - 11), (x + width + 3, top)), fill="#211c32")
        for wx in range(x + 8, x + width - 5, 15):
            for wy in range(top + 10, 178, 20):
                draw.rectangle((wx, wy, wx + 4, wy + 7), fill="#6c5551")

    draw.polygon(((546, 171), (575, 171), (649, 236), (450, 236)), fill="#211b2c")
    draw.line((546, 171, 450, 236), fill="#65506b")
    draw.line((575, 171, 649, 236), fill="#4d415e")
    for y, left, right in ((183, 529, 588), (196, 510, 604), (212, 486, 622), (231, 458, 644)):
        draw.line((left, y, right, y), fill="#44334c")
        for x in range(left + 8, right, 16):
            draw.line((x, y - 3, x + 3, y), fill="#36283f")

    for left, top, right in ((405, 116, 526), (590, 109, 716)):
        draw.rectangle((left, top, right, 183), fill="#352638", outline="#604052")
        for y in range(top + 4, 182, 5):
            draw.line((left + 1, y, right - 1, y), fill="#282133")
            for x in range(left + 3 + (y % 2) * 6, right, 13):
                draw.line((x, y - 3, x, y), fill="#493346")
        draw.polygon(((left - 5, top), (left + 15, top - 18),
                      (right - 14, top - 18), (right + 5, top)), fill="#211c30")
        draw.line((left + 15, top - 18, right - 14, top - 18), fill="#58415e")
        draw.line((left - 4, top, right + 4, top), fill="#876880", width=2)
        draw.line((left - 2, top + 3, right + 2, top + 3), fill="#4f3d54")
        for x in (left + 21, right - 24):
            draw.rectangle((x, top - 26, x + 7, top - 13), fill="#483044")
            draw.line((x - 1, top - 27, x + 8, top - 27), fill="#826072", width=2)
        for x in range(left + 10, right - 10, 25):
            for y in (top + 12, top + 39):
                draw.rectangle((x - 2, y - 2, x + 12, y + 20), fill="#151725", outline="#665269")
                draw.rectangle((x + 1, y, x + 9, y + 17), fill="#b68e53")
                glow.rectangle((x + 3, y + 2, x + 7, y + 15), fill="#432d18")
                draw.line((x + 5, y, x + 5, y + 18), fill="#3c2c3c")
                draw.line((x, y + 8, x + 10, y + 8), fill="#3c2c3c")
                draw.line((x - 3, y + 21, x + 13, y + 21), fill="#8b7182")
        draw.line((left, top + 36, right, top + 36), fill="#6a5167")
        draw.rectangle((left - 3, 184, right + 3, 187), fill="#504056")
        draw.line((left - 3, 184, right + 3, 184), fill="#897188")

    # A recessed garden gate and modest electronics replace the indoor workstation.
    draw.rectangle((548, 148, 571, 173), fill="#0c111e")
    draw.arc((547, 134, 572, 163), 180, 360, fill="#745c75", width=2)
    for x in range(551, 571, 4):
        draw.line((x, 148, x, 172), fill="#51435e")
    draw.line((549, 155, 570, 155), fill="#80708a")
    draw.rectangle((532, 158, 537, 168), fill="#222637", outline="#665775")
    draw.line((533, 160, 536, 160), fill=CYAN)
    draw.point((534, 165), fill=PURPLE)
    draw.line((595, 113, 615, 113), fill="#69558b")
    draw.line((677, 113, 700, 113), fill="#478a94")
    glow.line((677, 113, 700, 113), fill="#153d48")

    for left, right in ((398, 476), (615, 680), (707, 749)):
        draw.polygon(((left, 191), (right - 10, 191), (right, 201), (left - 5, 201)),
                     fill="#121c28", outline="#303442")
        for _ in range(38):
            x, y = garden.randrange(left, right), garden.randrange(182, 196)
            draw.rectangle((x, y, x + garden.randrange(2, 6), y + 3),
                           fill=garden.choice(("#172735", "#21313c", "#2c3546")))
        draw.line((left - 5, 202, right, 202), fill="#57405f")
    for x in (455, 631):
        draw.polygon(((x, 190), (x + 29, 190), (x + 33, 194), (x - 3, 194)), fill="#48334b")
        draw.line((x, 183, x + 28, 183), fill="#796078", width=2)
        draw.line((x, 187, x + 28, 187), fill="#614b65")
        for leg in (x + 1, x + 27):
            draw.line((leg, 184, leg, 201), fill="#514658", width=2)

    draw.polygon(((695, 208), (710, 208), (706, 163), (718, 116),
                  (713, 101), (700, 143), (688, 117), (681, 112), (695, 163)),
                 fill="#0c131d")
    draw.line((702, 199, 700, 163, 711, 121), fill="#36404c", width=2)
    draw.line((702, 145, 675, 116, 649, 108), fill="#0c131d", width=5)
    draw.line((713, 123, 738, 106, 749, 84), fill="#0c131d", width=4)
    for _ in range(170):
        x = garden.randrange(640, 750)
        y = garden.randrange(58, 103) + abs(x - 706) // 5
        draw.rectangle((x, y, x + garden.randrange(4, 13), y + garden.randrange(2, 6)),
                       fill=garden.choice(("#101c28", "#172633", "#22303c", "#293247")))
    for x, y in ((655, 110), (678, 108), (727, 109), (744, 105)):
        draw.line((x, y, x - 1, y + 12, x + 2, y + 16), fill="#414957")
        draw.line((x + 3, y, x + 3, y + 7), fill="#2f3c48")

    for x in (167, 382, 540, 580, 732):
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

    for _ in range(220):
        x, y = garden.randrange(395, 750), garden.randrange(204, 235)
        draw.point((x, y), fill=garden.choice(("#251f33", "#37283d", "#463147")))
    for x, color in ((280, "#776144"), (324, "#7f587f"), (370, "#815cb2"),
                     (416, "#478a94"), (610, "#478a94"), (659, "#815cb2"), (705, "#7f587f")):
        draw.line((x, 221, x + 24, 221, x + 30, 227, x + 43, 227), fill=color)
        draw.rectangle((x, 220, x + 2, 222), fill=color)
    draw.line((661, 226, 673, 226), fill=PINK)
    image = bloom(image, lights)
    draw = ImageDraw.Draw(image)

    # Extend the canopy and night sky into the former title band.
    for y in range(44):
        blend = max(0, y - 16) / 179
        draw.line((0, y, 749, y),
                  fill=(23 + int(13 * blend), 19 + int(5 * blend), 41 + int(14 * blend)))
    crown = random.Random(1771)
    for _ in range(55):
        x, y = crown.randrange(175, 389), crown.randrange(16, 43)
        draw.point((x, y), fill=crown.choice(("#453553", "#56405e", "#29253f")))
    for x, y, width in ((183, 26, 47), (211, 29, 65), (308, 19, 51), (328, 22, 38)):
        draw.line((x, y, x + width, y), fill="#30253f")
    draw.line((16, 57, 48, 36, 82, 34, 111, 44), fill="#0c131d", width=4)
    for _ in range(150):
        x = crown.randrange(0, 165)
        y = crown.randrange(25, 50) + abs(x - 70) // 14
        draw.rectangle((x, y, x + crown.randrange(4, 17), y + crown.randrange(2, 6)),
                       fill=crown.choice(("#111d28", "#192633", "#22303c", "#2d3447")))
    for _ in range(90):
        x, y = garden.randrange(396, 749), garden.randrange(17, 91)
        draw.point((x, y), fill=garden.choice(("#453553", "#56405e", "#29253f")))
    for x, y, width in ((415, 33, 63), (443, 36, 76), (549, 24, 54), (567, 27, 62)):
        draw.line((x, y, x + width, y), fill="#30253f")
    draw.line((0, 1, 170, 1, 181, 12, 573, 12, 584, 1, 749, 1), fill="#614883")
    draw.line((0, 1, 62, 1), fill=PURPLE, width=2)
    draw.rectangle((0, 237, 749, 249), fill=INK)
    text(draw, (20, 240), "SOFTWARE ENGINEERING / COMPUTER SCIENCE", MUTED)
    text(draw, (610, 240), "GNUJASON / 07", PURPLE)
    draw.rectangle((0, 0, 749, 249), outline="#463553")
    return image


if __name__ == "__main__":
    save_pixel(montage(), "cofc/cofc-montage.png", factor=4)

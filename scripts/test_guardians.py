"""Regression tests for visible totems and unchanged project-card pixels."""

from html.parser import HTMLParser
import unittest

from PIL import Image, ImageChops

import build_guardians as guardians
from build_profile import ROOT, ASSETS


class ProjectParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.href = None
        self.cards = []
        self.sources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p" and attrs.get("id") == "project-bays":
            self.active = True
        if self.active and tag == "a":
            self.href = attrs["href"]
        if self.active and tag == "source":
            self.sources.append((self.href, attrs))
        if self.active and tag == "img":
            self.cards.append((self.href, attrs))

    def handle_endtag(self, tag):
        if tag == "a":
            self.href = None
        if tag == "p":
            self.active = False


class GuardianTests(unittest.TestCase):
    def test_artwork_is_static_reproducible_and_visible(self):
        for side in guardians.PALETTES:
            path = guardians.OUTPUT / f"project-guardian-{side}.png"
            with Image.open(path) as image:
                self.assertEqual(image.size, (100, 800))
                self.assertEqual(image.n_frames, 1)
                self.assertEqual(image.tobytes(), guardians.guardian(side).tobytes())
                for region in ((0, 0, 100, 150), (0, 150, 100, 500),
                               (0, 500, 100, 800)):
                    colors = image.crop(region).getcolors(100000)
                    self.assertGreater(len(colors), 10)
                    self.assertTrue(any(max(color) >= 130 for count, color in colors))
                self.assertLess(path.stat().st_size, 50_000)
        self.assertIsNotNone(ImageChops.difference(
            guardians.guardian("left"), guardians.guardian("right")).getbbox())

    def test_composite_preserves_every_original_card_pixel(self):
        for name, side, row in guardians.CARDS:
            with self.subTest(card=name):
                with Image.open(guardians.OUTPUT / f"framed-{name}.png") as result:
                    self.assertEqual(result.size, guardians.PANEL_SIZE)
                    self.assertEqual(result.tobytes(),
                                     guardians.framed_card(name, side, row).tobytes())
                    bounds = (100, 0, 900, 400) if side == "left" else (0, 0, 800, 400)
                    with Image.open(ASSETS / f"ui-elements/project-{name}.png") as original:
                        self.assertEqual(result.crop(bounds).tobytes(),
                                         original.convert("RGB").tobytes())
                    bounds = (0, 0, 100, 400) if side == "left" else (800, 0, 900, 400)
                    self.assertEqual(result.crop(bounds).tobytes(),
                                     guardians.guardian(side).crop(
                                         (0, row * 400, 100, (row + 1) * 400)).tobytes())

    def test_responsive_originals_and_links(self):
        readme = (ROOT / "README.md").read_text()
        parser = ProjectParser()
        parser.feed(readme)
        urls = ["https://github.com/GnuJason/F1", "https://github.com/GnuJason/geome",
                "https://github.com/GnuJason/Pulse-of-Humanity",
                "https://github.com/GnuJason/spratforge"]
        self.assertEqual([href for href, _ in parser.cards], urls)
        self.assertEqual([href for href, _ in parser.sources], urls)
        for (name, _, _), (_, image), (_, source) in zip(
                guardians.CARDS, parser.cards, parser.sources):
            self.assertEqual(image["src"], f"assets/ui-elements/project-{name}.png")
            self.assertEqual(image["width"], "390")
            self.assertTrue(image["alt"])
            self.assertEqual(source["srcset"], f"assets/guardians/framed-{name}.png")
            self.assertEqual(source["media"], "(min-width: 1280px)")
            self.assertEqual(source["width"], "420")
            self.assertTrue((ROOT / source["srcset"]).is_file())
        self.assertNotIn("<table", readme)
        self.assertNotIn("style=", readme)
        self.assertNotIn("<script", readme)


if __name__ == "__main__":
    unittest.main()

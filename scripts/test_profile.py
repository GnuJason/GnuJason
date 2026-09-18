"""Checks for generated profile artwork and GitHub README embeds."""

from html.parser import HTMLParser
import unittest

from PIL import Image, ImageChops, ImageSequence

import build_profile as profile


class ReadmeImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.anchors = []
        self.targets = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "source":
            self.sources.append(attrs)
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if "id" in attrs:
            self.targets.add(attrs["id"])


class ProfileTests(unittest.TestCase):
    def test_banner_contract(self):
        path = profile.ASSETS / "banners/bunker-engineer.gif"
        with Image.open(path) as image:
            self.assertEqual(image.size, (3000, 1000))
            self.assertEqual(image.n_frames, 40)
            self.assertEqual(image.info["loop"], 0)
            self.assertEqual(sum(frame.info["duration"] for frame in ImageSequence.Iterator(image)), 4000)
        self.assertLess(path.stat().st_size, 5 * 1024 * 1024)

    def test_motion_regions(self):
        base = profile.background()
        first = profile.banner_frame(base, 0)
        later = profile.banner_frame(base, 5)
        for label, region in (("rain", (422, 37, 646, 92)),
                              ("equalizer", (448, 101, 495, 124)),
                              ("cursor", (511, 149, 516, 152)),
                              ("server LEDs", (405, 107, 435, 202))):
            with self.subTest(region=label):
                self.assertIsNotNone(ImageChops.difference(first.crop(region), later.crop(region)).getbbox())

    def test_deterministic_art(self):
        first = profile.banner_frame(profile.background(), 3)
        repeated = profile.banner_frame(profile.background(), 3)
        self.assertIsNone(ImageChops.difference(first, repeated).getbbox())

    def test_exact_pixel_scaling(self):
        with Image.open(profile.ASSETS / "banners/bunker-engineer.png") as image:
            small = image.resize((750, 250), Image.Resampling.NEAREST)
            restored = small.resize(image.size, Image.Resampling.NEAREST)
            self.assertIsNone(ImageChops.difference(image, restored).getbbox())

    def test_readme_embeds_and_anchors(self):
        parser = ReadmeImages()
        parser.feed((profile.ROOT / "README.md").read_text())
        self.assertGreater(len(parser.images), 15)
        for attrs in parser.images:
            self.assertIn("alt", attrs)
            self.assertTrue((profile.ROOT / attrs["src"]).is_file(), attrs["src"])
        self.assertEqual(len(parser.sources), 2)
        for attrs in parser.sources:
            self.assertEqual(attrs["media"], "(prefers-reduced-motion: reduce)")
            self.assertTrue((profile.ROOT / attrs["srcset"]).is_file())
        for anchor in parser.anchors:
            self.assertIn(anchor, parser.targets)

    def test_typing_animation(self):
        with Image.open(profile.ASSETS / "animations/bunker-typing.gif") as image:
            self.assertEqual(image.size, (1500, 84))
            self.assertGreater(image.n_frames, 30)
            self.assertEqual(image.info["loop"], 0)
            self.assertEqual(sum(frame.info["duration"] for frame in ImageSequence.Iterator(image)), 6400)

    def test_project_cards(self):
        for name in ("f1", "geome", "pulse", "spratforge"):
            with Image.open(profile.ASSETS / f"ui-elements/project-{name}.png") as image:
                self.assertEqual(image.size, (800, 400))


if __name__ == "__main__":
    unittest.main()
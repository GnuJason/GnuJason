"""Checks for generated profile artwork and GitHub README embeds."""

from html.parser import HTMLParser
import unittest
from unittest.mock import patch

import markdown
from PIL import Image, ImageChops, ImageSequence

import build_cofc
import build_profile as profile


class ReadmeImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.anchors = []
        self.targets = set()
        self.headings = []
        self.target_elements = []

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
            self.target_elements.append((tag, attrs))
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(tag)


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
        self.assertEqual(len(parser.sources), 3)
        for attrs in parser.sources:
            self.assertEqual(attrs["media"], "(prefers-reduced-motion: reduce)")
            self.assertTrue((profile.ROOT / attrs["srcset"]).is_file())
        for anchor in parser.anchors:
            self.assertIn(anchor, parser.targets)

    def test_opensuse_badge(self):
        expected = profile.opensuse_badge()
        self.assertEqual(expected.size, (750, 112))
        self.assertEqual(expected.tobytes(), profile.opensuse_badge().tobytes())
        self.assertIn((171, 133, 239), {color for count, color in expected.getcolors()})
        for region in ((17, 18, 167, 89), (188, 29, 426, 97), (462, 17, 738, 95)):
            with self.subTest(region=region):
                self.assertGreater(len(expected.crop(region).getcolors()), 3)
        with Image.open(profile.ASSETS / "opensuse/opensuse-pixel.png") as image:
            self.assertEqual(image.size, (1500, 224))
            self.assertEqual(image.n_frames, 1)
            self.assertEqual(image.convert("RGB").tobytes(),
                             expected.resize((1500, 224), Image.Resampling.NEAREST).tobytes())
        readme = (profile.ROOT / "README.md").read_text()
        parser = ReadmeImages()
        parser.feed(readme)
        badge = next(attrs for attrs in parser.images
                     if attrs["src"] == "assets/opensuse/opensuse-pixel.png")
        self.assertEqual(badge["width"], "100%")
        self.assertNotIn("height", badge)
        self.assertIn('href="https://www.opensuse.org"', readme)
        self.assertLess(readme.index(badge["src"]), readme.index("assets/banners/bunker-footer.png"))
        self.assertEqual(parser.images[-1]["src"], "assets/banners/bunker-footer.png")

    def test_heritage_stills(self):
        for source, destination in (
            ("animations/ILoveYouHeartGIFbyCarawrrr.gif", "icons/finger-heart.png"),
            ("animations/KoreanKickingGIFbyTomtomi.gif", "animations/korean-character-still.png"),
        ):
            with self.subTest(source=source):
                with Image.open(profile.ASSETS / source) as original:
                    with Image.open(profile.ASSETS / destination) as still:
                        self.assertEqual(still.n_frames, 1)
                        self.assertEqual(still.size, original.size)
                        self.assertEqual(still.convert("RGBA").tobytes(), original.convert("RGBA").tobytes())

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

    def test_cofc_montage(self):
        expected = build_cofc.montage()
        self.assertEqual(expected.size, (750, 250))
        self.assertEqual(expected.tobytes(), build_cofc.montage().tobytes())
        path = profile.ASSETS / "cofc/cofc-montage.png"
        with Image.open(path) as image:
            self.assertEqual(image.size, (3000, 1000))
            self.assertEqual(image.mode, "RGB")
            self.assertEqual(image.n_frames, 1)
            self.assertEqual(image.tobytes(),
                             expected.resize(image.size, Image.Resampling.NEAREST).tobytes())
        self.assertLess(path.stat().st_size, 1024 * 1024)
        colors = expected.getcolors(expected.width * expected.height)
        gold = sum(count for count, (r, g, b) in colors
                   if r > 100 and r > g > b and g > b * 1.2)
        self.assertGreater(gold, 0)
        self.assertLess(gold / (expected.width * expected.height), 0.05)
        for region in ((0, 44, 175, 235), (175, 44, 395, 235), (395, 44, 750, 235)):
            with self.subTest(region=region):
                self.assertGreater(len(expected.crop(region).getcolors(750 * 250)), 20)

    def test_cofc_placement(self):
        readme = (profile.ROOT / "README.md").read_text()
        parser = ReadmeImages()
        parser.feed(readme)
        image = next(attrs for attrs in parser.images
                     if attrs["src"] == "assets/cofc/cofc-montage.png")
        self.assertEqual(image["width"], "100%")
        self.assertNotIn("height", image)
        for description in ("Jason", "Charleston", "courtyard", "workstation"):
            self.assertIn(description, image["alt"])
        anchors = ("operator-log", "college-of-charleston", "project-bays",
                   "toolchain", "open-channel")
        positions = [readme.index(f'id="{anchor}"') for anchor in anchors]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(positions[1], readme.index(image["src"]))
        self.assertLess(readme.index(image["src"]), positions[2])
        self.assertIn("College of Charleston · Software Engineering / Computer Science · "
                      "Charleston, South Carolina", readme)

    def test_invisible_section_anchors(self):
        readme = (profile.ROOT / "README.md").read_text()
        rendered = markdown.markdown(readme, extensions=["fenced_code"])
        parser = ReadmeImages()
        parser.feed(rendered)
        self.assertEqual(parser.headings, ["h1"])
        self.assertEqual(parser.target_elements, [
            ("a", {"id": "operator-log"}),
            ("p", {"id": "college-of-charleston", "align": "center"}),
            ("p", {"id": "project-bays", "align": "center"}),
            ("p", {"id": "toolchain", "align": "center"}),
            ("a", {"id": "open-channel"}),
        ])
        self.assertNotRegex(rendered, r'<p>\s*<a id="[^"]+"></a>\s*</p>')
        self.assertNotRegex(readme, r"0[1-5] / (Operator Log|College of Charleston|"
                           r"Project Bays|Toolchain|Open Channel)")
        self.assertFalse(any(attrs["src"].startswith("assets/icons/") for attrs in parser.images))
        for anchor in parser.anchors:
            self.assertIn(anchor, parser.targets)

    def test_cofc_environment_replaces_title(self):
        with patch("build_cofc.text", wraps=build_cofc.text) as labels:
            image = build_cofc.montage()
        for call in labels.call_args_list:
            self.assertNotIn("COLLEGE OF CHARLESTON", call.args[2].upper())
        self.assertGreater(len(image.crop((20, 23, 260, 43)).getcolors(4800)), 8)


if __name__ == "__main__":
    unittest.main()
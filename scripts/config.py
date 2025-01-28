from os import path

ROOT = path.abspath(path.join(path.dirname(__file__), "../"))


def root_path(*paths: str) -> str:
    return path.abspath(path.join(ROOT, *paths))


FONT_SOURCE_PATH = root_path("fonts-to-subset")
GLYPHS_PATH = root_path("glyph-sets")
WESTERN_GLYPHS_PATH = path.join(GLYPHS_PATH, "western.txt")
TYPEFACES_PATH = root_path("typefaces")
OUTPUT_PATH = root_path("dist")
GLYPHS_OUTPUT_PATH = path.join(OUTPUT_PATH, "glyphs.json")

OUTPUT_FONT_FORMAT = "woff2"
OUTPUT_FONT_POSTFIX = "-western"

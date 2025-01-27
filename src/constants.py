from os import path

dirname = path.dirname(__file__)

GLYPHS_PATH = path.abspath(path.join(dirname, "./glyphs.txt"))
OUTPUT_PATH = path.abspath(path.join(dirname, "../dist"))
OUTPUT_FONT_FORMAT = "woff2"
OUTPUT_FONT_POSTFIX = "-western"
SOURCE_FONT_PATH = path.abspath(path.join(dirname, "./fonts"))
FONT_CATELOG_PATH = path.abspath(path.join(dirname, "../font-catelog"))

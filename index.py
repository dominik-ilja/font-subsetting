import json
import os

from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

GLYPHS_PATH = "src/glyphs.txt"
FONT_FORMAT = "woff2"
FONT_PATHS = [
    {
        "source": "src/Inter-Regular.otf",
        "output": f"dist/inter-western-regular.{FONT_FORMAT}"
    },
    {
        "source": "src/Inter-Medium.otf",
        "output": f"dist/inter-western-medium.{FONT_FORMAT}"
    },
    {
        "source": "src/Inter-Bold.otf",
        "output": f"dist/inter-western-bold.{FONT_FORMAT}"
    }
]


def buildFont(source, output, unicodes):
    print(f"Building: {source}")
    font = TTFont(source)
    subsetter = Subsetter()
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    font.flavor = FONT_FORMAT
    font.save(output)

    prevSize = os.path.getsize(source)
    currSize = os.path.getsize(output)

    print(f"Outputting: {output}")
    print(
        f"Previous size: {prevSize}, Current size: {currSize}, Difference of {prevSize - currSize} bytes")


def getUnicodes():
    glyphFile = open(GLYPHS_PATH, encoding="utf-8")
    glyphs = glyphFile.read()
    unicodes = {}

    for char in glyphs:
        if (char not in unicodes):
            unicodes[char] = ord(char)

    jsonOuput = open("dist/glyphs.json", "w")
    jsonOuput.write(json.dumps(unicodes))

    return list(unicodes.values())


def main():
    unicodes = getUnicodes()

    for path in FONT_PATHS:
        buildFont(path["source"], path["output"], unicodes)

    print("Done")


main()

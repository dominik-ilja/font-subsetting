import json
import os
from typing import List, Tuple

from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

from constants import GLYPHS_PATH, OUTPUT_FONT_FORMAT, OUTPUT_FONT_POSTFIX, OUTPUT_PATH, SOURCE_FONT_PATH


def getBasenameAndExt(path) -> Tuple[str, str]:
    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    return (name, ext)


def getOutputPaths() -> List[str]:
    paths = []

    for file in os.listdir(OUTPUT_PATH):
        path = os.path.join(OUTPUT_PATH, file)

        if os.path.isfile(path) and path.endswith(OUTPUT_FONT_FORMAT):
            paths.append(path)

    return paths


def getSourcePaths():
    paths = []

    for file in os.listdir(SOURCE_FONT_PATH):
        path = os.path.join(SOURCE_FONT_PATH, file)

        if os.path.isfile(path):
            paths.append(path)

    return paths


def buildFontFace(file: str, font_family: str, font_weight: int) -> str:
    file_ext = getBasenameAndExt(file)[1]
    format = ""

    if file_ext == ".otf":
        format = "opentype"
    elif file_ext == ".ttf":
        format = "truetype"
    elif file_ext == ".woff2":
        format = "woff2"
    else:
        raise ValueError(f"The file extension \"{file_ext}\" is not supported")

    font_face = f"""
@font-face {{
  font-family: "{font_family}";
  font-style: normal;
  font-weight: {font_weight};
  src: url("./{file}") format("{format}");
}}

"""

    return font_face.lstrip()


def buildCSS():
    print("Building CSS")
    css_file = open(os.path.join(OUTPUT_PATH, "style.css"), "w")
    file_contents = ""
    output_font_paths = getOutputPaths()
    fonts = []

    # Font names that have been processed will be in the following format:
    # [name]-[weight]-[modifier].[ext] an example would be "inter-bold-western.woff2"
    for path in output_font_paths:
        name, ext = getBasenameAndExt(path)
        parts = name.split("-")

        # If we start supporting "Italic", then we'll need to adjust this
        family = f"{parts[0].capitalize()} {parts[2].capitalize()}"
        weight = parts[1]

        if weight == "regular":
            weight = 400
        elif weight == "medium":
            weight = 500
        elif weight == "bold":
            weight = 700
        else:
            raise ValueError(
                f"Invalid font weight \"{weight}\"")

        fonts.append({"file": name + ext, "family": family, "weight": weight})

    sorted_fonts = sorted(fonts, key=lambda x: (x["family"], x["weight"]))

    for font in sorted_fonts:
        font_face = buildFontFace(font["file"], font["family"], font["weight"])
        file_contents += font_face

    css_file.write(file_contents)


def buildFont(source_path, unicodes):
    print(f"Building: {source_path}")
    font = TTFont(source_path)
    subsetter = Subsetter()
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    file_path = os.path.splitext(source_path)[0]
    output_file = f"{os.path.basename(file_path)}{OUTPUT_FONT_POSTFIX}.{OUTPUT_FONT_FORMAT}"
    output_path = os.path.join(OUTPUT_PATH, output_file)

    font.flavor = OUTPUT_FONT_FORMAT
    font.save(output_path)

    prevSize = os.path.getsize(source_path)
    currSize = os.path.getsize(output_path)

    print(f"Outputting: {output_path}")
    print(
        f"Previous size: {prevSize}, Current size: {currSize}, Difference of {prevSize - currSize} bytes")


def getUnicodes():
    glyphFile = open(GLYPHS_PATH, encoding="utf-8")
    glyphs = glyphFile.read()
    unicodes = {}

    for char in glyphs:
        if (char not in unicodes):
            unicodes[char] = ord(char)

    jsonOuput = open(f"{OUTPUT_PATH}/glyphs.json", "w")
    jsonOuput.write(json.dumps(unicodes, indent=2))

    return list(unicodes.values())


def main():
    unicodes = getUnicodes()

    for path in getSourcePaths():
        buildFont(path, unicodes)

    buildCSS()
    print("Done")


main()

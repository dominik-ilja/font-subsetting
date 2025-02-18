import json
import os
import shutil
from typing import List, Tuple

from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

from config import (
    FONT_SOURCE_PATH,
    GLYPHS_OUTPUT_PATH,
    GLYPHS_PATH,
    OUTPUT_FONT_FORMAT,
    OUTPUT_FONT_POSTFIX,
    OUTPUT_PATH,
    WESTERN_GLYPHS_PATH,
    TEST_GLYPHS_PATH,
    STATS_PATH
)


class FontSubsetter:
    def __init__(self, output_dir, unicode_path, font_source_dir):
        self._output_dir = output_dir
        self._unicode_path = unicode_path
        self._font_source_dir = font_source_dir
        self._unicode_output = os.path.join(output_dir, "unicodes.json")

    def run(self):
        unicodes = self._get_unicode_characters()
        font_paths = self._get_source_paths()
        stats = []

        for path in font_paths:
            stat = self._build_font(path, unicodes)
            stats.append(stat)

        stat_output = open(os.path.join(self._output_dir, "stats.json"), "w")
        stat_output.write(json.dumps(stats, indent=2))

    def _build_font(self, source_path, unicodes):
        print(f"Building: {source_path}")

        font = TTFont(source_path)
        data = {
            "file": None,
            "previous": None,
            "current": None,
            "difference": None
        }

        prev_cmap = font.getBestCmap()
        prev_chars = len(prev_cmap) if prev_cmap else 0
        prev_glyphs = len(font.getGlyphOrder())
        prev_size = os.path.getsize(source_path)
        data["previous"] = self._create_font_stat(
            prev_chars, prev_glyphs, prev_size)

        subsetter = Subsetter()
        subsetter.populate(unicodes=unicodes)
        subsetter.subset(font)

        file_path = os.path.splitext(source_path)[0]
        output_file = f"{os.path.basename(file_path)}{OUTPUT_FONT_POSTFIX}.{OUTPUT_FONT_FORMAT}"
        output_path = os.path.join(OUTPUT_PATH, output_file)

        font.flavor = OUTPUT_FONT_FORMAT
        font.save(output_path)

        curr_cmap = font.getBestCmap()
        curr_chars = len(curr_cmap) if curr_cmap else 0
        curr_glyphs = len(font.getGlyphOrder())
        curr_size = os.path.getsize(output_path)
        data["current"] = self._create_font_stat(
            curr_chars, curr_glyphs, curr_size)

        diff_chars = prev_chars - curr_chars
        diff_glyphs = prev_glyphs - curr_glyphs
        diff_size = prev_size - curr_size
        data["difference"] = self._create_font_stat(diff_chars, diff_glyphs, diff_size) | {
            "character_count_reduction": f"{self._calculate_precentage_diff(prev_chars, curr_chars)}%",
            "file_size_reduction": f"{self._calculate_precentage_diff(prev_size, curr_size)}%",
            "glyph_reduction": f"{self._calculate_precentage_diff(prev_glyphs, curr_glyphs)}%",
        }

        data["file"] = os.path.basename(file_path)

        print(f"Outputting: {output_path}")
        print(
            f"Previous size: {prev_size}, Current size: {curr_size}, Difference of {diff_size} bytes")

        return data

    def _calculate_precentage_diff(self, prev, curr):
        return 100 - round(curr / prev * 100, 2)

    def _create_font_stat(self, character_count, glyph_count, file_size):

        return {
            "character_count": character_count,
            "glyph_count": glyph_count,
            "file_size": file_size,
            "file_size_formatted": f"{self._size_in_kilobytes(file_size)} KB",
        }

    def _get_source_paths(self):
        paths = []

        for file in os.listdir(self._font_source_dir):
            path = os.path.join(self._font_source_dir, file)

            if os.path.isfile(path):
                paths.append(path)

        return paths

    def _get_unicode_characters(self):
        with open(self._unicode_path, encoding="utf-8") as file:
            characters = file.read()
            characters = "".join(sorted(list(characters)))
            codes = {}

            for char in characters:
                code = ord(char)
                if char not in codes and not self._is_command_character(code):
                    codes[char] = ord(char)

            data = {
                "total": len(codes),
                "codes": codes
            }

            with open(self._unicode_output, "w") as output:
                output.write(json.dumps(data, indent=2))

            return list(codes.values())

    def _is_command_character(self, code):
        return code < 31 or code == 127 or (code >= 128 and code <= 159)

    def _size_in_kilobytes(self, size):
        bytes_in_kilobytes = 1024
        return round(size / bytes_in_kilobytes, 2)


class CSSFileWriter:
    def __init__(self, dir, font_format):
        self._dir = dir
        self._file = os.path.join(self._dir, "style.css")
        self._font_format = font_format
        self._file_exts = {
            ".otf": "opentype",
            ".ttf": "truetype",
            # ".woff": "woff",
            ".woff2": "woff2"
        }
        self._style_order = {"normal": 0, "italic": 1}
        self._styles = {
            "normal": "normal",
            "italic": "italic",
        }
        self._weights = {
            "thin": 100,
            "extralight": 200,
            "light": 300,
            "regular": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700,
            "extrabold": 800,
            "black": 900,
        }

    def run(self):
        print("Building CSS")

        with open(self._file, "w") as file:
            file_contents = ""
            output_font_paths = self._get_output_paths()
            font_metadata = []

            # Font names that have been processed will be in the following format:
            # [name]-[weight]-[modifier].[ext] an example would be "inter-bold-western.woff2"
            for path in output_font_paths:
                name = self._get_basename_and_ext(path)[0]
                metadata = self._get_font_metadata(name)
                font_metadata.append(metadata)

            sorted_fonts = sorted(font_metadata, key=lambda x: (
                x["family"], x["weight"], self._style_order[x["style"]]))

            for font in sorted_fonts:
                font_face = self._build_font_face(
                    font["file"],
                    font["family"],
                    font["weight"],
                    font["style"]
                )
                file_contents += font_face

            file.write(file_contents)

    def _build_font_face(self, file: str, font_family: str, font_weight: int, font_style: str) -> str:
        file_ext = self._get_basename_and_ext(file)[1]
        format = ""

        if file_ext in self._file_exts:
            format = self._file_exts[file_ext]
        else:
            raise ValueError(
                f"The file extension \"{file_ext}\" is not supported")

        font_face = f"""
@font-face {{
  font-family: "{font_family}";
  font-style: {font_style};
  font-weight: {font_weight};
  src: url("./{file}") format("{format}");
}}

"""

        return font_face.lstrip()

    def _get_basename_and_ext(self, path) -> Tuple[str, str]:
        base = os.path.basename(path)
        name, ext = os.path.splitext(base)
        return (name, ext)

    def _get_font_metadata(self, name: str):
        # expected format is "inter-bold-western"
        name_parts = []
        parts = name.split("-")
        style = self._styles["normal"]
        style_parts = []
        weight = self._weights["regular"]
        weight_parts = []

        for part in parts:
            if part in self._weights:
                weight = self._weights[part]
                weight_parts.append(part)
            elif part in self._styles:
                style = self._styles[part]
                style_parts.append(part)
            else:
                name_parts.append(part.capitalize())

        file = "-".join(
            [*name_parts, *weight_parts, *style_parts]
        ).lower() + "." + self._font_format

        return {
            "file": file,
            "family": " ".join(name_parts),
            "weight": weight,
            "style": style
        }

    def _get_output_paths(self) -> List[str]:
        paths = []

        for file in os.listdir(self._dir):
            path = os.path.join(self._dir, file)

            if os.path.isfile(path) and path.endswith(self._font_format):
                paths.append(path)

        return paths


def main():
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)

    os.makedirs(OUTPUT_PATH)

    FontSubsetter(OUTPUT_PATH, os.path.join(
        GLYPHS_PATH, "western.txt"), FONT_SOURCE_PATH).run()
    CSSFileWriter(OUTPUT_PATH, OUTPUT_FONT_FORMAT).run()
    print("Done")


main()

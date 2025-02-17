from config import TYPEFACES_PATH
import os
from typing import List


def get_fonts() -> List[str]:
    entries = []

    def traverse(path: str):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                entries.append(full_path)
            elif os.path.isdir(full_path):
                traverse(full_path)

    traverse(TYPEFACES_PATH)

    return entries


def main():
    fonts = get_fonts()

    for font in fonts:
        dirname = os.path.dirname(font)
        base = os.path.basename(font).lower()
        name, ext = base.split(".")
        parts = name.split("-")
        format = parts.pop()
        search = "italic"

        # we need to separate the weight and style and append the pieces back to parts
        if format != search and search in format:
            index = format.find(search)
            font_weight = format[:index]
            font_style = format[index:]

            parts.append(font_weight)
            parts.append(font_style)
        else:
            parts.append(format)

        normalized_name = '-'.join(parts) + "." + ext
        normalized_path = os.path.join(dirname, normalized_name)
        os.rename(font, normalized_path)


main()

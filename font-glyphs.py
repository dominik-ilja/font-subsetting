from fontTools.ttLib import TTFont

FONT_PATHS = [
    "src/Inter-Regular.otf",
    "dist/inter-western-regular.woff2",
    "src/Roboto-Regular.ttf",
    "dist/roboto-western-regular.woff2",
]

for path in FONT_PATHS:
    font = TTFont(path)
    print(f"\"{path}\" contains {len(font.getGlyphSet())} glyphs")

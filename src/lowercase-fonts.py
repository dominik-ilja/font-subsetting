from constants import FONT_CATELOG_PATH

import os

files = []

# for file in os.listdir(FONT_CATELOG_PATH):
#     text = file.replace("...", "")
#     index = len(text) - 3  # 3 characters from the end
#     new_path = os.path.join(
#         FONT_CATELOG_PATH, text[:index] + '.' + text[index:])
#     os.rename(os.path.join(FONT_CATELOG_PATH, file), new_path)


for file in os.listdir(FONT_CATELOG_PATH):
    path = os.path.join(FONT_CATELOG_PATH, file)

    if os.path.isfile(path):
        lowered_path = os.path.join(FONT_CATELOG_PATH, path.lower())
        name, ext = lowered_path.split(".")
        parts = name.split("-")
        weightAndStyle = parts.pop()

        # We want to separate the font weight from the font style
        if "italic" in weightAndStyle:
            index = weightAndStyle.find("italic")
            parts.append(weightAndStyle[:index])
            parts.append(weightAndStyle[index:])
        else:
            parts.append(weightAndStyle)

        os.rename(path, "-".join(parts) + "." + ext)
        files.append(lowered_path)

for file in files:
    paths = os.path.splitext(file)
    print(os.path.basename(paths[0]))

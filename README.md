# Font Subsetting

This project is for me to automate the process of subsetting fonts. Font subsetting is the process of only using a portion of the total characters provided by a font. This allows you to ship only what you plan on using.

When self hosting fonts, I've been left confused why my files were hitting 1mb+ in size. After so investigation, I found that using one font weight in Inter was hitting around 250kb. This left me hitting around 750kb to use regular, medium, and bold.

When working with fonts like Inter or Roboto there are a lot of additional characters you'll never end using. To give you some numbers, Inter contains 2,548 glyphs while Roboto contains 1,321. This is obviously to support languages around the world which is great. However, for my writings, I know I will only be using english. This means thousands of characters are irrelevant to me.

For Inter, it removed around 250kb per font. For Roboto it removed around 130kb per font.

## How it works

All the characters I plan on using are contained within `src/glyphs.txt`. This allows me to easily copy and paste characters from [Font Squirrel](https://www.fontsquirrel.com/tools/webfont-generator) for ease of getting what I need.

In the `index.py` script, we'll grab the characters from `src/glyphs.txt` and build a list of unique unicodes. The font is then built using the unicodes to select the characters we want. We also make the output font a `woff2` for smaller file sizes.

## Installation

Setup virtual environment:

```sh
python3 -m venv .env
```

Activate virtual environment:

```sh
# Unix
source .env/bin/activate

# Windows
.env\Scripts\activate

# Git bash
source .env\Scripts\activate
```

Install the required packages:

```py
pip install -r requirements.txt
```

## Todo

- [x] Automate generating the CSS for the fonts
- [x] Move src fonts to a single directory, so we only need to specify the path to the folder
- [x] See if we can come up with a way to automate the renaming. I'm thinking we could aimply append `-western` to the original name

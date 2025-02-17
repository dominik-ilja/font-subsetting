# subset-font.py

We always want to have a clean directory, so before every run we remove the "dist" directory completely, then rebuild it.

We retrieve all of the glyphs that are to be included in the font (this is probably better to be referred to as characters. The reason for this is that a character can have multiple glyphs within a font). We just have a file that contains the characters we wish to include.

> Important
> The file containing the characters must be using utf-8 enconding to prevent errors

Characters within the file are sorted then deduplicated. We write the characters to a JSON file for analysis purposes.
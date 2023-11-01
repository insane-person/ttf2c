
# TTF2C

~~~
usage: ttf2c [-h] --font FONT --size SIZE [--output OUTPUT] [--range RANGE] [--img IMG] [--mono] [--inv]
             [--bp {vertical,horizontal}] [--am {vertical,horizontal}] [--rx] [--ry] [--bn {little,big}]
~~~

Yet another ttf2c parser. Program is designed to convert TrueType .ttf fonts to a format applicable in embedded devices .c files. This program differs from all other programs by its ability to save font characters with a large set of parameters such as mirroring, inversion, bit numbering etc.


An important note: the upper left corner of glyph is taken as the XY basis (0, 0).

Examples:
~~~
python.exe ttf2c.py -f MyFavoriteFont.ttf -s 33
python.exe ttf2c.py -f MyFavoriteFont.ttf -s 19 --img './FontImages' --range 48-57, 59 --mono
~~~


              
## Options:
~~~
  -h, --help            show this help message and exit
  --font FONT, -f FONT  Path to the .ttf file.
  --size SIZE, -s SIZE  Bitmap font height in px. Important: The size is specified for the whole chosen font, not for an
                        individual glyph. The font is scaled based on the size of the largest glyph. Therefore, chosen
                        characters glyphs could be smaller or larger than specified by this parameter. And the same glyph
                        can have different alignment bits in different sets.
  --output OUTPUT, -o OUTPUT
                        Path to dir where C file will be saved. By default save in working directory
  --range RANGE, -r RANGE
                        Range of glyphs codes for conversion. Example: 0x30-0x39,0x2D or 48-57,45. By the default will be
                        generated all glyphs of font. Not printable glyphs will be excluded from generation.
  --img IMG, -i IMG     Path to the folder where the images of individual glyphs and the full set glyphs on one image will
                        be saved. With this parameter generates several type of images: separate glyphs images, glyph set
                        in one line, glyph set map. The map is formed in an unordered way and is used for debugging and
                        general viewing of the font.
  --mono, -m            Aligns glyphs to the width of the widest glyph. In some circumstances this saves memory and the
                        table of character widths is not generated.
  --inv                 This option inverts the colors of the glyphs to opposite.
                        vertical mode. The first column goes first, then the second, then the third.
  --rx                  Mirrors (reverse) the glyph on the X-axis. This option is used if you want to change the zero
                        coordinate of a glyph.
  --ry                  Mirrors (reverse) the glyph on the Y-axis. This option is used if you want to change the zero
                        coordinate of a glyph.
  --bn {little,big}     Bit numbering or bit order or MSB, LSB. Default value 'little'. As an example, a glyph '!' of size
                        8x1 bits can be represented as a set of 8 bytes in LSB as 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                        0x00, 0x01 or as 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80 im MSB order
~~~

## License
GPLv3. Copyright (C) 2023  Vasilii Tsarevskii

### Used libraries:
|Name            |License|
|----------------|----------------------------------------------------|
| Pillow         | Historical Permission Notice and Disclaimer (HPND) |
| freetype-py    |BSD License |
|numpy           |BSD License |
|rectangle-packer|MIT License|

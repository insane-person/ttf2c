#
# Copyright (c) 2023 by Vasilii Tsarevkii
#
# See the README and LISENSE files for information on usage and redistribution.
#

import argparse
import os
import re


def font_path_checker(font_path):
    path = str(font_path)
    abs_path = os.path.abspath(path)
    if os.path.splitext(abs_path)[-1].lower() != '.ttf':
        raise argparse.ArgumentTypeError(f'Unsupported font type: {path}')
    if not os.path.isfile(abs_path):
        raise argparse.ArgumentTypeError(f'Font file not found: {path}')
    return abs_path


def size_checker(size):
    err_str = f'Invalid size value: {size}'
    try:
        num = int(size)
    except:
        raise argparse.ArgumentTypeError(err_str)
    if num < 0:
        raise argparse.ArgumentTypeError(err_str)
    return num


def output_checker(path):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    return abs_path


def range_checker(glyph_range):
    if glyph_range is not None:
        err_list = re.findall(r"[^0-9a-fxA-F,-]+", glyph_range)
        if len(err_list) != 0:
            raise ValueError

        glyph_range = glyph_range.rstrip('-')
        glyph_range = glyph_range.rstrip(',')
        glyph_range = glyph_range.lstrip('-')
        glyph_range = glyph_range.lstrip(',')

        glyph_range_list = glyph_range.split(",")
        glyph_list = []
        for r in glyph_range_list:
            def str_to_int(value):
                if value.startswith('0x'):
                    return int(value, 16)
                return int(value)

            if '-' in r:
                rl = r.split("-")
                if len(rl) == 2:
                    x1 = str_to_int(rl[0])
                    x2 = str_to_int(rl[1])
                    if x1 > x2:
                        raise ValueError
                    glyph_list += [x for x in range(x1, x2 + 1)]
                else:
                    raise ValueError
            else:
                glyph_list.append(str_to_int(r))

        char_set = list(set(glyph_list))
        char_set.sort()
        return char_set
    else:
        return None


def img_path_checker(path):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    return abs_path


prog_description = """Yet another ttf2c parser. Program is designed to convert .ttf fonts to a format applicable in 
embedded devices. This program differs from all other programs by its ability to save font characters with a large set 
of parameters such as mirroring, inversion, bit numbering etc.
An important note: the upper left corner of glyph is taken as the XY basis (0, 0).

Examples:
python.exe ttf2c.py -f MyFavoriteFont.ttf -s 33
python.exe ttf2c.py -f MyFavoriteFont.ttf -s 19 --img './FontImages' --range 48-57, 59 --mono

Used libraries:
Name              License
Pillow            Historical Permission Notice and Disclaimer (HPND)
freetype-py       BSD License
numpy             BSD License
rectangle-packer  MIT License"""

size_description = """Bitmap font height in px. 
Important: The size is specified for the whole chosen font, not for an individual glyph. 
The font is scaled based on the size of the largest glyph. Therefore, chosen characters glyphs could be smaller or 
larger than specified by this parameter. And the same glyph can have different alignment bits in different sets."""

output_description = """Path to dir where C file will be saved. By default save in working directory"""

range_description = """Range of glyphs codes for conversion. Example: 0x30-0x39,0x2D or 48-57,45. By the default will be
 generated all glyphs of font. Not printable glyphs will be excluded from generation."""

img_description = """Path to the folder where the images of individual glyphs and the full set glyphs on one image will 
be saved. With this parameter generates several type of images: separate glyphs images, glyph set in one line, glyph set
 map. The map is formed in an unordered way and is used for debugging and general viewing of the font."""

mono_description = """Aligns glyphs to the width of the  widest glyph. In some circumstances this saves memory and the 
table of character widths is not generated."""

inv_description = """This option inverts the colors of the glyphs to opposite."""

bp_description = """Bit pack mode. Default value 'vertical'. Each glyph is a two-dimensional array of bits. 
When packing the array of bits into bytes, vertical or horizontal option can be used. As an example, a glyph '!' of size
 8x1 bits can be represented vertically as the value 0x5f or as a set of 8 bytes horizontally as 
0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01."""

am_description = """Default value 'horizontal'. There are 2 different memory addressing mode 
horizontal or vertical addressing mode. This parameter describes how bytes will be packed into the array. In case of 
horizontal mode, bytes from the first row will be packed first, then bytes from the second row, etc. The same is for 
vertical mode. The first column goes first, then the second, then the third."""

rx_description = """Mirrors (reverse) the glyph on the X-axis. This option is used if you want to change the zero 
coordinate of a glyph"""

ry_description = """Mirrors (reverse) the glyph on the Y-axis. This option is used if you want to change the zero 
coordinate of a glyph"""

bn_description = """Bit numbering or bit order or MSB, LSB. Default value 'little'. As an example, a glyph '!' of size
8x1 bits can be represented as a set of 8 bytes in LSB as 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01 or
as 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80 im MSB order"""

epilog = """
Copyright (C) 2023 under GPLv3 by Vasilii Tsarevskii
This program comes with ABSOLUTELY NO WARRANTY.
"""

parser = argparse.ArgumentParser(prog='ttf2c',
                                 description=prog_description,
                                 epilog=epilog,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--font', '-f', type=font_path_checker, required=True, help='Path to the .ttf file.')
parser.add_argument('--size', '-s', type=size_checker, required=True, help=size_description)
parser.add_argument('--output', '-o', type=output_checker, default='.', help=output_description)
parser.add_argument('--range', '-r', type=range_checker, default=None, help=range_description)
parser.add_argument('--img', '-i', type=img_path_checker, help=img_description)
parser.add_argument('--mono', '-m', action='store_true', help=mono_description)
parser.add_argument('--inv', action='store_true', help=inv_description)
parser.add_argument('--bp', choices=['vertical', 'horizontal'], default='vertical', help=bp_description)
parser.add_argument('--am', choices=['vertical', 'horizontal'], default='horizontal', help=am_description)
parser.add_argument('--rx', action='store_true', help=rx_description)
parser.add_argument('--ry', action='store_true', help=ry_description)
parser.add_argument('--bn', choices=['little', 'big'], default='little', help=bn_description)

args = parser.parse_args()


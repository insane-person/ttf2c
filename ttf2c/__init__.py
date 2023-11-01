#
# Copyright (c) 2023 by Vasilii Tsarevkii
#
# See the README and LISENSE files for information on usage and redistribution.
#

import os
from .args import args
from .ttf2np import GlyphSet
from .np2c import generate_c_file
from .glyph_img import draw_glyphs


def ttf2c():
    glyph_set = GlyphSet(font=args.font, size=args.size, char_set=args.range, mono=args.mono)

    # Bit conversions over each glyph
    # Inverse (mirror) array in X direction
    if args.rx:
        glyph_set.flip(1)

    # Inverse (mirror) array in Y direction
    if args.ry:
        glyph_set.flip(0)

    # Inverse bits (color)
    if args.inv:
        glyph_set.inverse()

    # Pack bits to bytes
    axis = 0
    if args.bp == 'horizontal':
        axis = 1
    bitmap_packed = glyph_set.pack(axis, args.bn)

    # Create images
    if args.img:
        draw_glyphs(glyph_set.bitmaps, args.img, inverse=args.inv)

    base = os.path.basename(args.font)
    font_name = os.path.splitext(base)[0]

    # Create C file
    generate_c_file(font_name,
                    args.output,
                    args.mono,
                    glyph_set.char_set,
                    bitmap_packed,
                    glyph_set.bitmaps,
                    glyph_set.baseline,
                    glyph_set.max_height,
                    glyph_set.max_width,
                    glyph_set.kerning_px,
                    glyph_set.space_width_px)
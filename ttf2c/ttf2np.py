#
# Copyright (c) 2023 by Vasilii Tsarevkii
#
# See the README and LISENSE files for information on usage and redistribution.
#

from freetype import Face, FT_LOAD_RENDER, FT_LOAD_MONOCHROME, FT_LOAD_TARGET_MONO, FT_GLYPH_BBOX_SUBPIXELS
import numpy


class GlyphSet:
    def __init__(self, font: str, size: int, char_set: list = None, mono: bool = False):
        self.font = font
        self.size = size
        self.char_set = char_set
        self.mono = mono
        self.max_height = 0
        self.max_width = 0
        self.baseline = 0
        self.glyph_set = []
        self.bitmaps = []

        face = Face(self.font)

        if self.char_set is None:
            self.char_set = self.__ttf_get_charset()

        face.set_pixel_sizes(0, self.size)
        slot = face.glyph

        # Get space width
        face.load_char(32, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
        self.space_width_px = slot.advance.x // 64

        # First two passes to compute bbox
        kerning = []

        for c in self.char_set:
            face.load_char(c, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
            if slot.metrics.width == 0 or slot.metrics.height == 0:
                self.char_set.remove(c)
                continue
            bitmap = slot.bitmap

            kerning.append(slot.advance.x // 64 - bitmap.width + slot.metrics.horiBearingX // 64)

            self.max_width = max(self.max_width, bitmap.width)
            self.baseline = max(self.baseline, max(0, bitmap.rows - slot.bitmap_top))

        # Take the average indentation value for each glyph
        import statistics
        self.kerning_px = int(statistics.median(kerning))

        for c in self.char_set:
            face.load_char(c, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
            self.max_height = max(self.max_height, self.baseline + slot.bitmap_top)

        # Render glyphs
        for c in self.char_set:
            face.load_char(c, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)

            width = slot.bitmap.width
            if self.mono:
                width = self.max_width

            bitmap = slot.bitmap
            glyph = numpy.full(shape=(self.max_height, width), fill_value=False, dtype=bool)

            z2 = numpy.array(bitmap.buffer, dtype=numpy.uint8)
            z3 = numpy.reshape(z2, (slot.bitmap.rows, slot.bitmap.pitch))
            z4 = numpy.unpackbits(z3, axis=1, count=slot.bitmap.width)

            if self.mono:
                ws = (self.max_width - slot.bitmap.width) // 2
            else:
                ws = 0

            w = bitmap.width
            top = slot.bitmap_top
            h = bitmap.rows
            y = self.max_height - self.baseline - top
            glyph[y:y+h, ws:ws+w] = z4

            self.bitmaps.append(numpy.copy(glyph))

    def __ttf_get_charset(self):
        face = Face(self.font)
        char_set = []
        for c, i in face.get_chars():
            char_set.append(c)
        return char_set

    def flip(self, axis):
        for i, glyph in enumerate(self.bitmaps):
            self.bitmaps[i] = numpy.flip(self.bitmaps[i], axis=axis)

    def inverse(self):
        for i, glyph in enumerate(self.bitmaps):
            self.bitmaps[i] = numpy.invert(self.bitmaps[i])

    def pack(self, axis, bit_order):
        glyph_pack_list = []
        for i, glyph in enumerate(self.bitmaps):
            # Pack bits to bytes
            packed_glyph = numpy.packbits(self.bitmaps[i], axis=axis, bitorder=bit_order)
            glyph_pack_list.append(packed_glyph)
        return glyph_pack_list

# menuTitle: copy glyph order from Roman default to Italic default

import os, glob

familyName    = 'AmstelvarA2'
srcSubFamily  = 'Roman'
dstSubFamily  = 'Italic'
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
srcFontPath   = os.path.join(baseFolder, 'Sources', srcSubFamily, f'{familyName}-{srcSubFamily}_{defaultName}.ufo')
dstFontPath   = os.path.join(baseFolder, 'Sources', dstSubFamily, f'{familyName}-{dstSubFamily}_{defaultName}.ufo')

srcFont = OpenFont(srcFontPath, showInterface=False)
dstFont = OpenFont(dstFontPath, showInterface=False)

print('glyphs in Roman but not in Italic:')
print(list(set(srcFont.templateGlyphOrder).difference(set(dstFont.templateGlyphOrder))))
print()

print('glyphs in Italic but not in Roman:')
print(list(set(dstFont.templateGlyphOrder).difference(set(srcFont.templateGlyphOrder))))
print()

print(f"copying template glyph order from Roman default to Italic default...", end=' ')
dstFont.templateGlyphOrder = srcFont.templateGlyphOrder
dstFont.save()
print('done.\n')


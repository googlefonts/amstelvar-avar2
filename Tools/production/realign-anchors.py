# menuTitle: horizontally align anchors based on the default

import os, math
from xTools4.modules.fontutils import getGlyphs2

# WARNING: the script does not work well with Italic fonts (yet)

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1] 
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultPath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')

anchorNames = [
    'top',
    'GRKtop',
    'center',
    'bottom',
]
tempEditModeKey = 'com.xTools4.tempEdit.mode'

defaultFont = OpenFont(defaultPath, showInterface=False)

f = CurrentFont()
italicAngle = defaultFont.info.italicAngle
italicSlantOffsetX = defaultFont.lib['com.typemytype.robofont.italicSlantOffset']

glyphNames = getGlyphs2(f)

for glyphName in glyphNames:

    glyph = f[glyphName]

    if f.lib.get(tempEditModeKey) == 'glyphs':
        defaultGlyphName = glyphName[:glyphName.rfind('.')]
    else:
        defaultGlyphName = glyphName
        
    defaultGlyph = defaultFont[defaultGlyphName]

    # if italicAngle:
    #     g = defaultGlyph.copy()
    #     g.moveBy((italicSlantOffsetX, 0))
    #     g.skewBy((-italicAngle, 0))
    #     g.round()
    #     defaultGlyph = g
    
    print(f'realigning anchors in {glyphName}...')
    glyph.prepareUndo('realigning anchors')
    for i, a in enumerate(glyph.anchors):
        if a.name not in anchorNames:
            continue
        xPos = defaultGlyph.width / defaultGlyph.anchors[i].x
        xNew = glyph.width / xPos
        print(f'\t{a.name}: {a.x} -> {int(xNew)}')
        a.x = int(xNew)
    glyph.performUndo()
    print()
    
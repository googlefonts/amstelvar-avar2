# menuTitle: build glyphs from glyph constructions in sources

from importlib import reload
import xTools4.modules.accents
reload(xTools4.modules.accents)

import os, glob
from mojo.smartSet import readSmartSets
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from xTools4.modules.accents import buildAccentedGlyphs

def getComponentGlyphNamesFromSmartSets(smartSetNames, smartSetsPath, defaultPath):
    smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)
    f = OpenFont(defaultPath, showInterface=False)
    glyphNames = []
    for smartGroup in smartSets:
        if not smartGroup.groups:
            continue
        for smartSet in smartGroup.groups:
            if smartSet.name in smartSetNames:
                for glyphName in smartSet.glyphNames:
                    if glyphName not in f:
                        continue
                    g = f[glyphName]
                    if len(g.components):
                        glyphNames.append(glyphName)
    return glyphNames


familyName        = 'AmstelvarA2'
subFamilyName     = ['Roman', 'Italic'][0]
baseFolder        = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder     = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultPath       = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
constructionsPath = os.path.join(baseFolder, 'Sources', subFamilyName, f'{familyName}-{subFamilyName}.glyphConstruction')
smartSetsPath     = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.roboFontSets')

# settings

# smartSetNames = [
#     # 'uppercase latin',
#     # 'uppercase greek',
#     # 'uppercase cyrillic',
#     # 'uppercase digraphs',
#     # 'lowercase latin',
#     # 'lowercase greek',
#     # 'lowercase cyrillic',
#     # 'lowercase digraphs',
# ]
# glyphNames = getComponentGlyphNamesFromSmartSets(smartSetNames, smartSetsPath, defaultPath) # [ 'ellipsis' ]

glyphNames = [
    'ohungarumlaut',
    'Ohungarumlaut',
    'Ghestroke',
    'ghestroke',
    'El.bgr',
    'igrave.bgr',
    'increment',
    'periodcentered-loclCAT.case',
] 

dstFonts   = []
preflight  = False
verbose    = True

# batch build glyphs

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

# get constructions
with open(constructionsPath, 'r') as f:
    glyphConstructions = f.read()

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:
        dstFont = OpenFont(ufoPath, showInterface=False)
        print(f'building glyphs in {os.path.split(ufoPath)[-1]}...')
        if not preflight:
            buildAccentedGlyphs(dstFont, glyphNames, glyphConstructions, clear=True, verbose=verbose, autoUnicodes=False, indentLevel=1)
            print(f'\tsaving font...')
            dstFont.save()
        # dstFont.close()
        print()


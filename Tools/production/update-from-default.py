# menuTitle: update default glyphs in all sources

from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import os, glob
from xTools4.modules.validation import assignValidationGroup

# --------
# settings
# --------

familyName     = 'AmstelvarA2'
subFamilyName  = ['Roman', 'Italic'][0]
glyphNames     = ['V']
newDefaultName = 'wght400'
oldDefaultName = 'WDSP0'
preflight      = False

# ---------
# functions
# ---------

def updateGlyphsFromDefault(currentFont, oldDefaultFont, newDefaultFont, glyphNames):
    name = os.path.splitext(os.path.split(currentFont.path)[-1])[0].split('_')[-1]
    fontChanged = False
    for glyphName in glyphNames:
        if glyphName not in oldDefaultFont or glyphName not in currentFont or glyphName not in newDefaultFont:
            continue

        print(familyName, subFamilyName, name)

        oldDefaultGlyph = oldDefaultFont[glyphName]
        currentGlyph    = currentFont[glyphName]
        newDefaultGlyph = newDefaultFont[glyphName]

        validationGroupOldNew = assignValidationGroup(oldDefaultGlyph, newDefaultGlyph)
        if validationGroupOldNew == 'contoursEqual':
            print(familyName, subFamilyName, name)
            print(f'old default /{glyphName} is equal to new default, skipping...')
            continue

        validationGroupOldCurrent = assignValidationGroup(oldDefaultGlyph, currentGlyph)
        if validationGroupOldCurrent == 'contoursEqual':
            # current glyph is equal to old default!
            print(f'\tupdating /{glyphName} from default...')
            font.insertGlyph(newDefaultGlyph, name=glyphName)
            if not fontChanged:
                fontChanged = True

    if fontChanged and not preflight:
        print('\tsaving font...')
        font.save()
        font.close()

    print()

# ---------------------------
# batch update default glyphs
# ---------------------------

baseFolder     = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder  = os.path.join(baseFolder, 'Sources', subFamilyName)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

newDefaultPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{newDefaultName}.ufo')
oldDefaultPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{oldDefaultName}.ufo')

newDefault = OpenFont(newDefaultPath, showInterface=False)
oldDefault = OpenFont(oldDefaultPath, showInterface=False)

ufoPaths.remove(newDefaultPath)
ufoPaths.remove(oldDefaultPath)

for ufoPath in sorted(ufoPaths):
    font = OpenFont(ufoPath, showInterface=False)
    updateGlyphsFromDefault(font, oldDefault, newDefault, glyphNames)

updateGlyphsFromDefault(oldDefault, oldDefault, newDefault, glyphNames)

# menuTitle: copy default glyphs to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
defaultName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultPath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')
assert os.path.exists(defaultPath)

# options

glyphNames = ['zero'] # 'threequartersemdash figuredash'.split()
dstFonts   = []
preflight  = False

# batch copy glyphs

defaultFont = OpenFont(defaultPath, showInterface=False)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == defaultPath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'copying glyphs to {os.path.split(ufoPath)[-1]}...')
        for glyphName in glyphNames:
            if glyphName not in defaultFont:
                print(f'\tERROR: {glyphName} not in source font')
                continue
            print(f'\tcopying {glyphName}...')
            if not preflight:
                dstFont.insertGlyph(defaultFont[glyphName], name=glyphName)

        if not preflight:
            print(f'\tsaving font...')
            dstFont.save()

        # dstFont.close()
        print()

# menuTitle: copy unicodes from default font to other sources

### DEPRECATED >>> use xProject.copyUnicodesFromDefault

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

dstFonts  = []
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:
        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'\tcopying unicodes to {os.path.split(ufoPath)[-1]}...')
        for glyphName in sourceFont.glyphOrder:
            if glyphName not in sourceFont or glyphName not in dstFont:
                continue
            if dstFont[glyphName].unicodes != sourceFont[glyphName].unicodes:
                print(f'\tcopying unicodes in {glyphName}...')
                if not preflight:
                    dstFont[glyphName].unicodes = sourceFont[glyphName].unicodes

        if not preflight:
            print(f'\tsaving font...')
            dstFont.save()

        # dstFont.close()
        print()

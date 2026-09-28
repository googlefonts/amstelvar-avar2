# menuTitle: copy unicodes from Roman default to Italic default

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

preflight = False

print('copying unicodes from Roman to Italic default:\n')

for glyphName in srcFont.glyphOrder:
    if glyphName not in srcFont or glyphName not in dstFont:
        continue
    if dstFont[glyphName].unicodes != srcFont[glyphName].unicodes:
        print(f'\tcopying unicodes in {glyphName}...')
        if not preflight:
            dstFont[glyphName].unicodes = srcFont[glyphName].unicodes

if not preflight:
    print()
    print('\tsaving Italic default...')
    dstFont.save()

print('\n...done!\n')


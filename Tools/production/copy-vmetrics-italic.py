# menuTitle: copy veritcal metrics from Roman default to Italic default

import os, glob

familyName    = 'AmstelvarA2'
srcSubFamily  = 'Roman'
dstSubFamily  = 'Italic'
defaultName   = 'wght400'
preflight     = True

baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
srcFontPath   = os.path.join(baseFolder, 'Sources', srcSubFamily, f'{familyName}-{srcSubFamily}_{defaultName}.ufo')
dstFontPath   = os.path.join(baseFolder, 'Sources', dstSubFamily, f'{familyName}-{dstSubFamily}_{defaultName}.ufo')

srcFont = OpenFont(srcFontPath, showInterface=False)
dstFont = OpenFont(dstFontPath, showInterface=False)

print(f"copying vertical metrics from Roman default to Italic default...\n")

for attr in ['capHeight', 'xHeight', 'unitsPerEm', 'descender', 'ascender']:
    srcValue = getattr(srcFont.info, attr)
    dstValue = getattr(dstFont.info, attr)
    if dstValue != srcValue:
        print(f'\tcopying {attr}: {srcValue} -> {dstValue}')

if not preflight:
    print(f"\n\tsaving Italic font...")
    dstFont.save()

print('\n...done.\n')


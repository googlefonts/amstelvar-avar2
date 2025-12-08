# menuTitle: set style names in corner tuning sources

import os, glob

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
subFamilyName    = ['Roman', 'Italic'][0]
familyName       = f'AmstelvarA2 {subFamilyName}'
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
tunersFolder     = os.path.join(sourcesFolder, 'corners')

assert os.path.exists(tunersFolder)

ufoPaths = glob.glob(f'{tunersFolder}/*.ufo')

for ufoPath in ufoPaths:
    styleName = os.path.splitext(os.path.split(ufoPath)[-1])[0]

    f = OpenFont(ufoPath, showInterface=False)

    f.info.styleName = styleName
    f.features.text = ''

    f.save()
    f.close()

    
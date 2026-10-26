# create rvrn alternates for gyphs with BARS in all sources

import os
from controller import AmstelvarA2Controller

folder = os.path.dirname(os.path.dirname(os.getcwd()))

subFamily = ['Roman', 'Italic'][1]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

ufoPaths = p.sourcesPaths + list(p.referenceSourcesPaths.values())

glyphNames = p.smartSets['BARS']

for ufoPath in ufoPaths:
    f = OpenFont(ufoPath, showInterface=False)
    for glyphName in glyphNames:
        f[f'{glyphName}.rvrn'] = f[glyphName]
    f.close(save=False)

# check tabular figures width 

import os
from controller import AmstelvarA2Controller

folder = os.path.dirname(os.path.dirname(os.getcwd()))

subFamily = ['Roman', 'Italic'][0]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

glyphNames = p.smartSets['figures']['tabular']

for styleName, ufoPath in p.referenceSourcesPaths.items():
    f = OpenFont(ufoPath, showInterface=False)    
    widths = [f[glyphName].width for glyphName in glyphNames]
    multiWidth = len(set(widths)) > 1
    maxWidth = max(widths)
    if multiWidth:
        print(styleName, maxWidth)


from importlib import reload
import xTools4.modules.blendsPreview
reload(xTools4.modules.blendsPreview)

import os, time
from mojo.smartSet import readSmartSets
from xTools4.modules.blendsPreview import BlendsPreview
from xTools4.modules.sys import timer

def importGroupsFromSmartSets(smartsetsPath):
    smartSets = readSmartSets(smartsetsPath, useAsDefault=False, font=None)
    glyphGroups = {}
    for smartGroup in smartSets:
        if not smartGroup.groups:
            continue
        for smartSet in smartGroup.groups:
            glyphGroups[smartSet.name] = smartSet.glyphNames
    return glyphGroups

#---------
# options
#---------

compareFonts = {
    'Roman'  : 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf',
    'Italic' : 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf',
}

baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
familyName      = 'AmstelvarA2'
subFamilyName   = ['Roman', 'Italic'][0]
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.designspace')
smartsetsPath   = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.roboFontSets')
defaultPath     = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_wght400.ufo')
compareFontPath = os.path.join(baseFolder, 'Fonts', 'legacy', compareFonts[subFamilyName])

axesList = [
    ('opsz', (8, 14, 144)),
    ('wght', (100, 400, 1000)),
    ('wdth', (50, 100, 125)),
]

groupNames = [
    # 'uppercase latin',
    # 'uppercase greek',
    # 'uppercase cyrillic',
    # 'lowercase latin',
    # 'lowercase greek',
    # 'lowercase cyrillic',
]

savePDF = True

#-------------
# build proof
#-------------

start = time.time()

glyphGroups = importGroupsFromSmartSets(smartsetsPath)
# print(glyphGroups.keys())

glyphNames  = list('HOVTnov')
glyphNames += ['zero', 'one']

B = BlendsPreview(designspacePath)
B.compareFontPath = compareFontPath
B.axesList   = axesList
B.compare    = True
B.margins    = True
B.labels     = True
B.levels     = False
B.levelsShow = [1, 2, 3, 4]
B.header     = True
B.footer     = True
B.points     = False

for glyphName in glyphNames:
    if not glyphName:
        continue
    B.draw(glyphName)

if savePDF:
    pdfPath = os.path.join(baseFolder, 'Proofs', 'PDF', 'blending', f'blending-preview_{subFamilyName}.pdf')
    print(f'saving {pdfPath}...', end=' ')
    B.save(pdfPath)
    print(f'done!\n')

end = time.time()
timer(start, end)

import os
from ufoProcessor.ufoOperator import UFOOperator

baseFolder       = os.path.dirname(os.getcwd())
subFamily        = ['Roman', 'Italic'][1]
designspacePath  = os.path.join(baseFolder, 'Sources', subFamily, f'AmstelvarA2-{subFamily}.designspace')
designspacePath2 = os.path.join(baseFolder, 'Sources', subFamily, f'AmstelvarA2-{subFamily}_avar2.designspace')

D = UFOOperator(designspacePath)
print(os.path.split(designspacePath)[-1])
print('default:', D.findDefault().location)
print()

D2 = UFOOperator(designspacePath2)
print(os.path.split(designspacePath2)[-1])
print('axes:', [a.tag for a in D2.axes]) # blended axes are listed...
print('default:', D2.findDefault()) # but the default cannot be found :()

# L = {
#     'opsz': 18,
#     'wght': 600,
#     'wdth': 85,
# }

# g = D.makeOneGlyph('H', L, decomposeComponents=True, useVarlib=True, clip=True)
# scale(0.5)
# drawGlyph(g)

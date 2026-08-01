# drawBot

import os, json
import operator
from fontTools.designspaceLib import DesignSpaceDocument

baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
familyName      = 'AmstelvarA2'
subFamilyName   = ['Roman', 'Italic'][0]
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.designspace')
defaultPath     = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_wght400.ufo')
blendsPath      = os.path.join(sourcesFolder, 'blends.json')

savePDF = False

opszs = [8, 14, 144]
wghts = [100, 400, 1000]
wdths = [50, 100, 125]

def getShortStyleName(opsz, wght, wdth):
    styleNameParts = []
    if opsz != 14:
        styleNameParts.append(f'opsz{opsz}')
    if wght != 400:
        styleNameParts.append(f'wght{wght}')
    if wdth != 100:
        styleNameParts.append(f'wdth{wdth}')
    if opsz == 14 and wght == 400 and  wdth == 100:
        styleNameParts.append(f'wght{wght}')
    return '_'.join(styleNameParts)

with open(blendsPath, 'r', encoding='utf-8') as f:
    blendsData = json.load(f)

designspace = DesignSpaceDocument()
designspace.read(designspacePath)

axes = {}
for axis in designspace.axes:
    axes[axis.tag] = {
        'maximum' : axis.maximum,
        'minimum' : axis.minimum,
        'default' : axis.default,
    }

srcNames = []
for opsz in opszs:
    for wght in reversed(wghts):
        for wdth in wdths:
            srcName = getShortStyleName(opsz, wght, wdth)
            srcNames.append(srcName)

for srcName in srcNames:
    parameters = {}
    axisSides = {}

    for axisName, axisValue in blendsData['sources'][srcName].items():
        if axisName.startswith('TN'):
            continue

        if axes[axisName]['default'] < axisValue < axes[axisName]['maximum']:
            subAxisSide = 'max'
            axisInfluence = (axisValue - axes[axisName]['default']) / (axes[axisName]['maximum'] - axes[axisName]['default'])

        elif axes[axisName]['minimum'] < axisValue < axes[axisName]['default']:
            subAxisSide = 'min'
            axisInfluence = (axes[axisName]['default'] - axisValue) / (axes[axisName]['default'] - axes[axisName]['minimum'])

        else:
            subAxisSide = None        
            axisInfluence = 0

        parameters[axisName] = axisInfluence
        axisSides[axisName]  = subAxisSide

    parameters = list(reversed(sorted(parameters.items(), key=operator.itemgetter(1))))

    newPage('A4')
    font('Menlo')
    fontSize(14)
    text(srcName, (width()/2, height()-30), align='center')

    x, y = 100, height()-60
    w, h = 400, 11
    d = 2

    fontSize(9)
    for axisName, axisInfluence in parameters:
        axisSide = axisSides.get(axisName) if axisSides.get(axisName) is not None else ''
        fill(0.9)
        rect(x, y, w, h)
        fill(0)
        text(f'{"+" if axisSide == "max" else "-" if axisSide == "min" else " "} {axisName}', (x-40, y+2))
        text(f'{axisInfluence:.2f}', (x+w+10, y+2))
        rect(x, y, w*axisInfluence, h)
        translate(0, -h-d)


if savePDF:
    pdfPath = os.path.join(baseFolder, 'Proofs', 'PDF', f'parameter-influence_{subFamilyName}.pdf')
    saveImage(pdfPath)


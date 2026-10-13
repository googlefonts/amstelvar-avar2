import os
from controller import AmstelvarA2Controller
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph

folder = os.path.dirname(os.path.dirname(os.getcwd()))

subFamily = ['Roman', 'Italic'][1]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

glyphNames = p.defaultFont.glyphOrder # tweak all glyphs

tweakParametersBlended = {
    "wght1000": {
        "XOPQ" : 132,
        "XTRA" : 320,
        "XSHA" : 74,
    },
    "wght1000_wdth125": {
        "XOPQ" : 160,
        "YOPQ" : 71,
        "XTRA" : 318,
    },
}

preflight = True

# convert blended locations to parametric
tweakParameters = {}
for styleName, blendedLocation in tweakParametersBlended.items():
    for part in styleName.split('_'):
        name, value = part[:4], part[4:]
        blendedLocation[name] = int(value)
    parametersAll = getEffectiveLocation(p.designspacePath, blendedLocation)
    parametersChildren = {}
    for parentParameter, parentValue in blendedLocation.items():
        for param in p.measurements['font'].keys():
            if p.measurements['font'][param]['parent'] == parentParameter:
                if param in parametersAll:                
                    parametersChildren[param] = int(parametersAll[param])    
    tweakParameters[styleName] = parametersChildren

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

print(f'parametrically tweaking reference sources...')

for styleName in tweakParameters.keys():
    print(f'\ttweaking {styleName}...')
    # open reference source
    referenceSourceName = f'Amstelvar-{subFamily}_{styleName}'
    referenceSourcePath = p.referenceSourcesPaths.get(referenceSourceName)
    referenceSource = OpenFont(referenceSourcePath, showInterface=False)
    # get current blend parameters for this style
    parameters = p.blendedSources[styleName]
    # apply tweaks to blend parameters
    for k, v in tweakParameters[styleName].items():
        print(f'\t\t{k}: {parameters[k]} -> {v}')
        parameters[k] = v
    # instantiate glyphs from parameters
    for glyphName in glyphNames:
        print(f'\t\tinstantiating {glyphName}...')
        g = instantiateGlyph(operator, glyphName, parameters)
        referenceSource[glyphName] = RGlyph(g)
    # close and save reference source
    if not preflight:
        print(f'\t\tsaving...')
        referenceSource.close(save=True)
    else:
        referenceSource.openInterface()

print('...done!\n')

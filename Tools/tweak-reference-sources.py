from controller import AmstelvarA2Controller
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.blendsPreview import instantiateGlyph

folder = '/Users/gferreira/fontbureau/amstelvar-avar2'

p = AmstelvarA2Controller(folder, 'AmstelvarA2', 'Roman')

glyphNames = p.smartSets['figures']['proportional']

parametersTweak = {
    "wght100": {
      "XTFI": 430,
    },
    "wght100_wdth50": {
      "XTFI": 286,
    },
    "wght1000": {
      "XTFI": 268,
    },
    "opsz8": {
      "XTFI": 355,
    },
    "opsz8_wght100": {
      "XTFI": 450,
    },
    "opsz8_wght1000": {
      "XTFI": 266,
    },
    "opsz8_wdth50": {
      "XTFI": 185,
    },
    "opsz8_wdth125": {
      "XTFI": 490,
    },
    "opsz144": {
      "XTFI": 320,
    },
    "opsz144_wdth125": {
      "XTFI": 490,
    },
    "opsz144_wght1000": {
      "XTFI": 225,
    }
}

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

print(f'parametrically tweaking reference sources...')

for styleName in parametersTweak.keys():
    print(f'\ttweaking {styleName}...')
    # open reference source
    referenceSourceName = f'Amstelvar-Roman_{styleName}'
    referenceSourcePath = p.referenceSourcesPaths.get(referenceSourceName)
    referenceSource = OpenFont(referenceSourcePath, showInterface=False)
    # get current blend parameters for this style
    parameters = p.blendedSources[styleName]
    # apply tweaks to blend parameters
    for k, v in parametersTweak[styleName].items():
        print(f'\t\t{k}: {parameters[k]} -> {v}')
        parameters[k] = v
    # instantiate glyphs from parameters
    for glyphName in glyphNames:
        print(f'\t\tinstantiating {glyphName}...')
        g = instantiateGlyph(operator, glyphName, parameters)
        referenceSource[glyphName] = RGlyph(g)
    # close and save reference source
    referenceSource.close(save=True)

print('...done!\n')


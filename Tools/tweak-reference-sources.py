from controller import AmstelvarA2Controller
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.blendsPreview import instantiateGlyph

folder = '/Users/gferreira/fontbureau/amstelvar-avar2'

subFamily = ['Roman', 'Italic'][0]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

glyphNames = p.smartSets['figures']['currency']

preflight = True

parametersTweak = {
    "opsz8_wght100": {
      "XTFI": 601,
    },
}

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

print(f'parametrically tweaking reference sources...')

for styleName in parametersTweak.keys():
    print(f'\ttweaking {styleName}...')
    # open reference source
    referenceSourceName = f'Amstelvar-{subFamily}_{styleName}'
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
    if not preflight:
        print(f'\t\tsaving...')
        referenceSource.save()
    referenceSource.close()

print('...done!\n')


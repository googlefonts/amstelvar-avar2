# menuTitle: calculate tuning glyphs

# from importlib import reload
# import controller
# reload(controller)
# import xTools4.modules.measurements
# reload(xTools4.modules.measurements)

import os, glob, time, string
from ufoProcessor.ufoOperator import UFOOperator
from controller import AmstelvarA2Controller
from xTools4.modules.measurements import *
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph
from xTools4.modules.sys import timer

subFamily    = ['Roman', 'Italic'][0]
glyphNames   = list(string.ascii_uppercase)
tuneDuovars  = True
tuneTrivars  = True
tuneQuadvars = True

start = time.time()

folder = os.path.dirname(os.getcwd())
p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

referenceFontPath = os.path.join(p.referenceSourcesFolder, 'Amstelvar-Roman_wght400.ufo')
referenceFont = OpenFont(referenceFontPath, showInterface=False)

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

referenceSources = {'_'.join(k.split('_')[1:]): OpenFont(v, showInterface=False) for k, v in p.referenceSources.items()}

for glyphName in glyphNames:

    glyphDefault = p.defaultFont[glyphName]
    glyphReference = referenceFont[glyphName]
    matchingPoints = getMatchingPoints(glyphDefault, glyphReference)

    print(f'calculating tuning sources for /{glyphName}...\n')

    for styleName, ufoPath in p.tuningSources.items():
        styleNameParts = styleName.split('_')

        if len(styleNameParts) == 1 and not tuneDuovars:
            continue
        if len(styleNameParts) == 2 and not tuneTrivars:
            continue
        if len(styleNameParts) == 3 and not tuneQuadvars:
            continue

        print(f'\ttuning {styleName}...')

        # get blended glyph (parametric)
        blendedLocation = { part[:4]: int(part[4:]) for part in styleNameParts }
        parametricLocation = getEffectiveLocation(p.designspacePath, blendedLocation)
        blendedGlyph = RGlyph(instantiateGlyph(operator, glyphName, parametricLocation))

        # get reference glyph
        blendedReference = referenceSources[styleName][glyphName]

        # make tuning glyph
        tuningGlyph = makeTuningGlyph(blendedGlyph, blendedReference, glyphDefault, matchingPoints)

        # save glyph to tuning source
        tuningSource = OpenFont(ufoPath, showInterface=False)
        tuningSource.insertGlyph(tuningGlyph, name=glyphName)
        tuningSource.save()

    print()

print('...done!\n')

end = time.time()
timer(start, end)

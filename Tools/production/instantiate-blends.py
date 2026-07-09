# menuTitle: instantiate blended glyphss

import os
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph

subFamily       = ['Roman', 'Italic'][0]
baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamily)
designspacePath = os.path.join(sourcesFolder, 'AmstelvarA2-Roman.designspace')

assert os.path.exists(designspacePath)

font = CurrentFont()

fileName = os.path.splitext(os.path.split(font.path)[-1])[0]
styleName = ' '.join(fileName.split('_')[1:])

# get blended location from style name
blendedLocation = { p[:4] : int(p[4:]) for p in styleName.split(' ') }

# get parametric location from blended location
parametricLocation = getEffectiveLocation(designspacePath, blendedLocation)

operator = UFOOperator()
operator.read(designspacePath)
operator.loadFonts()

glyphNames = getGlyphs2(font)

for glyphName in glyphNames:
    g = RGlyph(instantiateGlyph(operator, glyphName, parametricLocation))
    dstGlyph = font[glyphName].getLayer('background')
    dstGlyph.clear()
    dstGlyph.appendGlyph(g)
    dstGlyph.width = g.width

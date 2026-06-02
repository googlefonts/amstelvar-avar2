from importlib import reload
import controller
reload(controller)

import os
from controller import AmstelvarA2Controller
from xTools4.modules.measurements import *

#----------
# settings
#----------

subFamily = ['Roman', 'Italic'][0]
glyphName = 'V'
x, y = 100, 220
s = 0.42             # glyph scale
r = 8                # point radius
margin = 100

guidesColor = 0.7,
measurementsColor = 1, 0, 0
measurementsDash = 3, 12
pointsColor = 0,

folder = os.path.dirname(os.getcwd())

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

glyphDefault = p.defaultFont[glyphName]

yMetrics = set([
    p.defaultFont.info.descender,
    0,
    p.defaultFont.info.xHeight,
    p.defaultFont.info.capHeight,
    p.defaultFont.info.ascender
])

referenceFontPath = os.path.join(p.referenceSourcesFolder, subFamily, 'Amstelvar-Roman_wght400.ufo')
referenceFont = OpenFont(referenceFontPath, showInterface=False)
glyphReference = referenceFont[glyphName]

#-----------
# functions
#-----------

def _drawGlyph(glyph, pos, scale_, label):

    x, y = pos

    with savedState():
        stroke(*guidesColor)
        for _x in [0, glyph.width]:
            line((x+_x*s, 0), (x+_x*s, height()))

    save()
    translate(x, y)
    scale(scale_)

    with savedState():
        fill(0.9)
        stroke(None)
        drawGlyph(glyph)

    with savedState():
        fill(*pointsColor)
        stroke(None)
        font('Menlo')
        fontSize(36)
        n = 0
        for c in glyph.contours:
            for p in c.points:
                oval(p.x-r, p.y-r, r*2, r*2)        
                text(str(n), (p.x, p.y-50), align='center')
                n += 1

    with savedState():
        fill(*pointsColor)
        fontSize(81)
        text(label, (glyph.width/2, -400), align='center')

    restore()

def _drawMeasurements(glyph, glyphMeasurements, pos, scale_):
    save()
    translate(x, y)
    scale(scale_)
    lineCap('round')
    strokeWidth(5)
    stroke(*measurementsColor)
    lineDash(*measurementsDash)
    for ID, m in glyphMeasurements.items():
        pt1_index, pt2_index = ID.split()
        try:
            pt1 = getPointAtIndex(glyph, int(pt1_index))
        except:
            pt1 = getAnchorPoint(glyph.font, pt1_index)
        try:
            pt2 = getPointAtIndex(glyph, int(pt2_index))
        except:
            pt2 = getAnchorPoint(glyph.font, pt2_index)
        
        if pt1 is None or pt2 is None:
            continue
        
        line((pt1.x, pt1.y), (pt2.x, pt2.y))

    restore()

def _transferMeasurements(glyphMeasurements, srcGlyph, dstGlyph):
    dstMeasurements = {} # glyphMeasurements.copy()
    for ID, m in glyphMeasurements.items():
        pt1_index, pt2_index = ID.split()

        try:
            pt1_index = int(pt1_index)
            pt1 = getPointAtIndex(srcGlyph, pt1_index)
            dstIndex = None
            n = 0
            for c in dstGlyph.contours:
                for p in c.points:
                    if p.x == pt1.x and p.y == pt1.x:
                        dstIndex = n
                    n += 1       
            pt1_index = dstIndex
        except:
            pass

        # pt2_index = int(pt2_index)
        # pt2 = getPointAtIndex(srcGlyph, pt2_index)
        # dstIndex = None
        # n = 0
        # for c in dstGlyph.contours:
        #     for p in c.points:
        #         if p.x == pt2.x and p.y == pt2.x:
        #             dstIndex = n
        #         n += 1       
        # pt2_index = dstIndex


        dstMeasurements[f'{pt1_index} {pt2_index}'] = m

    # print(dstMeasurements)

    return dstMeasurements

# print(p.measurements['glyphs'][glyphName])
# print()

glyphMeasurementsReference = _transferMeasurements(p.measurements['glyphs'][glyphName], glyphDefault, glyphReference)

#-------
# draw!
#-------

newPage(3000, 1000)
blendMode('multiply')

# draw verical metrics
with savedState():
    stroke(*guidesColor)
    for _y in yMetrics:
        line((0, y+_y*s), (width(), y+_y*s))

_drawGlyph(glyphDefault, (x, y), s, 'default')
_drawMeasurements(glyphDefault, p.measurements['glyphs'][glyphName], (x, y), s)

x += glyphDefault.width*s + margin

_drawGlyph(glyphReference, (x, y), s, 'reference')
_drawMeasurements(glyphReference, glyphMeasurementsReference, (x, y), s)


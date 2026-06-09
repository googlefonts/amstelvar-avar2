# drawBot

from importlib import reload
import controller
reload(controller)
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, glob
from ufoProcessor.ufoOperator import UFOOperator
from controller import AmstelvarA2Controller
from xTools4.modules.measurements import *
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual

#-----------
# functions
#-----------

def _drawVerticalMetrics(pos, yMetrics):
    x, y = pos
    with savedState():
        stroke(*guidesColor)
        for _y in yMetrics:
            line((0, y+_y*s), (width(), y+_y*s))

def _drawGlyph(glyph, pos, scale_, label, points=True, index=True, color=(0.5,), drawFill=True):

    x, y = pos

    with savedState():
        stroke(*color, 0.5)
        for _x in [0, glyph.width]:
            line((x+_x*s, 0), (x+_x*s, height()))

    save()
    translate(x, y)
    scale(scale_)

    with savedState():
        if drawFill:
            fill(*color, 0.2)
            stroke(None)
        else:
            fill(None)
            stroke(*color, 0.5)
        drawGlyph(glyph)

    if points:
        with savedState():
            fill(*color)
            stroke(None)
            font('Menlo')
            fontSize(28)
            n = 0
            for c in glyph.contours:
                for p in c.points:
                    oval(p.x-r, p.y-r, r*2, r*2)
                    if index:
                        text(str(n), (p.x, p.y-36), align='center')
                    n += 1

    with savedState():
        fill(*color)
        fontSize(81)
        text(label, (glyph.width/2, -400), align='center')

    restore()

def _drawMeasurements(glyph, glyphMeasurements, pos, scale_):

    measurementsColor       = 0,
    measurementsDash        = 3, 12
    measurementsStrokeWidth = 5

    save()
    translate(x, y)
    scale(scale_)
    strokeWidth(measurementsStrokeWidth)
    stroke(*measurementsColor)
    lineDash(*measurementsDash)
    lineCap('round')
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
            print(pt1, pt2)
            continue

        line((pt1.x, pt1.y), (pt2.x, pt2.y))
    restore()

def _drawDeltas(glyph1, glyph2, pos, scale_, matchingPoints=None, color=None):
    save()
    translate(*pos)
    scale(scale_)
    strokeWidth(5)
    lineCap('round')

    if not matchingPoints: # assume matching point indexes
        matchingPoints = []
        for ci, c in enumerate(glyph1.contours):
            for pi, p in enumerate(c.points):
                matchingPoints.append( ((ci, pi), (ci, pi)) )

    for mp1, mp2 in matchingPoints:
        ci1, pi1 = mp1
        ci2, pi2 = mp2
        p1 = glyph1.contours[ci1].points[pi1]
        p2 = glyph2.contours[ci2].points[pi2]

        if color is not None:
            stroke(*color)
        else:
            if p1.x == p2.x or p1.y == p2.y:
                stroke(*colorCheckTrue)
            else:
                stroke(*colorCheckFalse)

        if p1.x == p2.x and p1.y == p2.y:
            continue

        line((p1.x, p1.y), (p2.x, p2.y))

    restore()

#----------
# settings
#----------

subFamily = ['Roman', 'Italic'][0]
glyphName = 'U'

x0, y0 = 100, 220  # origin position
w, h = 5000, 1000  # page size
s = 0.42           # glyph scale
r = 7              # point radius
margin = 100       # margin glyphs

guidesColor = 0.85,
color1 = 0, 1, 1
color2 = 1, 0, 1

# 1: duovars only / 2: duovars + trivars / 3: duovars + trivars + quadvars
tuningLevel = 3

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

referenceFontPath = os.path.join(p.referenceSourcesFolder, 'Amstelvar-Roman_wght400.ufo')
referenceFont = OpenFont(referenceFontPath, showInterface=False)
glyphReference = referenceFont[glyphName]

# transfer glyph measurements to reference font
glyphMeasurementsReference = transferGlyphMeasurements(p.measurements['glyphs'][glyphName], glyphDefault, glyphReference)

#-------
# draw!
#-------

x, y = x0, y0

newPage(w, h)
blendMode('multiply')

_drawVerticalMetrics((x, y), yMetrics)
_drawGlyph(glyphDefault, (x, y), s, 'default')
_drawMeasurements(glyphDefault, p.measurements['glyphs'][glyphName], (x, y), s)

x += glyphDefault.width*s + margin

_drawGlyph(glyphReference, (x, y), s, 'reference')
_drawMeasurements(glyphReference, glyphMeasurementsReference, (x, y), s)

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

referenceSources = {'_'.join(k.split('_')[1:]): OpenFont(v, showInterface=False) for k, v in p.referenceSources.items()}

for styleName, ufoPath in p.tuningSources.items():
    styleNameParts = styleName.split('_')

    if len(styleNameParts) > tuningLevel:
        continue

    # get blended glyph (parametric)
    blendedLocation = { part[:4]: int(part[4:]) for part in styleNameParts }
    parametricLocation = getEffectiveLocation(p.designspacePath, blendedLocation)
    blendedGlyph = RGlyph(instantiateGlyph(operator, glyphName, parametricLocation))

    # get reference glyph
    blendedReference = referenceSources[styleName][glyphName]

    # make tuning glyph
    matchingPoints = getMatchingPoints(glyphDefault, glyphReference)
    tuningGlyph = makeTuningGlyph(blendedGlyph, blendedReference, glyphDefault, matchingPoints)

    # draw page
    x, y = x0, y0
    newPage(w, h)
    blendMode('multiply')
    _drawVerticalMetrics((x, y), yMetrics)    
    _drawGlyph(blendedGlyph, (x, y), s, styleName, color=color1)

    x += blendedGlyph.width*s + margin

    _drawGlyph(blendedReference, (x, y), s, 'reference', color=color2)

    x += blendedReference.width*s + margin
    
    _drawGlyph(blendedGlyph, (x, y), s, 'diff', points=True, index=False, color=color1, drawFill=False)
    _drawGlyph(blendedReference, (x, y), s, 'diff', points=True, index=False, color=color2, drawFill=False)
    _drawDeltas(blendedGlyph, blendedReference, (x, y), s, matchingPoints=matchingPoints, color=(0, 0, 1))

    x += max(blendedGlyph.width, blendedReference.width)*s + margin 

    _drawGlyph(tuningGlyph, (x, y), s, 'tuning', points=True, index=False, drawFill=False)
    _drawGlyph(glyphDefault, (x, y), s, '', points=False, index=False, drawFill=True)
    _drawDeltas(tuningGlyph, glyphDefault, (x, y), s)

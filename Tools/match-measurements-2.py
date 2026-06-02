from importlib import reload
import controller
reload(controller)

import os, glob
from ufoProcessor.ufoOperator import UFOOperator
from controller import AmstelvarA2Controller
from xTools4.modules.measurements import *
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph, getTTFGlyphForChar

#----------
# settings
#----------

subFamily = ['Roman', 'Italic'][0]
glyphName = 'V'
x0, y0 = 100, 220
w, h = 4000, 1000
s = 0.42             # glyph scale
r = 4                # point radius
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

referenceFontPath = os.path.join(p.referenceSourcesFolder, 'Amstelvar-Roman_wght400.ufo')
referenceFont = OpenFont(referenceFontPath, showInterface=False)
referenceFontTTF = os.path.join(p.fontsFolder, 'legacy', 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')

glyphReference = referenceFont[glyphName]

#-----------
# functions
#-----------

def _drawVerticalMetrics(pos, yMetrics):
    x, y = pos
    with savedState():
        stroke(*guidesColor)
        for _y in yMetrics:
            line((0, y+_y*s), (width(), y+_y*s))

def _drawGlyph(glyph, pos, scale_, label, points=True, index=True):

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

    if points:
        with savedState():
            fill(*pointsColor)
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
            print(pt1, pt2)
            continue
        
        line((pt1.x, pt1.y), (pt2.x, pt2.y))

    restore()

def _transferMeasurements(glyphMeasurements, srcGlyph, dstGlyph):
    dstMeasurements = {}
    for ID, m in glyphMeasurements.items():
        pt1_index, pt2_index = ID.split()

        if pt1_index not in ['-1', '99']:            
            try:
                pt1_index = int(pt1_index)
                pt1 = getPointAtIndex(srcGlyph, pt1_index)
                dstIndex = None
                n = 0
                for c in dstGlyph.contours:
                    for p in c.points:
                        if p.x == pt1.x and p.y == pt1.y:
                            dstIndex = n
                        n += 1       
                pt1_index = dstIndex
            except:
                pass

        if pt2_index not in ['-1', '99']:            
            try:
                pt2_index = int(pt2_index)
                pt2 = getPointAtIndex(srcGlyph, pt2_index)
                dstIndex = None
                n = 0
                for c in dstGlyph.contours:
                    for p in c.points:
                        if p.x == pt2.x and p.y == pt2.y:
                            dstIndex = n
                        n += 1       
                pt2_index = dstIndex
            except:
                pass

        dstMeasurements[f'{pt1_index} {pt2_index}'] = m

    return dstMeasurements

glyphMeasurementsReference = _transferMeasurements(p.measurements['glyphs'][glyphName], glyphDefault, glyphReference)

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

tuningLevel = 2 # 1: duovars / 2: trivars / 3: quadvars

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

    x, y = x0, y0
    newPage(w, h)
    blendMode('multiply')
    _drawVerticalMetrics((x, y), yMetrics)    
    _drawGlyph(blendedGlyph, (x, y), s, styleName)

    x += blendedGlyph.width*s + margin

    _drawGlyph(blendedReference, (x, y), s, 'reference')

    x += blendedReference.width*s + margin
    
    _drawGlyph(blendedGlyph, (x, y), s, 'diff', points=True, index=False)
    _drawGlyph(blendedReference, (x, y), s, '', points=True, index=False)

    save()
    translate(x, y)
    scale(s)
    stroke(0)
    matchingPoints = []

    glyphTuning = glyphDefault.copy()

    for ci, c in enumerate(glyphDefault.contours):
        for pi, pt in enumerate(c.points):
            # find matching reference point
            for cci, cc in enumerate(glyphReference.contours):
                for ppi, pp in enumerate(cc.points):
                    if pp.x == pt.x and pp.y == pt.y:
                        matchingPoints.append(((ci, pi), (cci, ppi)))

    for mp1, mp2 in matchingPoints:
        ci1, pi1 = mp1
        ci2, pi2 = mp2
        p1 = blendedGlyph.contours[ci1].points[pi1]
        p2 = blendedReference.contours[ci2].points[pi2]
        line((p1.x, p1.y), (p2.x, p2.y))

        deltaX = p2.x - p1.x
        deltaY = p2.y - p1.y
        pt = glyphTuning.contours[ci1].points[pi1]
        pt.x += deltaX
        pt.y += deltaY
       
    restore()

    x += max(blendedGlyph.width, blendedReference.width)*s + margin 

    _drawGlyph(glyphDefault, (x, y), s, '', points=False, index=False)
    _drawGlyph(glyphTuning, (x, y), s, 'tuning', points=False, index=False)

    


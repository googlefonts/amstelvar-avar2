# menuTitle: visualize the combination of parametric axes into a blended parent axis

import os, glob
from colorsys import hsv_to_rgb
from xTools4.modules.measurements import FontMeasurements, permille
from xTools4.modules.linkPoints2 import readMeasurements

# --------
# settings
# --------

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath  = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_avar2.designspace')
measurementsPath = os.path.join(sourcesFolder, f'measurements.json')

parentAxesRoman  = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA XVAA YHAA'.split() # XTEQ YTEQ
parentAxesItalic = parentAxesRoman

parametricAxesRoman  = 'XOUC XOLC XOFI YOUC YOLC YOFI XTUC XTUR XTUD XTLC XTLR XTLD XTFI YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XVAU YHAU XVAL YHAL XVAF YHAF XTTW YTTL YTOS XUCS XUCR XUCD XLCS XLCR XLCD XFIR WDSP XDOT BARS XQUC YQUC XQLC YQLC XQFI YQFI'.split()
parametricAxesItalic = parametricAxesRoman

parentAxesDefaults = {
    'XOPQ' : 'XOUC',
    'YOPQ' : 'YOUC',
    'XTRA' : 'XTUC',
    'XSHA' : 'XSHU',
    'YSHA' : 'YSHU',
    'XSVA' : 'XSVU',
    'YSVA' : 'YSVU',
    'XVAA' : 'XVAU',
    'YHAA' : 'YHAU',
    'XTEQ' : 'XQUC',
    'YTEQ' : 'YQUC',
}

drawRanges   = True
drawMappings = True
savePDF      = False
trimExtremes = False

p   = 55
d   = 100
r1  = 4
r2  = 2
sw  = 1
fs1 = 14
fs2 = 7
fs3 = 24

# ------------
# collect data
# ------------

parentAxes     = parentAxesRoman if subFamilyName == 'Roman' else parentAxesItalic
parametricAxes = parametricAxesRoman if subFamilyName == 'Roman' else parametricAxesItalic
parentAxisName = parentAxes[2] # 'XTRA'

defaultUFO  = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
defaultFont = OpenFont(defaultUFO, showInterface=False)

measurements     = readMeasurements(measurementsPath)
fontMeasurements = measurements['font']

measurementsDefault = FontMeasurements()
measurementsDefault.read(measurementsPath)
measurementsDefault.measure(defaultFont)

parametricSources = glob.glob(f'{sourcesFolder}/*.ufo')

defaultLocation = { name: permille(measurementsDefault.values[name], defaultFont.info.unitsPerEm) for name in parametricAxes }

parentMeasurement = fontMeasurements[parentAxisName]

# get parametric axes for parent
parametricAxes = {}
childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisName]
for childName in childNames:
    # get min/max values from file names
    values = []
    for ufo in parametricSources:
        if childName in ufo:
            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
            values.append(value)
    if not len(values) == 2:
        print(parentAxisName, childName, values)
        continue
    values.sort()

    parametricAxes[childName] = {
        'minimum' : values[0],
        'maximum' : values[1],
        'default' : defaultLocation[childName],
    }

parentDefault = parentAxesDefaults[parentAxisName]

# get parent ranges and default from parametric axes
parentAxis = {
    parentAxisName : {
        'default' : parametricAxes[parentDefault]['default'],
        'minimum' : min([
            parametricAxes[a]['minimum'] + parametricAxes[parentDefault]['default'] - parametricAxes[a]['default'] 
            for a in parametricAxes.keys()
        ]),
        'maximum' : max([
            parametricAxes[a]['maximum'] + parametricAxes[parentDefault]['default'] - parametricAxes[a]['default'] 
            for a in parametricAxes.keys()
        ]),
        'color'   : (0, 0, 0),  
    }
}
axes = { **parentAxis, **parametricAxes }

# make unique colors for parametric axis
colors = { 
    n : hsv_to_rgb(i * 1.0 / len(parametricAxes), 1, 1) 
    for i, n in enumerate(parametricAxes.keys()) 
}
colors[parentAxisName] = (0, 0, 0)

# ------------------
# draw visualization
# ------------------

w, h = 930, d * len(parametricAxes) + p*2

newPage(w, h)

x, y = width()*0.585, height() - p*1.27

translate(x, y)

for i, axisName in enumerate(axes.keys()):
    axis = axes[axisName]
    xMin, xMax, xDef = axis['minimum'], axis['maximum'], axis['default']
    c = colors[axisName]

    save()
    translate(-xDef, 0)

    # draw mapping guides
    with savedState():
        stroke(0.85, 0.35)
        if i == 0:
            line((xDef, -y), (xDef, height()))
        else:
            if drawMappings:
                line((xMin, -y), (xMin, height()))
                line((xMax, -y), (xMax, height()))

    with savedState():    
        stroke(*c)
        strokeWidth(sw)
        line((xMin, 0), (xMax, 0))

    with savedState():    
        stroke(None)
        fontSize(fs1)

        # draw minimum / maximum / default
        if drawRanges:
            for xx in [xMin, xMax, xDef]:
                with savedState():  
                    stroke(*c)
                    strokeWidth(sw)
                    fill(None)
                    oval(xx-r1, -r1, r1*2, r1*2)
                    translate(xx, -25)
                    fill(*c)
                    stroke(None)
                    text(str(xx), (0, 2), align='center')

        # calculate mapping steps
        if drawMappings:
            steps = []
            for aName, a in axes.items():
                if aName == parentAxis:
                    continue
                aShift = - a['default'] + xDef
                minValue = a['minimum'] 
                maxValue = a['maximum'] 
                ### NOT WORKING YET
                # if aName != parentAxisName:
                #     if trimExtremes:
                #         if minValue < xMin:
                #             print('min', minValue, xMin)
                #             minValue = xMin
                #         elif maxValue < xMax:
                #             print('max', maxValue, xMax)
                #             maxValue = xMax
                steps += [ minValue + aShift, maxValue + aShift ]
            fontSize(fs2)

            # draw mapping steps
            for xxx in sorted(steps):
                fill(*c)
                oval(xxx-r2, -r2, r2*2, r2*2)
                with savedState():    
                    fill(*c)
                    oval(xxx-r2, -r2, r2*2, r2*2)
                    translate(xxx, 18)
                    rotate(90)
                    text(str(xxx), (0, -3), align='center')

    # draw axis name
    with savedState():    
        stroke(None)
        fill(*c)
        fontSize(fs3)
        text(axisName, (xDef, 32), align='center')

    restore()
    translate(0, -d)

# save to PDF file
if savePDF:
    folder = os.getcwd()
    pdfPath = os.path.join(folder, 'parent-parametric-axes.pdf')
    saveImage(pdfPath)

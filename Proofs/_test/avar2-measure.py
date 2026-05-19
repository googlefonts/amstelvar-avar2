from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os
from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont
from xTools4.modules.measurements import FontMeasurements, permille

folder  = os.path.dirname(os.path.dirname(os.getcwd()))
ttfPath = os.path.join(folder, 'Fonts', 'AmstelvarA2-Roman_avar2.ttf')

font(ttfPath)
parameters = fontVariations()

# parameters['opsz'] = 36 # doesn't have any effect!
parameters['XOPQ'] = 120
# parameters['XTRA'] = 500
# parameters['YOPQ'] = 62

varfont = TTFont(ttfPath)
partial = instantiateVariableFont(varfont, parameters)

partialPath = ttfPath.replace('.ttf', '_temp.ttf')
partial.save(partialPath)

x, y = 100, 300

with savedState():
    fontSize(240)
    font(partialPath)
    fill(1, 0, 0)
    text('abcd', (x, y))

measurementsPath = os.path.join(folder, 'Sources', 'Roman', 'measurements.json')

assert os.path.exists(measurementsPath)

f = OpenFont(partialPath, showInterface=False)
# this fixes most indexes, but not all
# for g in f:
#     if not len(f):
#         continue
#     g.correctDirection(trueType=True)

M = FontMeasurements()
M.reverse = True
M.read(measurementsPath)
M.measure(f)

x, y = 720, 950

fontsize   = 14
lineheight = 1.5

fill(0)
fontVariations(resetVariations=True)
font('Menlo')
fontSize(fontsize)
tabs((90, "right"), (150, "right"))

for tag, value in M.values.items():
    valuePermill = permille(value, f.info.unitsPerEm)
    if tag not in parameters:
        continue
    text(f'{tag}\t{value}\t{valuePermill}', (x, y))
    y -= fontsize * lineheight

# menuTitle: extract parametric blends from Amstelvar1 extrema

from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, glob, json
from xTools4.modules.measurements import extractMeasurements

subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName, 'reference')
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
blendsPath       = os.path.join(sourcesFolder, 'blends.json')

parametricAxesRoman  = 'XOUC XOLC XOFI XOET YOUC YOLC YOFI YOET XOUA XOLA YOUA YOLA XTUC XTUR XTUD XTUA XTLC XTLR XTLD XTLA XTFI XTET YTUC YTJD YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS XUCS XUCR XUCD XLCS XLCR XLCD XFIR XETS WDSP XDOT XQUC XQLC XQFI YQUC YQLC YQFI XVAU'.split() # U#XO U#YO U#XT U#XQ YHAU XVAL YHAL XVAF YHAF
parametricAxesItalic = parametricAxesRoman

parametricAxes = parametricAxesRoman if subFamilyName == 'Roman' else parametricAxesItalic

assert os.path.exists(sourcesFolder)
assert os.path.exists(measurementsPath)

# define blended axes

axes = {
    "opsz" : {
      "name"    : "Optical size",
      "default" : 14,
      "minimum" : 8,
      "maximum" : 144,
    },
    "wght" : {
      "name"    : "Weight",
      "default" : 400,
      "minimum" : 100,
      "maximum" : 1000,
    },
    "wdth": {
      "name"    : "Width",
      "default" : 100,
      "minimum" : 50,
      "maximum" : 125,
    }
}

# extract measurements from Amstelvar1 instances

ufos = [f for f in glob.glob(f'{sourcesFolder}/*.ufo') if 'GRAD' not in f]

sources = extractMeasurements(ufos, measurementsPath, parametricAxes)

# save measurements to JSON blends file

blendsDict = {
    'axes'    : axes,
    'sources' : sources,
}

print('saving blended axes and measurements to blends.json...\n')

with open(blendsPath, 'w', encoding='utf-8') as f:
    json.dump(blendsDict, f, indent=2)

print('...done!\n')

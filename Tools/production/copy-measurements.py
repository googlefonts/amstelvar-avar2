from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from xTools4.modules.measurements import copyFontMeasurements, copyGlyphMeasurements

baseFolder          = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder       = os.path.join(baseFolder, 'Sources')
measurementsPathSrc = os.path.join(sourcesFolder, 'Italic',  'measurements.json')
measurementsPathDst = os.path.join(sourcesFolder, 'Italic', 'reference', 'measurements.json') 

assert os.path.exists(measurementsPathSrc)
assert os.path.exists(measurementsPathDst)

# copy font-level measurements
measurementNames = 'XETS XOET XTET YOET'.split() # 'YTUO YTLO YTFO YTAO YTDO XOAC YOAC XOUA XOLA YOUA YOLA YTUA YTLA YUAT YLAT XTUA XTLA'.split()
copyFontMeasurements(measurementsPathSrc, measurementsPathDst, measurementNames)

# # copy glyph-level measurements
# glyphNames = ['AE'] # CurrentFont().selectedGlyphNames
# copyGlyphMeasurements(measurementsPathSrc, measurementsPathDst, glyphNames)

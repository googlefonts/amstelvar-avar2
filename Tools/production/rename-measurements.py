# menuTitle : rename glyph measurements

from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from xTools4.modules.measurements import renameGlyphMeasurements

subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources')
measurementsPath = os.path.join(sourcesFolder, subFamilyName,  'measurements.json')

assert os.path.exists(measurementsPath)

glyphNames = 'exclam quotesingle quotedbl numbersign ampersand parenleft parenright asterisk comma hyphen period slash colon semicolon question at bracketleft backslash bracketright asciicircum underscore braceleft bar braceright exclamdown brokenbar section copyright ordfeminine registered degree paragraph periodcentered ordmasculine questiondown quoteleft quoteright guillemotleft guillemotright .null CR nbspace .notdef numero commercialMinusSign ellipsis quotesinglbase quotedblleft quotedblright quotedblbase guilsinglleft guilsinglright hyphentwo endash emdash softhyphen dagger daggerdbl bullet trademark fraction divisionslash primemod doubleprimemod apostrophemod minute second leftanglebracket rightanglebracket micro ohm numeralsign lownumeralsign gr:question anoteleia threequartersemdash figuredash'.split()

renameDict = {
    # 'XOPQ' : 'XOET',
    # 'YOPQ' : 'YOET',
    # 'XTUC' : 'XTET',
    'XSHL' : 'XSHE',
    'YSHL' : 'YSHE',
    # 'XSVU' : 'XSVE',
    # 'YSVU' : 'YSVE',
}

renameGlyphMeasurements(measurementsPath, glyphNames, renameDict)

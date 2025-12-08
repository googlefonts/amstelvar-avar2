# menuTitle: cleanup unnecessary data & normalize all sources

from importlib import reload
import xTools4.modules.normalization
reload(xTools4.modules.normalization)

import os
from xTools4.modules.normalization import cleanupSources, normalizeSources

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
cornersFolder = os.path.join(sourcesFolder, 'corners')

sources = False
corners = True

ignoreFontLibs = [
    'com.typemytype.robofont.italicSlantOffset',
    'com.typemytype.robofont.segmentType',
]

ignoreLayers = [
    'foreground',
    'background',
]

if sources:
    cleanupSources(sourcesFolder, preflight=False, ignoreFontLibs=ignoreFontLibs, ignoreLayers=ignoreLayers)
    normalizeSources(sourcesFolder)

if corners:
    cleanupSources(cornersFolder, preflight=False, ignoreFontLibs=ignoreFontLibs, ignoreLayers=ignoreLayers)
    normalizeSources(cornersFolder)

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

cleanup   = True
normalize = True

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
    if cleanup:
        cleanupSources(sourcesFolder, preflight=False, ignoreFontLibs=ignoreFontLibs, ignoreLayers=ignoreLayers)
    if normalize:
        normalizeSources(sourcesFolder)

if corners:
    if cleanup:
        cleanupSources(cornersFolder, preflight=False, ignoreFontLibs=ignoreFontLibs, ignoreLayers=ignoreLayers)
    if normalize:
        normalizeSources(cornersFolder)

# menuTitle: cleanup unnecessary data & normalize all sources

from importlib import reload
import xTools4.modules.normalization
reload(xTools4.modules.normalization)

import os, time
from xTools4.modules.sys import timer
from xTools4.modules.normalization import cleanupSources, normalizeSources

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
cornersFolder = os.path.join(sourcesFolder, 'corners')

# which sources to clean/normalize
sources = False
corners = True

# which actions to perform
cleanup   = True
normalize = True

ignoreFontLibs = [
    'com.typemytype.robofont.italicSlantOffset',
    'com.typemytype.robofont.segmentType',
]

ignoreLayers = [
    'foreground',
    'background',
]

start = time.time()

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

end = time.time()
timer(start, end)

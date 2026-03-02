from importlib import reload
import xTools4.modules.glyphSetProofer
reload(xTools4.modules.glyphSetProofer)

import os, glob, time
from xTools4.modules.glyphSetProofer import GlyphSetProofer
from xTools4.modules.sys import timer

familyName      = 'AmstelvarA2'
subFamily       = ['Roman', 'Italic'][1]
baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
pdfsFolder      = os.path.join(baseFolder, 'Proofs', 'PDF')
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamily)
defaultFontPath = os.path.join(sourcesFolder, f'{familyName}-{subFamily}_wght400.ufo')
sourcePaths     = sorted(glob.glob(f'{sourcesFolder}/*.ufo'))

assert os.path.exists(pdfsFolder)
assert os.path.exists(sourcesFolder)
assert os.path.exists(defaultFontPath)

sourcePaths.remove(defaultFontPath)

start = time.time()
P = GlyphSetProofer(f'{familyName} {subFamily}', defaultFontPath, sourcePaths)
P.build(savePDF=True, folder=pdfsFolder)
end = time.time()

timer(start, end)

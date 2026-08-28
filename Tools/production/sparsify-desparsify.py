from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import os
from xTools4.modules.validation import sparsifySource, desparsifySource

subFamily = ['Roman', 'Italic'][0]
baseFolder = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamily)

assert os.path.exists(sourcesFolder)

sourceName  = 'XOUC310'
defaultName = 'wght400'

sourcePath  = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamily}_{sourceName}.ufo')
defaultPath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamily}_{defaultName}.ufo')

assert os.path.exists(sourcePath)
assert os.path.exists(defaultPath)

sourceFont  = OpenFont(sourcePath, showInterface=False)
defaultFont = OpenFont(defaultPath, showInterface=False)

sparsifySource(sourceFont, defaultFont)

sourceFont.openInterface()

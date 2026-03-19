from importlib import reload
import xTools4.modules.glyphMemeProofer
reload(xTools4.modules.glyphMemeProofer)

import os
from xTools4.modules.glyphMemeProofer import GlyphMemeProofer

subFamilyName = ['Roman', 'Italic'][1]
baseFolder = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
proofsFolder =  os.path.join(baseFolder, 'Proofs', 'PDF', 'glyph-memes')

savePDF = True

assert os.path.exists(sourcesFolder)

designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.designspace')

glyphNames  = list('HOVTnov')
glyphNames += ['zero', 'one']

for glyphName in glyphNames:

    P = GlyphMemeProofer(glyphName, designspacePath)
    P.anchorsDraw = True 
    P.draw()

    pdfFileName = os.path.splitext(os.path.split(designspacePath)[-1])[0]

    if savePDF:
        P.save(proofsFolder, pdfFileName)

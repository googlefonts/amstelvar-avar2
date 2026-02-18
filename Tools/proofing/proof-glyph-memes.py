from importlib import reload
import xTools4.modules.glyphMemeProofer
reload(xTools4.modules.glyphMemeProofer)

import os
from xTools4.modules.glyphMemeProofer import GlyphMemeProofer

subFamilyName = ['Roman', 'Italic'][0]
baseFolder = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
proofsFolder =  os.path.join(baseFolder, 'Proofs', 'PDF', 'glyph-memes')

savePDF = True

assert os.path.exists(sourcesFolder)

designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_avar2.designspace')

for glyphName in 'nov':

    P = GlyphMemeProofer(glyphName, designspacePath)
    P.draw()

    pdfFileName = f'glyph-memes_{subFamilyName}'

    if savePDF:
        P.save(proofsFolder, pdfFileName)

    newDrawing()

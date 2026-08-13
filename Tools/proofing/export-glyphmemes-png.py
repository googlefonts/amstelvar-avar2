# drawBot

'''Export GlyphMeme images in PNG format for parameters documentation.'''

import os
from fontTools.ufoLib.glifLib import glyphNameToFileName

subFamily = ['Roman', 'Italic'][0]
folder = os.path.dirname(os.path.dirname(os.getcwd()))
proofsFolder = os.path.join(folder, 'Proofs', 'PDF', 'glyph-memes')
imgsFolder = '/Users/gferreira/fontbureau/designing-parametric-sources/imgs'

glyphName  = 'n'
pageNumber = 3
sourceName = 'XOPQmin'

glifName = os.path.splitext(glyphNameToFileName(glyphName, None))[0]
fileName = f'AmstelvarA2-{subFamily}_{glifName}.pdf'
pdfPath = os.path.join(proofsFolder, fileName)

assert os.path.exists(pdfPath)

w, h = imageSize(pdfPath)

size(w, h)
image(pdfPath, (0, 0), pageNumber=pageNumber)

imgName = f'AmstelvarA2-{subFamily}_{glifName}_{sourceName}.png'
imgPath = os.path.join(imgsFolder, imgName)

saveImage(imgPath, imageResolution=150)

print(imgPath, os.path.exists(imgPath))
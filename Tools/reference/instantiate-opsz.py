import os, shutil
from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont

subFamily = ['Roman', 'Italic'][1]

romanFontName  = 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf'
italicFontName = 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf'

# get Amstelvar1 from AmstelvarA2 folder
folder = os.getcwd()
ttfPath = os.path.join(os.path.dirname(folder), 'amstelvar-avar2', 'Proofs', romanFontName if subFamily == 'Roman' else italicFontName)

assert os.path.exists(ttfPath)

dstFolder = os.path.join(folder, subFamily)

varfont = TTFont(ttfPath)

for opsz in [24, 36, 84]:
    # instantiate TTF
    partial = instantiateVariableFont(varfont, dict(opsz=opsz))
    partialPath = ttfPath.replace('.ttf', f'_opsz{opsz}.ttf')
    partial.save(partialPath)
    # convert to UFO
    f = OpenFont(partialPath, showInterface=False)
    folder, fileName = os.path.split(partialPath)
    ufoPath = os.path.join(dstFolder, f'Amstelvar-{subFamily}_opsz{opsz}.ufo')
    if os.path.exists(ufoPath):
        shutil.rmtree(ufoPath)        
    print(f'saving {ufoPath}...')
    f.save(ufoPath)
    # clear temp TTF
    os.remove(partialPath)

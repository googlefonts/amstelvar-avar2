import os
from xTools4.modules.encoding import char2psname

subFamilyNames  = ['Roman', 'Italic']
folderAmstelvar = '/Users/gferreira/hipertipo/fonts/amstelvar'

opticalSizes = [
    'opsz8',
    'wght400',  # 14pt (default)
    'opsz24',
    'opsz36',
    'opsz84',
    'opsz144',
]

txt = 'HOE noez 017¥'
s = 0.05
x, y = 120, 800
lh = 1.25

for subFamilyName in subFamilyNames:
    sourcesFolder   = os.path.join(folderAmstelvar, subFamilyName)

    newPage()
    save()
    translate(x, y)
    scale(s)

    for opsz in opticalSizes:
        sourcePath = os.path.join(sourcesFolder, f'Amstelvar-{subFamilyName}_{opsz}.ufo')
        f = OpenFont(sourcePath, showInterface=False)
    
        save()
        with savedState():
            fontSize(240)
            fill(1, 0, 0)
            sz = 'opsz14' if opsz == 'wght400' else opsz
            text(f'{sz[4:]} pt', (x-1600, y))
        for char in txt:
            glyphName = char2psname(char)
            glyph = f[glyphName]
            drawGlyph(glyph)
            translate(glyph.width, 0)
        restore()
        
        translate(0, -f.info.unitsPerEm*lh)

    restore()

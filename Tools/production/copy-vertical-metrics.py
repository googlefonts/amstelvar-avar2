from controller import AmstelvarA2Controller

folder = '/Users/gferreira/fontbureau/amstelvar-avar2'

subFamily = ['Roman', 'Italic'][1]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

attrs = ['unitsPerEm', 'capHeight', 'xHeight', 'ascender', 'descender']

preflight = False

# get default vmetrics
vMetrics = { attr: getattr(p.defaultFont.info, attr) for attr in attrs }

sourcesPaths  = p.sourcesPaths
sourcesPaths += p.tuningSourcesPaths

for ufoPath in sourcesPaths:
    if ufoPath == p.defaultSourcePath:
        continue
    f = OpenFont(ufoPath, showInterface=False)
    print(f'copying vertical metrics to {f.info.styleName}...')
    print('\tcopying unitsPerEm...')
    f.info.unitsPerEm = vMetrics['unitsPerEm']
    if 'YTLC' not in f.info.styleName:
        print('\tcopying xHeight...')
        f.info.xHeight = vMetrics['xHeight'] 
    if 'YTUC' not in f.info.styleName:
        print('\tcopying capHeight...')
        f.info.capHeight = vMetrics['capHeight'] 
    if 'YTAS' not in f.info.styleName:
        print('\tcopying ascender...')
        f.info.ascender = vMetrics['ascender'] 
    if 'YTDE' not in f.info.styleName:
        print('\tcopying descender...')
        f.info.descender = vMetrics['descender'] 
    if not preflight:
        print('\tsaving...')
        f.save()
    f.close()
    print()

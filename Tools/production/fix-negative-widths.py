import os, glob

subFamily     = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamily, 'tuning')

sources = glob.glob(f'{sourcesFolder}/*.ufo')

for source in sources:
    f = OpenFont(source, showInterface=False)
    for g in f:
        if g.width < 0:
            print(f.info.styleName, g.name, g.width)
            g.width = 0
    f.close(save=True)

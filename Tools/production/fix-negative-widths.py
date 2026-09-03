import os, glob

sourcesFolder = '/Users/gferreira/fontbureau/amstelvar-avar2/Sources/Roman/tuning'

sources = glob.glob(f'{sourcesFolder}/*.ufo')

for source in sources:
    f = OpenFont(source, showInterface=False)
    for g in f:
        if g.width < 0:
            print(f.info.styleName, g.name, g.width)
            g.width = 0
    f.save()
    f.close()

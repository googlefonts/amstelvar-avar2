# menuTitle: rename Italic wght900 to wght1000

import os, glob, shutil

baseFolder       = os.getcwd()
sourcesFolder    = os.path.join(baseFolder, 'Italic')

sources = glob.glob(f'{sourcesFolder}/*.ufo')

for src in sources:
    if 'wght900' in src:
        srcNew = src.replace('wght900', 'wght1000')
        shutil.move(src, srcNew)
        print('old:', src)
        print('new:', srcNew)
        print()

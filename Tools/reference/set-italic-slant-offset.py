# menuTitle: set italic slant offset in all italic sources

import os, glob, shutil

subfamilyName  = ['Roman', 'Italic'][1]
slantOffset    = -144

baseFolder1    = os.getcwd()
sourcesFolder1 = os.path.join(baseFolder1, subfamilyName)

baseFolder2    = os.path.join(os.path.dirname(baseFolder1), 'amstelvar-avar2')
sourcesFolder2 = os.path.join(baseFolder2, 'Sources', subfamilyName)

for i, sourcesFolder in enumerate([sourcesFolder1, sourcesFolder2]):
    familyName = 'AmstelvarA2' if i else 'Amstelvar'
    print(f'setting italic slant offset ({slantOffset}) in {familyName} sources:')
    sources = glob.glob(f'{sourcesFolder}/*.ufo')
    for sourcePath in sources:
        f = OpenFont(sourcePath, showInterface=False)
        before = f.lib.get('com.typemytype.robofont.italicSlantOffset')
        f.lib['com.typemytype.robofont.italicSlantOffset'] = slantOffset
        print(f'\tsetting offset in {os.path.split(sourcePath)[-1]}... ({before} -> {slantOffset})')
        f.save()
        f.close()
    print(f'...done.\n')

import os
from controller import AmstelvarA2Controller
from xTools4.modules.fontutils import swapGlyphs
from xTools4.modules.glyphutils import centerGlyph

folder = os.path.dirname(os.getcwd())

p = AmstelvarA2Controller(folder, 'AmstelvarA2', 'Roman')

cases = ['lowercase', 'uppercase']

ignoreGlyphs = ['firsttonechinese', 'periodcentered.loclCAT']

for ufoPath in p.referenceSourcesPaths.values():

    f = OpenFont(ufoPath, showInterface=False)

    for case in cases:
        spacingAccents = p.smartSets[case]['accents spacing']
        combiningAccents = p.smartSets[case]['accents comb']

        # 1. convert combining accents to contours, make zero-width, align center
        for glyphName in combiningAccents:
            if glyphName not in f:
                f.newGlyph(glyphName)

            g = f[glyphName]
            g.decompose()

            deltaX = 0
            for a in g.anchors:
                if a.name == '_top':
                    deltaX = a.x
                elif a.name == '_bottom':
                    deltaX = a.x

            f[glyphName].width = 0

            if deltaX:
                g.moveBy((-deltaX, 0))
            else:
                centerGlyph(f[glyphName])

        # 2. rebuild spacing accents with components, align center
        for glyphName in spacingAccents:
            if glyphName in ignoreGlyphs:
                continue

            if case == 'lowercase':
                glyphNameComb = f'{glyphName}comb'
            else:
                glyphNameComb = f"{glyphName.replace('.case', '')}comb.case"

            if glyphName not in f:
                f.newGlyph(glyphName)
                f[glyphName].width = 1024

            f[glyphName].clear()
            f[glyphName].appendComponent(glyphNameComb)
            centerGlyph(f[glyphName])

    f.close(save=True)

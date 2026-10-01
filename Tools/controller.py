# menuTitle: AmstelvarA2 Controller

from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, glob, time, json, string
from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, AxisMappingDescriptor, RuleDescriptor
from xTools4.modules.xproject import xProject
from xTools4.modules.measurements import setSourceNamesFromMeasurements, readMeasurements, extractMeasurements, permille
from xTools4.modules.sys import timer
from xTools4.modules.fontutils import parseGString


_parametricAxesRoman  = 'WDSP GRAD '

                        # XOPQ/YOPQ          # XTRA              # YTRA         # serifs                 # spacing
_parametricAxesRoman += 'XOUC YOUC XOUA YOUA XTUC XTUR XTUD XTUA YTUC YTJD      XSHU YSHU XSVU YSVU XVAU XUCS XUCR XUCD ' # uppercase
_parametricAxesRoman += 'XOLC YOLC XOLA YOLA XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL      XLCS XLCR XLCD ' # lowercase
_parametricAxesRoman += 'XOFI YOFI           XTFI                YTFI           XSHF YSHF XSVF YSVF      XFIR           ' # figures
_parametricAxesRoman += 'XOET YOET           XTET                                                        XETS           ' # etcetera  # XSHE YSHE XSVE YSVE ??

_parametricAxesRoman += 'XDOT YTOS XTTW YTTL' # BARS
_parametricAxesRoman  = _parametricAxesRoman.split()

_parametricAxesItalic = _parametricAxesRoman


class AmstelvarA2Controller(xProject):

    _parametricAxes = {
        'Roman'  : _parametricAxesRoman,
        'Italic' : _parametricAxesItalic,
    }

    # parametric axes with arbitrary scales
    _customParametricAxes = {
        'GRAD' : 0,
    }

    _blendedAxesMappings = {
        'opsz' : {
            (   8.0,   8.0 ),
            (  14.0,  14.0 ),
            (  36.0,  64.0 ),
            (  84.0, 123.0 ),
            ( 144.0, 144.0 ),
        }
    }

    _spacingAxes = [
        'XUCS', 'XUCR', 'XUCD',
        'XLCS', 'XLCR', 'XLCD',
        'XFIR',
    ]

    _parentParametricAxesRoman  = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA'.split()
    _parentParametricAxesItalic = _parentParametricAxesRoman

    _parentParametricAxesDefaults = {
        'XOPQ' : 'XOUC',
        'YOPQ' : 'YOUC',
        'XTRA' : 'XTUC',
        'XSHA' : 'XSHU',
        'YSHA' : 'YSHU',
        'XSVA' : 'XSVU',
        'YSVA' : 'YSVU',
        'XVAA' : 'XVAU',
        'YHAA' : 'YHAU',
    }
    _parentParametricHidden = False

    _substitutionRules = {
        "bars" : [
            # condition sets
            [
                [
                    dict(name="wght", minimum=750, maximum=1000),
                ],
                [
                    dict(name="wdth", minimum=50, maximum=75)
                ],
            ],
            # substitutions
            [
                ( "Q",           "Q.rvrn" ),
                ( "Oslash",      "Oslash.rvrn" ),
                ( "Oslashacute", "Oslashacute.rvrn" ),
                ( "oslash",      "oslash.rvrn" ),
                ( "oslashacute", "oslashacute.rvrn" ),
                ( "dollar",      "dollar.rvrn" ),
                ( "cent",        "cent.rvrn" ),
                ( "naira",       "naira.rvrn" ),
                ( "won",         "won.rvrn" ),
                ( "kip",         "kip.rvrn" ),
                ( "peso",        "peso.rvrn" ),
                ( "cedi",        "cedi.rvrn" ),
                ( "colonsign",   "colonsign.rvrn" ),
                ( "guarani",     "guarani.rvrn" ),
            ],
        ],
    }

    tuning = True

    def __init__(self, folder, familyName, subFamily):
        self.baseFolder = folder
        self.familyName = familyName
        self.subFamily  = subFamily

    @property
    def designspaceFile(self):
        return f"{self.familyName.replace(' ', '')}-{self.subFamily.replace(' ', '')}.designspace"

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, self.sourcesFolderName, self.subFamily)

    @property
    def defaultSourcePath(self):
        return os.path.join(self.sourcesFolder, f"{self.familyName.replace(' ', '')}-{self.subFamily.replace(' ', '')}_{self.defaultName}.ufo")

    @property
    def varFontFile(self):
        return self.designspaceFile.replace('.designspace', '_avar2.ttf')

    @property
    def parametricAxes(self):
        return self._parametricAxes[self.subFamily]

    @property
    def parentParametricAxes(self):
        return self._parentParametricAxesRoman if self.subFamily == 'Roman' else self._parentParametricAxesItalic

    @property
    def defaultLocation(self):
        location = super().defaultLocation.copy()
        # add custom parametric axes (not based on measurement)
        for tag in ['GRAD']:
            axisName = self.getAxisName(tag)
            location[axisName] = 0
        return location

    @property
    def referenceFontName(self):
        return f'Amstelvar-{self.subFamily}.ttf'

    @property
    def referenceFontPath(self):
        return os.path.join(self.fontsFolder, 'reference', self.referenceFontName)

    @property
    def referenceMeasurementsPath(self):
        # reference sources are now compatible with parametric sources
        return self.measurementsPath

    def setSourceNamesFromMeasurements(self, preflight=True, ignoreTags=['wght', 'GRAD']):
        setSourceNamesFromMeasurements(
                self.sourcesFolder,
                f'{self.familyName} {self.subFamily}',
                self.measurementsPath,
                preflight=preflight,
                ignoreTags=ignoreTags,
                infoFamilyName=f'{self.familyName} {self.subFamily}',
        )

    def updateGlyphsFromDefault(self, glyphNames, oldDefaultName, preflight=True, parametric=True, tuning=True):
        oldDefaultPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamily}_{oldDefaultName}.ufo')
        super().updateGlyphsFromDefault(glyphNames, oldDefaultPath, preflight=preflight, parametric=parametric, tuning=tuning)

    def extractMeasurements(self):

        # maybe this needs to be defined somewhere else
        axes = {
            "opsz" : {
              "name"    : "Optical size",
              "default" : 14,
              "minimum" : 8,
              "maximum" : 144,
            },
            "wght" : {
              "name"    : "Weight",
              "default" : 400,
              "minimum" : 100,
              "maximum" : 1000,
            },
            "wdth": {
              "name"    : "Width",
              "default" : 100,
              "minimum" : 50,
              "maximum" : 125,
            }
        }

        # ignore GRAD sources
        referenceSources = [ufoPath for ufoPath in self.referenceSourcesPaths.values() if 'GRAD' not in os.path.split(ufoPath)[-1]]

        parametricAxes = [a for a in self.parametricAxes if a not in self._customParametricAxes]

        sources = extractMeasurements(referenceSources, self.referenceMeasurementsPath, parametricAxes)

        # save measurements to reference blends file
        blendsDict = {
            'axes'    : axes,
            'sources' : sources,
        }

        print(f'saving blended axes and measurements to {self.subFamily}/reference/blends.json...', end=' ')

        referenceBlendsPath = os.path.join(self.referenceSourcesFolder, self.blendsFile)

        with open(referenceBlendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

        print(f'({os.path.exists(referenceBlendsPath)})\n')

    def addParametricSources(self):
        super().addParametricSources(familyName=f'{self.familyName} {self.subFamily}')

    def addDefaultSource(self):
        super().addDefaultSource(familyName=f'{self.familyName} {self.subFamily}')

    def addBlendedAxes(self):
        super().addBlendedAxes()
        for axis in self.designspace.axes:
            if axis.tag in self._blendedAxesMappings:
                axis.map = self._blendedAxesMappings[axis.tag]
            # hide parent parametric axes
            if self._parentParametricHidden and axis.tag in self.parentParametricAxes:
                axis.hidden = True

    def addTuningSources(self):
        super().addTuningSources(familyName=f'{self.familyName} {self.subFamily}')

    def addInstances(self):
        super().addInstances(familyName=f'{self.familyName} {self.subFamily}')

    def addSubstitutionRules(self):
        for ruleName, rule in self._substitutionRules.items():
            conditionSets, substitutions = rule
            R = RuleDescriptor()
            R.name = ruleName
            for conditionSet in conditionSets:
                _conditionSet = []
                for condition in conditionSet:
                    condition['name'] = self.getAxisName(condition['name'])
                    _conditionSet.append(condition)
                R.conditionSets.append(_conditionSet)
            for substitution in substitutions:
                R.subs.append(substitution)
            self.designspace.addRule(R)

    def buildBlendsFile(self, parentParametric=True):
        if not os.path.exists(self.referenceBlendsPath):
            return

        with open(self.referenceBlendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        if self.verbose:
            print('\tbuilding blends file...')

        # add parent spacing axis
        blendsDict['axes']['XTSP'] = {
            "name"    : "Spacing",
            "default" : 0,
            "minimum" : -100,
            "maximum" : 100,
        }
        blendsDict['sources']['XTSP-100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP100']  = self.defaultLocation.copy()

        ### REMOVE GRAD FROM BLENDS -- THIS IS A HACK !
        axisName = self.getAxisName('GRAD')
        for srcName in ['XTSP-100', 'XTSP100']:
            del blendsDict['sources'][srcName][axisName]

        if self.tuning:
            # add tuning axes to blended locations
            for styleName in blendsDict['sources']:
                if styleName == 'wght400':
                    continue
                for tuningStyle, tuningAxis in self.tuningAxes.items():
                    tuningValue = tuningAxis.maximum if styleName == tuningStyle else tuningAxis.default
                    # print(f'\t\tadding tuning blend: {styleName} {tuningAxis.tag} {tuningValue}...')
                    tuningAxisName = tuningStyle if self.useLongAxisNames else tuningAxis.tag
                    blendsDict['sources'][styleName][tuningAxisName] = tuningValue

        for axisName in self._spacingAxes:
            values = []
            for ufo in self.sourcesPaths:
                value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                if axisName in ufo:
                    values.append(value)
            assert len(values)
            values.sort()
            blendsDict['sources']['XTSP-100'][axisName] = values[0]
            blendsDict['sources']['XTSP100'][axisName]  = values[1]

        # add parent parametric axes

        if parentParametric:

            measurements = readMeasurements(self.measurementsPath)
            fontMeasurements = measurements['font']

            parametricAxesDict = self.getParametricAxesFromSourceNames()

            for parentAxisTag in self.parentParametricAxes:
                parentMeasurement = fontMeasurements[parentAxisTag]

                # get parametric axes for parent
                parametricAxes = {}
                childTags = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisTag]

                for childTag in childTags:
                    childName = self.getAxisName(childTag)
                    if childName not in self.defaultLocation:
                        print(f'no parameter {childTag} in default location, skipping...')
                        continue

                    # get min/max values from file names
                    values = []
                    for ufo in self.sourcesPaths:
                        if childTag in ufo:
                            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                            values.append(value)
                    if not len(values) == 2:
                        if self.verbose:
                            print(f'\t\tskipping child axis {childTag} ({parentAxisTag}) {values}...')
                        continue
                    values.sort()

                    parametricAxes[childName] = {
                        'minimum' : values[0],
                        'maximum' : values[1],
                        'default' : self.defaultLocation[childName],
                    }

                parentDefault = self._parentParametricAxesDefaults[parentAxisTag]
                parentAxis, mappings = self.makeParentParametricAxis(parentAxisTag, parametricAxes, parentDefault)

                # clip mapping values to the available parametric ranges
                mappingsClipped = {}
                for parentValue in mappings.keys():
                    mappingsClipped[parentValue] = {}
                    for axisName, value in mappings[parentValue].items():
                        # get tag from axis name
                        if self.useLongAxisNames:
                            tag = [key for key in fontMeasurements.keys() if axisName == fontMeasurements[key]['description']][0]
                        else:
                            tag = axisName

                        if value < parametricAxesDict[tag]['minimum']:
                            clippedValue = parametricAxesDict[tag]['minimum']
                        elif value > parametricAxesDict[tag]['maximum']:
                            clippedValue = parametricAxesDict[tag]['maximum']
                        else:
                            clippedValue = value
                        mappingsClipped[parentValue][tag] = clippedValue
                mappings = mappingsClipped

                # add parent axis
                blendsDict['axes'][parentAxisTag] = parentAxis

                # add parametric mappings
                for mappingValue in mappings:
                    blendsDict['sources'][f'{parentAxisTag}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappings[mappingValue].items():
                        blendsDict['sources'][f'{parentAxisTag}{mappingValue}'][parametricAxisName] = parametricValue

        # done!

        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def buildDesignspace(self, instances=False, parentParametric=False, substitutionRules=True):

        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.buildBlendsFile(parentParametric=parentParametric)

        self.designspace = DesignSpaceDocument()

        self.addBlendedAxes()
        self.addParametricAxes(self._customParametricAxes)

        if self.tuning:
            self.addTuningAxes()

        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()

        if self.tuning:
            self.addTuningSources()

        if instances:
            self.addInstances()

        if substitutionRules:
            self.addSubstitutionRules()

        self.addCustomKeysToLib()

        # HACK: change GRAD axis visibility and order
        gradeAxis = [axis for axis in self.designspace.axes if axis.tag == 'GRAD'][0]
        gradeAxis.hidden = False
        sortedAxes = []
        for i, axis in enumerate(self.designspace.axes):
            if axis.tag == 'GRAD':
                continue
            if i == 3:
                sortedAxes.append(gradeAxis)
            sortedAxes.append(axis)
        self.designspace.axes = sortedAxes

        self.save()

    def proofSourcesGlyphSet(self, showCompatible=True, validateComposites=True):
        familyName = f'{self.familyName} {self.subFamily}'
        proofsFolder = os.path.join(self.proofsFolder, 'PDF', 'glyphset', self.subFamily)
        super().proofSourcesGlyphSet(familyName=familyName, showCompatible=showCompatible, validateComposites=validateComposites, proofsFolder=proofsFolder)

    def proofBlends(self, glyphNames, margins=True, labels=True, levels=False, levelsShow=[1, 2, 3, 4], header=True, footer=True, points=False):
        proofsFolder = os.path.join(self.proofsFolder, 'PDF', 'blending', self.subFamily)
        if self.tuning:
            proofsFolder = os.path.join(proofsFolder, 'tuned')
        super().proofBlends(glyphNames, margins=margins, labels=labels, levels=levels, levelsShow=levelsShow, header=header, footer=footer, points=points, proofsFolder=proofsFolder)

    def proofGlyphMemes(self, glyphNames, anchors=True):
        proofsFolder = os.path.join(self.proofsFolder, 'PDF', 'glyph-memes', self.subFamily)
        super().proofGlyphMemes(glyphNames, anchors=anchors, proofsFolder=proofsFolder)

    def proofTuning(self, glyphNames, referenceSource, levels=[2, 3, 4]):
        proofsFolder = os.path.join(self.proofsFolder, 'PDF', 'tuning', self.subFamily)
        super().proofTuning(glyphNames, referenceSource, levels=levels, proofsFolder=proofsFolder)


if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman', 'Italic'][1]

    start = time.time()

    p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

    # glyphNames = ['eight.tab']
    # glyphNames = p.defaultFont.glyphOrder
    # glyphNames = 'Acircumflexgrave Ecircumflexgrave Ocircumflexgrave acircumflexgrave ecircumflexgrave ocircumflexgrave'.split()
    # glyphNames = parseGString(p.defaultFont, '/ae/OE')
    # glyphNames = p.smartSets['figures']['tabular']
    # glyphNames = p.smartSets['lowercase']['cyrillic'] # + p.smartSets['lowercase']['cyrillic']
    # glyphNames = [g for g in glyphNames if g not in p.smartSets['Latin 1']]
    # glyphNames = [f'{g}.rvrn' for g in p.smartSets['BARS']]
    # glyphNames.remove('figuredash')
    # print(glyphNames)

    # --- managing sources ---
    # p.createParametricSources(['XVAU'], minSource=True, maxSource=True)
    # p.setSourceNamesFromMeasurements(preflight=True)
    # for src, dst in [('XOLC', 'XOET'), ('YOLC', 'YOET'), ('XTLC', 'XTET'), ('XLCS', 'XETS')]:
    #     p.splitSources(src, dst, glyphNames, preflight=False)

    # --- copy from default ---
    # p.updateGlyphsFromDefault(glyphNames, 'WDSP0', preflight=False, parametric=True, tuning=False)
    # p.copyGlyphsFromDefault(list('ij'), parametric=False, tuning=True)
    # p.copyGroupsFromDefault()
    # p.copyUnicodesFromDefault(preflight=False, parametric=True, tuning=True, reference=True)
    # p.copyGlyphOrderFromDefault(parametric=True, tuning=True, reference=True, preflight=False, trim=False)
    # p.copyKerningFromDefault()

    # --- building glyphs ---
    # p.buildCompositeGlyphs(glyphNames, parametric=True, tuning=False, reference=True, preflight=False)

    # --- measuring ---
    # p.extractMeasurements()

    # --- build designspace ---
    # p.parametricAxesHidden = True
    # p.tuningAxesHidden = True
    # p.tuning = True # also used to direct BlendsPreview proof to its folder
    # p.useLongAxisNames = True # keep it disabled during development!
    # p.buildDesignspace(instances=True, parentParametric=True, substitutionRules=True)
    # p.validateDesignspace(locx    ations=True, mappings=True, instances=False)
    # p.validateSources(parametric=False, tuning=False, reference=True)

    # --- tuning ---
    # p.tuningLevels = [1, 2, 3]
    # p.createTuningSources(sparse=False)
    # p.resetTuningSources()
    # p.calculateTuningSources(glyphNames, levels=[1,2,3], tuneBaseGlyphs=True)

    # --- normalization ---
    # p.roundSources(parametric=True, tuning=True, reference=True)
    # p.cleanupSources(parametric=True, tuning=True, reference=True)
    p.normalizeSources(parametric=True, tuning=True, reference=True)

    # --- project info ---
    # p.printSettings()
    # p.printAxes()
    # print(p.defaultLocation)

    # --- proofing ---
    # p.proofGlyphMemes(glyphNames, anchors=True)
    # p.proofBlends(glyphNames, margins=True, labels=True, levels=False, levelsShow=[1,2,3,4], header=True, footer=True, points=False)
    # p.proofTuning(glyphNames, referenceSource, levels=[1,2,3])
    # p.proofSourcesGlyphSet(showCompatible=False, validateComposites=True)

    # --- build fonts ---
    # p.buildVariableFont(debug=False, featureWriter=False, noGDEF=False, subset=None)
    # p.buildInstancesVariableFont(clear=True, ufo=True)

    end = time.time()
    timer(start, end)
 
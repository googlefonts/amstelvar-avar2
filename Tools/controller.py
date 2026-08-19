# menuTitle: AmstelvarA2 Controller

from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, glob, time, json, string, itertools
from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, AxisMappingDescriptor
from xTools4.modules.xproject import xProject, makeParentAxis
from xTools4.modules.measurements import setSourceNamesFromMeasurements, readMeasurements, extractMeasurements, permille
from xTools4.modules.sys import timer
from xTools4.modules.fontutils import parseGString


_parametricAxesRoman  = 'WDSP GRAD '

                        # XOPQ/YOPQ          # XTRA              # YTRA         # serifs                 # EQ      # XTSP
_parametricAxesRoman += 'XOUC YOUC XOUA YOUA XTUC XTUR XTUD XTUA YTUC YTJD      XSHU YSHU XSVU YSVU XVAU XQUC YQUC XUCS XUCR XUCD ' # uppercase
_parametricAxesRoman += 'XOLC YOLC XOLA YOLA XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL      XQLC YQLC XLCS XLCR XLCD ' # lowercase
_parametricAxesRoman += 'XOFI YOFI           XTFI                YTFI           XSHF YSHF XSVF YSVF      XQFI YQFI XFIR           ' # figures
_parametricAxesRoman += 'XOET YOET           XTET                                                                  XETS           ' # etcetera

_parametricAxesRoman += 'XDOT YTOS XTTW YTTL BARS'
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
        'XTEQ' : 'XQUC',
        'YTEQ' : 'YQUC',
    }
    _parentParametricHidden = False

    _matchRangeAxes = {
        'XQUC' : 'XTUR',
        'XQLC' : 'XTLR',
        'XQFI' : 'XTFI',
    }

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
        location['GRAD'] = 0

        # TO-DO: move the sorting code below to a separate, reusable method

        # sort parameters based on list of parametric axes
        locationSorted = {}
        for parameterName in self.parametricAxes:
            locationSorted[parameterName] = location[parameterName]
        for key, value in location.items():
            if key not in locationSorted:
                locationSorted[key] = value

        return locationSorted

    @property
    def referenceFontName(self):
        return 'Amstelvar-Roman.ttf'

    @property
    def referenceFontPath(self):
        return os.path.join(self.fontsFolder, 'reference', self.referenceFontName)

    def setSourceNamesFromMeasurements(self, preflight=True, ignoreTags=['wght', 'GRAD']):
        setSourceNamesFromMeasurements(
                self.sourcesFolder,
                f'{self.familyName} {self.subFamily}',
                self.measurementsPath,
                preflight=preflight,
                ignoreTags=ignoreTags,
                infoFamilyName=f'{self.familyName} {self.subFamily}',
        )

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

        ### THIS IS A HACK !
        del blendsDict['sources']['XTSP-100']['GRAD']
        del blendsDict['sources']['XTSP100']['GRAD']

        if self.tuning:
            # add tuning axes to blended locations
            for styleName in blendsDict['sources']:
                for tuningStyle, tuningAxis in self.tuningAxes.items():
                    tuningValue = tuningAxis.maximum if styleName == tuningStyle else tuningAxis.default
                    # print(f'\t\tadding tuning blend: {styleName} {tuningAxis.tag} {tuningValue}...')
                    blendsDict['sources'][styleName][tuningAxis.tag] = tuningValue

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

            for parentAxisName in self.parentParametricAxes:
                parentMeasurement = fontMeasurements[parentAxisName]

                # get parametric axes for parent
                parametricAxes = {}
                childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisName]
                for childName in childNames:
                    # get min/max values from file names
                    values = []
                    for ufo in self.sourcesPaths:
                        if childName in ufo:
                            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                            values.append(value)
                    if not len(values) == 2:
                        if self.verbose:
                            print(f'\t\tskipping child axis {childName} ({parentAxisName}) {values}...')
                        continue
                    values.sort()

                    parametricAxes[childName] = {
                        'minimum' : values[0],
                        'maximum' : values[1],
                        'default' : self.defaultLocation[childName],
                    }

                parentDefault = self._parentParametricAxesDefaults[parentAxisName]
                parentAxis, mappings = makeParentAxis(parentAxisName, parametricAxes, parentDefault, self._matchRangeAxes)

                # clip mapping values to the available parametric ranges
                mappingsClipped = {}
                for parentValue in mappings.keys():
                    mappingsClipped[parentValue] = {}
                    for tag, value in mappings[parentValue].items():
                        if value < parametricAxesDict[tag]['minimum']:
                            clippedValue = parametricAxesDict[tag]['minimum']
                        elif value > parametricAxesDict[tag]['maximum']:
                            clippedValue = parametricAxesDict[tag]['maximum']
                        else:
                            clippedValue = value
                        mappingsClipped[parentValue][tag] = clippedValue

                # add parent axis
                blendsDict['axes'][parentAxisName] = parentAxis

                # add parametric mappings
                for mappingValue in mappingsClipped:
                    blendsDict['sources'][f'{parentAxisName}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappingsClipped[mappingValue].items():
                        blendsDict['sources'][f'{parentAxisName}{mappingValue}'][parametricAxisName] = parametricValue

        # done!

        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def patchBlendsFile(self):

        # import blends data
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # import & apply patch data
        patchPath = self.blendsPath.replace('.json', '_patch.json')
        with open(patchPath, 'r', encoding='utf-8') as f:
            patchDict = json.load(f)

        if self.verbose:
            print('\tpatching blends file...')

        for key1, value1 in patchDict.items():
            if key1 not in blendsDict:
                print(f'{key1} not in blends dict')
                continue
            for key2, value2 in value1.items():
                for k, v in value2.items():
                    blendsDict[key1][key2][k] = v

        # save patched blends data
        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def buildDesignspace(self, patchBlends=True, instances=False, parentParametric=False):

        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.buildBlendsFile(parentParametric=parentParametric)
        if patchBlends:
            self.patchBlendsFile()

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

        self.addCustomKeysToLib()

        self.save()

    def proofSourcesGlyphSet(self, showCompatible=True, validateComposites=True):
        familyName = f'{self.familyName} {self.subFamily}'
        super().proofSourcesGlyphSet(familyName=familyName, showCompatible=showCompatible, validateComposites=validateComposites)

    def proofBlends(self, glyphNames, margins=True, labels=True, levels=False, levelsShow=[1, 2, 3, 4], header=True, footer=True, points=False):
        super().proofBlends(glyphNames, familyName=self.subFamily, margins=margins, labels=labels, levels=levels, levelsShow=levelsShow, header=header, footer=footer, points=points)

    def updateGlyphsFromDefault(self, glyphNames, oldDefaultName, preflight=True, parametric=True, tuning=True):
        oldDefaultPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamily}_{oldDefaultName}.ufo')
        super().updateGlyphsFromDefault(glyphNames, oldDefaultPath, preflight=preflight, parametric=parametric, tuning=tuning)

    def proofGlyphMemes(self, glyphNames, anchors=True):
        proofsFolder = os.path.join(self.proofsFolder, 'PDF', 'glyph-memes', self.subFamily)
        super().proofGlyphMemes(glyphNames, anchors=anchors, proofsFolder=proofsFolder)


class AmstelvarA2Controller2(AmstelvarA2Controller):

    '''
    Alternative implementation of the AmstelvarA2 designspace.

    - insert reference sources directly into parametric space
    - no tuning axes or tuning sources needed
    - keep mappings for blended sources
    
    '''

    @property
    def defaultLocation(self):
        '''Returns the parametric location of the default source.'''
        if not self.measurementsDefault:
            return

        # get parametric measurements
        location = {}
        for name in self.parametricAxes:
            if name in self.measurementsDefault.values:
                location[name] = permille(self.measurementsDefault.values[name], self.defaultFont.info.unitsPerEm)

        location['GRAD'] = 0

        # sort parameters based on list of parametric axes
        locationSorted = {}
        for parameterName in self.parametricAxes:
            locationSorted[parameterName] = location[parameterName]
        for key, value in location.items():
            if key not in locationSorted:
                locationSorted[key] = value

        return locationSorted

    @property
    def designspaceFile(self):
        return f"{self.familyName.replace(' ', '')}-{self.subFamily.replace(' ', '')}_v2.designspace"

    def addReferenceSources(self, familyName=None):
        '''Add reference sources to the designspace.'''

        if self.verbose:
            print('\tadding reference sources...')

        referenceSources = { '_'.join(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[1:]) : ufoPath for ufoPath in self.referenceSourcesPaths.values() if 'GRAD' not in os.path.split(ufoPath)[-1] }

        for styleName in referenceSources.keys():
            parameters = self.blendedSources.get(styleName)

            if styleName == self.defaultName:
                print(f'skipping {styleName}...')
                continue

            src = SourceDescriptor()
            src.path = referenceSources[styleName]
            src.familyName = self.familyName if not familyName else familyName
            src.styleName = src.name = styleName
            L = parameters

            src.location = L
            self.designspace.addSource(src)

    def addBlendedSources(self):
        '''Add blended sources (mappings) to the designspace.'''

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        if self.verbose:
            print('\tadding blend mappings...')

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag = param[:4]

                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation
            m.description    = styleName

            self.designspace.addAxisMapping(m)

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

        ### THIS IS A HACK !
        del blendsDict['sources']['XTSP-100']['GRAD']
        del blendsDict['sources']['XTSP100']['GRAD']

        # if self.tuning:
        #     # add tuning axes to blended locations
        #     for styleName in blendsDict['sources']:
        #         for tuningStyle, tuningAxis in self.tuningAxes.items():
        #             tuningValue = tuningAxis.maximum if styleName == tuningStyle else tuningAxis.default
        #             # print(f'\t\tadding tuning blend: {styleName} {tuningAxis.tag} {tuningValue}...')
        #             blendsDict['sources'][styleName][tuningAxis.tag] = tuningValue

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

            for parentAxisName in self.parentParametricAxes:
                parentMeasurement = fontMeasurements[parentAxisName]

                # get parametric axes for parent
                parametricAxes = {}
                childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisName]
                for childName in childNames:
                    # get min/max values from file names
                    values = []
                    for ufo in self.sourcesPaths:
                        if childName in ufo:
                            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                            values.append(value)
                    if not len(values) == 2:
                        if self.verbose:
                            print(f'\t\tskipping child axis {childName} ({parentAxisName}) {values}...')
                        continue
                    values.sort()

                    parametricAxes[childName] = {
                        'minimum' : values[0],
                        'maximum' : values[1],
                        'default' : self.defaultLocation[childName],
                    }

                parentDefault = self._parentParametricAxesDefaults[parentAxisName]
                parentAxis, mappings = makeParentAxis(parentAxisName, parametricAxes, parentDefault, self._matchRangeAxes)

                # clip mapping values to the available parametric ranges
                mappingsClipped = {}
                for parentValue in mappings.keys():
                    mappingsClipped[parentValue] = {}
                    for tag, value in mappings[parentValue].items():
                        if value < parametricAxesDict[tag]['minimum']:
                            clippedValue = parametricAxesDict[tag]['minimum']
                        elif value > parametricAxesDict[tag]['maximum']:
                            clippedValue = parametricAxesDict[tag]['maximum']
                        else:
                            clippedValue = value
                        mappingsClipped[parentValue][tag] = clippedValue

                # add parent axis
                blendsDict['axes'][parentAxisName] = parentAxis

                # add parametric mappings
                for mappingValue in mappingsClipped:
                    blendsDict['sources'][f'{parentAxisName}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappingsClipped[mappingValue].items():
                        blendsDict['sources'][f'{parentAxisName}{mappingValue}'][parametricAxisName] = parametricValue

        # done!

        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def buildDesignspace(self, patchBlends=True, instances=False, parentParametric=False):

        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.buildBlendsFile(parentParametric=parentParametric)
        if patchBlends:
            self.patchBlendsFile()

        self.designspace = DesignSpaceDocument()

        self.addBlendedAxes()
        self.addParametricAxes(self._customParametricAxes)

        # if self.tuning:
        #     self.addTuningAxes()

        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()

        if self.tuning:
            self.addReferenceSources()

        if instances:
            self.addInstances()

        self.addCustomKeysToLib()

        self.save()




if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman', 'Italic'][0]

    start = time.time()

    controller = [AmstelvarA2Controller, AmstelvarA2Controller2][0]

    p = controller(folder, 'AmstelvarA2', subFamily)

    referenceSource = os.path.join(p.referenceSourcesFolder, f'Amstelvar-{subFamily}_wght400.ufo')

    # glyphNamesEtcetera = list(set(itertools.chain(*[items for items in p.smartSets['etcetera'].values()])))
    # glyphNamesPunctuation = 'period exclam comma colon semicolon question'.split()

    # --- managing sources ---
    # p.createParametricSources(['XVAU'], minSource=True, maxSource=True)
    # p.setSourceNamesFromMeasurements(preflight=True)
    # for src, dst in [('XOLC', 'XOET'), ('YOLC', 'YOET'), ('XTLC', 'XTET'), ('XLCS', 'XETS')]:
    #     p.splitSources(src, dst, glyphNamesEtcetera, preflight=False)

    # --- copy from default ---
    # p.updateGlyphsFromDefault(['dollar'], 'WDSP1000', preflight=False, parametric=True, tuning=True)
    # p.copyGlyphsFromDefault(list('ij'), parametric=False, tuning=True)
    # p.copyGroupsFromDefault()
    # p.copyUnicodesFromDefault(preflight=False, parametric=True, tuning=True, reference=True)
    # p.copyGlyphOrderFromDefault()
    # p.copyKerningFromDefault()

    # --- building glyphs ---
    # p.buildCompositeGlyphs('i j'.split(), preflight=False)

    # --- measuring ---
    # p.extractMeasurements()

    # --- tuning ---
    # p.tuningLevels = [1, 2, 3]
    # p.createTuningSources(sparse=False)
    # p.resetTuningSources()
    # p.calculateTuningSources('cent copyright registered trademark'.split(), referenceSource, levels=[1,2,3], tuneBaseGlyphs=True)

    # --- build designspace ---
    # p.parametricAxesHidden = True
    # p.tuningAxesHidden = True
    # p.tuning = True
    # p.buildDesignspace(patchBlends=False, instances=True, parentParametric=True)
    # p.validateDesignspace(locations=True, mappings=True, instances=False)
    # p.validateSources(parametric=False, tuning=False, reference=True)

    # --- normalization ---
    p.cleanupSources(parametric=True, tuning=True, reference=True)
    p.normalizeSources(parametric=True, tuning=True, reference=True)

    # --- project info ---
    # p.printSettings()
    # p.printAxes()
    # print(p.defaultLocation)

    # --- proofing ---
    # glyphNames = ['Icyr'] # parseGString(p.defaultFont, 'Џ')
    # p.proofGlyphMemes(glyphNames, anchors=True)
    # p.proofSourcesGlyphSet(showCompatible=True, validateComposites=True)
    # p.proofBlends(list(string.ascii_uppercase + string.ascii_lowercase), margins=True, labels=True, levels=False, levelsShow=[2], header=True, footer=True, points=False)
    # p.proofTuning(['idot'], referenceSource, level=3)

    # --- build fonts ---
    # p.buildVariableFont(debug=False, featureWriter=False, noGDEF=True, subset=None)
    # p.buildInstancesVariableFont(clear=True, ufo=True)

    end = time.time()
    timer(start, end)

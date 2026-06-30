# menuTitle: AmstelvarA2 Controller

from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, glob, time, json, string
from fontTools.designspaceLib import DesignSpaceDocument
from xTools4.modules.xproject import xProject, makeParentAxis
from xTools4.modules.measurements import setSourceNamesFromMeasurements, readMeasurements
from xTools4.modules.sys import timer


_parametricAxesRoman  = 'WDSP GRAD '

                        # XOPQ/YOPQ          # XTRA              # YTRA         # serifs                 # EQ      # XTSP
_parametricAxesRoman += 'XOUC YOUC XOUA YOUA XTUC XTUR XTUD XTUA YTUC YTJD      XSHU YSHU XSVU YSVU XVAU XQUC YQUC XUCS XUCR XUCD ' # uppercase
_parametricAxesRoman += 'XOLC YOLC XOLA YOLA XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL      XQLC YQLC XLCS XLCR XLCD ' # lowercase
_parametricAxesRoman += 'XOFI YOFI           XTFI                YTFI           XSHF YSHF XSVF YSVF      XQFI YQFI XFIR           ' # figures
# _parametricAxesRoman += 'XOET YOET           XTET                               XSET YSET XSET YSET                XETS           ' # etcetera

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

    def addTuningSources(self):
        super().addTuningSources(familyName=f'{self.familyName} {self.subFamily}')

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
            parentAxes = self._parentParametricAxesRoman if self.subFamily == 'Roman' else self._parentParametricAxesItalic

            for parentAxisName in parentAxes:
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
                        print(parentAxisName, childName, values)
                        continue
                    values.sort()

                    parametricAxes[childName] = {
                        'minimum' : values[0],
                        'maximum' : values[1],
                        'default' : self.defaultLocation[childName],
                    }

                parentDefault = self._parentParametricAxesDefaults[parentAxisName]
                parentAxis, mappings = makeParentAxis(parentAxisName, parametricAxes, parentDefault, self._matchRangeAxes)

                # add parent axis
                blendsDict['axes'][parentAxisName] = parentAxis

                # add parametric mappings
                for mappingValue in mappings:
                    blendsDict['sources'][f'{parentAxisName}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappings[mappingValue].items():
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

    def updateGlyphsFromDefault(self, glyphNames, oldDefaultName, preflight=True, parametricSources=True, tuningSources=True):
        oldDefaultPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamily}_{oldDefaultName}.ufo')
        super().updateGlyphsFromDefault(glyphNames, oldDefaultPath, preflight=preflight, parametricSources=parametricSources, tuningSources=tuningSources)


if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman', 'Italic'][1]

    start = time.time()

    p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

    referenceSource = os.path.join(p.referenceSourcesFolder, f'Amstelvar-{subFamily}_wght400.ufo')

    # --- managing sources ---
    # p.createParametricSources(['XVAU'], minSource=True, maxSource=True)
    # p.setSourceNamesFromMeasurements(preflight=True)
    # p.splitSources('XOLC', 'XOET', [])

    # --- copy from default ---
    # p.updateGlyphsFromDefault(list('Y'), 'WDSP1000', preflight=False, parametricSources=True, tuningSources=True)
    # p.copyGlyphsFromDefault(glyphNames)
    # p.copyGroupsFromDefault()
    # p.copyUnicodesFromDefault(preflight=False)
    # p.copyGlyphOrderFromDefault()
    # p.copyKerningFromDefault()

    # --- building glyphs ---
    # p.buildCompositeGlyphs('aacute acircumflex'.split(), preflight=True)

    # --- tuning ---
    # p.tuningLevels = [1, 2, 3]
    # p.createTuningSources(sparse=False)
    # p.resetTuningSources()
    # p.calculateTuningSources(list(string.ascii_lowercase), referenceSource, levels=[1,2,3])

    # --- build designspace ---
    # p.parametricAxesHidden = True
    # p.tuningAxesHidden = True
    # p.tuning = True
    # p.buildDesignspace(patchBlends=False, instances=False, parentParametric=False)
    # p.validateDesignspace(locations=True, mappings=True, instances=False)
    # p.validateSources()

    # --- normalization ---
    # p.cleanupSources(parametric=True, tuning=True)
    p.normalizeSources(parametric=False, tuning=True)

    # --- project info ---
    # p.printSettings()
    # p.printAxes()
    # print(p.defaultLocation)

    # --- proofing ---
    # p.proofGlyphMemes(list(string.ascii_uppercase)+list(string.ascii_lowercase), anchors=False)
    # p.proofSourcesGlyphSet(showCompatible=True, validateComposites=True)
    # p.proofBlends(list(string.ascii_uppercase) + list(string.ascii_lowercase), margins=True, labels=True, levels=False, levelsShow=[2], header=True, footer=True, points=False)
    # p.proofTuning(list(string.ascii_lowercase), referenceSource, level=3)

    # --- build fonts ---
    # p.buildVariableFont(debug=False, featureWriter=False, noGDEF=True, subset='ASCII')
    # p.buildInstancesVariableFont(clear=True, ufo=True)

    end = time.time()
    timer(start, end)

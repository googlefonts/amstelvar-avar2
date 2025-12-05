from importlib import reload
import xTools4.modules.sys
reload(xTools4.modules.sys)
import xTools4.modules.ttx
reload(xTools4.modules.ttx)
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, glob, shutil, json, time, datetime
import subprocess
from xml.etree.ElementTree import parse
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from defcon import Font
from ufo2ft import compileVariableTTF
from mojo.smartSet import readSmartSets
import ufoProcessor # upgrade to UFOOperator?
from extractor import extractUFO
from xTools4.modules.measurements import FontMeasurements, permille
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.sys import timer
from xTools4.modules.ttx import ttf2ttx, ttx2ttf


### DEPRECATED!
### copy implementation from RobotoDelta
def makeParentAxis(parentName, parametricAxes, defaultName):
    r'''
    Calculate a parent axis to control several parametric axes, 
    with mappings to limit the range of each child axis.

    ::
        parentName  = 'XTRA'
        parametricAxes = {
            'XTUC' : dict(minimum=72, maximum=668, default=400),
            'XTUR' : dict(minimum=60, maximum=902, default=561),
            'XTUD' : dict(minimum=76, maximum=686, default=410),
            'XTLC' : dict(minimum=42, maximum=500, default=243),
            'XTLR' : dict(minimum=46, maximum=625, default=337),
            'XTLD' : dict(minimum=84, maximum=501, default=248),
            'XTFI' : dict(minimum=40, maximum=604, default=329),
        }
        defaultName = 'XTUC'

        parentAxis, mappings = makeParentAxis(parentName, parametricAxes, defaultName)
        
        print('parent parametric axis:')
        print(parentAxis)
        print()
        print('parent mappings to child parameters:')
        for parentValue, mapping in sorted(mappings.items()):
            print(f'\t{ parentValue } { mapping }')

    '''
    # THIS IS THE WRONG PLACE FOR THIS KIND OF DATA!
    # MOVE TO DESIGNSPACE BUILDER? MEASUREMENTS FORMAT?
    matchRangeAxes = {
        'XQUC' : 'XTUR',
        'XQLC' : 'XTLR',
        'XQFI' : 'XTFI',
    }

    defaultValue = parametricAxes[defaultName]['default']
    minValues = []
    maxValues = []
    for axisName, axis in parametricAxes.items():
        # SKIP MATCHED RANGE AXES
        if axisName in matchRangeAxes:
            continue
        axisShift = defaultValue - axis['default'] 
        minValue  = axis['minimum'] + axisShift
        maxValue  = axis['maximum'] + axisShift
        minValues.append(minValue)
        maxValues.append(maxValue)
    
    parentAxis = {
        'name'    : parentName,
        'default' : defaultValue,
        'minimum' : min(minValues),
        'maximum' : max(maxValues),
    }

    mappingValues = set(minValues + maxValues)
    mappings = {}
    for mappingValue in sorted(mappingValues):
        mappings[mappingValue] = {}
        for axisName, axis in parametricAxes.items():
            # SKIP MATCHED RANGE AXES
            if axisName in matchRangeAxes:
                continue
            axisShift = defaultValue - axis['default'] 
            value = mappingValue - axisShift
            mappings[mappingValue][axisName] = value

    # ADD AXES WITH MATCHED RANGES

    for mappingValue, maps in mappings.items():
        for axisName, mapAxisName in matchRangeAxes.items():
            if mapAxisName in maps:
                
                axisDefault = parametricAxes[axisName]['default']
                axisMinimum = parametricAxes[axisName]['minimum']
                axisMaximum = parametricAxes[axisName]['maximum']

                mapAxisDefault = parametricAxes[mapAxisName]['default']
                mapAxisMinimum = parametricAxes[mapAxisName]['minimum']
                mapAxisMaximum = parametricAxes[mapAxisName]['maximum']

                mapAxisValue = maps[mapAxisName]

                if mappingValue < defaultValue:
                    axisRange = axisDefault    - axisMinimum   
                    mapRange  = mapAxisDefault - mapAxisMinimum
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisMinimum) * mapScale
                    axisValue = axisMinimum + mapValue

                elif mappingValue > defaultValue:
                    axisRange = axisMaximum    - axisDefault
                    mapRange  = mapAxisMaximum - mapAxisDefault
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisDefault) * mapScale
                    axisValue = axisDefault + mapValue

                maps[axisName] = int(axisValue)

    return parentAxis, mappings



class AmstelvarA2DesignSpaceBuilder:
    '''
    Builds the AmstelvarA2 designspace from:

    - UFO sources
    - blends.json (Amstelvar1)
    - measurements.json

    Build steps:

    - build blends file
    - create designspace
    - add blended axes
    - add parametric axes
    - add mappings
    - add default source
    - add parametric sources
    - add instances

    '''
    familyName  = 'AmstelvarA2'
    defaultName = 'wght400'

    parentAxesBuild  = False
    parentAxesRoman  = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA XVAA YHAA'.split() # XTEQ YTEQ
    parentAxesItalic = parentAxesRoman

    opszMapping = [
        # input, output
        (   8.0,   8.0 ),
        (  14.0,  14.0 ),
        (  36.0,  64.0 ),
        (  84.0, 123.0 ),
        ( 144.0, 144.0 ),
    ]

    parentAxesDefaults = {
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

    parametricAxesRoman  = 'WDSP GRAD '
                            # XOPQ              # XTRA              # YTRA         # serifs                      # EQ      # XTSP
    parametricAxesRoman += 'XOUC YOUC XOUA YOUA XTUC XTUR XTUD XTUA YTUC YTJD      XSHU YSHU XSVU YSVU XVAU YHAU XQUC YQUC XUCS XUCR XUCD ' # uppercase
    parametricAxesRoman += 'XOLC YOLC XOLA YOLA XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL XVAL YHAL XQLC YQLC XLCS XLCR XLCD ' # lowercase
    parametricAxesRoman += 'XOFI YOFI           XTFI                YTFI           XSHF YSHF XSVF YSVF XVAF YHAF XQFI YQFI XFIR           ' # figures

    parametricAxesRoman += 'XDOT YTOS XTTW YTTL BARS'
    parametricAxesRoman  = parametricAxesRoman.split()
    parametricAxesItalic = parametricAxesRoman

    spacingAxes = [
        'XUCS', 'XUCR', 'XUCD',
        'XLCS', 'XLCR', 'XLCD',
        'XFIR', # 'XFIS', 
    ]

    verbose = True

    def __init__(self, subFamilyName='Roman'):
        self.subFamilyName = subFamilyName
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def designspaceName(self):
        return f'{self.familyName}-{self.subFamilyName}_avar2.designspace'

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Sources', self.subFamilyName)

    @property
    def cornerSourcesFolder(self):
        return os.path.join(self.sourcesFolder, 'corners')

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def instances(self):
        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        return D.instances

    @property
    def varFontsFolder(self):
        return os.path.join(self.baseFolder, 'Fonts')

    @property
    def varFontPath(self):
        return os.path.join(self.varFontsFolder, self.designspaceName.replace('.designspace', '.ttf'))

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['GRAD'] = 0
        L['TRIV'] = 0
        return L

    @property
    def amstelvarFolder(self):
        # path to a local copy of http://github.com/gferreira/amstelvar
        return os.path.join(os.path.dirname(self.baseFolder), 'amstelvar')

    @property
    def amstelvarBlendsPath(self):
        return os.path.join(self.amstelvarFolder, self.subFamilyName, 'blends.json')

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, 'blends.json')

    @property
    def blendedAxes(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    @property
    def cornerSources(self):
        return { os.path.splitext(os.path.split(ufo)[-1])[0] : ufo for ufo in glob.glob(f'{self.cornerSourcesFolder}/*.ufo') }

    @property
    def parametricAxes(self):
        if self.subFamilyName == 'Italic':
            return self.parametricAxesItalic
        else:
            return self.parametricAxesRoman

    @property
    def smartSetsPath(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}.roboFontSets')

    @property
    def glyphConstructionsPath(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}.glyphConstruction')

    # methods

    def addParametricAxes(self):

        if self.verbose:
            print('\tadding parametric axes...')

        for name in self.parametricAxes:

            # get default value
            if name == 'GRAD':
                defaultValue = 0
            else:
                defaultValue = permille(self.measurementsDefault.values[name], self.unitsPerEm)
            # get min/max values from file names
            values = []
            for ufo in self.parametricSources:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            if len(values) == 2:
                values.sort()
                minValue, maxValue = values
            elif len(values) == 1:
                values.append(defaultValue)
                values.sort()
                minValue, maxValue = values
            else:
                print(f'ERROR: {name}: {values}')
                # continue

            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = minValue
            a.maximum = maxValue
            a.default = defaultValue
            self.designspace.addAxis(a)

    def addCornerTuningAxes(self):

        if self.verbose:
            print('\tadding corner tuning axes...')

        # create TRIVARS axis
        a = AxisDescriptor()
        a.name    = 'TRIV'
        a.tag     = 'TRIV'
        a.minimum = 0
        a.maximum = 100
        a.default = 0
        self.designspace.addAxis(a)


    def addDefaultSource(self):
        if self.verbose:
            print('\tadding default source...')

        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = f'{self.familyName} {self.subFamilyName}'
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation
        self.designspace.addSource(src)

    def addParametricSources(self):
        if self.verbose:
            print('\tadding parametric sources...')

        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = f'{self.familyName} {self.subFamilyName}'
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addCornerTuningSources(self):

        if self.verbose:
            print('\tadding corner tuning sources...')

        for styleName, ufo in self.cornerSources.items():
            styleNameParts = styleName.split('_')

            # TRIVARS
            if len(styleNameParts) == 2:
                src = SourceDescriptor()
                src.path       = ufo
                src.familyName = f'{self.familyName} {self.subFamilyName}'
                L = self.defaultLocation.copy()
                value = 100
                src.styleName  = f'TRIV{value}'
                L['TRIV'] = value
                src.location = L
                self.designspace.addSource(src)

            # QUADVARS
            # elif len(styleNameParts) == 3:
            #     quadvars[styleName] = srcPath

    def addInstances(self):
        if self.verbose:
            print('\tadding instances...')

        for styleName in self.blendedSources.keys():
            # add only opsz/wght/wdth as instances
            if not ('opsz' in styleName or 'wght' in styleName or 'wdth' in styleName):
                continue

            L = self.defaultLocation.copy()
            for axis, value in self.blendedSources[styleName].items():
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName     = f'{self.familyName} {self.subFamilyName}'
            I.styleName      = styleName.replace('_', ' ')
            I.name           = styleName
            I.designLocation = L
            I.filename       = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)

    def addBlendedAxes(self):
        if self.verbose:
            print('\tadding blended axes...')

        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['minimum']
            a.maximum = self.blendedAxes[tag]['maximum']
            a.default = self.blendedAxes[tag]['default']
            if tag == 'opsz':
                a.map = self.opszMapping
            self.designspace.addAxis(a)

    def buildBlendsFile(self):
        if not os.path.exists(self.amstelvarBlendsPath):
            return

        # import Amstelvar blends
        with open(self.amstelvarBlendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # -------------
        # add XTSP axis
        # -------------

        blendsDict['axes']['XTSP'] = {
            "name"    : "XTSP",
            "default" : 0,
            "minimum" : -100,
            "maximum" : 100,
        }
        blendsDict['sources']['XTSP-100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP100'] = self.defaultLocation.copy()

        for axisName in self.spacingAxes:
            values = []    
            for ufo in self.parametricSources:
                value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                if axisName in ufo:
                    values.append(value)
            assert len(values)
            values.sort()
            blendsDict['sources']['XTSP-100'][axisName] = values[0]
            blendsDict['sources']['XTSP100'][axisName] = values[1]

        # -----------------------
        # add blended PARENT axes
        # -----------------------

        if self.parentAxesBuild:

            measurements = readMeasurements(self.measurementsPath)
            fontMeasurements = measurements['font']
            parentAxes = self.parentAxesRoman if self.subFamilyName == 'Roman' else self.parentAxesItalic

            for parentAxisName in parentAxes:
                parentMeasurement = fontMeasurements[parentAxisName]

                # get parametric axes for parent
                parametricAxes = {}
                childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxisName]
                for childName in childNames:
                    # get min/max values from file names
                    values = []
                    for ufo in self.parametricSources:
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

                parentDefault = self.parentAxesDefaults[parentAxisName]
                parentAxis, mappings = makeParentAxis(parentAxisName, parametricAxes, parentDefault)

                # add parent axis
                blendsDict['axes'][parentAxisName] = parentAxis

                # add parametric mappings
                for mappingValue in mappings:
                    blendsDict['sources'][f'{parentAxisName}{mappingValue}'] = {}
                    for parametricAxisName, parametricValue in mappings[mappingValue].items():
                        blendsDict['sources'][f'{parentAxisName}{mappingValue}'][parametricAxisName] = parametricValue

        # -----------------------
        # save AmstelvarA2 blends
        # -----------------------

        if self.verbose:
            print('\tbuilding blends file...')

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

    def addMappings(self):

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        if self.verbose:
            print('\tadding mappings...')

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # if 'XTSP' not in styleName:
            #     inputLocation['XTRA'] = int(blendedSources[styleName]['XTUC'])

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            if styleName in self.cornerSources:
                styleNameParts = styleName.split('_')
                if len(styleNameParts) == 2:
                    outputLocation['TRIV'] = 100
                # elif len(styleNameParts) == 3:
                #     outputLocation['QUAD'] = 100

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation
            m.description    = styleName


            self.designspace.addAxisMapping(m)

    def save(self):
        if not self.designspace:
            return
        if self.verbose:
            print(f'\tsaving designspace...', end=' ')

        self.designspace.lib['com.xTools4.xProject.smartSetsPath']          = os.path.split(self.smartSetsPath)[-1]
        self.designspace.lib['com.xTools4.xProject.measurementsPath']       = os.path.split(self.measurementsPath)[-1]
        self.designspace.lib['com.xTools4.xProject.glyphConstructionsPath'] = os.path.split(self.glyphConstructionsPath)[-1]

        self.designspace.write(self.designspacePath)
        if self.verbose:
            print(os.path.exists(self.designspacePath))
            print()

    def build(self, patchBlends=True):
        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.buildBlendsFile()
        if patchBlends:
            self.patchBlendsFile()
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addCornerTuningAxes()
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()
        self.addCornerTuningSources()
        # self.addInstances()
        self.save()

    def buildInstances(self, clear=True):

        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)

        ufoProcessor.build(self.designspacePath)
        ufos = glob.glob(f'{self.instancesFolder}/*.ufo')

        # copy glyph order from default
        f = OpenFont(self.defaultUFO, showInterface=False)
        glyphOrder = f.glyphOrder
        f.close()

        for ufo in ufos:
            f = OpenFont(ufo, showInterface=False)
            f.glyphOrder = glyphOrder
            f.save()
            f.close()

    def buildVariableFont(self, subset=None, setVersionInfo=True, debug=False, fixGDEF=False, removeMarkFeature=False):

        print(f'generating variable font for {self.designspaceName}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            if debug:
                print(f'\t\tloading {src.familyName} {src.styleName}...')
            src.font = Font(src.path)

        # generate variable font with fontmake

        if 'PYTHONHOME' in os.environ:
           del os.environ['PYTHONHOME']

        print(f"\tbuilding avar2 font... ", end='')

        # cmd  = ['/opt/homebrew/bin/fontmake']
        cmd  = ['/Library/Frameworks/Python.framework/Versions/3.11/bin/fontmake']
        cmd += ['-m', self.designspacePath]
        cmd += ['-o', 'variable']
        cmd += ['--output-path', self.varFontPath]
        cmd += ['--feature-writer', 'None']
        cmd += ['--no-generate-GDEF']
        cmd += ['--keep-direction']
        cmd += ['--verbose WARNING']
        cmd  = ' '.join(cmd)

        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout.readlines():
                print(line,)
            retval = p.wait()

        print(f'{os.path.exists(self.varFontPath)}')

        # subset ascii variable font with pyftsubset
        if subset:
            print('\tsubsetting variable font...')
            asciiGlyphs = subset.split()
            font = TTFont(self.varFontPath)
            subsetter = Subsetter()
            subsetter.populate(glyphs=asciiGlyphs)
            subsetter.subset(font)
            font.save(self.varFontPath)

        if setVersionInfo or fixGDEF:

            # convert ttf to ttx
            ttf2ttx(self.varFontPath)

            # load XML from ttx
            ttxPath = self.varFontPath.replace('.ttf', '.ttx')
            tree = parse(ttxPath)
            root = tree.getroot()

            # set version info in the font's unique name
            if setVersionInfo:
                print('\tsetting version info...')
                # make unique name with timestamp
                timestamp = time.strftime("%Y%m%d%H%M", time.localtime())
                uniqueName = f'{self.familyName} {self.subFamilyName} {timestamp}'
                # add version info to unique name -- nameID 3
                for child in root.find('name'):
                    if child.attrib['nameID'] == '3':
                        child.text = uniqueName

            # fix buggy class in GDEF table
            if fixGDEF:
                defaultFont = OpenFont(self.defaultUFO, showInterface=False)
                # 1. get a list of all combining accents
                combiningAccents = getCombingingAccents(self.smartSetsPath)
                # 2. get a list of all glyphs with anchors starting with underscore
                underscoreGlyphs = findGlyphsWithUnderscoreAnchors(defaultFont)
                # subtract (1) from (2) to get a list of glyphs to fix
                glyphsToFix = list(underscoreGlyphs.difference(combiningAccents))

                print('\tfixing bug in GDEF table...')
                for child in root.find('GDEF'):
                    if child.tag == 'GlyphClassDef':
                        for g in child.iter('ClassDef'):
                            glyphName = g.get('glyph')
                            if glyphName in glyphsToFix:
                                # change GDEF class from 3 to 1
                                g.set('class', '1')

            # save XML to ttx
            tree.write(ttxPath)

            # convert ttx back to ttf
            ttx2ttf(ttxPath)

            # clear ttx file
            os.remove(ttxPath)

        # remove buggy `mark` feature
        if removeMarkFeature: ### NOT WORKING YET
            print("\tremoving buggy 'mark' feature...")

            cmd  = ['/opt/homebrew/bin/fonttools']
            cmd += ['subset', self.varFontPath, "glyphs='*'"]
            cmd += ["--layout-features-='mark','mkmk'"]
            cmd  = ' '.join(cmd)

            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
                for line in p.stdout.readlines():
                    print(line,)
                retval = p.wait()

        print('...done.\n')

    def buildInstancesVariableFont(self, clear=True, ufo=False):

        varInstancesFolder = os.path.join(self.varFontsFolder, 'instances', self.subFamilyName)

        if clear:
            varInstances = glob.glob(f'{varInstancesFolder}/*.ttf')
            for instance in varInstances:
                os.remove(instance)
            if ufo:
                ufos = glob.glob(f'{varInstancesFolder}/*.ufo')
                for ufo in ufos:
                    shutil.rmtree(ufo)

        # http://stackoverflow.com/questions/65184937/fatal-python-error-init-fs-encoding-failed-to-get-the-python-codec-of-the-file
        if 'PYTHONHOME' in os.environ:
           del os.environ['PYTHONHOME']

        print(f"building AmstelvarA2 {self.subFamilyName} instances...")

        for instance in self.instances:
            ttfPath = os.path.join(varInstancesFolder, f'AmstelvarA2-{self.subFamilyName}_avar2_{instance.name}.ttf')
            print(f"\tbuilding {instance.name}...", end=' ')
            cmd  = ['/opt/homebrew/bin/fontmake']
            cmd += ['-m', self.designspacePath]
            cmd += ['-o', 'ttf']
            cmd += ['-i', instance.name, '--expand-features-to-instances']
            cmd += ['--feature-writer', 'None']
            cmd += ['--output-path', ttfPath]
            cmd += ['--keep-direction', '--keep-overlaps']
            cmd += ['--verbose ERROR']
            cmd  = ' '.join(cmd)

            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
                for line in p.stdout.readlines():
                    print(line,)
                retval = p.wait()

            print(f'({os.path.exists(ttfPath)})')

        if ufo:
            print(f"Converting instances to UFO format...")
            ttfPaths = glob.glob(f'{varInstancesFolder}/*.ttf')
            for ttfPath in ttfPaths:
                ufo = Font()
                extractUFO(ttfPath, ufo)
                ufoPath = ttfPath.replace('.ttf', '.ufo')
                print(f"\tSaving {os.path.split(ufoPath)[-1]}...")
                ufo.save(ufoPath)

            # set slant offset in Italic fonts
            ufoPaths = glob.glob(f'{varInstancesFolder}/*.ufo')
            defaultFont = OpenFont(self.defaultUFO, showInterface=False)
            slantOffset = defaultFont.lib.get('com.typemytype.robofont.italicSlantOffset')
            if slantOffset:
                for ufoPath in ufoPaths:
                    f = OpenFont(ufoPath, showInterface=False)
                    f.features.text = '' # clear OpenType features
                    f.lib['com.typemytype.robofont.italicSlantOffset'] = slantOffset
                    f.save()
                    f.close()

        print("done!")

    def printAxes(self):

        print()

        measurements = {}
        for d in self.measurementsDefault.definitions:
            measurements[d[0]] = d[7]

        # print('### Parent parametric axes\n')
        # for n, axis in enumerate(self.parentAxesRoman):
        #     print(f'{n+1}. `{axis}` {measurements[axis]}')

        print('\n### Parametric axes\n')
        for n, axis in enumerate(self.parametricAxesRoman):
            print(f'{n+1}. `{axis}` {measurements[axis]}')

        print()

# -----
# build
# -----

if __name__ == '__main__':

    subFamilyName = ['Roman', 'Italic'][0]

    start = time.time()

    D = AmstelvarA2DesignSpaceBuilder(subFamilyName)
    D.build(patchBlends=True)

    # D.buildVariableFont(subset=None, setVersionInfo=True, fixGDEF=False, removeMarkFeature=False, debug=False)
    # D.buildInstancesVariableFont(clear=True, ufo=True)
    # D.printAxes()

    end = time.time()
    timer(start, end)

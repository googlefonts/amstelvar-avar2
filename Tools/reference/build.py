import os, glob, shutil, json
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
from defcon import Font
from ufo2ft import compileTTF, compileVariableTTF
import ufoProcessor # upgrade to UFOOperator
from xTools4.modules.measurements import FontMeasurements, permille


class AmstelvarDesignSpaceBuilder:
    '''
    Original Amstelvar1 designspace. Used to extract measurements for AmstelvarA2 blended extrema.

    - opsz
    - wght
    - wdth

    + builds instances for measuring

    '''
    familyName      = 'Amstelvar'
    subFamilyName   = ['Roman', 'Italic'][1]
    defaultName     = 'wght400'
    designspaceName = f'{familyName}-{subFamilyName}.designspace'

    _axes = {
        "opsz" : {
          "name"    : "Optical size",
          "default" : 14,
          "min"     : 8,
          "max"     : 144,
        },
        "wght" : {
          "name"    : "Weight",
          "default" : 400,
          "min"     : 100,
          "max"     : 1000,
        },
        "wdth": {
          "name"    : "Width",
          "default" : 100,
          "min"     : 50,
          "max"     : 125,
        }
    }

    instances = [
        # monovar 
        'wght400',
        # duovars
        'wght200', 'wght800', 'wdth85', 'wdth125', 'opsz8', 'opsz144',
        # trivars
        'wght200_wdth85', 'wght200_wdth125', 'wght800_wdth85', 'wght800_wdth125', 
        'opsz8_wght200',   'opsz8_wght800',   'opsz8_wdth85',   'opsz8_wdth125',
        'opsz144_wght200', 'opsz144_wght800', 'opsz144_wdth85', 'opsz144_wdth125',
        # quadvars
        'opsz8_wght200_wdth85',   'opsz8_wght200_wdth125',   'opsz8_wght800_wdth85',   'opsz8_wght800_wdth125',
        'opsz144_wght200_wdth85', 'opsz144_wght200_wdth125', 'opsz144_wght800_wdth85', 'opsz144_wght800_wdth125',
    ]

    def __init__(self):
        pass

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, self.subFamilyName)

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def defaultLocation(self):
        L = { self.axes[tag]['name']: self.axes[tag]['default'] for tag in self.axes }
        return L

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def sources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def axes(self):
        return self._axes # [self.subFamilyName]

    def addAxes(self):
        for tag in self.axes.keys():
            a = AxisDescriptor()
            a.name    = self.axes[tag]['name']
            a.tag     = tag
            a.minimum = self.axes[tag]['min']
            a.maximum = self.axes[tag]['max']
            a.default = self.axes[tag]['default']
            self.designspace.addAxis(a)

    def addSources(self):
        for srcPath in self.sources:
            fileName = os.path.splitext(os.path.split(srcPath)[-1])[0]
            styleName = fileName[fileName.find('_')+1:]
            if 'GRAD' in styleName:
                continue
            src = SourceDescriptor()
            src.path       = srcPath
            src.familyName = self.familyName
            src.styleName  = styleName
            L = self.defaultLocation.copy()
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                name  = self.axes[tag]['name']
                L[name] = value
            src.location = L
            self.designspace.addSource(src)

    def addInstances(self):
        for styleName in self.instances: 
            I = InstanceDescriptor()
            I.familyName = self.familyName
            I.styleName  = styleName
            I.name       = styleName
            I.filename   = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')
            L = self.defaultLocation.copy()
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                name  = self.axes[tag]['name']
                L[name] = value
            I.designLocation = L
            self.designspace.addInstance(I)

    def buildInstances(self, clear=True):
        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)

        # build UFOs
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

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addAxes()
        self.addSources()
        self.addInstances()

    def save(self):
        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)


# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()
    # D.buildInstances()
    
    
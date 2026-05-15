from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, time
from fontTools.designspaceLib import DesignSpaceDocument
from xTools4.modules.xproject import xProject
from xTools4.modules.measurements import setSourceNamesFromMeasurements
from xTools4.modules.sys import timer


parametricAxesRoman  = 'WDSP GRAD '
parametricAxesRoman += 'XOUC YOUC XOUA YOUA XTUC XTUR XTUD XTUA YTUC YTJD      XSHU YSHU XSVU YSVU XQUC YQUC XUCS XUCR XUCD '
parametricAxesRoman += 'XOLC YOLC XOLA YOLA XTLC XTLR XTLD XTLA YTLC YTAS YTDE XSHL YSHL XSVL YSVL XQLC YQLC XLCS XLCR XLCD '
parametricAxesRoman += 'XOFI YOFI           XTFI                YTFI           XSHF YSHF XSVF YSVF XQFI YQFI XFIR           '
parametricAxesRoman += 'XDOT YTOS XTTW YTTL BARS'
parametricAxesRoman  = parametricAxesRoman.split()
parametricAxesItalic = parametricAxesRoman

customParametricAxes = {
    'GRAD' : 0,
}


class AmstelvarA2Controller(xProject):

    _parametricAxes = {
        'Roman'  : parametricAxesRoman,
        'Italic' : parametricAxesItalic,
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
    def referenceBlendsPath(self):
        pass

    @property
    def referenceFontPath(self):
        referenceFonts = {
            'Roman'  : 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf',
            'Italic' : 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf' ,
        }
        return os.path.join(self.fontsFolder, 'legacy', referenceFonts[self.subFamily])

    @property
    def parametricAxes(self):
        return self._parametricAxes[self.subFamily]

    @property
    def defaultLocation(self):
        L = super().defaultLocation
        L['GRAD'] = 0
        return L

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

    def buildBlendsFile(self):
        pass

    def patchBlendsFile(self):
        pass

    def buildDesignspace(self, patchBlends=True, tuneDuovars=True, tuneTrivars=True, tuneQuadvars=True, instances=False):
        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        # self.buildBlendsFile()
        # if patchBlends:
        #     self.patchBlendsFile()

        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes(customParametricAxes)
        # self.addTuningAxes(duovars=tuneDuovars, trivars=tuneTrivars, quadvars=tuneQuadvars)
        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()
        # self.addTuningSources()
        # self.addInstances()
        self.addCustomKeysToLib()
        self.save()


if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman', 'Italic'][0]

    start = time.time()

    p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)
    # p.printSettings()
    # p.createParametricSources(['XVAU'], minSource=True, maxSource=True)

    # p.cleanupSources(parametric=True, tuning=False)
    # p.normalizeSources(parametric=True, tuning=False)

    # p.setSourceNamesFromMeasurements(preflight=True)

    p.parametricAxesHidden = True
    p.buildDesignspace(patchBlends=False)

    # D.build(patchBlends=True, tuneDuovars=tune, tuneTrivars=tune, tuneQuadvars=tune)
    # D.buildVariableFont(subset=None, setVersionInfo=True, fixGDEF=False, removeMarkFeature=False, debug=False)
    # # D.buildInstancesVariableFont(clear=True, ufo=True)
    # # D.printAxes()

    end = time.time()
    timer(start, end)


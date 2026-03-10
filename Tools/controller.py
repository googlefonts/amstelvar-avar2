from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os
from xTools4.modules.xproject import xProject


class AmstelvarA2Controller(xProject):

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




if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman', 'Italic'][0]

    p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)
    # p.printSettings()

    p.buildDesignspace()

    # D.build(patchBlends=True, tuneDuovars=tune, tuneTrivars=tune, tuneQuadvars=tune)
    # D.buildVariableFont(subset=None, setVersionInfo=True, fixGDEF=False, removeMarkFeature=False, debug=False)
    # # D.buildInstancesVariableFont(clear=True, ufo=True)
    # # D.printAxes()



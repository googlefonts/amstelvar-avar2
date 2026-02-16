# menuTitle: set source names from measurements

from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os
from xTools4.modules.measurements import setSourceNamesFromMeasurements

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
subFamilyName    = ['Roman', 'Italic'][0]
familyName       = f'AmstelvarA2 {subFamilyName}'
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
ignoreTags       = ['wght', 'GRAD'] # 'BARS',

setSourceNamesFromMeasurements(
        sourcesFolder,
        familyName,
        measurementsPath,
        preflight=False,
        ignoreTags=ignoreTags,
)

from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import os
from xTools4.modules.validation import validateDesignspace

folder          = os.path.dirname(os.path.dirname(os.getcwd()))
subFamilyName   = ['Roman', 'Italic'][0]
sourcesFolder   = os.path.join(folder, 'Sources', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}.designspace')

assert os.path.exists(designspacePath)

validateDesignspace(designspacePath, locations=True, mappings=True, instances=False)

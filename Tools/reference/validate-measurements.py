# menuTitle: validate measurements

'''
validate the Amstelvar measurements file against the AmstelvarA2 one
measurements for the default in both projects must be equal!

'''

import os
from xTools4.modules.measurements import FontMeasurements

subfamilyName     = ['Roman', 'Italic'][1]
defaultName       = 'wght400'

baseFolder1       = os.path.dirname(os.getcwd())
sourcesFolder1    = os.path.join(baseFolder1, subfamilyName)
measurementsPath1 = os.path.join(sourcesFolder1, 'measurements.json')
defaultPath1      = os.path.join(sourcesFolder1, f'Amstelvar-{subfamilyName}_{defaultName}.ufo')

assert os.path.exists(defaultPath1)

baseFolder2       = os.path.join(os.path.dirname(baseFolder1), 'amstelvar-avar2')
sourcesFolder2    = os.path.join(baseFolder2, 'Sources', subfamilyName)
measurementsPath2 = os.path.join(sourcesFolder2, 'measurements.json')
defaultPath2      = os.path.join(sourcesFolder2, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')

assert os.path.exists(defaultPath2)
  
f1 = OpenFont(defaultPath1, showInterface=False)
M1 = FontMeasurements()
M1.read(measurementsPath1)
M1.measure(f1)

f2 = OpenFont(defaultPath2, showInterface=False)
M2 = FontMeasurements()
M2.read(measurementsPath2)
M2.measure(f2)

for key, value2 in M2.values.items():
    value1 = M1.values.get(key)
    if value2 != value1:
        print(key, ':', value2, '(2)', value1, '(1)')

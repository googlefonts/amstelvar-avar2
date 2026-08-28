from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from xTools4.modules.measurements import readMeasurements

baseFolder          = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder       = os.path.join(baseFolder, 'Sources')
measurementsPathSrc = os.path.join(sourcesFolder, 'Roman', 'measurements.json')
measurementsPathDst = os.path.join(sourcesFolder, 'Italic', 'measurements.json')

assert os.path.exists(measurementsPathSrc)
assert os.path.exists(measurementsPathDst)

measurementsSrc = readMeasurements(measurementsPathSrc)
measurementsDst = readMeasurements(measurementsPathDst)

for tag in measurementsSrc['font'].keys():
    print(tag, measurementsSrc['font'][tag]['description'])
    if tag not in measurementsDst['font']:
        print(f'tag {tag} missing in target file, skipping...')
        continue    
    measurementsDst['font'][tag]['description'] = measurementsSrc['font'][tag]['description'] 

with open(measurementsPathDst, 'w', encoding='utf-8') as f:
    json.dump(measurementsDst, f, indent=2)

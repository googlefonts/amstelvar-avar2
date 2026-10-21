import os, sys

print('initializing AmstelvarA2 controller...\n')

libFolder = os.getcwd()
if libFolder not in sys.path:
    sys.path.append(libFolder)

from importlib import reload
import controller
reload(controller)

print(controller)

print('\n...done.\n')
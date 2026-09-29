import os, sys

libFolder = os.getcwd()
if libFolder not in sys.path:
    sys.path.append(libFolder)

from importlib import reload
import controller
reload(controller)

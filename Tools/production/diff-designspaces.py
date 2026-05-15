import os
from difflib import HtmlDiff, unified_diff

baseFolder         = os.path.dirname(os.path.dirname(os.getcwd()))
subFamilyName      = ['Roman', 'Italic'][0]
familyName         = 'AmstelvarA2'
sourcesFolder      = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePathNew = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}.designspace')
designspacePathOld = designspacePathNew.replace('.designspace', '_old.designspace')

assert os.path.exists(designspacePathNew)
assert os.path.exists(designspacePathOld)

with open(designspacePathOld, mode='r') as fileOld:
    srcOld = fileOld.readlines()

with open(designspacePathNew, mode='r') as fileNew:
    srcNew = fileNew.readlines()

diff = unified_diff(srcOld, srcNew, fromfile=designspacePathOld, tofile=designspacePathNew)
print("".join(diff), end="")

import os, sys
import pathlib
import bpy


worksapce = str(pathlib.Path.home() / 'Documents' / 'workspace' / 'BlenderLib') + '/'

print('----------- LOAD LIB -----------')

runString = """import sys, os

filesDir = '""" + worksapce + """'
initFile = '__init__.py'
 
if filesDir not in sys.path:
    sys.path.append(filesDir)
 
file = os.path.join(filesDir, initFile)
 
if 'DEBUG_MODE' not in sys.argv:
    sys.argv.append('DEBUG_MODE')
 
exec(compile(open(file).read(), initFile, 'exec'))
 
if 'DEBUG_MODE' in sys.argv:
    sys.argv.remove('DEBUG_MODE')

"""

bpy.ops.text.new()
script = bpy.data.texts[-1]
script.name = 'autorun.py'
script.write(runString)
script.use_module = True
exec(script.as_string())

print('----------- DONE -----------')
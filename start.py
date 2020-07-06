import bpy
from mathutils import *

D = bpy.data
C = bpy.context

print('----------- LOAD LIB -----------')

runString = """import os
import bpy
 
filename = os.path.join('/Users/lorenzoargentieri/Documents/workspace/BlenderLib/add-ons/', 'utils.py')
exec(compile(open(filename).read(), filename, 'exec'))
"""

bpy.ops.text.new()
script = D.texts[-1]
script.name = 'autorun.py'
script.write(runString)
script.use_module = True
exec(script.as_string())

print('----------- DONE -----------')
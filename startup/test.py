import bpy
from mathutils import *
D = bpy.data
C = bpy.context

for c in C.collection.keys():
    print(c)
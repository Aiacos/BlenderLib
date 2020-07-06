import bpy

C = bpy.context
D = bpy.data

print('LIIIIIIB')
def select(obj, selectionSet=False):
    if isinstance(obj, str):
        obj = D.objects[obj]
    # to select the object in the 3D viewport,
    # this way you can also select multiple objects
    if selectionSet:
        obj.select_set(True)
    else:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)

    # to set the active object
    bpy.context.view_layer.objects.active = obj

print('Test Selection Light')
select('Light')

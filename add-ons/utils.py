bl_info = {
    "name": "BlenderLib",
    "author": "Lorenzo Argentieri",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "location": "View3D > BlenderLib",
    "description": "Tools Operators",
    "warning": "",
    "doc_url": "",
    "category": "Development"#"BlenderLib"
}


import bpy

C = bpy.context
D = bpy.data

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

class VIEW3D_MT_menu(bpy.types.Menu):
    bl_label = "BlenderLib"

    def draw(self, context):
        self.layout.operator("mesh.primitive_monkey_add")
        self.layout.operator("mesh.primitive_cube_add")

def addmenu_callback(self, context):
    self.layout.menu("VIEW3D_MT_menu")


def register():
    bpy.utils.register_class(VIEW3D_MT_menu)
    bpy.types.VIEW3D_HT_header.prepend(addmenu_callback)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(addmenu_callback)
    bpy.utils.unregister_class(VIEW3D_MT_menu)


if __name__ == "__main__":
    register()

    print('LIIIIIIB')
    print('Test Selection Light')
    select('Light')

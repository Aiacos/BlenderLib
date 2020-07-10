import bpy


class VIEW3D_MT_menu(bpy.types.Menu):
    bl_label = "BlenderLib"

    def draw(self, context):
        self.layout.operator("mesh.primitive_monkey_add")
        self.layout.operator("mesh.primitive_cube_add")
        self.layout.operator("bpy.ops.object.simple_operator")

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

    #print('LIIIIIIB')
    #print('Test Selection Light')
    #select('Light')

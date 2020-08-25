import bpy


class TOPBAR_MT_blenderLib(bpy.types.Menu):
    bl_label = "BlenderLib"

    def draw(self, context):
        self.layout.operator("mesh.primitive_monkey_add")
        self.layout.operator("mesh.primitive_cube_add")
        self.layout.menu("SHADER_MT_libMenu")

class SHADER_MT_libMenu(bpy.types.Menu):
    bl_label = "ShaderLib"

    def draw(self, context):
        self.layout.operator("materials.shaders_converter")
        self.layout.operator("materials.shaders_duplicate_remover")

class VIEW3D_MT_menu(bpy.types.Menu):
    bl_label = "BlenderLib"

    def draw(self, context):
        self.layout.operator("mesh.primitive_monkey_add")
        self.layout.operator("mesh.primitive_cube_add")
        self.layout.operator("materials.shaders_converter")

def add_blenderlib_callback(self, context):
    self.layout.menu("TOPBAR_MT_blenderLib")

def addmenu_callback(self, context):
    self.layout.menu("VIEW3D_MT_menu")


def register():
    bpy.utils.register_class(TOPBAR_MT_blenderLib)
    bpy.utils.register_class(SHADER_MT_libMenu)
    bpy.utils.register_class(VIEW3D_MT_menu)
    bpy.types.VIEW3D_HT_header.prepend(addmenu_callback)
    bpy.types.TOPBAR_MT_editor_menus.append(add_blenderlib_callback)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(addmenu_callback)
    bpy.types.TOPBAR_MT_editor_menus.remove(add_blenderlib_callback)
    bpy.utils.unregister_class(VIEW3D_MT_menu)
    bpy.utils.unregister_class(TOPBAR_MT_blenderLib)
    bpy.utils.unregister_class(SHADER_MT_libMenu)


if __name__ == "__main__":
    register()

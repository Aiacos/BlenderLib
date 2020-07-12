import shaderLib.texture as tx
import bpy

C = bpy.context
D = bpy.data
O = bpy.ops

class ShadersConverter(object):
    def __init__(self, removeDuplicateShaders=False):
        self.folderManager = tx.ProjectFolder()

        model_collection = D.collections['Model']
        objects = model_collection.objects

        if removeDuplicateShaders:
            print('------- REMOVE DUPLICATE -------')
            for obj in objects:
                self.removeDuplicateShader(obj)
            print('-------')

        for obj in objects:
            self.iterateMaterialSlot(obj)

    def select(self, obj, selectionSet=False):
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

    def removeDuplicateShader(self, obj):
        self.select(obj)
        material_slots = bpy.context.object.material_slots
        for idx, slot in zip(range(0, len(material_slots)), material_slots):
            # print(idx, slot)
            if slot.material.name[-3:].isnumeric():
                original_name = slot.material.name[:-4]
                mat = bpy.data.materials.get(original_name)

                slot.material = mat

        for idx, slot in zip(range(0, len(material_slots)), material_slots):
            mat_name_end = slot.material.name.split('_')[-1]
            if '(' in mat_name_end and ')' in mat_name_end:
                original_name2 = slot.material.name.replace('_' + mat_name_end, '')

                usefullNameList = []
                for i in D.materials.keys():
                    if original_name2 in i:
                        usefullNameList.append(i)

                usefullNameList = list(set(usefullNameList))
                usefullNameList.sort()
                # print(original_name2, ' ---- ', usefullNameList[0], ' ---- ', len(usefullNameList))

                mat = bpy.data.materials.get(usefullNameList[0])

                slot.material = mat

    def iterateMaterialSlot(self, obj):
        self.select(obj)
        material_slots = C.object.material_slots
        for idx, slot in zip(range(0, len(material_slots)), material_slots):
            if slot.material.name != 'Dots Stroke':
                C.object.active_material_index = idx
                ShaderPBRConverter(slot.material, self.folderManager.get_images(), str(self.folderManager.texture_folder)+'/')

class ShaderPBRConverter(object):
    def __init__(self, material, img_list, sourceimages):
        self.material = material
        self.shader_node = material.node_tree.nodes['Principled BSDF']
        self.links = material.node_tree.links

        self.texture_base_name = self.get_texture_base_name()
        self.shader_texture_list = self.texture_filter(img_list)
        self.node_wrangle_texture_dict = self.node_wrangler_texture_dict(self.shader_texture_list)

        print('MATERIAL: ', self.material)
        if self.shader_texture_list:
            self.build_node_wrangler_principled_bsdf(sourceimages, str(self.texture_base_name), self.node_wrangle_texture_dict)
        else:
            print('Empty Material', self.texture_base_name)

    def get_texture_base_name(self):
        """
        Get texture base name: concrete_BaseColor.png > concrete
        :return: (str) texture base name
        """
        baseColor_texture_fullpath = ''
        for l in self.links:
            if isinstance(l.from_node, bpy.types.ShaderNodeTexImage):
                baseColor_texture_fullpath = tx.getTextureFromNode(l.from_node.image.filepath)

                return tx.getTextureBaseName(baseColor_texture_fullpath.stem)
        return baseColor_texture_fullpath

    def texture_filter(self, img_list):
        shader_texture_list = []
        for img in img_list:
            if self.texture_base_name in tx.getTextureFromNode(img).stem:
                shader_texture_list.append(img)

        if shader_texture_list:
            return shader_texture_list

        return []

    def node_wrangler_texture_dict(self, shader_texture_list):
        imgDictList = []
        for i in shader_texture_list:
            imgDict = {'name': i, 'name': i}
            imgDictList.append(imgDict)

        return imgDictList


    def build_node_wrangler_principled_bsdf(self, folder, baseColor_texture, shader_textures):
        old_type = C.area.ui_type
        C.area.ui_type = 'ShaderNodeTree'

        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        #################
        #O.node.select_all(action='TOGGLE')
        nodes = self.material.node_tree.nodes
        self.shader_node.select = True
        nodes.active = self.shader_node

        #######################

        area = C.area
        area.type = 'NODE_EDITOR'
        for sp in area.spaces:
            print(sp, sp.type, "has tree_treetype", hasattr(sp, "tree_type"))

            if hasattr(sp, "tree_type"):
                space = area.spaces.active
                space.tree_type = 'ShaderNodeTree'

                for a in C.screen.areas:
                    if a.type == 'NODE_EDITOR':
                        x = a.x
                        y = a.y
                        width = a.width
                        height = a.height

                C.window.cursor_warp(x + width / 2, y + height / 2)

        ########################
                print('Context: ', C.space_data.node_tree)
                O.node.nw_add_textures_for_principled(filepath=baseColor_texture, directory=folder+'/', files=shader_textures, relative_path=True)

        C.area.ui_type = old_type

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def main(context):
    ShadersConverter()

        #C.area.ui_type = old_type

    def build_principled_bsdf(self, folder, shader_textures):
        pass

class ShadersConverterOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "materials.shaders_converter"
    bl_label = "Shaders PBR Converter"
    bl_context = "node"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ShadersConverter()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ShadersConverterOperator)


def unregister():
    bpy.utils.unregister_class(ShadersConverterOperator)


if __name__ == "__main__":
    register()
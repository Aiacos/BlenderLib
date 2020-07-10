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
            for obj in objects:
                self.removeDuplicateShader(obj)

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
                ShaderPBRConverter(slot.material, self.folderManager.get_images(), self.folderManager.texture_folder()+'/')

class ShaderPBRConverter(object):
    def __init__(self, material, img_list, sourceimages):
        self.shader_node = material.node_tree.nodes['Principled BSDF']
        self.links = material.node_tree.links

        self.texture_base_name = self.get_texture_base_name()
        self.shader_texture_list = self.texture_filter(img_list)
        self.node_wrangle_texture_dict = self.node_wrangler_texture_dict(self.shader_texture_list)

        nodes = self.shader_node.node_tree.nodes
        nodes.active = self.shader_node

        self.build_node_wrangler_principled_bsdf(sourceimages, str(self.texture_base_name), self.shader_texture_list)

    def get_texture_base_name(self):
        """
        Get texture base name: concrete_BaseColor.png > concrete
        :return: (str) texture base name
        """
        for l in self.links:
            if isinstance(l.from_node, bpy.types.ShaderNodeTexImage):
                baseColor_texture_fullpath = tx.getTextureFromNode(l.from_node.image.filepath)

        return tx.getTextureBaseName(baseColor_texture_fullpath)

    def texture_filter(self, img_list):
        shader_texture_list = []
        for img in img_list:
            if self.get_texture_base_name() in tx.getTextureFromNode(img).stem:
                shader_texture_list.append(img)

        return shader_texture_list

    def node_wrangler_texture_dict(self, shader_texture_list):
        imgDictList = []
        for i in shader_texture_list:
            imgDict = {'name': i, 'name': i}
            imgDictList.append(imgDict)

        return imgDictList


    def build_node_wrangler_principled_bsdf(self, folder, baseColor_texture, shader_textures):
            old_type = C.area.ui_type
            C.area.ui_type = 'ShaderNodeTree'

            O.node.nw_add_textures_for_principled(filepath=baseColor_texture, directory=folder+'/', files=shader_textures, relative_path=True)

            C.area.ui_type = old_type

def main(context):
    ShadersConverter()


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
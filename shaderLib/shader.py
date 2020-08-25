import shaderLib.texture as tx
import bpy

C = bpy.context
D = bpy.data
O = bpy.ops


class ShadersConverter(object):
    def __init__(self, removeDuplicateShaders=True):
        self.folderManager = tx.ProjectFolder()
        self.complete_material_list = []

        model_collection = D.collections['Model']
        objects = model_collection.objects

        if removeDuplicateShaders:
            print('------- REMOVE DUPLICATE -------')
            for obj in objects:
                self.removeDuplicateShader(obj)
            bpy.ops.outliner.orphans_purge()
            bpy.ops.outliner.orphans_purge()
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
                if 'fire' not in str(slot.material.name).lower():
                    C.object.active_material_index = idx
                    if slot.material not in self.complete_material_list:
                        ShaderPBRConverter(slot.material, self.folderManager.get_images(), str(self.folderManager.texture_folder)+'/')
                        self.complete_material_list.append(slot.material)


class RemoveDuplicateShader(object):
    def __init__(self, collection='Model'):
        self.material_index = {}

        model_collection = D.collections[collection]
        objects = model_collection.objects

        self.build_material_index(objects)
        self.remove_duplicates(objects)

        bpy.ops.outliner.orphans_purge()
        bpy.ops.outliner.orphans_purge()

    def build_material_index(self, objects, sort=True):
        for obj in objects:
            self.select(obj)
            material_slots = bpy.context.object.material_slots
            for idx, slot in zip(range(0, len(material_slots)), material_slots):
                material = slot.material
                material_name = material.name
                links = material.node_tree.links
                texture_name = self.get_texture_name(links)

                if not texture_name in self.material_index.keys():
                    self.material_index[texture_name] = [material_name]
                else:
                    self.material_index[texture_name].append(material_name)

        if sort:
            for key, value in self.material_index.items():
                value.sort()

    def remove_duplicates(self, objects):
        for obj in objects:
            self.select(obj)
            material_slots = bpy.context.object.material_slots
            for idx, slot in zip(range(0, len(material_slots)), material_slots):
                material = slot.material
                material_name = material.name
                links = material.node_tree.links
                texture_name = self.get_texture_name(links)

                if texture_name in self.material_index.keys():
                    original_name = self.material_index[texture_name][0]
                    mat = bpy.data.materials.get(original_name)
                    slot.material = mat


    def get_texture_name(self, links):
        """
        Get texture base name: concrete_BaseColor.png > concrete
        :return: (str) texture base name
        """
        baseColor_texture_fullpath = ''
        for l in links:
            if isinstance(l.from_node, bpy.types.ShaderNodeTexImage):
                baseColor_texture_fullpath = tx.getTextureFromNode(l.from_node.image.filepath)

                return tx.getTextureBaseName(baseColor_texture_fullpath.stem)
        return None

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


class ShaderPBRConverter(object):
    def __init__(self, material, img_list, sourceimages):
        self.material = material
        self.shader_node = material.node_tree.nodes['Principled BSDF']
        self.links = material.node_tree.links

        self.texture_base_name = self.get_texture_base_name()
        self.shader_texture_list = self.texture_filter(img_list)
        #self.node_wrangle_texture_dict = self.node_wrangler_texture_dict(self.shader_texture_list)

        print('MATERIAL: ', self.material)
        if self.shader_texture_list:
            print(' -- Material Texture', self.texture_base_name)
            #self.build_node_wrangler_principled_bsdf(sourceimages, str(self.texture_base_name), self.node_wrangle_texture_dict)
            PrincipledBSDF(self.material, sourceimages, self.shader_texture_list)
        else:
            print(' -- Empty Material', self.texture_base_name)

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
        return None

    def texture_filter(self, img_list):
        shader_texture_list = []
        if self.texture_base_name:
            for img in img_list:
                if self.texture_base_name in tx.getTextureFromNode(img).stem:
                    shader_texture_list.append(img)

            if shader_texture_list:
                return shader_texture_list

        return None

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


class PrincipledBSDF(object):
    base_color_name_list = str('diffuse diff albedo base col color basecolor').split(' ')
    subsurface_color_name_list = str('sss subsurface').split(' ')
    metallic_name_list = str('metallic metalness metal mtl').split(' ')
    specular_name_list = str('specularity specular spec spc').split(' ')
    roughness_name_list = str('roughness rough rgh').split(' ')
    gloss_name_list = str('gloss glossy glossiness').split(' ')
    normal_name_list = str('normal nor nrm nrml norm').split(' ')
    bump_name_list = str('bump bmp').split(' ')
    displacement_name_list = str('displacement displace disp dsp height heightmap').split(' ')
    trasmission_name_list = str('opacity').split(' ')
    alpha_name_list = str('alpha').split(' ')
    emission_name_list = str('emission').split(' ')

    diffuse = 0
    subsurface = 1

    metallic = 4
    specular = 5

    roughness = 7

    trasmission = 15
    emission = 17
    alpha = 18
    normal = 19

    def __init__(self, material, folder, shader_textures):
        self.channel_list = [self.base_color_name_list,
                             self.subsurface_color_name_list,
                             self.metallic_name_list,
                             self.specular_name_list,
                             self.roughness_name_list,
                             self.gloss_name_list,
                             self.emission_name_list,
                             self.alpha_name_list,
                             self.bump_name_list,
                             self.normal_name_list,
                             self.displacement_name_list]

        self.material = material
        self.shader_node = self.material.node_tree.nodes['Principled BSDF']
        self.uv_node = self.material.node_tree.nodes.new('ShaderNodeTexCoord')
        self.mapping_node = self.material.node_tree.nodes.new('ShaderNodeMapping')

        self.links = self.material.node_tree.links
        self.links.new(self.uv_node.outputs[2], self.mapping_node.inputs[0])

        # def specular
        self.shader_node.inputs[self.specular].default_value = 0.5
        self.shader_node.inputs[self.roughness].default_value = 0.05

        self.folder = folder
        self.connect_textures(shader_textures)

    def connect_textures(self, textures):
        for tex in textures:
            channel = str(tex.split('.')[0]).split('_')[-1]
            print('Texture: ', tex, ' -- Channel: ', channel)
            if channel.lower() in self.base_color_name_list:
                self.connect_color(tex)
            if channel.lower() in self.metallic_name_list:
                self.connect_noncolor(tex, self.metallic)
            if channel.lower() in self.specular_name_list:
                self.connect_noncolor(tex, self.specular)
            if channel.lower() in self.roughness_name_list:
                self.connect_noncolor(tex, self.roughness)
            if channel.lower() in self.gloss_name_list:
                self.connect_noncolor(tex, self.roughness, invert=True)
            if channel.replace('-OGL', '').lower() in self.normal_name_list:
                self.connect_normal(tex)
            if channel.lower() in self.trasmission_name_list:
                self.connect_noncolor(tex, self.trasmission)

    def connect_color(self, texture, socket=0):
        img_datablock = bpy.data.images.load(self.folder + texture)

        diffuse_node = self.material.node_tree.nodes.new('ShaderNodeTexImage')
        diffuse_node.image = img_datablock
        diffuse_node.image.colorspace_settings.name = 'sRGB'  # 'Non-Color'

        self.links.new(self.mapping_node.outputs[0], diffuse_node.inputs[0])
        self.links.new(diffuse_node.outputs[0], self.shader_node.inputs[socket])

    def connect_noncolor(self, texture, socket, invert=False):
        img_datablock = bpy.data.images.load(self.folder + texture)

        if not invert:
            diffuse_node = self.material.node_tree.nodes.new('ShaderNodeTexImage')
            diffuse_node.image = img_datablock
            diffuse_node.image.colorspace_settings.name = 'Non-Color'

            self.links.new(self.mapping_node.outputs[0], diffuse_node.inputs[0])
            self.links.new(diffuse_node.outputs[0], self.shader_node.inputs[socket])
        else:
            diffuse_node = self.material.node_tree.nodes.new('ShaderNodeTexImage')
            invert_node = self.material.node_tree.nodes.new('ShaderNodeInvert')
            diffuse_node.image = img_datablock
            diffuse_node.image.colorspace_settings.name = 'Non-Color'  # 'Non-Color'

            self.links.new(self.mapping_node.outputs[0], diffuse_node.inputs[0])
            self.links.new(diffuse_node.outputs[0], invert_node.inputs[1])
            self.links.new(invert_node.outputs[0], self.shader_node.inputs[7])

    def connect_normal(self, texture, socket=19):
        img_datablock = bpy.data.images.load(self.folder + texture)

        diffuse_node = self.material.node_tree.nodes.new('ShaderNodeTexImage')
        normalMap_node = self.material.node_tree.nodes.new('ShaderNodeNormalMap')
        diffuse_node.image = img_datablock
        diffuse_node.image.colorspace_settings.name = 'Non-Color'  # 'Non-Color'

        self.links.new(self.mapping_node.outputs[0], diffuse_node.inputs[0])
        self.links.new(diffuse_node.outputs[0], normalMap_node.inputs[1])
        self.links.new(normalMap_node.outputs[0], self.shader_node.inputs[socket])

    def connect_displacement(self, texture, socket):
        pass


class ShadersConverterOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "materials.shaders_converter"
    bl_label = "Shaders PBR Converter"
    #bl_context = "node"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ShadersConverter()
        return {'FINISHED'}

class RemoveDuplicateShaderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "materials.shaders_duplicate_remover"
    bl_label = "Remove Duplicate Shader"
    #bl_context = "node"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        RemoveDuplicateShader()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ShadersConverterOperator)
    bpy.utils.register_class(RemoveDuplicateShaderOperator)


def unregister():
    bpy.utils.unregister_class(ShadersConverterOperator)
    bpy.utils.unregister_class(RemoveDuplicateShaderOperator)


if __name__ == "__main__":
    register()

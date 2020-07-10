import os, glob, platform
import pathlib
import bpy


C = bpy.context
D = bpy.data
O = bpy.ops


def buildImgList(path):
    imgList = []
    os.chdir(path)
    for file in glob.glob('*.png'):
        imgList.append(file)

    return imgList

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

def removeDuplicateShader(collection='Model'):
    model_collection = D.collections[collection]
    objects = model_collection.objects

    for obj in objects:
        # print(obj)
        select(obj)
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

def buildPrincipledBSF(path, fullImgList, material):
    shader_node = material.node_tree.nodes['Principled BSDF']
    links = material.node_tree.links

    # file path
    folder = path
    baseColor_texture_path = ''
    for l in links:
        if isinstance(l.from_node, bpy.types.ShaderNodeTexImage):
            baseColor_texture_path = pathlib.Path(l.from_node.image.filepath)

    # filter images
    if baseColor_texture_path != '':
        imgList = []
        for img in fullImgList:
            img_name = '_'.join(img.split('_')[:-1])
            if img_name in str(baseColor_texture_path) and img_name != '':
                print('--IMG NAME: ', img, ' --- Match: ', img_name)
                imgList.append(img)

        imgDictList = []
        for i in imgList:
            imgDict = {'name': i, 'name': i}
            imgDictList.append(imgDict)

        print('IMG DICT LIST: ')
        print(imgDictList)


        # build Principled BSDF
        old_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'ShaderNodeTree'
        nodes = material.node_tree.nodes
        nodes.active = shader_node
        try:
            bpy.ops.node.nw_add_textures_for_principled(filepath=baseColor_texture_path, directory=folder, files=imgList, relative_path=True)
        except:
            pass
        bpy.context.area.ui_type = old_type

def main(context):
    if platform.system() == 'Windows':
        sourceimages_folder = pathlib.Path('D:\Lorenzo\Qsync\Project\Inn\sourceimages')
    else:
        sourceimages_folder = pathlib.Path('/Users/lorenzoargentieri/Qsync/Project/Inn/sourceimages')

    print('------------ START --------------')
    matList = D.materials
    fullImgList = buildImgList(sourceimages_folder)

    for mat in matList:
        if mat.name != 'Dots Stroke':
            print('MATERIAL: ', mat.name)
            buildPrincipledBSF(sourceimages_folder, fullImgList, mat)


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
import bpy

C = bpy.context
D = bpy.data
O = bpy.ops


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

def waxUpgrade(material):
    if str('Wax').lower() in str(material.name).lower():
        print('------- WAX UPGRADE -------')
        shader_node = material.node_tree.nodes['Principled BSDF']
        shader_node.inputs[1].default_value = 0.25
        shader_node.inputs[2].default_value[0] = 0.2
        shader_node.inputs[2].default_value[1] = 0.2
        shader_node.inputs[2].default_value[2] = 0.2

        #sheen
        shader_node.inputs[10].default_value = 1
        #clearcoat
        shader_node.inputs[12].default_value = 0.5

def glassUpgrade(material):# input 15
    if str('Glass_Bottle').lower() in str(material.name).lower() or str('content_Bottle').lower() in str(material.name).lower():
        print('------- GLASS UPGRADE -------')
        shader_node = material.node_tree.nodes['Principled BSDF']
        shader_node.inputs[15].default_value = 1

def candleUpgrade(material):
    if str('LightSphere_Flame').lower() in str(material.name).lower():
        print('------- LIGHT UPGRADE -------')
        material_output = material.node_tree.nodes['Material Output']
        shader_node = material.node_tree.nodes['Principled BSDF']
        links = material.node_tree.links

        mix_shader = material.node_tree.nodes.new('ShaderNodeMixShader')
        light_path_node = material.node_tree.nodes.new('ShaderNodeLightPath')
        transparent_shader = material.node_tree.nodes.new('ShaderNodeBsdfTransparent')

        links.new(light_path_node.outputs[0], mix_shader.inputs[0])
        links.new(shader_node.outputs[0], mix_shader.inputs[1])
        links.new(transparent_shader.outputs[0], mix_shader.inputs[2])
        links.new(mix_shader.outputs[0], material_output.inputs[0])

        for l in links:
            if isinstance(l.from_node, bpy.types.ShaderNodeBsdfPrincipled):
                links.remove(l)

    if str('flame_Flame').lower() in str(material.name).lower():
        print('------- FLAME UPGRADE -------')
        shader_node = material.node_tree.nodes['Principled BSDF']
        links = material.node_tree.links

        blackbody_node = material.node_tree.nodes.new('ShaderNodeBlackbody')
        blackbody_node.inputs[0].default_value = 2250

        links.new(blackbody_node.outputs[0], shader_node.inputs[17])

def fixFabric(material):
    if str('M-Fabric').lower() in str(material.name).lower():
        print('------- FABRIC FIX -------')
        shader_node = material.node_tree.nodes['Principled BSDF']
        links = material.node_tree.links

        l = shader_node.inputs['Transmission'].links[0]
        links.remove(l)


def matIterator():
    model_collection = D.collections['Model']
    objects = model_collection.objects

    for obj in objects:
        select(obj)
        material_slots = bpy.context.object.material_slots
        for idx, slot in zip(range(0, len(material_slots)), material_slots):
            print('Material: ', slot.name)
            waxUpgrade(slot.material)
            glassUpgrade(slot.material)
            candleUpgrade(slot.material)
            fixFabric(slot.material)

if __name__ == '__main__':
    matIterator()


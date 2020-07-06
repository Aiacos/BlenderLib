import bpy

C = bpy.context
D = bpy.data

matList = D.materials


for mat in matList:
    path = ''
    name_base = ''
    
    links = mat.node_tree.links
    for l in links:
        if isinstance(l.from_node, bpy.types.ShaderNodeTexImage):
            texture_path = l.from_node.image.filepath
            textpath = '/'.join(texture_path.split('/')[:-1])
            textname = texture_path.split('/')[-1].split('.')[0].split('_')[:-1]
            
            path = textpath
            name_base = '_'.join(textname)
            
    print(name_base)
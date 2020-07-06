import bpy

C = bpy.context
D = bpy.data

def select(obj):
    #obj.select_set(True)

    # to select the object in the 3D viewport,
    # this way you can also select multiple objects

    bpy.context.view_layer.objects.active = obj
    # to set the active object
    

model_collection = D.collections['Model']
objects = model_collection.objects

for obj in objects:
    print(obj)
    select(obj)
    material_slots = bpy.context.object.material_slots
    for idx, slot in zip(range(0, len(material_slots)), material_slots):
        print(idx, slot)
        if slot.material.name[-3:].isnumeric():
            original_name = slot.material.name[:-4]
            mat = bpy.data.materials.get(original_name)
            
            slot.material = mat
        
        
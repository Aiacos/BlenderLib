import bpy

C = bpy.context
D = bpy.data
O = bpy.ops

scene = bpy.data.scenes['Scene']

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

renderCamList = ['Camera', 'Camera.001', 'Camera.003']
camList = [cam.name for cam in list(D.cameras)]

for cam in renderCamList:
    print(cam)
    if cam in camList:

        currentCam = D.objects[cam]
        currentCam.data.clip_start = 0.01
        select(currentCam)


        # render settings
        scene.camera = currentCam
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = "F:/image.png"
        bpy.ops.render.render(write_still=True)


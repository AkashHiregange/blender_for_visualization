import bpy
import time

'''
Helper script for command line rendering of images from all the scenes in .blend file. The script loops over all
the scenes and all the cameras within each scene. Change the render engine to a desired one from one of the following:
CYCLES for cycles
BLENDER_EEVEE_NEXT for eevee
BLENDER_WORKBENCH_NEXT for workbench
'''

start = time.time()
scenes = bpy.data.scenes

for sc in scenes:
    bpy.context.window.scene = sc
    for a in sc.objects:
        if 'Camera' in a.name:
            #            print('in here')
            camera_name = a.name
            print(f"Rendering scene: {sc.name} with Camera: {camera_name}")
            sc.camera = a
            sc.render.engine = "BLENDER_EEVEE_NEXT"
            # sc.render.engine = "CYCLES"
            sc.cycles.samples = 128
            sc.cycles.device = "GPU"
            sc.render.filepath = f"images/{sc.name}_{camera_name}"
            bpy.ops.render.render(write_still=True)

end = time.time()

print('\n---------------------------')
print('Total time taken to render all the images: ', end - start)
print('---------------------------')


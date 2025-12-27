from import_geometry_file_to_viewport import create_structure_in_viewport, get_color
from ase.io import read
import bpy

# this bit of code is for visualizing a trajectory file where the atom characteristics (type, color, etc) does not
# change but the positions of atoms change in each image (like an MD trajectory). The best interpolation for such
# animation is the LINEAR interpolation.

traj = read("visual_benzene.traj", index=":")
nframes = len(traj)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = nframes

atoms0 = traj[0]
atom_objects = create_structure_in_viewport(atoms0)

for frame, atoms in enumerate(traj, start=1):
    print(frame)
    bpy.context.scene.frame_set(frame)

    positions = atoms.get_positions()

    for i, obj in enumerate(atom_objects):
        obj.location = positions[i]
        obj.keyframe_insert(data_path="location", frame=frame)
    

# this bit of code is for visualizing the benzene separation and also changing the color of few atoms in each animation
# frame. The original colors are first restored in each frame before changing the colors for the next frame.
# The best interpolation method for such case where atoms positions are not changed in CONSTANT interpolation.

traj = read("visual_benzene.traj", index=":")
nframes = len(traj)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = nframes

atoms0 = traj[0]
atom_objects = create_structure_in_viewport(atoms0)

carbon_ind_to_remove = [0, 2, 4]
number_of_carbon_remove = [1, 2, 3]
from itertools import combinations

combinations_list = []
for i in number_of_carbon_remove:
    temp_list = list(combinations(carbon_ind_to_remove, i))
    for j in temp_list:
        combinations_list.append(j)
print(combinations_list)

original_color_list = []
for i, obj in enumerate(atom_objects):
    mat = obj.data.materials[0]

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    #            if bsdf is None:
    #                print(obj.name, "has no Principled BSDF")
    #                continue

    color = tuple(bsdf.inputs["Base Color"].default_value)
    original_color_list.append(color)

for frame, atoms in enumerate(traj, start=1):
    print(frame)
    bpy.context.scene.frame_set(frame)
    #    bpy.ops.object.select_all(action='SELECT')
    #    bpy.ops.object.delete()
    #    create_structure_in_viewport(atoms)

    if frame <= 3:
        positions = atoms.get_positions()

        for i, obj in enumerate(atom_objects):
            obj.location = positions[i]
            obj.keyframe_insert(data_path="location", frame=frame)
            mat = obj.data.materials[0]
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].keyframe_insert(data_path="default_value", frame=frame)
    else:
        for i, obj in enumerate(atom_objects):
            mat = obj.data.materials[0]

            bsdf = mat.node_tree.nodes.get("Principled BSDF")

            bsdf.inputs["Base Color"].default_value = original_color_list[i] # change back to original colors before doing anything

            if i in combinations_list[frame - 4]:
                bsdf.inputs["Base Color"].default_value = (*get_color("N"), 1.0)

            bsdf.inputs["Base Color"].keyframe_insert(data_path="default_value", frame=frame)


'''
Old versions of code that might be helpful later
'''

# traj = read("visual_benzene.traj", index=":")
# nframes = len(traj)

# scene = bpy.context.scene
# scene.frame_start = 1
# scene.frame_end = nframes

# def delete_atoms():
#    for obj in list(bpy.data.objects):
#        if obj.name.startswith("Atom_"):
#            bpy.data.objects.remove(obj, do_unlink=True)

# for frame, atoms in enumerate(traj, start=1):
#    scene.frame_set(frame)

#    delete_atoms()
#    create_structure_in_viewport(atoms)

# -----------------------------------------------

# new_mat = make_material(get_color("N"))

# for i, obj in enumerate(atom_objects):
#    mat = obj.data.materials[0]

#    bsdf = mat.node_tree.nodes.get("Principled BSDF")
#    if bsdf is None:
#        print(obj.name, "has no Principled BSDF")
#        continue

#    color = bsdf.inputs["Base Color"].default_value
#    print(obj.name, "Base Color:", tuple(color))
#    if i in ind_to_color:
#        obj.data.materials[0] = new_mat
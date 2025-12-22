#ADD SPHERE IN BLENDER
import bpy

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,0))
obj = bpy.context.active_object
bpy.ops.object.shade_smooth()

# Create material
mat = bpy.data.materials.new("AtomMat")
mat.use_nodes = True

nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

bsdf = nodes.new("ShaderNodeBsdfPrincipled")
out  = nodes.new("ShaderNodeOutputMaterial")

color = (0.8, 0.4, 0.1, 1.0)

bsdf.inputs["Base Color"].default_value = color
links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

mat.diffuse_color = color

obj.data.materials.append(mat)
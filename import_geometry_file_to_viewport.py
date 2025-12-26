import sys
# sys.path.append("/home/akash/.local/lib/python3.12/site-packages")
# sys.path.append('/home/akash/venv-blender/lib/python3.12/site-packages')
sys.path.append('/home/akash/.local/lib/python3.11/site-packages')
import bpy
import numpy as np
from mathutils import Vector
from ase.io import read

print(sys.executable)
print(sys.path)

import ase
print(ase.__version__)

atoms = read("interface_Co3O4_TiO2_unoptimized.xyz")  # change file if needed
positions = atoms.get_positions()
symbols = atoms.get_chemical_symbols()
cell = atoms.cell

default_colors = {
    "H":  (1.0, 1.0, 1.0),
    "C":  (0.05, 0.05, 0.05),
    "N":  (0.1, 0.1, 1.0),
    "O":  (1.0, 0.05, 0.05),
    "F":  (0.56,0.87,0.31),
    "Co": (0.94,0.56,0.62),
    "Ti": (0.74, 0.76, 0.78),
    "Cu": (1.0, 0.85, 0.2),
} # we can add more colors based on Jmol color conventions

def get_color(sym):
    return default_colors.get(sym, (0.6, 0.6, 0.6))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


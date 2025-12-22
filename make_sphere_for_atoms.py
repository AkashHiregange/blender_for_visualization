import os
from ase.io import read
import pickle
import numpy as np
from pymatgen.analysis.elasticity import  diff_fit
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.analysis.elasticity import stress
from pymatgen.core.structure import Structure
from pymatgen.analysis.elasticity.elastic import ElasticTensorExpansion
from ase.build import make_supercell
home = os.getcwd()

ase_atoms_eq = read('CoO_RS_NM_pri_Opt_rSCAN.traj')
t = np.array([[-1, 1, 1],[1, -1, 1],[1, 1, -1]])
ase_atoms_eq = make_supercell(ase_atoms_eq, t)

structure = AseAtomsAdaptor.get_structure(ase_atoms_eq)
with open('strain_tensor.pkl', 'rb') as fp:
    strain_tensor = pickle.load(fp)


def read_strain_tensor_from_pkl(pkl_file):
    with open(pkl_file, 'rb') as fp:
        strain_tensor = pickle.load(fp)
    return strain_tensor

def read_stress_from_outputs(output_file_type=None,aims_out_file=False):
    file_ext = ['.traj', '.xyz']
    if output_file_type is not None:
        if output_file_type in file_ext:
            stress_list = []
            for defor in os.listdir():
                if os.path.isdir(f'{home}/{defor}'):
                    for file in os.listdir(f'{home}/{defor}'):
                        if file.endswith(output_file_type):
                            atoms = read(f'{home}/{defor}/{file}')
                            stress = atoms.get_stress(voigt=False)
                            stress_list.append(stress)
        else:
            raise ValueError(
                f'The file extension provided is not supported. Please make sure it is one of the following'
                f'{file_ext}')

        stress_tensor = np.array(stress_list)

        return stress_tensor

    elif aims_out_file:
        stress_list = []
        for defor in os.listdir():
            if os.path.isdir(f'{home}/{defor}'):
                for file in os.listdir(f'{home}/{defor}'):
                    if file.endswith('.out'):
                        pass
                        # f = open(f'{home}/{defor}/{file}', 'r')
                        # # print(f'{home}/{defor}/')
                        # # print('reading')
                        # stress = []
                        # # manually searching for stress components in aims.out file. Hopefully there is a better way to do it.
                        # lines = f.readlines()
                        # search_str = '  |                    Cartesian components [eV/A**3]                 |\n'
                        # if search_str in lines:
                        #     # print(lines.index(search_str))
                        #     index = lines.index(search_str)
                        #     stress.append(float(lines[index + 4].split()[2]))
                        #     stress.append(float(lines[index + 4].split()[3]))
                        #     stress.append(float(lines[index + 4].split()[4]))
                        #     stress.append(float(lines[index + 5].split()[2]))
                        #     stress.append(float(lines[index + 5].split()[3]))
                        #     stress.append(float(lines[index + 5].split()[4]))
                        #     stress.append(float(lines[index + 6].split()[2]))
                        #     stress.append(float(lines[index + 6].split()[3]))
                        #     stress.append(float(lines[index + 6].split()[4]))
                        #
                        # try:
                        #     stress = np.array(stress).reshape(3,3)
                        #     stress_list.append(stress)
                        #     # print(stress)
                        #     f.close()
                        # except Exception as e:
                        #     print('Error encountered. See the message below')
                        #     print(e)
                        #     f.close()

        stress_tensor = np.array(stress_list)

        return stress_tensor

    else:
        raise Exception(f'There was an error reading the output file. The arguments passed to the function were '
              f'{output_file_type=}, {aims_out_file=}. Make sure one of them is set to find an output file.')


def compute_elasticity_tensor(strain_tensor,stress_tensor,write_elasticity_tensor=True,write_output=True):
    elasticity_tensor = diff_fit(strain_tensor, stress_tensor, order=2)
    print(np.unique(np.array(elasticity_tensor[0]), return_index=True)[0] * 160.2716621)

    if write_output:
        try:
            f = open('elasticity_tensor_calculation_output.txt', 'x')
            f.close()
        except:
            print('The file already exists. Overwriting the file...')

        f = open('elasticity_tensor_calculation_output.txt', 'w')
        f.write(str(np.round(np.unique(np.array(elasticity_tensor[0]), return_index=True)[0],3) * 160.2176621) + '\n')
        f.write(str(np.round(np.unique(np.array(elasticity_tensor[0]), return_index=True)[0],3)) + '\n')
        f.write('Elasticity tensor in full. The above values show the unique values in the tensor.\n')
        f.write(str(np.array(elasticity_tensor[0])) + '\n')
        f.write('Stress tensor for all deformations in full. Shape is Nx3x3 where N is the number of deformations '
                'used to compute the elasticity tensor.\n')
        f.write(str(stress_tensor)+'\n')
        f.write(str(stress_tensor.shape)+'\n')
        f.write('Strain tensor for all deformations in full. Shape is Nx3x3 where N is the number of deformations '
                'used to compute the elasticity tensor.\n')
        f.write(str(strain_tensor)+'\n')
        f.write(str(strain_tensor.shape)+'\n')
        f.close()

    if write_elasticity_tensor:
        with open('elasticity_tensor.pkl', 'wb') as fp:
            pickle.dump(np.array(elasticity_tensor[0]), fp)

    return elasticity_tensor




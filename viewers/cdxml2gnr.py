# pylint: disable=no-member
"""Widget to convert SMILES to nanoribbons."""

import numpy as np
from scipy.stats import mode
import re

from IPython.display import clear_output
import ipywidgets as ipw
import nglview

from traitlets import Instance

from ase import Atoms
from ase.data import covalent_radii,chemical_symbols
from ase.neighborlist import NeighborList
import ase.neighborlist


from sklearn import manifold, datasets
from sklearn.decomposition import PCA
try:
    from openbabel import pybel as pb
except ImportError:
    import pybel as pb



class CdxmlUpload2GnrWidget(ipw.VBox):
    """Class that allows to upload structures from user's computer."""
    structure = Instance(Atoms, allow_none=True)

    def __init__(self, title='CDXML to GNR', description="Upload Structure"):
        try:
            import openbabel  # pylint: disable=unused-import
        except ImportError:
            super().__init__(
                [ipw.HTML("The SmilesWidget requires the OpenBabel library, "
                          "but the library was not found.")])
            return
        
        self.title = title
        self.mols=None
        self.original_structure = None
        self.selection = set()        
        self.file_upload = ipw.FileUpload(description=description, multiple=False, layout={'width': 'initial'})
        supported_formats = ipw.HTML(
            """<a href="https://pubs.acs.org/doi/10.1021/ja0697875" target="_blank">
        Supported structure formats: ".cdxml"
        </a>""")
        
        self.file_upload.observe(self._on_file_upload, names='value')
        
        self.allmols = ipw.Dropdown(options=[None],description='Select mol',value=None, disabled=True)
        self.allmols.observe(self._on_sketch_selected)
        
        super().__init__(children=[self.file_upload, supported_formats,self.allmols])


    @staticmethod
    def guess_scaling_factor(atoms):
        """Scaling factor to correct the bond length."""

        # Set bounding box as cell.
        c_x = 1.5 * (np.amax(atoms.positions[:, 0]) - np.amin(atoms.positions[:, 0]))
        c_y = 1.5 * (np.amax(atoms.positions[:, 1]) - np.amin(atoms.positions[:, 1]))
        c_z = 15.0
        atoms.cell = (c_x, c_y, c_z)
        atoms.pbc = (True, True, True)

        # Calculate all atom-atom distances.
        c_atoms = [a for a in atoms if a.symbol[0] == "C"]
        n_atoms = len(c_atoms)
        dists = np.zeros([n_atoms, n_atoms])
        for i, atom_a in enumerate(c_atoms):
            for j, atom_b in enumerate(c_atoms):
                dists[i, j] = np.linalg.norm(atom_a.position - atom_b.position)

        # Find bond distances to closest neighbor.
        dists += np.diag([np.inf] * n_atoms)  # Don't consider diagonal.
        bonds = np.amin(dists, axis=1)

        # Average bond distance.
        avg_bond = float(mode(bonds)[0])

        # Scale box to match equilibrium carbon-carbon bond distance.
        cc_eq = 1.4313333333
        return cc_eq / avg_bond 
    
    @staticmethod    
    def scale(atoms, s):
        """Scale atomic positions by the `factor`."""
        c_x, c_y, c_z = atoms.cell
        atoms.set_cell((s * c_x, s * c_y, c_z), scale_atoms=True)
        atoms.center()
        return atoms
 
    @staticmethod    
    def pybel2ase(mol):  
        """converts pybel molecule into ase Atoms"""
        asemol = Atoms()
        species=[chemical_symbols[atm.atomicnum] for atm in mol.atoms]
        pos=np.asarray([atm.coords for atm in mol.atoms])
        pca = PCA(n_components=3)
        posnew=pca.fit_transform(pos)
        atoms = Atoms(species, positions=posnew)
        sys_size = np.ptp(atoms.positions,axis=0)
        atoms.rotate(-90, 'z') #cdxml are rotated
        atoms.pbc=True
        atoms.cell = sys_size + 10
        atoms.center()

        return atoms

    @staticmethod    
    def construct_cell(atoms, id1, id2):
        """Construct periodic cell based on two selected equivalent atoms."""

        pos = [[atoms[id2].x, atoms[id2].y], [atoms[id1].x, atoms[id1].y], [atoms[id2].x + int(1), atoms[id1].y]]

        vec = [np.array(pos[0]) - np.array(pos[1]), np.array(pos[2]) - np.array(pos[1])]
        c_x = np.linalg.norm(vec[0])

        angle = np.math.atan2(np.linalg.det([vec[0], vec[1]]), np.dot(vec[0], vec[1]))
        if np.abs(angle) > 0.01:
            atoms.rotate_euler(center=atoms[id1].position, phi=-angle, theta=0.0, psi=0.0)

        c_y = 15.0 + np.amax(atoms.positions[:, 1]) - np.amin(atoms.positions[:, 1])
        c_z = 15.0 + np.amax(atoms.positions[:, 2]) - np.amin(atoms.positions[:, 2])

        atoms.cell = (c_x, c_y, c_z)
        atoms.pbc = (True, True, True)
        atoms.center()
        atoms.wrap(eps=0.001)
        

        # Remove redundant atoms. ORIGINAL
        tobedel = []

        n_l = NeighborList([covalent_radii[a.number] for a in atoms], bothways=False, self_interaction=False)
        n_l.update(atoms)

        for atm in atoms:
            indices, offsets = n_l.get_neighbors(atm.index)
            for i, offset in zip(indices, offsets):
                dist = np.linalg.norm(atm.position - (atoms.positions[i] + np.dot(offset, atoms.get_cell())))
                if dist < 0.4:
                    tobedel.append(atoms[i].index)

        del atoms[tobedel]

        # Find unit cell and apply it.

        ## Add Hydrogens.
        n_l = NeighborList([covalent_radii[a.number] for a in atoms], bothways=True, self_interaction=False)
        n_l.update(atoms)

        need_hydrogen = []
        for atm in atoms:
            if len(n_l.get_neighbors(atm.index)[0]) < 3:
                if atm.symbol == 'C' or atm.symbol=='N' :
                    need_hydrogen.append(atm.index)

        print("Added missing Hydrogen atoms: ", need_hydrogen)

        for atm in need_hydrogen:
            vec = np.zeros(3)
            indices, offsets = n_l.get_neighbors(atoms[atm].index)
            for i, offset in zip(indices, offsets):
                vec += -atoms[atm].position + (atoms.positions[i] + np.dot(offset, atoms.get_cell()))
            vec = -vec / np.linalg.norm(vec) * 1.1 + atoms[atm].position
            atoms.append(ase.Atom('H', vec))

        return atoms

        
    def _on_file_upload(self, change=None):
        """When file upload button is pressed."""
        self.mols=None
        listmols = []
        molid = 0
        for fname, item in change['new'].items():
            frmt = fname.split('.')[-1]
            if frmt == 'cdxml':
                cdxml_file_string = self.file_upload.value[fname]['content'].decode('ascii')
                self.mols=re.findall('<fragment(.*?)/fragment', cdxml_file_string, re.DOTALL)
                for m in self.mols:
                    m = pb.readstring('cdxml','<fragment'+m+'/fragment>')
                    self.mols[molid] = m
                    listmols.append((str(molid)+': '+m.formula, molid)) ## m MUST BE a pb object!!!
                    molid += 1
                self.allmols.options = listmols  
                self.allmols.value = 0
                self.allmols.disabled=False
            break  
            
    def _on_sketch_selected(self,change=None):
        self.structure = None #needed to empty view in second viewer
        if self.mols is None or self.allmols.value is None:
            return
        atoms = self.pybel2ase(self.mols[self.allmols.value])
        factor = self.guess_scaling_factor(atoms)
        struct = self.scale(atoms, factor)
        self.structure = struct
        self.file_upload.value.clear()        


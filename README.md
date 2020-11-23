[![DOI](https://zenodo.org/badge/188820720.svg)](https://zenodo.org/badge/latestdoi/188820720)

# Materials Cloud - Empa MFH TB App

This [Materials Cloud jupyter](https://jupyter.materialscloud.org) app is a GUI fto compute 
MFH TB of nanographenes

Python library to perform tight-binding mean field Hubbard calculations on the conjugated π-networks of organic systems.
Only carbon atoms are supported and each atom is modelled by a single p<sub>z</sub> orbital hosting a single electron.

The modelled Hamiltonian is the following:

![](https://latex.codecogs.com/svg.latex?\dpi{280}\large{\hat{H}_\text{MFH}=-t\sum\limits_{\langle{i,j}\rangle,\sigma}\left(\hat{c}^{\dag}_{i,\sigma}\hat{c}_{j,\sigma}+\text{h.c.}\right)+U\sum\limits_{i,\sigma}\langle{\hat{n}_{i,\sigma}}\rangle%20\hat{n}_{i,\overline{\sigma}}-U\sum\limits_{i}\langle{\hat{n}_{i,\uparrow}}\rangle\langle{\hat{n}_{i,\downarrow}}\rangle,})

where c<sup>†</sup>, c and n are respectively the creation, annihiliation and number operators, t is the hopping integral and U denotes the on-site Coulomb repulsion.

Refer to https://github.com/eimrek/tb-mean-field-hubbard.

## Uploading a new structure
File formats compatible with [ASE](https://wiki.fysik.dtu.dk/ase/) can be used.
In the example a .mol file for a structure is generated with ChemDraw. 

The structure is uploaded, a warning message is provided if similar structures were already computed.

The structure is stored in the database.

The structure created with ChemDraw is properly scaled to conventional C-C sp2 bond lengths.

A unit cell is created identifying two equivalent atoms in the edited (scaled) structure.


## Contact

For inquiries concerning Materials Cloud, please use the [public issue tracker](https://github.com/materialscloud-org/issues).
For inquiries concerning the Empa Nanoribbon App, please contact [carlo.pignedoli@empa.ch](mailto:carlo.pignedoli@empa.ch).

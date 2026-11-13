# AiiDAlab - Empa TB MFH app

This [Materials Cloud jupyter](https://jupyter.materialscloud.org) app provides a convenient graphical user interface (GUI) around the tight binding (TB) mean field Hubbard (MFH) library found at https://github.com/eimrek/tb-mean-field-hubbard. The library performs TB MFH calculations on the conjugated π-networks of organic systems.
Only carbon atoms are supported and each atom is modelled by a single p<sub>z</sub> orbital hosting a single electron.

The modelled Hamiltonian is the following:

![](https://latex.codecogs.com/svg.latex?\dpi{280}\large{\hat{H}_\text{MFH}=-t\sum\limits_{\langle{i,j}\rangle,\sigma}\left(\hat{c}^{\dag}_{i,\sigma}\hat{c}_{j,\sigma}+\text{h.c.}\right)+U\sum\limits_{i,\sigma}\langle{\hat{n}_{i,\sigma}}\rangle%20\hat{n}_{i,\overline{\sigma}}-U\sum\limits_{i}\langle{\hat{n}_{i,\uparrow}}\rangle\langle{\hat{n}_{i,\downarrow}}\rangle,})

where c<sup>†</sup>, c and n are respectively the creation, annihiliation and number operators, t is the hopping integral and U denotes the on-site Coulomb repulsion.


## Software attribution and scientific acknowledgements

Please credit [aiidalab-empa-tb-mfh](https://github.com/nanotech-empa/aiidalab-empa-tb-mfh) and its
[contributors](https://github.com/nanotech-empa/aiidalab-empa-tb-mfh/graphs/contributors),
and identify the release or immutable commit used. Existing author,
contributor and funding acknowledgements remain authoritative.

Preserve the copyright and permission notices in [LICENSE.txt](LICENSE.txt)
when copying or distributing copies or substantial portions of MIT-licensed
code. Separately licensed components retain their own notices. A name or
repository link does not replace the applicable licence notices.

For research using AiiDAlab, acknowledge its team and cite
[both platform papers](https://github.com/nanotech-empa/.github/blob/main/CITATION_GUIDANCE.md#aiidalab). When AiiDA workflows or
provenance also helped the research, follow the [AiiDA citation guidance](https://github.com/nanotech-empa/.github/blob/main/CITATION_GUIDANCE.md#aiida).

Retain credit to the [tb-mean-field-hubbard library](https://github.com/eimrek/tb-mean-field-hubbard) and its contributors, separately from this interface, and cite the scientific methods actually used.

The [shared credit guide](https://github.com/nanotech-empa/.github/blob/main/CITATION_GUIDANCE.md) keeps software attribution, licence
compliance and scientific citation requests separate. Scientific citation
requests are not additional MIT licence conditions.

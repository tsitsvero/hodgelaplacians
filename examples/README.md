# HodgeLaplacians

Output:
* Boundary operator matrices
* Hodge and Bochner Laplacians
* Combinatorial Forman-Ricci curvature
* Eigenvectors and Eigenvalues of Laplacians
* Higher order heat kernels and diffusion

Input:
* List of simplices
* Symplex tree with filtration values ([GUDHI format](http://gudhi.gforge.inria.fr/python/latest/simplex_tree_ref.html#gudhi.SimplexTree.get_skeleton))



## Example
```python
from hodgelaplacians import HodgeLaplacians

simplices = ((1,2,3), (2,3), (1,2,4), (6,3))

hl = HodgeLaplacians(simplices)
L1 = hl.getHodgeLaplacian(1)
```

Full example output is available in the [Jupyter notebook](examples/laplacians_combinatorial_data.ipynb).

## Docker file and running on Gitpod
This repository also contains Dockerfile based on Ubuntu 18.04 which contains basic python dependencies as well as installation of Gudhi library.

To run this repository with Dockerfile (all C++ and Python dependencies pre-loaded) on Gitpod type

![Open on Gitpod](/help/browser_field.gif "Open on Gitpod")

or simply press [https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians](https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians).

After you have [launched the workspace](https://misha.website/share/video/open_workspace.webm), you can simply [launch the Jupyter Lab](https://misha.website/share/video/open_examples_proteins.webm) to play with [examples and tutorials](https://github.com/tsitsvero/hodgelaplacians/tree/master/examples).


## Coming soon
* Random walks on simplicial complexes
* Tutorials on spectral theory of simplicial complexes
* Tutorials with point cloud examples
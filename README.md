# HodgeLaplacians

This package provides an interface for construction of Hodge and Bochner Laplacian matrices from the set of simplices.

`HodgeLaplacians` uses [sparse matrices](https://docs.scipy.org/doc/scipy/reference/sparse.html) `dok_matrix` and `csr_matrix` from `scipy.sparse module.` Eigenvalues and eigenvectors are computed using [Scipy ARPACK algorithm](https://docs.scipy.org/doc/scipy/reference/tutorial/arpack.html).

HodgeLaplacian class currently provides

Output:
* Boundary operator matrices
* Hodge and Bochner Laplacians
* Combinatorial Forman-Ricci curvature
* Eigenvectors and Eigenvalues of Laplacians
* Higher order heat kernels and diffusion

Input:
* List of simplices
* Symplex tree with filtration values ([GUDHI format](http://gudhi.gforge.inria.fr/python/latest/simplex_tree_ref.html#gudhi.SimplexTree.get_skeleton))


## Installation
```python
pip3 install hodgelaplacians
```

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

[]![Open on Gitpod](/help/browser_field.gif "Open on Gitpod")

or simply press [https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians](https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians).

## Dependencies
* Numpy
* Scipy

## Tutorials and packages on TDA

There are many tools available on Topological Data Analysis.

Here just a few introductory blog posts
* [Constructing Connectivities](https://datawarrior.wordpress.com/2015/09/14/tda-2-constructing-connectivities/)
* [Homology and Betti Numbers](https://datawarrior.wordpress.com/2015/11/03/tda-3-homology-and-betti-numbers/)

There is a wiki page with a [list of TDA packages](https://en.wikipedia.org/wiki/Persistent_homology#Computation).

## Coming soon
* Random walks on simplicial complexes
* Tutorials on spectral theory of simplicial complexes
* Tutorials with point cloud examples
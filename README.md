[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians)

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


## Mathematical Formulae

### Boundary Operator

The $d$-th boundary operator $\partial_d$ maps a $d$-simplex to an alternating signed sum of its $(d-1)$-faces:

$$\partial_d([v_0, \dots, v_d]) = \sum_{i=0}^{d} (-1)^i \, [v_0, \dots, \hat{v}_i, \dots, v_d]$$

where $\hat{v}_i$ denotes that vertex $v_i$ is omitted.

### Hodge Laplacian

Let $B_d$ denote the matrix of $\partial_d$. The $d$-th Hodge Laplacian is:

$$L_d = \begin{cases} B_1 B_1^\top & d = 0 \\ B_{d+1} B_{d+1}^\top + B_d^\top B_d & 0 < d < d_{\max} \\ B_d^\top B_d & d = d_{\max} \end{cases}$$

By the Hodge decomposition theorem, $\ker L_d \cong H_d$ — the $d$-th homology group of the complex.

### Bochner Laplacian

The Bochner Laplacian is obtained from $L_d$ via the **Weitzenböck decomposition**, replacing the diagonal with row-wise $\ell^1$ norms:

$$LB_d = L_d - \mathrm{diag}(L_d) + \mathrm{diag}(\|L_d\|_{\mathrm{row},1})$$

### Combinatorial Forman–Ricci Curvature

The discrete Ricci curvature of each $d$-simplex is the diagonal of the difference between the two Laplacians:

$$\mathrm{Ric}_d = \mathrm{diag}(L_d - LB_d)$$

### Heat Kernels

Heat diffusion on $d$-chains is governed by the matrix exponential:

$$H_d(t) = e^{-t\, L_d}, \qquad HB_d(t) = e^{-t\, LB_d}$$

### Chain Diffusion

A $d$-chain $c$ evolves under diffusion time $t$ as:

$$c(t) = H_d(t)\, c = e^{-t\, L_d}\, c \qquad \mathrm{(Hodge)}$$

$$c(t) = HB_d(t)\, c = e^{-t\, LB_d}\, c \qquad \mathrm{(Bochner)}$$

### Spectral Decomposition

Eigenvalues $\lambda$ and eigenvectors $v$ of the Laplacians satisfy:

$$L_d\, v = \lambda\, v \qquad \mathrm{(Hodge\ spectrum)}$$

$$LB_d\, v = \lambda\, v \qquad \mathrm{(Bochner\ spectrum)}$$

Computed efficiently using the ARPACK shift-invert method. Zero eigenvalues of $L_d$ count the independent $d$-dimensional holes (Betti numbers).

---

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

![Open on Gitpod](/help/browser_field.gif "Open on Gitpod")

or simply press [https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians](https://gitpod.io/#https://github.com/tsitsvero/hodgelaplacians).

After you have [launched the workspace](https://server.misha.website/share/video/open_workspace.webm), you can simply [launch the Jupyter Lab](https://server.misha.website/share/video/open_examples_proteins.webm) (please run "jupyter lab --ip 127.0.0.1" instead of just "jupyter lab") to play with [examples and tutorials](https://github.com/tsitsvero/hodgelaplacians/tree/master/examples).

See [video instructions](https://misha.website/2019/10/17/working-with-hodgelaplacians-class/) embedded on a single page.

## Dependencies
* Numpy
* Scipy

## More tutorials and packages on TDA

There are many tools available on Topological Data Analysis.

Here just a few introductory blog posts
* [Constructing Connectivities](https://datawarrior.wordpress.com/2015/09/14/tda-2-constructing-connectivities/)
* [Homology and Betti Numbers](https://datawarrior.wordpress.com/2015/11/03/tda-3-homology-and-betti-numbers/)

There is a wiki page with a [list of TDA packages](https://en.wikipedia.org/wiki/Persistent_homology#Computation).

## Coming soon
* Random walks on simplicial complexes
* Tutorials on spectral theory of simplicial complexes
* Tutorials with point cloud examples

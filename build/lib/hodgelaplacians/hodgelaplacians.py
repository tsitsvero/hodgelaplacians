
from functools import lru_cache
from scipy.sparse import dok_matrix
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs, eigsh
from scipy.sparse.linalg import norm
from scipy.sparse import diags

import numpy as np
from scipy.linalg import expm

from warnings import warn

from itertools import combinations


class HodgeLaplacians:
    """Class for construction of Hodge and Bochner Laplacians from either collection of simplices
    or simplicial tree."""
    def __init__(self, simplices, maxdimension=2, mode='normal'):
        self.mode = mode
        
        if mode == 'normal':
            self.import_simplices(simplices=simplices)
            max_simplex_size = len(max(self.face_set, key=lambda el: len(el)))
            if maxdimension > max_simplex_size-1:
                warn(f"Maximal simplex in the collection has size {max_simplex_size}. \n maxdimension is set to {max_simplex_size-1}")
                self.maxdim = max_simplex_size - 1
            elif maxdimension < 0:
                raise ValueError(f"maxdimension should be a positive integer!")
            else: 
                self.maxdim = maxdimension
                
        elif mode == 'gudhi':
            self.simplices = [tuple(a[0]) for a in simplices] # Removing filtration values
            self.face_set = self.simplices # Assume that the set of simplices is full
            max_simplex_size = len(max(self.face_set, key=lambda el: len(el)))
            if maxdimension > max_simplex_size-1:
                warn(f"Maximal simplex in the collection has size {max_simplex_size}. \n maxdimension is set to {max_simplex_size-1}")
                self.maxdim = max_simplex_size - 1
            elif maxdimension < 0:
                raise ValueError(f"maxdimension should be a positive integer!")
            else: 
                self.maxdim = maxdimension
        else:
            raise ValueError(f"Désolé... Import modes different from 'normal' and 'gudhi' are not implemented yet...")

            
    def import_simplices(self, simplices=[]):
        self.simplices = tuple(map(lambda simplex: tuple(sorted(simplex)), simplices))
        self.face_set = self._faces(self.simplices)
              
    def n_faces(self, n):
        return tuple(filter(lambda face: len(face) == n+1, self.face_set))

    def _faces(self, simplices):
        faceset = set()
        for simplex in simplices:
            numnodes = len(simplex)
            for r in range(numnodes, 0, -1):
                for face in combinations(simplex, r):
                    faceset.add(tuple(sorted(face)))
        return faceset
    
    def boundary_operator(self, i):
        source_simplices = self.n_faces(i)
        target_simplices = self.n_faces(i-1)

        if len(target_simplices) == 0:
            S = dok_matrix((1, len(source_simplices)), dtype=np.float64)
            S[0, 0:len(source_simplices)] = 1
        else:
            source_simplices_dict = {source_simplices[j]:
                                     j for j in range(len(source_simplices))}
            target_simplices_dict = {target_simplices[i]:
                                     i for i in range(len(target_simplices))}

            S = dok_matrix((len(target_simplices),
                            len(source_simplices)),
                           dtype=np.float64)
            for source_simplex in source_simplices:
                for a in range(len(source_simplex)):
                    target_simplex = source_simplex[:a]+source_simplex[(a+1):]
                    i = target_simplices_dict[target_simplex]
                    j = source_simplices_dict[source_simplex]
                    S[i, j] = -1 if a % 2 == 1 else 1   # S[i, j] = (-1)**a
        return S
   
    @lru_cache(maxsize=32)
    def getBoundaryOperator(self,d):
        if d >= 0 and d <= self.maxdim:
            return self.boundary_operator(d).tocsr()
        else:
            raise ValueError(f"d should be not greater than {self.maxdim} (maximal allowed dimension for simplices)")
    
    @lru_cache(maxsize=32)
    def getHodgeLaplacian(self,d):
        if d == 0:
            B_next = self.getBoundaryOperator(d+1)
            Bt_next = B_next.transpose()
            L = B_next.dot(Bt_next)
        elif d < self.maxdim:
            B_next = self.getBoundaryOperator(d+1)
            Bt_next = B_next.transpose()
            B = self.getBoundaryOperator(d)
            Bt = B.transpose()
            L = B_next.dot(Bt_next) + Bt.dot(B)
        elif d == self.maxdim:
            B = self.getBoundaryOperator(d)
            Bt = B.transpose()
            L = Bt.dot(B)
        else:
            raise ValueError(f"d should be not greater than {self.maxdim} (maximal dimension simplices)")
        return L
       
    def getBochnerLaplacian(self,d):
        LB = self.getHodgeLaplacian(d)
        LB = LB - diags(LB.diagonal())
        ddd = norm(LB, 1, 1)
        LB = LB + diags(ddd) # Weitzenböck decomposition 
        return LB
    
    @lru_cache(maxsize=32)
    def getHodgeHeatKernel(self,d,t):
        L = self.getHodgeLaplacian(d)
        L = L.multiply(t)
        return expm(L)
    
    @lru_cache(maxsize=32)
    def getBochnerHeatKernel(self,d,t):
        LB = self.getBochnerLaplacian(d)
        LB = L.multiply(t)
        return expm(L)
    
    def diffuseChainHodge(self, d, chain, t):
        HK = self.getHodgeHeatKernel(d,t)
        diff_chain = HK.dot(chain)
        return diff_chain
    
    def diffuseChainBochner(self, d, chain, t):
        HK = self.getBochnerHeatKernel(d,t)
        diff_chain = HK.dot(chain)
        return diff_chain
    
    def getCombinatorialRicci(self,d):
        L = self.getHodgeLaplacian(d)
        LB = self.getBochnerLaplacian(d)
        Ricci = L - LB
        Ricci = Ricci.diagonal()
        return Ricci    
    
    def getHodgeSpectrum(self, d, k, around_point=0.01):
        """Obtain k eigenvalues and eigenvectors of d-Hodge Laplacian.
        Eigenvalues and eigenvectors are computed sufficently fast 
        using Shift-Invert mode of the ARPACK algorithm in SciPy.
        More info: https://docs.scipy.org/doc/scipy/reference/tutorial/arpack.html"""
        L = self.getHodgeLaplacian(d)
        vals, vecs = eigsh(L, k=k, sigma=around_point, which='LM')
        vecs = vecs.transpose()
        return vals, vecs
  
    def getBochnerSpectrum(self, d, k, around_point=0.01):
        """Obtain k eigenvalues and eigenvectors of d-Hodge Laplacian.
        Eigenvalues and eigenvectors are computed sufficently fast 
        using Shift-Invert mode of the ARPACK algorithm in SciPy.
        More info: https://docs.scipy.org/doc/scipy/reference/tutorial/arpack.html"""
        LB = self.getBochnerLaplacian(d)
        vals, vecs = eigsh(LB, k=k, sigma=around_point, which='LM')
        vecs = vecs.transpose()
        return vals, vecs
      
    def randomWalkDistribution(self, d, chain_distribution, time):
        """To be implemented based on the work
        S. Mukherjee￼ and J. Steenbergen, 
        Random walks on simplicial complexes and harmonics
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5324709/"""
        pass
    
    def randomWalkChain(self, d, chain, time):
        """To be implemented based on the work
        S. Mukherjee￼ and J. Steenbergen, 
        Random walks on simplicial complexes and harmonics
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5324709/"""
        pass
        

import numpy as np
A = np.random.rand(4,3,3)
def slow_inverse(A): 
    Ainv = np.zeros_like(A)

    for i in range(A.shape[0]):
        Ainv[i] = np.linalg.inv(A[i])
    return Ainv

def fast_inverse(A):
    identity = np.identity(A.shape[2], dtype=A.dtype)
    Ainv = np.zeros_like(A)

    for i in range(A.shape[0]):
        Ainv[i] = np.linalg.solve(A[i], identity)
    return Ainv

def fast_inverse2(A):
    identity = np.identity(A.shape[2], dtype=A.dtype)

    return array([np.linalg.solve(x, identity) for x in A])

from numpy.linalg import lapack_lite
lapack_routine = lapack_lite.dgesv
# Looking one step deeper, we see that solve performs many sanity checks.  
# Stripping these, we have:
def faster_inverse(A):
    b = np.identity(A.shape[2], dtype=A.dtype)

    n_eq = A.shape[1]
    n_rhs = A.shape[2]
    pivots = zeros(n_eq, np.intc)
    identity  = np.eye(n_eq)
    def lapack_inverse(a):
        b = np.copy(identity)
        pivots = zeros(n_eq, np.intc)
        results = lapack_lite.dgesv(n_eq, n_rhs, a, n_eq, pivots, b, n_eq, 0)
        if results['info'] > 0:
            raise LinAlgError('Singular matrix')
        return b

    return array([lapack_inverse(a) for a in A])


print slow_inverse(A)
print fast_inverse(A)
print fast_inverse2(A)
print faster_inverse(A)
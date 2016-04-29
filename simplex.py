import copy
import numpy as np


# This algorithm requires additional output.
#
# OUTPUT description:
# You algorithms should return three things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A called AI, you can construct
#       it with:
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
# 3. the index set I for the optimal solution.
#
# return them with the statement: return (v, x, I)
##########################################################
def dual_simplex_reference(I, c, A, b):
    while True:
        AI = np.linalg.inv(A[:,I])
        xI = AI.dot(b)
        cbar = c - A.T.dot(AI.T.dot(c[I]))
        i_neg = np.where(xI < -1e-12)[0]
        if len(i_neg) == 0:
            x = np.zeros(c.shape[0])
            x[I] = xI
            return (c[I].dot(xI), x, I) # optimal
        v = A.T.dot(AI.T[:,i_neg[0]])
        if np.all(v > 1e-12):
            return (-float("inf"), np.zeros(shape[0]))
        # if v is positive, then we don't want to pick it
        # if v is zero, then we may want to pick it, so make it very small negative
        v[(v >= -1e-12) & (v <= 1e-12)] = -1e-12
        k = np.argmin(-(cbar+ 1e-8*np.random.rand(cbar.shape[0]))/(v) + 1e10*(v >= -1e-12))
        #print 'k, I[i_net[0]]'
        #print k, I[i_neg[0]]
        I[i_neg[0]] = k

# return the updated system as well as the solution
def add_constraint_reference(I,c,A,b,g,h):
    A = np.vstack([A, g])
    basis_vec = basis_vector_reference(b.shape[0]+1, b.shape[0])
    A = np.column_stack([A, basis_vec])
    b = np.append(b, h)
    I = np.append(I, [c.shape[0]])
    c = np.append(c, [0])
    return (A,b,c,dual_simplex_reference(I, c, A, b))

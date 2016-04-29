import numpy as np
import astar
import Queue as Q
import simplex
import random
#from scipy.optimize import linprog

############## create linear programming model ############## 
#creates A,b,vars (variables used in linear program)
#inputs:
# 	n : number of nodes in hamiltonian path 
def tsp_lp(n):
    num_vars = 0
    varsb = []
    for i in xrange(0,n):
	for j in xrange(0,n):
	   if (i!= j):
	     num_vars += 1
	     varsb += [(i,j)]
    for i in xrange(1,n):
	varsb += [(-1,i)]
    #slack variables
    for i in xrange(1,n):
	for j in xrange(1,n):
		if (i!=j):
			varsb += [(-i,-j)]

    #ensures out degree is 1
    A = []
    vb = []
    for j in xrange(0,n):
	c = []
	for ele in varsb:
	     (a,b) = ele
             if (a == -1):
		c += [0]
		continue
	     if (b == j):
		 c += [1]
	     else:
		c += [0]
	A += [c]
        vb+= [1]

    #ensures in degree is 1
    for i in xrange(0,n):
	c = []
	for ele in varsb:
	    (a,b) = ele
	    if (a == -1):
		c += [0]		
		continue

	    if (a == i):
		c += [1]
	    else:
		c += [0]
        A += [c]
	vb += [1]


     #ensures there are no subtours
    for i in xrange(1,n):
	for j in xrange(1,n):
            if (i!=j):
	    	c = []
	    	for ele in varsb:
			(a,b) = ele
		        if ((a == -1) and (b == i)):
				c += [1]
				continue
			if ((a == -1) and (b == j)):
				c += [-1]
				continue
			if ((a == i) and (b == j)):
				c += [n-1]
				continue
			if ((a == -i) and (b == -j)):
				c += [1]
				continue
			c += [0]
                A += [c]
		vb += [n-2]


    return np.array(A),np.array(vb),varsb

			
		
   

def get_c(graph,varsb):
    c = []
    for ele in varsb:
	(a,b) = ele
	if ((a >= 0) and (b>= 0)):
        	c += [astar.get_edge_weight(a,b,graph)]
   	else:
		c += [0]
    return np.array(c)


def get_bounds(varsb):
    bounds = []
    for ele in varsb:
	(a,b) = ele
	if ((a >= 0) and (b >= 0)):
		bounds += [(0,1)]
        else:
		bounds += [(0,None)]
    return tuple(bounds)

#return c,A,b
def get_lp(graph,n):
    A,b,varsb= tsp_lp(n)
    c = get_c(graph,varsb)
    bounds = get_bounds(varsb)
    return c,A,b,bounds



#weights  = dict[(start,goal)] = weight
def create_graph(n,weights):
    graph = astar.newGraph()
    nodes = []
    for i in xrange(0,n):
	nodes += [astar.createNode(i)]
        astar.addNode(nodes[i],graph)

    for i in xrange(0,n):
	for j in xrange(0,n):
	     if (i != j):
		astar.addEdge(nodes[i],nodes[j],weights[(i,j)],graph)

    return graph



def test(n):
    weights = {}
    for i in xrange(0,n):
        for j in xrange(0,n):
                weights[(i,j)] = 1
    graph = create_graph(n,weights)
    c,A,b = get_lp(graph,n)

    return c,A,b

#returns constraints for problem
def get_constraints(n,weights):
    graph = create_graph(n,weights)
    c,A,b,bounds = get_lp(graph,n)
    return c,A,b,bounds



   
	


   

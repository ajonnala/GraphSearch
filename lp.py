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
def create_constraints(n):
    num_vars = n-1
    varsb = [(0,i) for i in xrange(1,num_vars+1)]
    for i in xrange(1,n):
	num_vars += (n-2)
        nv = [(i,j) for j in xrange(1,n) if (i!=j)]
        varsb += nv

    num_slack = 0
    for i in xrange(1,n):
	num_slack += (n-2) - (i-1)

    cols_A = num_vars + num_slack
    A = []
    b = []

    #constrains that ensures there are only (n-1) edges picked
    c_1a = [1 for i in xrange(0,num_vars)]
    c_1b = [0 for i in xrange(0,num_slack)]
    c_1 = c_1a + c_1b
    A += [c_1]
    b += [n-1]

   #constraints that ensure each vertex only visits one place
    c_a = [1 for i in xrange(0,n-1)]
    c_b = [0 for i in xrange(0,cols_A -(n-1))]
    c = c_a + c_b
    A += [c]
    b += [1]
    loc = n-1 #0 indexed
    for j in xrange(1,n):
         c_s = [0 for i in xrange(0,loc)]
         c_m = [1 for i in xrange(loc,loc + (n-2))]
         c_e = [0 for i in xrange(loc+(n-2),cols_A)]
         c = c_s + c_m + c_e
         A += [c]
         b += [1]
         loc += (n-2)

    #contraints that ensure each vertex is only visited once
    for i in xrange(1,n):
	c = []
        for val in varsb:
		if (val[1] == i):
			c += [1]
		else:
			c += [0]
        c += [0 for j in xrange(0,num_slack)]
        A += [c]
        b += [1]

    #create constraints that make sure each level can't go backwards 
    s_count = 0
    for i in xrange(1,n):
	for j in xrange(i+1,n):
                c = []
		for val in varsb:
	            if ((val == (i,j)) or (val == (j,i))):
			c += [1]
                    else:
			c+= [0]
                c += [1 if (k == s_count) else 0 for k in xrange(0,num_slack)]
                s_count +=1
                A += [c]
                b += [1]




    A = np.array(A)
    b = np.array(b)
    return A,b,varsb,num_slack


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




#return c,A,b
def get_lp(graph,n):
    A,b,varsb= tsp_lp(n)
    c = get_c(graph,varsb)
    return c,A,b



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
    print(graph)
    c,A,b = get_lp(graph,n)

    #v,x,I = simplex.dual_simplex_reference(I,c,A,b)
    return c,A,b


    
def test_builtin(n):
    weights = {}
    for i in xrange(0,n):
        for j in xrange(0,n):
                weights[(i,j)] = 1

    graph = create_graph(n,weights)
    I,c,A,b,bounds = get_lp(graph,n)
    res = linprog(c, A=A, b=b, bounds=bounds,options={"disp": True})


   
	


    

import numpy as np
############## create linear programming model ############## 
#creates A,c,b 
#inputs: 
#    n = number of levels (number of nodes to visit including the start
#    d = current depth in the graph ( start is 1 and on.. )

def create_constraints(n):
    num_vars = n-1
    vars = [(0,i) for i in xrange(1,num_vars+1)]
    for i in xrange(1,n):
	num_vars += (n-2)
        nv = [(i,j) for j in xrange(1,n) if (i!=j)]
        vars += nv

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
        for val in vars:
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
		for val in vars:
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
    print(A)
    print(b)








    

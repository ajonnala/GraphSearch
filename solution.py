import lp
import astar
import Queue as Q

graph = astar.get_graph()
rev_graph = astar.get_rev_graph()

def get_route(start,goal_list):
    weights= dict()
    bi_weights = dict()
    astar_paths = dict()
    bi_astar_paths = dict()
    start_list = [start] + goal_list
    node_map = dict()
    for i in xrange(0,len(start_list)):
	node_map[start_list[i]] = i
 
    for i in start_list:
	for j in start_list:
	    if (i!= j):
		((w,p),n_e) = astar.astar_wrapper(i,j,graph)
		((w1,p1),n_e1,d1) = astar.bi_astar_wrapper(i,j,graph,rev_graph)
		astar_paths[(i,j)] = (p,n_e,n_e)
                bi_astar_paths[(i,j)] = (p,n_e1,d1)
		weights[(node_map[i],node_map[j])] = w
		bi_weights[(node_map[i],node_map[j])] = w1


    n = len(start_list)
    print(weights)
    c1,A1,b1 = lp.get_constraints(n,weights)
    c2,A2,b2 = lp.get_constraints(n,bi_weights)
 
    #print_comp(astar_paths,bi_astar_paths)
    return c1,A1,b1,c2,A2,b2

def print_comp(p1,p2):
    for key in p1:
	print('astar       '+  str(key)+ str(p1[key]))
        print('bi_astar    '+ str(key) + str(p2[key]))


    
    

    


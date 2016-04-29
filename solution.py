import lp
import astar
import Queue as Q

graph = astar.get_graph()
rev_graph = astar.get_rev_graph()
c1 = []
A1 = []
b1 = []
bounds1 = []
c2 = []
A2 = []
b2 = []
bounds2 = []

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
    c1,A1,b1,bounds1,varsb1= lp.get_constraints(n,weights)
    c2,A2,b2,bounds2,varsb2 = lp.get_constraints(n,bi_weights)
 
    g_cont = make_bb_graph(n,weights)

   # print_comp(astar_paths,bi_astar_paths)
    return g_cont


def bfs_fill(node,n,weights,graph,visited,q,c=0):

    #add neighbors
    neigh = []
    for i in xrange(0,n):
	if( (i!= node[0]) and (i!= node[1]) and (not(i in visited[node]))):
		neigh += [(weights[node[1],i],(node[1],i))]
			
   #add to each visited and put in queue
    graph[node] = neigh
    for n_t in neigh:
	(w,(s,d)) = n_t
	l = visited[node] + [d]
	visited[n_t[1]] = l
        q.put(n_t)


    #base case
    if (q.empty()):
	return graph
   
   # print(visited)
    #print(len(neigh))
    next_node = q.get()
    return bfs_fill(next_node[1],n,weights,graph,visited,q,c+1) 
    




def make_bb_graph(n,weights):
    graph = {}
    visited = {}
    visited[(0,0)] = []
    q = Q.Queue()
    return bfs_fill((0,0),n,weights,graph,visited,q)
	


#CHANGE TO ACTUAL LP CODE
def solve_lp(c,A,b):
	return 0


def lp_h(path,dirc):
    cons_list = []
    for i in xrange(0,len(path)-1):
	cons_list += [(path[i][1],path[i+1][1])]

    if (dirc == 1):
	for ele in cons_list:
		(a,b) = ele
		A1,b1 = lp.add_constraint(A1,b1,varsb1,a,b)
        return solve_lp(c1,A1,b1)

    else:
	for ele in cons_list:
		(a,b) = ele
		A2,b2 = lp.add_constraint(A2,b2,varsb2,a,b)
	return solve_lp(c2,A2,b2)


def print_comp(p1,p2):
    for key in p1:
	print('astar       '+  str(key)+ str(p1[key]))
        print('bi_astar    '+ str(key) + str(p2[key]))


    
    

    


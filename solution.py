import lp
import astar
import Queue as Q


#returns -1 if no more bids
def add_next_bids(c,n,visited,paths,pq,graph):
    for i in xrange(0,n):
	if ((not(i in visited)) and (i != c)):
		val = astar.get_edge_weight(c,i,graph)
		val += get_lp_sol(n,paths[i]+c + i)
		pq.put((val,i))

def bb(c,n,visited,paths,pq,graph):
    add_next_bids(c,n,visited,paths,pq,graph)
    
    

    


#Author: Alekhya Jonnalagedda
import Queue as Q
import math
import solution

###################graph ##########################
BuiltGraph = {1 : [40.4378402, -79.9307115, None, 5, 2, None],
              10 : [40.4357557, -79.92765510000001, 6, 14, 11, 9],
              11 : [40.4360277, -79.9228808, 7, 15, 12, 10],
              12 : [40.4362326, -79.9191187, 8, 16, None, 11],
              13 : [40.4337409, -79.9305435, 9, None, 14, 30],
              14 : [40.4341272, -79.9276043, 10, 18, 15, 13],
              15 : [40.4347623, -79.922823, 11, 19, 16, 14],
              16 : [40.435329, -79.91899, 12, 20, None, 15],
              17 : [40.4322838, -79.9304975, None, None, 18, 30],
              18 : [40.4326106, -79.9275475, 14, 21, 19, 17],
              19 : [40.4337339, -79.92296139999999, 15, 23, 20, 18],
              2 : [40.4380409, -79.9277185, None, 6, 3, 1],
              20 : [40.4343515, -79.918747, 16, 24, None, 19],
              21 : [40.431024, -79.927482, 18, 26, 22, None],
              22 : [40.4323551, -79.9231405, 23, 27, 25, 21],
              23 : [40.4327777, -79.92308349999999, 19, 22, 24, None],
              24 : [40.4335219, -79.9185301, 20, 25, None, 23],
              25 : [40.4322827, -79.91822739999999, 24, 28, None, 22],
              26 : [40.4292774, -79.9274068, 21, None, 27, None],
              27 : [40.42972169999999, -79.9234981, 22, 29, 28, 26],
              28 : [40.4291604, -79.9211954, 25, None, None, 27],
              29 : [40.42972169999999, -79.9234981, 27, None, None, None],
              3 : [40.4380545, -79.922969, None, 7, 4, 2],
              30 : [40.4320756, -79.9348776, None, 17, 13, None],
              4 : [40.4380353, -79.9193406, None, 8, None, 3],
              5 : [40.4366026, -79.9306596, 1, 2, 6, None],
              6 : [40.4367864, -79.9276963, 2, 10, 7, 5],
              7 : [40.4369761, -79.92291639999999, 3, 11, 8, 6],
              8 : [40.4371133, -79.9192183, 4, 12, None, 7],
              9 : [40.43538849999999, -79.9306099, 5, 13, 10, None]
              }
def distanceBetween(from_place, to_place):
    ##DEBUG##print 'Distance between ' + SquirrelHill[from_place] + ' and ' + SquirrelHill[to_place]
    x1 = BuiltGraph[from_place][0]
    y1 = BuiltGraph[from_place][1]
    x2 = BuiltGraph[to_place][0]
    y2 = BuiltGraph[to_place][1]
    ##DEBUG##print math.sqrt((x1-x2)**2 + (y1-y2)**2)*1000 #Normalising values
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)*1000 #Normalising values

def get_graph():
    g = newGraph()
    for val in BuiltGraph:
	n = createNode(val)
	addNode(val,g)
	info = BuiltGraph[val]
	for i in xrange(2,6):
		if (info[i] == None):
			continue
		else:
			weight = distanceBetween(val,info[i])
			addEdge(val,info[i],weight,g)
    return g

def get_rev_graph():
    g = newGraph()
    for val in BuiltGraph:
        n = createNode(val)
        addNode(val,g)
        info = BuiltGraph[val]
        for i in xrange(2,6):
                if (info[i] == None):
                        continue
                else:
                        weight = distanceBetween(info[i],val)
                        addEdge(info[i],val,weight,g)
    return g

############### Graph Functions #################

#Weighted and Directed graph
#Node Representation : (weight,node name)

def newGraph():
    return dict()

def createNode(name):
    return (name)

def addNode(v,g):
    g[v] = []

def addEdge(s,e,w,g):
    if s in g:
	g[s] += [(e,w)]
    else:
	g[s] = [(e,w)]

#returns 0 is there is no such edge
def get_edge_weight(s,d,g):
    if (s in g):
	neigh = g[s]	
	for ele in neigh:
	    (e,w) = ele
	    if (e == d):
		return w
        return 0
    else:
	return 0

def getNeighbors(v,g):
    if v in g:
    	return g[v]
    else:
	return []

################### A* Search Implementation #############
    
########### heuristics #############

def h(n,g):
    return distanceBetween(n,g)




def astar_step(start,goal,pq,graph,paths,nodes_expanded,h_i = -1):
    if( start == -1):
	return -1,-1,-1,-1,-1,nodes_expanded
    neighbors = getNeighbors(start,graph)
    #case where we are at the original start node
    if (not(start in paths)):
        paths[start] = (0,[start])
    (current_pathWeight,current_path) = paths[start]
    for node in neighbors:
        (e,w) = node
        if (e in paths):
             (pathWeight,p) = paths[e]
             if ( pathWeight > (current_pathWeight + w)):
                paths[e] = (current_pathWeight+w,current_path + [e])
		if (h_i == -1): pq.put((current_pathWeight+w+h(e,goal),e))
		else : pq.put((current_pathWeight+w+solution.lp_h(paths[e][1],h_i),e))
        else:
             paths[e] = (current_pathWeight+w,current_path + [e])
             if (h_i == -1): pq.put((current_pathWeight+w +h(e,goal),e))
	     else: pq.put((current_pathWeight + w + solution.lp_h(paths[e][1],h_i),e))	     

    #STUCK AND FOUND NO PATH
    if pq.empty():
        return -1,-1,-1,-1,-1,nodes_expanded


    #recursive case
    nextNode = pq.get()
    return nextNode[1],goal,pq,graph,paths,nodes_expanded + 1

#regular astar
def astar(start,goal,pq,graph,paths,nodes_expanded):
    if (start == goal):
	return paths[goal],nodes_expanded
    
    nn,goal,pq,graph,paths,nodes_expanded = astar_step(start,goal,pq,graph,paths,nodes_expanded)
    if (nn == -1):
	return -1,nodes_expanded
    return astar(nn,goal,pq,graph,paths,nodes_expanded) 	

def multi_astar(start,goal_list,pq,graph,paths,nodes_expanded,dirc):
    if (start in goal_list):
	return paths[start],nodes_expanded

    nn,goal_list,pq,graph,paths,nodes_expanded = astar_step(start,goal_list,pq,graph,paths,nodes_expanded,dirc)
    if (nn == -1):
        return -1,nodes_expanded
    return multi_astar(nn,goal_list,pq,graph,paths,nodes_expanded,dirc)


#bidirectional astar
def bidirectional_astar(start,goal,node1,node2,pq1,pq2,graph1,graph2,paths1,paths2,nodes_expanded,n1_list,n2_list,depth):
    #base cases
    if (node1 == node2):
	(w1,p1) = paths1[node1]
        (w2,p2) = paths2[node2]
        p2.reverse()
        return ((w1+w2,p1 + p2[1:]),nodes_expanded,depth)

    if (node1 in n2_list):
        (w1,p1) = paths1[node1]
        (w2,p2) = paths2[node1]
        p2.reverse()
        return ((w1+w2,p1 + p2[1:]),nodes_expanded,depth)

    if (node2 in n1_list):
        (w1,p1) = paths1[node2]
        (w2,p2) = paths2[node2]
        p2.reverse()
        return ((w1+w2,p1 + p2[1:]),nodes_expanded,depth)

    # if direction 2 finishes before direction 2 its not a valid path !!
    if (node1 == goal):
	return (paths1[node1],nodes_expanded,depth)
    
    if (node2 == start):
	(w1,p1) = paths2[node2]
        p1.reverse()
	return ((w1,p1),nodes_expanded,depth)	

 
    #direction 1
    nn1,end1,pq1,graph1,paths1,nodes_expanded = astar_step(node1,goal,pq1,graph1,paths1,nodes_expanded)
    #direction 2
    nn2,end2,pq2,graph2,paths2,nodes_expanded = astar_step(node2,start,pq2,graph2,paths2,nodes_expanded)
    
    if ((nn1 == -1) and (nn2 == -1)):
	return -1,nodes_expanded,depth

    #if direction 1 finishes with no path, there is none
    if (nn1 == -1):
	return -1, nodes_expanded,depth
    
    #adding visited nodes
    n1_list += [nn1]
    n2_list += [nn2]

    #cases where one path does not find the goal, while the other still has nodes to search
    #FILL IN CASES WHERE EITHER NN1 = -1 OR NN2 = -1 BY ALTERNATIVELY CALLING JUST THE OLD ONES AGAIN OR JUST CALLING ASTAR ON THE REST

    return bidirectional_astar(start,goal,nn1,nn2,pq1,pq2,graph1,graph2,paths1,paths2,nodes_expanded,n1_list,n2_list,depth+1)

	

############### Main Function ################
def astar_wrapper(start,goal,graph):
    pq = Q.PriorityQueue()
    path,depth = astar(start,goal,pq,graph,dict(),0)
    return path,depth

#dirc is 1 for astar
#dirc is 2 for bidirectional astar
def multi_astar_wrapper(start,goal_list,graph,dirc):
    pq = Q.PriorityQueue()
    path,depth = multi_astar(start,goal_list,pq,graph,dict(),0)
    return path,depth

def bi_astar_wrapper(start,goal,graph,graph_rev):
    pq1 = Q.PriorityQueue()
    pq2 = Q.PriorityQueue()
    path2,nodes2,depth2 = bidirectional_astar(start,goal,start,goal,pq1,pq2,graph,graph_rev,dict(),dict(),0,[],[],0)
    return path2,nodes2,depth2

def main(argv = None):
    graph = get_graph()
    graph_rev = get_rev_graph()
    start = 1
    goal = 9
    print(astar_wrapper(start,goal,graph))
    print(bi_astar_wrapper(start,goal,graph,graph_rev))
    p,d = multi_astar_wrapper(start,[goal]+[5],graph)
    print(p,d)
if __name__ == "__main__": main()

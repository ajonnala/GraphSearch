#Author: Alekhya Jonnalagedda
import Queue as Q

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

def getNeighbors(v,g):
    if v in g:
    	return g[v]
    else:
	return []

################### A* Search Implementation #############
    
########### heuristics #############

def h(n,g):
    return 0

def h_reverse(n,g):
    return 0



def astar(start,goal,pq,graph,paths,nodes_expanded):
    #base case
    if (start == goal):
	return paths,nodes_expanded

    neighbors = getNeighbors(start,graph)
    #case where we are at the original start node
    if (not(start in paths)):
	paths[start] = (0,[0])  
    (current_pathWeight,current_path) = paths[start]
    for node in neighbors:
	(e,w) = node
        if (e in paths):
	     (pathWeight,p) = paths[e]
	     if ( pathWeight > (current_pathWeight + w)):
		paths[e] = (current_pathWeight+w,current_path + [e])
                pq.put((current_pathWeight+w+h(e,goal),e))
             #else:
		#dont think i need to add to pq in this case cause it should aldredy be in there
        else:
	     paths[e] = (current_pathWeight+w,current_path + [e])
	     pq.put((current_pathWeight+w +h(e,goal),e))

  
    #STUCK AND FOUND NO PATH
    if pq.empty():
    	return -1,nodes_expanded


    #recursive case
    nextNode = pq.get()
    print(nextNode)
    return astar(nextNode[1],goal,pq,graph,paths,nodes_expanded + 1) 


#one_node and two_node should be initialized to start and goal
# graph2 is reverse of graph1
def bidirectional_astar(start,goal,one_node,two_node,pq1,pq2,graph1,graph2,path1,path2,depth):
    #fill in base case here

    #both paths meet
    if (one_node == two_node):
	path2.reverse()
	new_path = path1 + path2[1:]
	return new_path,depth

    #path1 makes it to goal before path2
    if (one_node == goal):
	return path1,depth

    #path2 makes it to start before path1
    if (two_node == start):
	path2.reverse()
	return path2,depth


    #find direction 1
    neigh1 = getNeighbors(one_node,graph1)
    for node in neigh1:
	(e,w) = node
        pq1.put(((e,w),w+h(one_node,node[0])))

    if (not(pq1.empty())):
	nextNode1 = pq1.get()
	path1 += [nextNode1]
	

    #find direction 2
    neigh2 = getNeighbors(two_node,graph2)
    for node in neigh2:
	(e,w) = node
	pq2.put(((e,w),w+h_reverse(node[0],two_node))) # in case there are different heuristic values for going in reverse direction (eg. traffic)

    if (not(pq2.empty())):
	 nextNode2 = pq2.get()
	 path2 += [nextNode2]

   
    #both directions failed and did not find a path
    if (pq1.empty() and pq2.empty()):
	return -1,depth

    return bidrectional_astar(start,goal,nextNode1[0][0],nextNode1[0][0],pq1,pq2,graph1,graph2,path1,path2,depth+1)    
    
	
####################### clean up functions  ##################

#gets total cost of the path 
#for now it simple the addition of te costs of the edges, but can make more complicated
def totalCost(path):
    sum = 0
    for node in path:
	sum += node[0][1]
    return sum

def getPath(path,start,end):
    final_path = [start]
    for node in path:
	if (not((node == start) or (node == end))):
	     final_path += [node[0][0]]
    if (final_path[len(final_path)-1] != end):
	final_path += [end]
    return final_path


###############Testing helper function ##############

def makeGraph(graph):
    node0 = createNode(0)
    node1 = createNode(1)
    node2 = createNode(2)
    node3 = createNode(3)
    node4 = createNode(4)

   
    addNode(node0,graph)
    addNode(node1,graph)
    addNode(node2,graph)
    addNode(node3,graph)
    addNode(node4,graph)


    addEdge(node0,node1,8,graph)
    addEdge(node0,node2,1,graph)
    addEdge(node2,node3,20,graph)
    addEdge(node3,node4,1,graph)
    addEdge(node1,node3,1,graph)


############### Main Function ################
def main(argv = None):
    graph = newGraph()
    makeGraph(graph)
    print(graph)
    pq = Q.PriorityQueue()
    path,depth = astar(0,4,pq,graph,dict(),0)
    #final_path = getPath(path,0,2)
    #cost = totalCost(path)
    print(path,depth)


if __name__ == "__main__": main()

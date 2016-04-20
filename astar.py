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


def astar_step(start,goal,pq,graph,paths,nodes_expanded):

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
                pq.put((current_pathWeight+w+h(e,goal),e))
        else:
             paths[e] = (current_pathWeight+w,current_path + [e])
             pq.put((current_pathWeight+w +h(e,goal),e))


    #STUCK AND FOUND NO PATH
    if pq.empty():
        return -1,-1,-1,-1,-1,nodes_expanded


    #recursive case
    nextNode = pq.get()
    return nextNode[1],goal,pq,graph,paths,nodes_expanded + 1


def astar(start,goal,pq,graph,paths,nodes_expanded):
    if (start == goal):
	return paths[goal],nodes_expanded
    
    nn,goal,pq,graph,paths,nodes_expanded = astar_step(start,goal,pq,graph,paths,nodes_expanded)
    if (nn == -1):
	return -1,nodes_expanded
    return astar(nn,goal,pq,graph,paths,nodes_expanded) 	

def bidirectional_astar(start,goal,node1,node2,pq1,pq2,graph1,graph2,paths1,paths2,nodes_expanded):
    #base cases
    if (node1 == node2):
	(w1,p1) = paths1[node1]
        (w2,p2) = paths2[node2]
        p2.reverse()
        return ((w1+w2,p1 + p2[1:]),nodes_expanded)

    #ALSO WORRY ABOUT OTHER BASE CASES
   
    #direction 1
    nn1,end1,pq1,graph1,paths1,nodes_expanded = astar_step(node1,goal,pq1,graph1,paths1,nodes_expanded)
    #direction 2
    nn2,end2,pq2,graph2,paths2,nodes_expanded = astar_step(node2,start,pq2,graph2,paths2,nodes_expanded)
    
    if ((nn1 == -1) and (nn2 == -1)):
	return -1,nodes_expanded

    #FILL IN CASES WHERE EITHER NN1 = -1 OR NN2 = -1 BY ALTERNATIVELY CALLING JUST THE OLD ONES AGAIN OR JUST CALLING ASTAR ON THE REST

    return bidirectional_astar(start,goal,nn1,nn2,pq1,pq2,graph1,graph2,paths1,paths2,nodes_expanded)


def astarOld(start,goal,pq,graph,paths,nodes_expanded):
    #base case
    if (start == goal):
	return paths[goal],nodes_expanded

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
        else:
	     paths[e] = (current_pathWeight+w,current_path + [e])
	     pq.put((current_pathWeight+w +h(e,goal),e))

  
    #STUCK AND FOUND NO PATH
    if pq.empty():
    	return -1,nodes_expanded


    #recursive case
    nextNode = pq.get()
    return astar(nextNode[1],goal,pq,graph,paths,nodes_expanded + 1) 


	

###############Testing helper function ##############

def makeGraph(graph):
    node0 = createNode(0)
    node1 = createNode(1)
    node2 = createNode(2)
    node3 = createNode(3)
    node4 = createNode(4)
    node5 = createNode(5)
    node6 = createNode(6)
    node7 = createNode(7)
   
   
    addNode(node0,graph)
    addNode(node1,graph)
    addNode(node2,graph)
    addNode(node3,graph)
    addNode(node4,graph)
    addNode(node5,graph)
    addNode(node6,graph)
    addNode(node7,graph)

    addEdge(node0,node7,1,graph)
    addEdge(node7,node1,1,graph)
    addEdge(node1,node2,1,graph)
    addEdge(node2,node7,1,graph)
    addEdge(node2,node3,1,graph)
    addEdge(node3,node4,1,graph)
    addEdge(node3,node5,8,graph)
    addEdge(node5,node6,1,graph)
    addEdge(node4,node6,50,graph)

def makeReverseGraph(graph):
    node0 = createNode(0)
    node1 = createNode(1)
    node2 = createNode(2)
    node3 = createNode(3)
    node4 = createNode(4)
    node5 = createNode(5)
    node6 = createNode(6)
    node7 = createNode(7)


    addNode(node0,graph)
    addNode(node1,graph)
    addNode(node2,graph)
    addNode(node3,graph)
    addNode(node4,graph)
    addNode(node5,graph)
    addNode(node6,graph)
    addNode(node7,graph)

    addEdge(node7,node0,1,graph)
    addEdge(node1,node7,1,graph)
    addEdge(node2,node1,1,graph)
    addEdge(node7,node2,1,graph)
    addEdge(node3,node2,1,graph)
    addEdge(node4,node3,1,graph)
    addEdge(node5,node3,8,graph)
    addEdge(node6,node5,1,graph)
    addEdge(node6,node4,50,graph)


def makeGraph2(graph):
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

    addEdge(node0,node2,1,graph)
    addEdge(node0,node1,8,graph)
    addEdge(node2,node3,20,graph)
    addEdge(node1,node3,1,graph)
    addEdge(node3,node4,1,graph)


def makeReverseGraph2(graph):
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

    addEdge(node2,node0,1,graph)
    addEdge(node1,node0,8,graph)
    addEdge(node3,node2,20,graph)
    addEdge(node3,node1,1,graph)
    addEdge(node4,node3,1,graph)


############### Main Function ################
def main(argv = None):
    graph = newGraph()
    graph_rev = newGraph()
    makeGraph2(graph)
    makeReverseGraph2(graph_rev)
    print(graph)
    pq = Q.PriorityQueue()
    pq1 = Q.PriorityQueue()
    pq2 = Q.PriorityQueue()

    start = 0
    goal = 4

    path,depth = astar(start,goal,pq,graph,dict(),0)
    path2,depth2 = bidirectional_astar(start,goal,start,goal,pq1,pq2,graph,graph_rev,dict(),dict(),0)
    print(path,depth)
    print(path2,depth2)


if __name__ == "__main__": main()

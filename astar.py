#Author: Alekhya Jonnalagedda
import Queue as Q

############### Graph Functions #################

#Weighted and Directed graph
#Node Representation : (weight,node name)

def newGraph():
    return dict()

def createNode(name,weight):
    return (weight,name)

def addNode(v,g):
    g[v] = []

def addEdge(s,e,g):
    if s in g:
	g[s] += [e]
    else:
	g[s] = [e]

def getNeighbors(v,g):
    if v in g:
    	return g[v]
    else:
	return []

################### A* Search Implementation #############
    



def astar(start,goal,pq,graph,path):
    #base case
    if (start == goal):
	return path

    neighbors = getNeighbors(start,graph)
    for node in neighbors:
        #CHANGE WEIGHTS HERE FOR A*
	pq.put(node)
  
    #base case 
    if pq.empty:
    	return path


    #recursive case
    nextNode = pq.get()
    path += [nextNode] 
    return astar(nextNode,goal,pq,graph,path) 

    
	


############### Main Function ################
def main(argv = None):
    graph = newGraph()
    pq = Q.PriorityQueue()
    astar(start,goal,pq,graph,[])

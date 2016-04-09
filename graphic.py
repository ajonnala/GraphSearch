from Tkinter import *
import random
import time

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if (event.char == 's'):
	start = canvas.data.traversal[0]
        end = canvas.data.traversal[len(canvas.data.traversal)-1]
        canvas.data.nodes[start] = (canvas.data.nodes[start][0],canvas.data.nodes[start][1],canvas.data.nodes[start][2],canvas.data.nodes[start][3],"green")
        canvas.data.nodes[end] = (canvas.data.nodes[end][0],canvas.data.nodes[end][1],canvas.data.nodes[end][2],canvas.data.nodes[end][3],"green")
	canvas.data.start = True
	redrawAll()
    else:
	redrawAll()

def step(p,c):
     canvas.data.colors[(p,canvas.data.traversal[c])] = "red"

def timerFired():
    #FIX THE LAST STEP TIMING THING
    redrawAll()
    if (canvas.data.start):
	step(canvas.data.prevNode,canvas.data.curNode)
	canvas.data.prevNode = canvas.data.traversal[canvas.data.curNode]
        canvas.data.curNode += 1
        if (canvas.data.curNode == len(canvas.data.traversal)):
             canvas.data.curNode = 1
	     canvas.data.start = False
    delay = 250 # milliseconds
    if (canvas.data.start): delay = 1000
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    canvas.delete(ALL)
    drawGraph(canvas.data.graph)

#EITHER THE GRAPH NEEDS TO HAVE ALL VERTICES AS KEYS, OR NEED NUMBER OF VERTICES 
def drawGraph(g):
    index = 0
    for ele in canvas.data.nodes:
        canvas.create_text(ele[0]+ 6, ele[1] - 5, text=str(index), fill="purple", font =  "Helvetica 12 bold")
	canvas.create_oval(ele[0],ele[1],ele[2],ele[3],fill = ele[4])
        index +=1  
    
    index = 0
    for n in g:
	neigh = g[n]
        sCoord = canvas.data.nodes[n]
        for v in neigh:
            vCoord = canvas.data.nodes[v]
            canvas.create_line(vCoord[0]+6, vCoord[1]+6,sCoord[0]+6,sCoord[1]+6, fill=canvas.data.colors[(n,v)], width=2,arrow="first")
	    index += 1

        
def getNodes(n):
    nodes = []
    for i in xrange(0,n):
	l = random.randrange(10,500)
        r = random.randrange(10,500)
        nodes += [(l,r,l+12,r+12,"red")]
    return nodes

def getLineColors(g):
    colors = dict()
    for n in g:
	neigh = g[n]
        for v in neigh:
		colors[(n,v)] = ["black"]
    return colors 

def init():
     canvas.data.traversal = [0,1,2,3]
     canvas.data.graph = {0:[1,4],1:[2],2:[3],3:[1]}
     canvas.data.nodes = getNodes(5) #numVertices
     canvas.data.colors = getLineColors(canvas.data.graph)
     canvas.data.prevNode = 0
     canvas.data.curNode = 1
     canvas.data.start = False

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=1000, height=1000)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()

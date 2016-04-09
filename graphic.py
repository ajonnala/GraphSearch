from Tkinter import *
import random

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    redrawAll()

def timerFired():
    redrawAll()
    delay = 250 # milliseconds
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    canvas.delete(ALL)
    graph = {0:[1,4],1:[2],2:[3],3:[1]}  
    drawGraph(graph)

#EITHER THE GRAPH NEEDS TO HAVE ALL VERTICES AS KEYS, OR NEED NUMBER OF VERTICES 
def drawGraph(g):
    index = 0
    for ele in canvas.data.nodes:
        canvas.create_text(ele[0]+ 6, ele[1] - 5, text=str(index), fill="purple", font =  "Helvetica 12 bold")
	canvas.create_oval(ele[0],ele[1],ele[2],ele[3],fill = "red")
        index +=1  
    
    for n in g:
	neigh = g[n]
        sCoord = canvas.data.nodes[n]
        for v in neigh:
            vCoord = canvas.data.nodes[v]
            canvas.create_line(vCoord[0]+6, vCoord[1]+6,sCoord[0]+6,sCoord[1]+6, fill="black", width=2,arrow="last")

        
def getNodes(n):
    nodes = []
    for i in xrange(0,n):
	l = random.randrange(10,500)
        r = random.randrange(10,500)
        nodes += [(l,r,l+12,r+12)]
    return nodes


def init():
     canvas.data.nodes = getNodes(5) #numVertices

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

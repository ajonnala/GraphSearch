import requests
import sys
import math

SquirrelHill = [ "Forbes Ave and Murdoch St, Pittsburgh, PA 15217, USA",
                 "Forbes Ave and Wightman St, Pittsburgh, PA 15217, USA",
                 "Forbes Ave and Murray Av, Pittsburgh, PA 15217, USA",
                 "Forbes Ave and Shady Av, Pittsburgh, PA 15217, USA",
                 "Darlington St and Murdoch St, Pittsburgh, PA 15217, USA",
                 "Darlington St and Wightman St, Pittsburgh, PA 15217, USA",
                 "Darlington St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Darlington St and Shady Av, Pittsburgh, PA 15217, USA",
                 "Bartlett St and Murdoch St, Pittsburgh, PA 15217, USA",
                 "Bartlett St and Wightman St, Pittsburgh, PA 15217, USA",
                 "Bartlett St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Bartlett St and Shady Av, Pittsburgh, PA 15217, USA",
                 "Beacon St and Murdoch St, Pittsburgh, PA 15217, USA",
                 "Beacon St and Wightman St, Pittsburgh, PA 15217, USA",
                 "Beacon St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Beacon St and Shady Av, Pittsburgh, PA 15217, USA",
                 "Hobart St and Murdoch St, Pittsburgh, PA 15217, USA",
                 "Hobart St and Wightman St, Pittsburgh, PA 15217, USA",
                 "Hobart St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Hobart St and Shady Av, Pittsburgh, PA 15217, USA",
                 "Phillips Av and Wightman St, Pittsburgh, PA 15217, USA",
                 "Phillips Av and Murray Av, Pittsburgh, PA 15217, USA",
                 "Douglas St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Douglas St and Shady Av, Pittsburgh, PA 15217, USA",
                 "Phillips Av and Shady Av, Pittsburgh, PA 15217, USA",
                 "Pocusset St and Wightman St, Pittsburgh, PA 15217, USA",
                 "Pocusset St and Murray Av, Pittsburgh, PA 15217, USA",
                 "Forward Av and Shady Av, Pittsburgh, PA 15217, USA",
                 "Forward Av and Murray Av, Pittsburgh, PA 15217, USA",
                 "Beacon St and Hobart St, Pittsburgh, PA 15217, USA"]

#Dict Structure: Node : [lat, long, N, S, E, W]
SQGraph = {"1": [ 0, 0, None, 5, 2, None],
           "2": [ 0, 0, None, 6, 3, 1],
           "3": [ 0, 0, None, 7, 4, 2],
           "4": [ 0, 0, None, 8, None, 3],
           "5": [ 0, 0, 1, 2, 6, None],
           "6": [ 0, 0, 2, 10, 7, 5],
           "7": [ 0, 0, 3, 11, 8, 6],
           "8": [ 0, 0, 4, 12, None, 7],
           "9": [ 0, 0, 5, 13, 10, None],
           "10": [ 0, 0, 6, 14, 11, 9],
           "11": [ 0, 0, 7, 15, 12, 10],
           "12": [ 0, 0, 8, 16, None, 11],
           "13": [ 0, 0, 9, None, 14, 30],
           "14": [ 0, 0, 10, 18, 15, 13],
           "15": [ 0, 0, 11, 19, 16, 14],
           "16": [ 0, 0, 12, 20, None, 15],
           "17": [ 0, 0, None, None, 18, 30],
           "18": [ 0, 0, 14, 21, 19, 17],
           "19": [ 0, 0, 15, 23, 20, 18],
           "20": [ 0, 0, 16, 24, None, 19],
           "21": [ 0, 0, 18, 26, 22, None],
           "22": [ 0, 0, 23, 27, 25, 21],
           "23": [ 0, 0, 19, 22, 24, None],
           "24": [ 0, 0, 20, 25, None, 23],
           "25": [ 0, 0, 24, 28, None, 22],
           "26": [ 0, 0, 21, None, 27, None],
           "27": [ 0, 0, 22, 29, 28, 26],
           "28": [ 0, 0, 25, None, None, 27],
           "29": [ 0, 0, 27, None, None, None],
           "30": [ 0, 0, None, 17, 13, None],
           }
def distanceBetween(from_place, to_place):
    ##DEBUG##print 'Distance between ' + SquirrelHill[from_place] + ' and ' + SquirrelHill[to_place]
    x1 = SQGraph[str(from_place)][0]
    y1 = SQGraph[str(from_place)][1]
    x2 = SQGraph[str(to_place)][0]
    y2 = SQGraph[str(to_place)][1]
    ##DEBUG##print math.sqrt((x1-x2)**2 + (y1-y2)**2)*1000 #Normalising values
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)*1000 #Normalising values

def getNeighbours(node):
    lis = SQGraph[str(node)]
    print 'Neighbours for: ', SquirrelHill[node-1],
    if lis[2]: print ' North: ', SquirrelHill[lis[2]-1], ' Distance of ', distanceBetween(node, lis[2]) 
    if lis[3]: print ' South: ', SquirrelHill[lis[3]-1], ' Distance of ', distanceBetween(node, lis[3]) 
    if lis[4]: print ' East: ', SquirrelHill[lis[4]-1], ' Distance of ', distanceBetween(node, lis[4]) 
    if lis[5]: print ' West: ', SquirrelHill[lis[5]-1], ' Distance of ', distanceBetween(node, lis[5]) 
    print ''

def printGraph():
    for key in sorted(SQGraph):
        print key + " : " + str(SQGraph[key]) + ","

for key in sorted(SQGraph):
    Key = int(key) -1
    requestString = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + SquirrelHill[int(Key)].replace(' ','+') + '&key=' + sys.argv[1]
    resp = requests.get(requestString)
    Json = resp.json()
    SQGraph[key][0] = float(Json['results'][0]['geometry']['location']['lat'])
    SQGraph[key][1] = float(Json['results'][0]['geometry']['location']['lng'])
    ##DEBUG##print SquirrelHill[Key],SQGraph[key]

printGraph()

#distanceBetween(2,23)
#for i in range(len(SquirrelHill)):
#    getNeighbours(i+1)

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

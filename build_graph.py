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

for key in sorted(SQGraph):
    Key = int(key) -1
    requestString = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + SquirrelHill[int(Key)].replace(' ','+') + '&key=' + sys.argv[1]
    resp = requests.get(requestString)
    Json = resp.json()
    SQGraph[key][0] = float(Json['results'][0]['geometry']['location']['lat'])
    SQGraph[key][1] = float(Json['results'][0]['geometry']['location']['lng'])
    ##DEBUG##print SquirrelHill[Key],SQGraph[key]

#distanceBetween(2,23)
for i in range(len(SquirrelHill)):
    getNeighbours(i+1)

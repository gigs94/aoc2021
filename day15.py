import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

def print2darray(matrix, shape):
    print(shape)
    ycount=1
    for ycount,y in enumerate(matrix):
        for xcount,x in enumerate(y):
            print(f'{int(x)}', end='')
            if (xcount+1)%shape[0] == 0:
                print(' ', end='')
        print('')
        if (ycount+1)%shape[1] == 0:
            print('')


def adjacent_to_path(xy, visited):
    """ We know that if you get to an adjacency
    that youre path is going to be greater than
    just going there directly so abandon this path. 
    since you have to have one adjacency this returns
    false at 2"""
    right=tuple(np.add(xy,(0,1)))
    left=tuple(np.add(xy,(0,-1)))
    top=tuple(np.add(xy,(-1,0)))
    bottom=tuple(np.add(xy,(1,0)))

    adjacency=0
    for x in (right,left,top,bottom):
        if x[0] < 0 or x[1] < 0 or x[0] >= visited.shape[0] or x[1] >= visited.shape[1]:
            continue
        elif visited[x]:
            adjacency+=1
    return adjacency > 1

def can_go(matrix, pos, visited):
    rtn=False
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= matrix.shape[0] or pos[1] >= matrix.shape[1]:
        rtn = False
    elif visited[pos]:
        rtn = False
    elif adjacent_to_path(pos, visited):
        rtn = False
    else:
        visited[pos]=True 
        rtn = True
    return rtn

def do_traverse(matrix, xy, path, count, dest):
    global results
    if can_go(matrix, xy, path):
        count+=matrix[xy]
        if xy==dest:
            if count<results or results==0:
                results=count
            path[xy]=False
            return

        # Cardinal positions adjacent to current location
        right=tuple(np.add(xy,(0,1)))
        left=tuple(np.add(xy,(0,-1)))
        top=tuple(np.add(xy,(-1,0)))
        bottom=tuple(np.add(xy,(1,0)))

        for x in (right,left,top,bottom):
            do_traverse(matrix, x, path, count, dest)
        path[xy]=False
        return 
    else:    
        return

data=np.array([[int(x) for x in list(l)] for l in open(0).read().split('\n') ])

fm=[]
fm.append(data)
data_next=data
for i in range(1,10):
    data_next=data_next+np.ones(data.shape)
    data_next=np.where(data_next>9,1,data_next)
    fm.append(data_next)


new_data=np.zeros((data.shape[0]*5,data.shape[1]*5))
for a in range(0,5):
    row=np.zeros(data.shape)
    for b in range (0,5):
        if b != 0:
            row=np.append(row,fm[b+a],axis=1) 
        else:
            row=fm[b+a]
    if a != 0:
        new_data=np.append(new_data,row,axis=0)
    else:
        new_data=row

print(new_data.shape)
print2darray(new_data,data.shape)

data=new_data

### results=0
### path=np.zeros(data.shape)
### do_traverse(data,(0,0),path,0,tuple(np.add(data.shape,(-1,-1))))
### print(results)

import networkx as nx
g=nx.DiGraph()

for xy,v in np.ndenumerate(data):
    right=tuple(np.add(xy,(0,1)))
    left=tuple(np.add(xy,(0,-1)))
    top=tuple(np.add(xy,(-1,0)))
    bottom=tuple(np.add(xy,(1,0)))
    g.add_node(xy)
    for idx,d in enumerate([right,left,top,bottom]):
        if d[0] < 0 or d[1] < 0 or d[0] >= data.shape[0] or d[1] >= data.shape[1]:
            pass
        else:
            g.add_edge(xy,d,risk=data[d])

size=tuple(np.add(data.shape,(-1,-1)))
path=nx.shortest_path(g,(0,0),size,'risk')
print(path)

pscore=[int(g.edges[path[p],path[p+1]]['risk']) for p in range(0,len(path)-1)]
score=sum([g.edges[path[p],path[p+1]]['risk'] for p in range(0,len(path)-1)])

print(pscore,score)
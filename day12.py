import argparse as ap
from collections import defaultdict
from operator import truediv
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix, coo_matrix
from scipy.sparse.csgraph import dijkstra
import networkx as nx
from pprint import pprint

def can_go(pos,path,scr):
    # can't go to same node twice unless it's CAPS
    if scr:
        limit=False
        for x in np.unique(path):
            if x.islower():
                visited=path.count(x)
                if visited == 2:
                    small_cave_max=pos
                    limit=True
        if pos == 'start' or pos == 'end':
            if path.count(pos) == 0:
                return True
            else:
                return False
        elif pos.islower() and not limit:
            return True
        elif pos.islower() and limit:
            if pos in path:
                return False
            else:
                return True
        elif pos.isupper():
            return True
        else:
            return False 
    else:
        if pos.islower() and pos not in path:
            return True
        elif pos.isupper():
            return True
        else:
            return False 

paths2=[]

def traverse(m,pos,end,path,src):
    if pos == end:
        path.append(pos)
        paths2.append(list(path))
        path.pop()
    else:
        for p in m.adj[pos]:
            if can_go(pos,path,src):
                path.append(pos)
                traverse(m,p,end,path,src)
                pop=path.pop()


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day12.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data=list()
        m=list([tuple(x for x in list(l.strip().split('-'))) for l in f.readlines() ])
        n=np.unique([item for sublist in m for item in sublist])
        caps=list()
        [caps.append(x) if x.isupper() else False for x in n]

        G = nx.Graph()
        G.add_nodes_from(n)
        G.add_edges_from(m)

        traverse(G, 'start', 'end', [], False)
        answer1=len(paths2)
        paths2.clear()

        traverse(G, 'start', 'end', [], True)
        ##pprint(paths2)
        answer2=len(paths2)

        print(f'part1: {answer1}')
        print(f'part2: {answer2}')
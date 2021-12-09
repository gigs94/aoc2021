import argparse as ap
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks



import sys
from pprint import pprint

def can_go(matrix, pos, visited):
    rtn=False
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= matrix.shape[0] or pos[1] >= matrix.shape[1]:
        rtn = False
    elif visited[pos]:
        rtn = False
    else:
        visited[pos]=True 
        rtn = matrix[pos] != 9
    return rtn

def do_traverse(matrix, xy, visited, count):
    if can_go(matrix, xy, visited):
        count+=1
        right=tuple(np.add(xy,(0,1)))
        left=tuple(np.add(xy,(0,-1)))
        top=tuple(np.add(xy,(-1,0)))
        bottom=tuple(np.add(xy,(1,0)))

        for x in (right,left,top,bottom):
            count+=do_traverse(matrix, x, visited, 0) 
        return count
    else:
        return 0

def traverse(matrix):
    visited=np.zeros(matrix.shape)
    blah=np.zeros(matrix.shape)
    for x in range(0,matrix.shape[0]):
        for y in range(0,matrix.shape[1]):
            blah[x,y]=do_traverse(matrix, (x,y), visited, 0)
    top3=np.flip(np.sort(blah,axis=None))[0:3]
    return(np.prod(top3))


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day9.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data=list()
        i=np.array([[int(item) for item in list(l.strip())] for l in f.readlines() ])

        answer=0
        for x in range(0,i.shape[0]):
            for y in range(0,i.shape[1]):
                top = i[x][y] < i[x-1][y] if not x-1<0 else True
                bottom= i[x][y] < i[x+1][y] if not x+1>=i.shape[0] else True
                right = i[x][y] < i[x][y+1] if not y+1>=i.shape[1] else True
                left = i[x][y] < i[x][y-1] if not y-1<0 else True

                if left and right and top and bottom:
                    answer += i[x][y]+1
        print(f'part1: {answer}')
        print(f'part2: {traverse(i)}')
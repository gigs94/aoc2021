import argparse as ap
import numpy as np
import networkx as nx
from numpy.core.defchararray import endswith


def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 0)
    if pad_width[0] != 0:
        vector[:pad_width[0]] = pad_value
    if pad_width[1] != 0:
        vector[-pad_width[1]:] = pad_value


def fold(grid,ax,val):
    if ax==0:
        #take subgrids based on fold
        l=grid[0:val,:]
        r=grid[val+1:,:]
        diff=l.shape[0]-r.shape[0]
        if diff > 0:
            r=np.pad(r,((0,diff),(0,0)),pad_with,padder=0)
        else:
            l=np.pad(l,((abs(diff),0),(0,0)),pad_with,padder=0)
    else:
        l=grid[:,0:val]
        r=grid[:,val+1:]
        diff=l.shape[1]-r.shape[1]
        if diff > 0:
            r=np.pad(r,((0,0),(0,diff)),pad_with,padder=0)
        else:
            l=np.pad(l,((0,0),(abs(diff),0)),pad_with,padder=0)

    #take the right/bottom and reverse it
    r=np.flip(r,axis=ax)

    #add to the top/left
    return l+r

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day13.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        dots=list()
        folds=list()
        for l in f.readlines():
            if l[0].isdigit():
                dots.append(tuple(int(x) for x in list(l.strip().split(','))))
            elif l[0] == 'f':
                a,val=l.strip().split('=')
                f,along,axis=a.split(' ')
                axis=1 if axis=='y' else 0
                folds.append((axis,int(val)))

        uzip = list(zip(*dots))
        maxX = max(uzip[0])
        maxY = max(uzip[1])
        grid = np.zeros((maxX+1,maxY+1))
        d = np.array(dots)

        grid[tuple(d.T)]=1

        for ax,val in folds:
            grid=fold(grid,ax,val)
            print(np.count_nonzero(grid))

        answer=(grid.T>0)

        for x in answer:
            for y in x:
                print('#',end='') if y else print(' ',end='')
            print('')
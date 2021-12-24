import numpy as np
from numpy.core.defchararray import endswith
from scipy.ndimage import convolve
import sys
np.set_printoptions(threshold=sys.maxsize)

def print_matrix(a):
    for b in a:
        for c in b:
            print ('#' if c else ' ', end='')
        print()
    print(a.sum())
    
iea,_,*ii=open(0).read().split('\n')

ii=np.pad([[ int(p=='#') for p in row ] for row in ii],(100,100))
iea=np.array([ int(p=='#') for p in iea ])

bin2dec = 2**np.arange(9).reshape(3,3)

for i in range(50):
    ii = iea[convolve(ii, bin2dec)]
    if i+1 in (2, 50): print(ii.sum())
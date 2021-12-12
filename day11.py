import argparse as ap
import numpy as np


def flash(matrix):
    positions = list(zip(*np.where(matrix==-1)))

    if len(positions) == 0:
        return matrix
    else:
        for pos in positions:
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    xy=tuple(np.add(pos,(x,y)))
                    if xy[0] < 0 or xy[1] < 0 or xy[0] >= matrix.shape[0] or xy[1] >= matrix.shape[1] or (x==0 and y==0):
                        next
                    else:
                        if matrix[xy] != -1 and matrix[xy] != 0:
                           matrix[xy] += 1
        matrix=np.where(matrix==-1,0,matrix)
        matrix=np.where(matrix<=9,matrix,-1)
        return flash(matrix)
            

def run(m,steps):
    flashes=0
    npsize=m.shape[0]*m.shape[1]
    n=np.full(m.shape,fill_value=1,dtype=int)
    for i in range(0,steps):
        m1=m+n
        flashed=np.where(m1<=9,m1,-1)
        m=flash(flashed)
        flashes += np.count_nonzero(m==0)
    # keep going until they all flash simultaneously
    while np.count_nonzero(m==0) != npsize:
        i+=1
        m1=m+n
        flashed=np.where(m1<=9,m1,-1)
        m=flash(flashed)

    return i+1,m,flashes

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day11.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data=list()
        m=np.array([[int(x) for x in list(l.strip())] for l in f.readlines() ])
        answer2,n,answer1=run(m,100)

        print(n)

        print(f'part1: {answer1}')
        print(f'part2: {answer2}')
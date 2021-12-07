import argparse as ap
import numpy as np
import sys

def calc_fuel_part1(pos, crabs):
    return sum([ abs(crab-pos) for crab in crabs ])

def sum_fact(num):
    return sum([ i for i in range(1,num+1)])

def calc_fuel(pos, crabs):
    return sum([ sum_fact(abs(crab-pos)) for crab in crabs ])

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day7.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        crabs=[ int(x) for x in f.readline().strip().split(',') ]
        print(np.mean(crabs))
        fmin=sys.maxsize
        fpos=len(crabs)+1
        for i in range(min(crabs),max(crabs)):
            v=calc_fuel(i,crabs)
            if v < fmin:
                fmin = v
                fpos = i
            
        print(fpos, fmin)
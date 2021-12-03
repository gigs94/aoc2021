import argparse as ap
import numpy as np

def count(m):
    return [ (list(r).count("0"),list(r).count("1")) for r in m ]

def oxy_rating(m,pos):
    counts=count(m)
    if counts[pos][0] > counts[pos][1]:
        # zeros are true
        mask=np.invert(m.astype(bool))
    else:
        # ones are true
        mask=m.astype(bool)

    x=m.T[mask[pos]]
    return convert_to_int(x[0]) if x.shape[0]==1 else oxy_rating(x.T,pos+1)


def co2_rating(m,pos):
    counts=count(m)
    if counts[pos][0] <= counts[pos][1]:
        # zeros are true
        mask=np.invert(m.astype(bool))
    else:
        # ones are true
        mask=m.astype(bool)

    x=m.T[mask[pos]]
    return convert_to_int(x[0]) if x.shape[0]==1 else co2_rating(x.T,pos+1)

def convert_to_int(m):
    return int(''.join(m),2)


def run(file):
    with open(file) as f:
        m = np.asarray([ np.asarray(list(l.strip())) for l in f.readlines() ]).T
        counts=count(m)
        gamma=""
        epsilon=""
        for idx,(zero,one) in enumerate(counts):
            gamma += "0" if zero < one else "1"
            epsilon += "1"  if zero < one else "0"


        return [ int(gamma,2), int(epsilon,2), oxy_rating(m,0), co2_rating(m, 0) ]

parser = ap.ArgumentParser()
parser.add_argument('file', nargs='?', default='day3.dat', type=str)
args = parser.parse_args()

p1=run(args.file)
print(f'part1 : gamma={p1[0]:6}  epsilon={p1[1]:6}  answer={p1[0]*p1[1]:10}')
print(f'part2 : oxy={p1[2]:8}  co2={p1[3]:10}  answer={p1[2]*p1[3]:10}')

import argparse as ap
import numpy as np

def spawn(limit, cday, fishes):

    fish_counts = dict(zip(list(range(0,9)),[0]*9))

    for day in range(8,-1,-1):
        if day-1 >= 0:
            fish_counts[day-1]=fishes[day]
        elif day==0:
            fish_counts[6] += fishes[day]
            fish_counts[8] += fishes[day]
        else:
            print('huh?')
        
    if limit == cday:
        return sum(fish_counts.values())
    else:
        return spawn(limit,cday+1,fish_counts)

        
if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day6.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        fishes=[ int(x) for x in f.readline().strip().split(',') ]
        #create number of fish / day.   i.e. count all the fish with 1 day to hatching... and rotate them.
        unique, counts = np.unique(fishes, return_counts=True)
        input = np.asarray((unique, counts)).T
        fish_counts = dict(zip(list(range(0,9)),[0]*9))
        for i,j in input:
            fish_counts[i]=j
        answer=spawn(256,1,fish_counts)
        print(answer)
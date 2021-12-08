import argparse as ap
import numpy as np
import sys
from pprint import pprint

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day8.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data=list()
        for l in f.readlines():
            x,y=l.strip().split('|')
            data.append((x.split(),y.split()))
        count=0
        for j in data:
            for i in j[1]:
                if len(i) == 2 or len(i) == 3 or len(i) == 4 or len(i) == 7:
                    count+=1

        print(f'part1: number of 1,4,7,8\'s: {count}')


        answer=int()
        for dat in data:
           mhash = dict()
           mhash[6] = list() ## i.e. 6 seg numbers
           mhash[5] = list() ## i.e. 5 seg numbers

           for i in dat[0]:
                   if len(i) == 2:  #1
                       mhash[1]=i
                   elif len(i) == 3: #7
                       mhash[7]=i
                   elif len(i) == 4: #4
                       mhash[4]=i
                   elif len(i) == 7:  #8
                       mhash[8]=i
                   elif len(i) == 6: #0,6,9
                       mhash[6].append(i)
                   elif len(i) == 5: #2,3,5
                       mhash[5].append(i)

           ahash=dict()
           one=set(mhash[1])
           eight=set(mhash[8])
           seven=set(mhash[7])
           four=set(mhash[4])
           cde=eight.difference(mhash[6][0])
           cde.update(eight.difference(mhash[6][1]))
           cde.update(eight.difference(mhash[6][2]))
           bd=four.difference(mhash[1])
           ahash['a']=seven.difference(mhash[1])
           ahash['d']=bd.intersection(cde)
   
           # figure out 6 and 9... both have 6 digits... both has a and d
           ad=ahash['a'].union(ahash['d'])
           six_nine=list()
           for s in mhash[6]:
               if ad.issubset(set(s)):
                   six_nine.append(s)
   
           if one.issubset(six_nine[0]):
               nine=set(six_nine[0])
               six=set(six_nine[1])
           else:
               nine=set(six_nine[1])
               six=set(six_nine[0])
   
           ahash['e']=eight.difference(nine)
           ahash['c']=one.difference(six)
   
           for s in mhash[5]:
               if one.issubset(set(s)):
                   three=set(s)
   
           ahash['b']=eight-three-ahash['e']
           ahash['g']=eight-one-ahash['e']-ahash['a']-ahash['b']-ahash['c']-ahash['d']
           ahash['f']=one-ahash['c']
           zero=eight-ahash['d']
           two=eight-ahash['b']-ahash['f']
           five=eight-ahash['c']-ahash['e']
   
           rhash=dict()
           rhash[0]=zero
           rhash[1]=one
           rhash[2]=two
           rhash[3]=three
           rhash[4]=four
           rhash[5]=five
           rhash[6]=six
           rhash[7]=seven
           rhash[8]=eight
           rhash[9]=nine
   
           result=""
           for i in dat[1]:
                   for y in rhash:
                       if set(i) == rhash[y]:
                           result+=str(y)
           
           answer+=int(result)

        print("part2:", answer)
from re import U
import numpy as np
from collections import Counter, defaultdict
from pprint import pprint

def moves(pos, endv, pathz, rolls=0):
    if rolls==3:
        pathz.append(pos); return 

    for i in [ 1, 2, 3 ]:
        npos=(pos+i-1)%10+1
        moves(npos, endv, pathz, rolls+1)

possibilities={}
for x in range (1,11):
    pathz=[]
    moves(x,0,pathz) 
    #print(x, Counter(pathz), len(pathz))
    possibilities[x]=Counter(pathz)

#pu=dict({(4,0,8,0):1})
pu=dict({(7,0,6,0):1})
p1wins=0
p2wins=0
onesmove=0

aa=0
while len(pu.keys()) != 0:
    onesmove=not onesmove
    pun=defaultdict(int)
    for p1,s1,p2,s2 in pu.keys():
        universes=pu[(p1,s1,p2,s2)]
        if onesmove:
            for npos in possibilities[p1]:
                nscore=s1+npos
                if nscore>=21:
                    p1wins+=universes*possibilities[p1][npos]
                else:
                    pun[(npos,nscore,p2,s2)]+=universes*possibilities[p1][npos]
        else:
            for npos in possibilities[p2]:
                nscore=s2+npos
                if nscore>=21:
                    p2wins+=universes*possibilities[p2][npos]
                else:
                    pun[(p1,s1,npos,nscore)]+=universes*possibilities[p2][npos]
    pu=pun.copy()

print(f'player1 wins: {p1wins}')
print(f'player2 wins: {p2wins}')
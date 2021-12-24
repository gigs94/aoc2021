from collections import defaultdict, Counter
from io import StringIO; import numpy as np; from scipy.spatial import distance
from scipy.spatial.transform import Rotation as R
from pprint import pprint

def rotate_matrix(bb, rotation=None):
    if rotation:
        rx = R.from_euler('x', rotation[0], degrees=True)
        ry = R.from_euler('y', rotation[1], degrees=True)
        rz = R.from_euler('z', rotation[2], degrees=True)
        return rz.apply(ry.apply(rx.apply(bb))).astype(int)

    for x in [0,90,180,270]:
        rx = R.from_euler('x', x, degrees=True)
        for y in [0,90,270]:
            ry = R.from_euler('y', y, degrees=True)
            for z in [0,180]:
                rz = R.from_euler('z', z, degrees=True)
                b=rz.apply(ry.apply(rx.apply(bb).astype(int)).astype(int)).astype(int)
                yield (x,y,z),b

def sync_matrices(aa,bb,plane,DEBUG=False,atl=3):
    planeA=np.array([ plane[i][0] for i in range(len(plane)) ]).astype(int)
    planeB=np.array([ plane[i][1] for i in range(len(plane)) ]).astype(int)
    i=0
    for rotation,rpB in rotate_matrix(planeB):
        shift=planeA[0]-rpB[0]
        srpB=np.array(rpB+shift)
        if DEBUG: print(f'{list(srpB-planeA)}')
        if np.allclose(srpB,planeA,atol=atl):
            return rotation,shift
    print(f'didnt find a rotation?! {atl}')
    if not DEBUG: sync_matrices(aa,bb,plane,True,atl+1)

n = [ np.loadtxt(StringIO(x), delimiter=',', comments='---') for x in open(0).read().split('\n\n') ]
m=[ sorted(np.unique(distance.cdist(n[i], n[i], 'euclidean').reshape(-1))) for i in range(len(n)) ]
r=[ distance.cdist(n[i], n[i], 'euclidean') for i in range(len(n)) ]

answers={}
counts={}
for o in range(len(m)-1):
    if o not in counts: counts[o] = len(n[0])
    for p in range(o+1,len(m)):
        if p not in counts: counts[p] = len(n[p])
        q=set(m[o])&set(m[p])
        if len(q)>11:
            print (f'{o} in {p} == {len(q)}')
            matches=[]
            for s in q:
                if s==0.: continue
                ocords=np.where(r[o]==s)
                pcords=np.where(r[p]==s)
                if len(ocords[0]) != 2: print(f'error ocords {q}')
                if len(pcords[0]) != 2: print(f'error pcords {q}')

                matches.append((ocords[0],pcords[0]))
            
            supermatches=[]
            ### TODO need to assure that the 3 distances for each supermatch are not equal
            for i in matches:
                for j in i[0]:
                    for x in matches:
                        if np.array_equal(i[0],x[0]): continue
                        for y in x[0]:
                            if y==j:
                                #what are the 'opposites' in i[0]/x[0]
                                jj = i[0][0] if j == i[0][1] else i[0][1]
                                yy = x[0][0] if y == x[0][1] else x[0][1]
                                for a in matches:
                                    if ((jj==a[0][0] and yy==a[0][1]) or 
                                        (jj==a[0][1] and yy==a[0][0])):
                                        supermatches.append((i,x,a))

            if supermatches:
                supermatch=supermatches[0]
                unique_nodes=set()
                for sms in supermatches:
                    for item in sms:
                        for item1 in item:
                            [ unique_nodes.add(item2) for item2 in item1 ]
                counts[p] -= len(unique_nodes)

                c=[list(supermatch[x][0]) for x in range(len(supermatch))]
                d=[ int(x) for x in set(list(sum(c, []))) ]

                sets=defaultdict(list)
                [ sets[dd].append(sm[1]) for sm in supermatch for i,dd in enumerate(d) if dd in sm[0] ]
                plane=[]
                for k in sets.keys():
                    x=list(set(sets[k][0])&set(sets[k][1]))[0]
                    plane.append((tuple(n[o][k]),tuple(n[p][x])))
            
                answers[o,p]=sync_matrices(n[0],n[p],plane)

print([ len(a) for a in n ])
print(answers)
print(counts)
print(sum(counts.values()))
            

#print(r[0])
#m = (n == b).cumsum(0)                         # (numbers,boards,5,5)
#s = (n * b * (1-m)).sum((2,3))                 # (numbers,boards)
#w = (m.all(2) | m.all(3)).any(2).argmax(0)     # (boards,)

#print(s[w].diagonal()[w.argsort()[[0,-1]]])

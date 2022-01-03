import numpy as np
from re import findall
import copy


def intersect(points):
    a1,a2,b1,b2=points
    a1_inc=False; a2_inc=False; b1_inc=False; b2_inc=False
    assert(a1<=a2)
    assert(b1<=b2)

    if a2 < b1 or a1 > b2: return False

    if a1<=b1<=a2: b1_inc=True
    if a1<=b2<=a2: b2_inc=True
    if b1<=a1<=b2: a1_inc=True
    if b1<=a2<=b2: a2_inc=True

    if   b1_inc and b2_inc: rtn=(b1,b2)
    elif b1_inc and a2_inc: rtn=(b1,a2)
    elif a1_inc and a2_inc: rtn=(a1,a2)
    elif a1_inc and b2_inc: rtn=(a1,b2)

    return rtn

def check_cube(c):
    return (c[0]<=c[1]) and (c[2]<=c[3]) and (c[4]<=c[5])

def split(cube, intercept):
    new_cubes=[]
    if cube.x1 != intercept.x1:
        new_cubes.append((cube.x1, intercept.x1-1, cube.y1, cube.y2, cube.z1, cube.z2))
    if cube.x2 != intercept.x2:
        new_cubes.append((intercept.x2+1, cube.x2, cube.y1, cube.y2, cube.z1, cube.z2))

    if cube.y1 != intercept.y1:
        new_cubes.append((intercept.x1, intercept.x2, cube.y1, intercept.y1-1, cube.z1, cube.z2))
    if cube.y2 != intercept.y2:
        new_cubes.append((intercept.x1, intercept.x2, intercept.y2+1, cube.y2, cube.z1, cube.z2))

    if cube.z1 != intercept.z1:
        new_cubes.append((intercept.x1, intercept.x2, intercept.y1, intercept.y2, cube.z1, intercept.z1-1))
    if cube.z2 != intercept.z2:
        new_cubes.append((intercept.x1, intercept.x2, intercept.y1, intercept.y2, intercept.z2+1, cube.z2))

    return [ SubCube(a) for a in new_cubes if check_cube(a) ]



class SubCube():
    def __init__(s,coords):
        s.x1,s.x2,s.y1,s.y2,s.z1,s.z2 = coords

    def total(s):
        return (s.x2-s.x1+1)*(s.y2-s.y1+1)*(s.z2-s.z1+1)

    def __str__(s):
        return f'({s.x1},{s.x2},{s.y1},{s.y2},{s.z1},{s.z2}),{s.total()}'


class Cube():
    def __init__(s,coords, command):
        s.onoff= command == 'on'
        s.subs = [SubCube(coords)]

    def __str__(s):
        return ' '.join(str(x) for x in s.subs)

    def inclusive(s, c):
        remove_subs=[]
        add_subs=[]
        for a in s.subs:
            atot=a.total()
            for d in c.subs:
                x=intersect((a.x1,a.x2,d.x1,d.x2))
                y=intersect((a.y1,a.y2,d.y1,d.y2))
                z=intersect((a.z1,a.z2,d.z1,d.z2))
                if not x or not y or not z: continue
                nt=SubCube([i for b in (x,y,z) for i in b])
                splts=split(a,nt)
                add_subs.extend(splts)
                remove_subs.append(a)
        [s.subs.remove(x) for x in remove_subs]
        s.subs.extend(add_subs)

    def total(s):
        return sum([(a.total()) for a in s.subs]) if s.onoff else 0


data=[]

for line in open(0).readlines():
    c,d = line.split(' ')
    e=Cube(list(map(int, findall(r'-?\d+', d))),c)
    data.append(e)

for i,d in enumerate(data):
    for j in range(i-1,-1,-1):
        data[j].inclusive(d)

tot=0
for d in data:
    tot+=d.total()

print('total: ',tot)
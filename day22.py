import numpy as np
from re import findall

commands=[]
dat=[]

for line in open(0).readlines():
    c,d = line.split(' ')
    commands.append(c)
    dat.append(list(map(int, findall(r'-?\d+', d))))

data=np.array(dat)
shift=(-50, -50, -50)
size=(101,101,101)
onoff=np.full(size, False, dtype=bool)

for i,d in enumerate(data):
    d-=shift*2
    if max(d[0:2]) < 0 or min (d[0:2]) > 100: continue
    if max(d[2:4]) < 0 or min (d[2:4]) > 100: continue
    if max(d[4:6]) < 0 or min (d[4:6]) > 100: continue
    print(d,end=' ')
    x1,x2,y1,y2,z1,z2 = [ min(max(y,0),100) for y in d ]
    size=(min(abs(x2-x1),100)+1,min(abs(y2-y1),100)+1,min(abs(z2-z1),100)+1)
    print(np.prod(size), end=' ')
    v = np.full(size, commands[i] == "on", dtype=bool)
    onoff[x1:x2+1,y1:y2+1,z1:z2+1] = v
    print(commands[i], np.sum(onoff))

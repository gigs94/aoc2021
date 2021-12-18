import numpy as np
#target area: x=207..263, y=-115..-63
#line=re.match('target area: x=\d+..\d+, y=-\d+..\d+\n', open(0).read())
line=open(0).read().strip()
tx=sorted([ int(x) for x in line.split('=')[1].split(',')[0].split('..') ])
ty=sorted([ int(y) for y in line.split('=')[2].split(',')[0].split('..') ])
start=(0,0)

def on_target(xy):
    global tx,ty
    return ( tx[0] <= xy[0] <= tx[1] ) and ( ty[0] <= xy[1] <= ty[1] )

def overshot(x,y):
    global tx,ty
    return x > max(tx) or y < min(ty)

def shot_path(pos,shot):
    path=[]
    mh=0
    while(not overshot(*pos)):
        lpos=pos
        pos=(shot[0]+pos[0],shot[1]+pos[1])
        shot=(shot[0] if shot[0] == 0 else (abs(shot[0])-1)*np.sign(shot[0]), shot[1]-1)
        mh=mh if pos[1] < mh else pos[1]
    else:
        if on_target(lpos):
            max_height(mh)
            ot=True
            pos=lpos
        else:
            ot=False

    return ot,pos

def max_height(y):
    max_height.m = max(max_height.m,y)
    return max_height.m
max_height.m=0

assert(overshot(9999,9999) is True)
assert(overshot(-9999,9999) is False)
assert(overshot(9999,-9999) is True)
assert(on_target((207,-115)) is True)
assert(max_height(1) == 1)
assert(shot_path((0,0),(125,-45)) == (True, (249,-91)))
assert(shot_path((0,0),(250,-10)) == (False, (499, -21)))


def calc_maxx(minx,maxx):
    for a in range(maxx,0,-1):
        b=sum(range(0,a+1))
        if b < maxx:
            return a

def calc_minx(minx,maxx):
    for a in range(0,maxx):
        b=sum(range(0,a+1))
        if b > minx:
            return a

minx=calc_minx(*tx)
maxx=calc_maxx(*tx)

c=0
for i in range(minx,max(tx)+2):
    for j in range (min(ty)-2,6555):
        ot,last=shot_path((0,0),(i,j))
        if ot: c+=1

print(c,max_height.m)
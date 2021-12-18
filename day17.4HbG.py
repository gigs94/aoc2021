# Modified from https://www.reddit.com/r/adventofcode/comments/ri9kdq/2021_day_17_solutions/howmp71/?context=3
# 
import numpy as np
from re import findall
x1,x2,y1,y2 = map(int, findall(r'-?\d+', open(0).read()))

def xs(v, p=0):
    while p<=x2: yield p>=x1; p+=v; v-=(v>0)

def ys(v, p=0):
    while p>=y1: yield p<=y2; p+=v; v-=1

def hs(v, p=0):
    iv=v
    while p>=y1:
        if p>hs.maxh: hs.maxh=p; hs.iv=iv
        p+=v; v-=1
hs.maxh=0
hs.iv=0

z=np.array([ [ any(map(lambda a,b: a&b, xs(x), ys(y))) for x in range(1+x2) ] for y in range(y1,-y1) ]).T
[ hs(yi+y1) if any(z[:,yi]) else None for yi in range(z.shape[1]) ] 
xss=[ xi for xi in range(z.shape[0]) if z[xi,hs.iv] ] 
print(f'#solutions:{np.count_nonzero(z)}\nmax height:{hs.maxh}\nsolution coords:({xss}, {hs.iv})')
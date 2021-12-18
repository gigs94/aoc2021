from re import findall
x1,x2,y1,y2 = map(int, findall(r'-?\d+', open(0).read()))

def xs(v, p=0):
    while p<=x2: yield p>=x1; p+=v; v-=(v>0)

def ys(v, p=0):
    while p>=y1: yield p<=y2; p+=v; v-=1


c=0
for x in range(1+x2):
    for y in range(y1,-y1):
        z=map(lambda a,b: a&b, xs(x), ys(y))
        if any(z):
            print(list(z))
            c+=1
print(c)
#print(sum(any(map(lambda a,b: a&b, xs(x), ys(y))) for x in range(1+x2) for y in range(y1,-y1)))
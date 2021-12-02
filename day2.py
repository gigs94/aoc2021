def up(p, value):
    p[1] -= int(value)
    return p 

def down(p, value):
    p[1] += int(value)
    return p 

def forward(p, value):
    p[0] += int(value)
    return p
    
def part1(p):
    with open('day2.dat') as f:
        [ eval(x)(p,y) for x,y in ( l.split() for l in f ) ]
    return p

p=[0,0]
p1=part1(p)
print(p1, p1[0]*p1[1])

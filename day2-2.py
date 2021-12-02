def up(p, value):
    p[2] -= int(value)
    return p 

def down(p, value):
    p[2] += int(value)
    return p 

def forward(p, value):
    p[0] += int(value)
    p[1] += p[2]*int(value)
    return p
    
def run(p):
    #with open('day2.example.txt') as f:
    with open('day2.dat') as f:
        [ eval(x)(p,y) for x,y in ( l.split() for l in f ) ]
    return p

# x,y,aim
p=[0,0,0]
p1=run(p)
print(p1, p1[0]*p1[1])

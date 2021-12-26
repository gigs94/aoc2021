
def roll():
    roll.n+=1
    roll.v= roll.v+1 if roll.v != 100 else 1
    return roll.v
roll.v=0
roll.n=0

p1p=4
p2p=8
##p1p=7
##p2p=6
p1=0
p2=0

def move(s):
    x=(s+roll()+roll()+roll())%10
    return x if x!=0 else 10


for turn in range(10000):
    p1p=move(p1p)
    p1+=p1p
    if p1>=1000:break
    p2p=move(p2p)
    p2+=p2p
    if p2>=1000:break

print(p1*roll.n if p1<1000 else p2*roll.n)
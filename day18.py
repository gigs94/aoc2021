from regex import findall

def mag(vals,levs):
    while levs[0] != 0:
        i=0
        while levs[i] != levs[i+1]: i+=1
        vals.insert(i,vals.pop(i)*3+vals.pop(i)*2)
        l=levs.pop(i)-1; levs.pop(i)
        levs.insert(i,l)
    return vals[0]

def parse(line):
    vals = []; levs = []; level = 0
    for p in findall(r'\[|\]|-?\d+', line.strip()):
        if p.isnumeric():
            vals.append(int(p)); levs.append(level)
        else:
            level += '],['.find(p) - 1
    return vals,levs

def explode(vals,levs):
    i=0
    while levs[i] < 5: i+=1
    l=levs[i]-1

    if i-1 >= 0:
        vals[i-1]+=vals.pop(i); levs.pop(i)
    else:
        vals.pop(i); levs.pop(i)

    if i+1 < len(vals):
        x=vals.pop(i); levs.pop(i)
        vals[i]+=x
    else:
        vals.pop(i); levs.pop(i)

    vals.insert(i,0); levs.insert(i,l)
    return (vals,levs)


def split(vals,levs):
    i=0
    while vals[i] < 10: i+=1
    v=vals[i]; l=levs[i]+1
    vals.pop(i); levs.pop(i)
    low=v//2; high=(v+1)//2

    vals.insert(i,high); vals.insert(i,low)
    levs.insert(i,l); levs.insert(i,l)
    return (vals,levs)

def add(l1,l2):
    vals = l1[0].copy(); vals.extend(l2[0])
    levs = l1[1].copy(); levs.extend(l2[1])
    levs = [ int(x)+1 for x in levs ]

    while True:
        if (max(levs) >= 5): vals,levs=explode(vals,levs)
        elif (max(vals) >= 10): vals,levs=split(vals,levs)
        else: break

    return vals,levs

if __name__ == '__main__':
    z=[ parse(line) for line in open(0).readlines() ]
    result=z[0]; m=0
    for a in z[1:]:
        result=add(result, a)

    for a in range(len(z)-1):
        for b in range(a+1,len(z)):
            m=max(mag(*add(z[a], z[b])), m)
            m=max(mag(*add(z[b], z[a])), m)
    print(f'part1: {mag(*result)}\npart2: {m}')
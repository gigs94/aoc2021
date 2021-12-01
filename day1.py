def count(values):
    count=0
    p=values[0]
    for line in values[1:]:
        l=int(line)
        if l>p:
           count += 1
        p=l
    return count
    
def part1():
    with open('day1.txt') as f:
        p=int(f.readline())
        line=f.readline()
        count=0
        while line:
            l=int(line)
            if l>p:
               count += 1
            p=l
            line=f.readline()
        print(count)

def part2():
    with open('day1.txt') as f:
        m1=int(f.readline())
        m2=int(f.readline())
        line=f.readline()
        sums=[]
        while line:
            m3=int(line)
            sums.append(m1+m2+m3)
            m1=m2
            m2=m3
            line=f.readline()
        print(count(sums))

part1()
part2()

import argparse as ap
import numpy as np
import pprint as pp

opens=( '(','{','[','<' )
closes=( ')','}',']','>' )
escore= {'': 0,
         ')': 3,
         ']': 57,
         '}': 1197,
         '>': 25137}

iscore= {'': 0,
         ')': 1,
         ']': 2,
         '}': 3,
         '>': 4}

def incomplete_score(s):
    score=0
    multiplier=5
    while len(s) > 0:
        x=expected(s.pop())
        score = score*multiplier + iscore[x]
    return score

def expected(opener):
    return closes[opens.index(opener)]

def find_chunks(s,stack,pos):
    rtn=""
    if len(s) == pos: return rtn
    if s[pos] in opens:
        stack.append(s[pos])
        rtn += find_chunks(s, stack, pos+1)
    elif s[pos] in closes:
        opener=stack.pop() 
        if s[pos] != expected(opener):
            rtn += s[pos]
        else:
            rtn += find_chunks(s, stack, pos+1)
    else:
        print(f'invalid char {s[pos]}')
        rtn += s[pos]

    return rtn if rtn != '' else ''.join(str(j) for j in stack)
    

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day10.dat', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data=list()
        i=[list(l.strip()) for l in f.readlines() ]

        errors=[ find_chunks(x,[],0) for x in [ y for y in i ] ]
        error_score=sum([ escore[i] if i in escore else 0 for i in errors ])
        inc_score=sorted([ incomplete_score(list(i)) if len(i) > 1 else 0 for i in errors ])
        inc_score = [value for value in inc_score if value != 0]
        middle=int(len(inc_score)/2)
        print(f'part1: {error_score}')
        print(f'part2: {inc_score[middle]}')
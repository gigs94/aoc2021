# references:  https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s15.html
import math
import argparse as ap
import numpy as np
import networkx as nx
import regex as re
from numpy.core.defchararray import endswith


class Xlator(dict):
    """ All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._make_regex().sub(self, text)

def multiple_replace(rx, d, text):
  # For each match, look-up corresponding value in dictionary
  return rx.sub(lambda mo: d[mo.string[mo.start():mo.end()+1]], text) 

def create_re(d):
  rx = re.compile("(%s)" % "|".join(d.keys()))
  print(rx)
  return rx

def stats(line):
    last=line[-1]
    linel=line[0:-1]
    counts=np.array([linel.count(i) for i in ['B', 'C', 'H', 'N']])
    counts2=np.array([line.count(i) for i in ['B', 'C', 'H', 'N']])
    #remove the last value
    print(counts,counts2)
    return counts

def score(line):
    u=np.unique(list(line))
    counts=[line.count(i) for i in u]
    counts.sort()
    return abs(counts[0]-counts[-1])

def blah(line,subs,l,ljump,lmax, combstats):
    if l > lmax:
        return combstats
    first=''
    newline=''
    for second in line:
        if first != '':
            nl,stats=subs[first+second]
            combstats+=stats
            combstats+=blah(nl,subs,l+ljump,ljump,lmax,combstats)
        first=second
    last=line[-1]
    combstats+=np.array([last.count(i) for i in ['B', 'C', 'H', 'N']])
    return combstats

def substring(line,subs):
        first=''
        newline=''
        for second in line:
            if first != '':
                newline+=first
                newline+=subs[first+second]
            first=second
        newline+=second
        return newline

def add_results(a1,a2):
    a={}
    for k in np.unique(list(a1.keys())+list(a2.keys())):
        a[k]=a1[k] if k in a1 else 0
        a[k]+=a2[k] if k in a2 else 0

    return a

def traverse(c,d,l,lmax):
    if l==lmax+1:
        counts={i:1 for i in c[0]}
        return counts
    else:
        l+=1
    x=d[c]

    return add_results(a1=traverse(c[0]+x,d,l,lmax), a2=traverse(x+c[1],d,l,lmax))


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day14.dat', type=str)
    parser.add_argument('-c', default='10', type=int)
    args = parser.parse_args()

    with open(args.file) as f:
        first=True
        subs={}
        subs2={}
        subs2a={}
        for l in f.readlines():
            l=l.strip()
            if first:
                first=False
                line=l
            elif l != '':
                a,_,val=l.strip().split(' ')
                subs[a]=val
                b=f'{a[0]}(?={a[1]})'
                subs2[b]=a[0]+val
                subs2a[a]=a[0]+val

        print(subs)
        #print(subs2)
        #print(subs2a)

        #xlat=Xlator(subs2)
        #rx=create_re(subs2)
        #print(rx)

        #print(line[0:2])
        #print(line[1:3])
        #print(line[2:4])
        #print(line[-1])
        #score1=traverse(line[0:2],subs,0,args.c)
        #print(score1)
        #score2=traverse(line[1:3],subs,0,args.c)
        #print(score2)
        #score3=traverse(line[2:4],subs,0,args.c)
        #print(score3)
        #score4=add_results(score1,score2)
        #score5=add_results(score4,score3)

        #score=add_results(score5, {i:1 for i in line[-1]})
        #scores=list(score.values())
        #print(scores)
        #print(f'{abs(max(scores)-min(scores))}')
        #for i in range(0,args.c):
            #nal=substring(line) if i < 10 else None
            #nl=multiple_replace(rx,subs2a,line)
            #nl=xlat.xlat(line)
            #print(i+1,score(nl),nal==nl,nl,nal) if i < 10 else print(i+1,score(nl))
            #line=nl

        tenStep={}
        for k in subs.keys():
            l=k
            for i in range(0,10):
                nl=substring(l,subs)
                l=nl
            print(k,stats(l)) 
            tenStep[k]=[l, stats(l)]

        combstats=np.array([0,0,0,0]) #B,C,H,N
        results=blah(line,tenStep,0,10,40,combstats)
        print(results)
        print(f'{max(results)-min(results)}')

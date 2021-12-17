import math
import operator

D=False

ltotal,cur = 0,0

def reset():
    global ltotal,cur
    cur = 0
    ltotal = 0

def remaining():
    global ltotal,cur
    return ltotal-cur

def f(x, l):
    global cur,ltotal
    b= f'{int(x,16):0{len(x)*4}b}'
    ltotal=len(b)
    a = b[cur:cur+l]
    if D: print(f'{b} {len(b)} ltotal: {ltotal} cur: {cur}   a: {a}')
    cur += l
    return a

ids=[ 'sum', 'math.prod', 'min', 'max', '', 'operator.gt', 'operator.lt', 'operator.eq' ]

def process(id,vals):
    global ids
    if id < 4:
        return eval(ids[id])(vals)
    else:
        return eval(ids[id])(*vals)

def proc_msg(x):
    ver = int(f(x, 3), 2)
    if D: print(f'ver: {ver}')
    id = int(f(x, 3), 2)
    if D: print(id)
    if id == 4:
        field = bin(0)
        while f(x, 1) == "1":
            # read field
            field += f(x, 4)
        # this should be the last one
        field += f(x, 4)
        value=int(field,2)
    else:
        l = f(x, 1)
        if l == '0':
            tlen = int(f(x, 15),2)
            offset = cur+tlen
            if D: print(tlen,offset,ltotal,cur)
            vals=[]
            while(tlen > 0):
                v,val=proc_msg(x)
                ver+=v
                vals.append(val)
                if cur == offset:
                    break
            value=process(id,vals)

        elif l == '1':
            tpack = int(f(x, 11),2)
            if D: print(f'tpack: {tpack}')
            vals=[]
            for i in range(0,tpack):
                if D: print(f'....{i}')
                v,val=proc_msg(x)
                ver+=v
                vals.append(val)
                if D: print(f'loop:{i+1}/{tpack} ver: {ver}')
            value=process(id,vals)
        else:
            print(f'what?! l should be 0/1 but it was: "{l}"')
            print(f'{ltotal} {cur} {ver} {id}')
            exit()
    if D: print(f'return ver= {ver}')
    return ver,value


for x in open(0).read().strip().split('\n'):
    print(f'answer({x}): {proc_msg(x)}')
    reset()
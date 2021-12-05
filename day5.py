import argparse as ap
import numpy as np

def read_vents(fn):
    with open(fn) as f:
        vent_cords=[]
        for l in f.readlines():
            xyza=l.strip().replace(' -> ',',').split(',')
            vent_cords.append([(int(xyza[0]),int(xyza[1])), (int(xyza[2]),int(xyza[3]))])
        return vent_cords

def map_size(cs):
    x=0
    y=0
    for c in cs:
        x = c[0][0] if c[0][0] > x else x
        y = c[0][1] if c[0][1] > y else y
    return (x+1,y+1)

def get_hor_vert(vcs):
    only_hvs=[]
    only_diags=[]
    for start,end in vcs:
        if start[0] == end[0] or start[1] == end[1]:
            # we have a hor/ver line
            only_hvs.append((start,end))
        else:
            # diagonal
            only_diags.append((start,end))

    return only_hvs, only_diags
            
def bad_coords(vcs,s):
    bad_coords=np.zeros(s)
    for vc in vcs:
        x,y,z,a=vc[0][0],vc[0][1],vc[1][0],vc[1][1]
        xdir=-1 if x>z else 1 if x != z else 0
        ydir=-1 if y>a else 1 if y != a else 0
        
        xcur=x
        ycur=y

        while (xcur,ycur) != (z+xdir,a+ydir):
            bad_coords[xcur][ycur] += 1
            xcur+=xdir
            ycur+=ydir
            if (xdir and xcur > z) and (ydir and ycur > a) and (not xdir and xcur < z) and (not ydir and ycur < a):
                print(f'error!  data if fucked {x} {y} {z} {a} {xdir} {xcur} {ydir} {ycur}')

    return bad_coords
        
if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('file', nargs='?', default='day5.dat', type=str)
    args = parser.parse_args()

    v=read_vents(args.file)
    s=map_size(v)
    bcs=bad_coords(v,s)
    avoid=np.nonzero(bcs>1)
    print(len(avoid[0]))
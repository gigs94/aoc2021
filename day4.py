import argparse as ap
import numpy as np

def check_board(boards,bi):
    board=boards[bi]
#    print(board)
    return np.any(np.all(board==0,axis=0)) or np.any(np.all(board==0,axis=1))

def run(file):
    with open(file) as f:
        called_numbers = [int(i) for i in f.readline().strip().split(',')]

        boards=[]
        board=[]
        lines = f.readlines()
        counter=0
        for l in lines:
            a = [int(i) for i in l.strip().split()]

            if len(a) == 0: continue
            board.append(a)
            counter+=1
            
            if counter == 5:
                boards.append(np.asarray(board))
                board=[]
                counter=0

        ob=boards

        win_order=[]
        winners=[]

        for x in called_numbers:
            for bi,b in enumerate(boards):
                if bi in winners: continue
                
                for ri,r in enumerate(b):
                    for vi,v in enumerate(r):
                        if v == x: 
                            boards[bi][ri][vi] = 0
                if check_board(boards,bi):
                    winners.append(bi)
                    s=sum(sum(boards[bi]))
                    a=s*x
                    win_order.append([bi,s,x,a])
        print(f'winner = {win_order[0]}')
        print(f'loser = {win_order[-1]}')
        print(ob[win_order[-1][0]])

parser = ap.ArgumentParser()
parser.add_argument('file', nargs='?', default='day4.dat', type=str)
args = parser.parse_args()

a=run(args.file)
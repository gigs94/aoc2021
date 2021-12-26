p1, p2 = 0, []
points = [0, 3, 57, 1197, 25137]

for chunk in open(0):
    stack = []
    for p in chunk.strip():
        ix = '<{[( )]}>'.find(p) - 4
        if ix < 0:    # open bracket
            stack.append(-ix)
        elif ix != stack.pop():
            p1 += points[ix]
            break
    else:
        p2 += [sum(5**a * b for a, b in enumerate(stack))]

print(p1, sorted(p2)[len(p2)//2])
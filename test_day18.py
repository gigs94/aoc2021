from day18 import *

assert(mag(*parse('[[1,2],[[3,4],5]]')) == 143)
assert(mag(*parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')) == 1384)
assert(mag(*parse('[[[[1,1],[2,2]],[3,3]],[4,4]]')) == 445)
assert(mag(*parse('[[[[3,0],[5,3]],[4,4]],[5,5]]')) == 791)
assert(mag(*parse('[[[[5,0],[7,4]],[5,5]],[6,6]]')) == 1137)
assert(mag(*parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')) == 3488)

assert(explode(*parse('[[[[[9,8],1],2],3],4]')) == parse('[[[[0,9],2],3],4]'))
assert(explode(*parse('[7,[6,[5,[4,[3,2]]]]]')) == parse('[7,[6,[5,[7,0]]]]'))
assert(explode(*parse('[[6,[5,[4,[3,2]]]],1]')) == parse('[[6,[5,[7,0]]],3]'))
assert(explode(*parse('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')) == parse('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))
assert(explode(*parse('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')) == parse('[[3,[2,[8,0]]],[9,[5,[7,0]]]]'))

assert(split(*parse('[[[[0,7],4],[15,[0,13]]],[1,1]]')) == parse('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'))
assert(split(*parse('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')) == parse('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'))


x=parse('[[[[4,3],4],4],[7,[[8,4],9]]]')
y=parse('[1,1]')
assert(add(x,y) == parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'))

a=parse('[1,1]'); b=parse('[2,2]'); c=parse('[3,3]'); d=parse('[4,4]'); e=parse('[5,5]'); f=parse('[6,6]')
assert(add(add(add(a,b),c),d) == parse('[[[[1,1],[2,2]],[3,3]],[4,4]]'))
a=parse('[1,1]'); b=parse('[2,2]'); c=parse('[3,3]'); d=parse('[4,4]'); e=parse('[5,5]'); f=parse('[6,6]')
assert(add(add(add(add(a,b),c),d),e) == parse('[[[[3,0],[5,3]],[4,4]],[5,5]]'))
a=parse('[1,1]'); b=parse('[2,2]'); c=parse('[3,3]'); d=parse('[4,4]'); e=parse('[5,5]'); f=parse('[6,6]')
assert(add(add(add(add(add(a,b),c),d),e),f) == parse('[[[[5,0],[7,4]],[5,5]],[6,6]]'))
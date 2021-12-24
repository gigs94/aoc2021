
from collections import defaultdict
from itertools import combinations, product
from math import sqrt
from typing import List

from collections import namedtuple
from itertools import filterfalse, tee, islice
from pathlib import Path
from typing import List, Callable, Iterable, Iterator


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.x} {self.y}'


class Point3(namedtuple('Point', 'x y z')):
    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'

def to_point(p: str, sep=",") -> Point:
    p = p.split(sep)
    return Point(int(p[0]), int(p[1]))


def get_neighbours_4(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)]
    return filter(lambda x: is_in_grid(x, p_max), points)


def get_neighbours_8(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]
    return filter(lambda n: is_in_grid(n, p_max), points)


def is_in_grid(p: Point, p_max: Point) -> bool:
    return (p.x >= 0) and (p.y >= 0) and (p.x < p_max.x) and (p.y < p_max.y)


def from_grid(p: Point, grid: List[List[int]]) -> int:
    return grid[p.y][p.x]


def manhattan_distance(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_lines(file_name: str) -> List[str]:
    file = Path(__file__).parents[2] / "inputs" / file_name
    with file.open('r') as f:
        lines = f.read().splitlines()
    return lines


def partition(predicate: Callable, iterable: Iterable) -> (Iterable, Iterable):
    t1, t2 = tee(iterable)
    return filterfalse(predicate, t1), filter(predicate, t2)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def line_to_int(line: str, split_char=",") -> List[int]:
    return [int(i) for i in line.split(split_char) if len(i) > 0]

# performed x y z rotations in a loop and stored in a set
rotations = [([2, 0, 1], [-1, -1, 1]), ([0, 1, 2], [1, -1, -1]), ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, -1, 1]),
             ([0, 2, 1], [-1, -1, -1]), ([1, 2, 0], [1, -1, -1]), ([1, 0, 2], [-1, -1, -1]), ([1, 2, 0], [1, 1, 1]),
             ([0, 2, 1], [-1, 1, 1]), ([0, 1, 2], [-1, 1, -1]), ([0, 2, 1], [1, -1, 1]), ([2, 0, 1], [-1, 1, -1]),
             ([1, 0, 2], [1, 1, -1]), ([2, 1, 0], [1, 1, -1]), ([2, 0, 1], [1, 1, 1]), ([2, 1, 0], [-1, 1, 1]),
             ([0, 1, 2], [1, 1, 1]), ([1, 0, 2], [1, -1, 1]), ([1, 0, 2], [-1, 1, 1]), ([0, 1, 2], [-1, -1, 1]),
             ([1, 2, 0], [-1, 1, -1]), ([1, 2, 0], [-1, -1, 1]), ([0, 2, 1], [1, 1, -1]), ([2, 0, 1], [1, -1, -1])]


def parse_input(lines):
    scanners = {}
    cur_scanner = []
    i = 0
    lines.append("")
    for line in filter(lambda x: not x.startswith("---"), lines):
        if len(line) == 0 and len(cur_scanner) > 0:
            scanners[i] = cur_scanner
            cur_scanner = []
            i += 1
        else:
            cur_scanner.append([int(t) for t in line.split(",")])
    return scanners


def part_1(scanners) -> (int, List[List[int]]):
    intersects = get_intersections(scanners)
    mapping_dict = generate_mappings(intersects, scanners)
    beacons = set(to_point(p) for p in scanners[0])
    used_mappings = set()
    transformed_scanners = {0}
    scanner_origins = [[0, 0, 0]]
    while len(transformed_scanners) < len(scanners):
        queue = [k for k in mapping_dict.keys()
                 if k[0] in transformed_scanners and k[1] not in transformed_scanners]
        while len(queue) > 0:
            el = queue.pop()
            if el[1] in transformed_scanners:
                continue
            p_transpose = list(zip(*scanners[el[1]]))
            centroid = list(zip([0, 0, 0]))  # origin relative to scanner itself is 0, 0, 0
            use_mapping = el
            while True:
                centroid = transform(centroid, *mapping_dict[use_mapping])
                p_transpose = transform(p_transpose, *mapping_dict[use_mapping])
                new_points = set(to_point(p) for p in zip(*p_transpose))
                if use_mapping[0] == 0:
                    break
                for mapping in used_mappings:
                    if mapping[1] == use_mapping[0]:
                        use_mapping = mapping
                        break
            scanner_origins.append([centroid[0][0], centroid[1][0], centroid[2][0]])
            transformed_scanners.add(el[1])
            beacons.update(new_points)
            used_mappings.add(el)
    return len(beacons), scanner_origins


def part_2(scanner_origins: List) -> int:
    return max(sum(map(lambda x: abs(x[0] - x[1]), zip(*p))) for p in combinations(scanner_origins, 2))


def generate_mappings(intersects, scanners):
    mapping_dict = {}
    for i in intersects:
        p2dist_a = defaultdict(set)
        for p in combinations(scanners[i[0]], 2):
            dist = euclid_distance(*p)
            p2dist_a[to_point(p[0])].add(dist)
            p2dist_a[to_point(p[1])].add(dist)
        p2dist_b = defaultdict(set)
        for p in combinations(scanners[i[1]], 2):
            dist = euclid_distance(*p)
            p2dist_b[to_point(p[0])].add(dist)
            p2dist_b[to_point(p[1])].add(dist)
        points_a = []
        points_b = []
        for p in product(p2dist_a.keys(), p2dist_b.keys()):
            intersect = p2dist_a[p[0]].intersection(p2dist_b[p[1]])
            if len(intersect) >= 11:  # 12 common beacons 1 src and 11 dst for distance
                points_a.append(point_to_list(p[0]))
                points_b.append(point_to_list(p[1]))
        mapping_dict[i] = map_scanner_a_to_b(points_a, points_b)
    return mapping_dict


def map_scanner_a_to_b(points_a, points_b):
    a_transpose = list(zip(*points_a))
    b_transpose = list(zip(*points_b))
    for perms, signs in rotations:
        rotated = rotate(b_transpose, perms, signs)
        offset = []
        for p in zip(rotated, a_transpose):
            points = set([x[1] - x[0] for x in zip(p[0], p[1])])
            if len(points) == 1:
                offset.append(points.pop())
            if len(offset) == 3:
                return offset, perms, signs
    return None


def transform(to_transform, target_center, trans_perm, trans_sign):
    rotated = rotate(to_transform, trans_perm, trans_sign)
    return [list(map(lambda x: target_center[i] + x, p)) for i, p in enumerate(rotated)]


def get_intersections(scanners):
    intersections = []
    distance_dict = {i: set(euclid_distance(*p) for p in combinations(scanners[i], 2)) for i in scanners.keys()}
    for i in combinations(range(len(scanners)), 2):
        if len(distance_dict[i[0]].intersection(distance_dict[i[1]])) >= 66:  # 12!/10! / 2
            intersections.append(i)
            intersections.append((i[1], i[0]))
    return intersections


def rotate(point, perms, signs):
    return map(lambda n: n * signs[0], point[perms[0]]), \
           map(lambda n: n * signs[1], point[perms[1]]), \
           map(lambda n: n * signs[2], point[perms[2]])


def euclid_distance(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def to_point(plist):
    if len(plist) == 3:
        return Point3(plist[0], plist[1], plist[2])
    else:
        raise Exception("Can't cover to point")


def point_to_list(p):
    return [p.x, p.y, p.z]


def main():
    lines = open(0).read().split('\n')
    scanners = parse_input(lines)
    part1, centroids = part_1(scanners)
    print("Part 1:", part1)
    print("Part 2:", part_2(centroids))


if __name__ == '__main__':
    main()
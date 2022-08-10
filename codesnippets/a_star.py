from copy import deepcopy
from queue import PriorityQueue


def neighbors(node):
    global current_x0, current_y0

    result = set()

    for x in range(3):
        for y in range(3):
            if node[x][y] == 0:
                current_x0 = x
                current_y0 = y

    for (dx, dy) in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
        if 0 <= current_x0 + dx < 3 and 0 <= current_y0 + dy < 3:
            move = deepcopy(list(list(row) for row in node))
            move[current_x0][current_y0] = node[current_x0 + dx][current_y0 + dy]
            move[current_x0 + dx][current_y0 + dy] = node[current_x0][current_y0]
            result.add(tuple(tuple(row) for row in move))

    return result


def distance(current, target):
    global current_0, target_0

    for x in range(3):
        for y in range(3):
            if current[x][y] == 0:
                current_0 = (x, y)

    for x in range(3):
        for y in range(3):
            if target[x][y] == 0:
                target_0 = (x, y)

    return abs(target_0[0] - current_0[0]) + abs(target_0[1] - current_0[1])


def a_star(start, target):
    global v

    queue = PriorityQueue()
    queue.put((0, start))

    discovered = {start: (None, 0)}

    while queue:
        v = queue.get()[1]

        if v == target:
            break

        for w in neighbors(v):
            if w not in discovered:
                discovered[w] = (v, discovered[v][1] + 1)
                queue.put((discovered[w][1] + distance(w, target), w))

    path = [v]
    while v in discovered:
        v = discovered[v][0]
        path.append(v)

    path.reverse()
    return path


def main():
    start = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
    target = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

    path = a_star(start, target)
    for node in path:
        print(node)

    print(len(path) - 1)


main()

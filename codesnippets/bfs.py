from copy import deepcopy
from queue import PriorityQueue


def neighbors(node):
    global x0, y0

    result = set()

    for x in range(3):
        for y in range(3):
            if node[x][y] == 0:
                x0 = x
                y0 = y

    for (dx, dy) in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
        if 0 <= x0 + dx < 3 and 0 <= y0 + dy < 3:
            move = deepcopy(list(list(row) for row in node))
            move[x0][y0] = node[x0 + dx][y0 + dy]
            move[x0 + dx][y0 + dy] = node[x0][y0]
            result.add(tuple(tuple(row) for row in move))

    return result


def bfs(start, target):
    global v

    queue = PriorityQueue()
    queue.put(start)

    discovered = {start: None}

    while queue:
        v = queue.get()

        if v == target:
            break

        for w in neighbors(v):
            if w not in discovered:
                discovered[w] = v
                queue.put(w)

    path = [v]
    while v in discovered:
        v = discovered[v]
        path.append(v)

    path.reverse()
    return path


def dfs(start, target):
    global v

    stack = [start]
    discovered = {start: None}

    while stack:
        v = stack.pop()

        if v == target:
            break

        for w in neighbors(v):
            if w not in discovered:
                discovered[w] = v
                stack.append(w)

    path = [v]
    while v in discovered:
        v = discovered[v]
        path.append(v)

    path.reverse()
    return path


def main():
    start = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
    target = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

    path = bfs(start, target)
    for node in path:
        print(node)

    print(len(path) - 1)


main()
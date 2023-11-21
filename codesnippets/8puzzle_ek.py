import numpy as np
from copy import deepcopy
from queue import PriorityQueue


def move_left(data, x0, y0):
    for x in range(3):
        for y in range(3):
            ynew = y0 + 1
            if ynew >= 0 and ynew < 3:
                result = deepcopy(list(list(row) for row in data))
                result[x0][y0] = data[x0][ynew]
                result[x0][ynew] = data[x0][y0]
                return result


def move_right(data, x0, y0):
    for x in range(3):
        for y in range(3):
            ynew = y0 - 1
            if ynew >= 0 and ynew < 3:
                result = deepcopy(list(list(row) for row in data))
                result[x0][y0] = data[x0][ynew]
                result[x0][ynew] = data[x0][y0]
                return result


def move_up(data, x0, y0):
    for x in range(3):
        for y in range(3):
            xnew = x0 - 1
            if xnew >= 0 and xnew < 3:
                result = deepcopy(list(list(row) for row in data))
                result[x0][y0] = data[xnew][y0]
                result[xnew][y0] = data[x0][y0]
                return result


def move_down(data, x0, y0):
    for x in range(3):
        for y in range(3):
            xnew = x0 + 1
            if xnew >= 0 and xnew < 3:
                result = deepcopy(list(list(row) for row in data))
                result[x0][y0] = data[xnew][y0]
                result[xnew][y0] = data[x0][y0]
                return result


def get_moves(node):
    global x0, y0

    result = set()

    # find posi of 0
    for x in range(3):
        for y in range(3):
            if node[x][y] == 0:
                x0 = x
                y0 = y

    # print("x: %d y: %d"%(x0,y0))
    #add all paths that can be done to the resultlist
    if (move_down(node, x0, y0)):
        result.add(tuple(tuple(row) for row in move_down(node, x0, y0)))
    if (move_up(node, x0, y0)):
        result.add(tuple(tuple(row) for row in move_up(node, x0, y0)))
    if (move_left(node, x0, y0)):
        result.add(tuple(tuple(row) for row in move_left(node, x0, y0)))
    if (move_right(node, x0, y0)):
        result.add(tuple(tuple(row) for row in move_right(node, x0, y0)))

    return result


#breadth first search
def bfs(start, target):
    global v

    queue = PriorityQueue()
    queue.put(start)

    reached = {start: None}
    while queue:
        v = queue.get()

        # state = goal
        if v == target:
            break

        # expandieren
        for w in get_moves(v):
            if w not in reached:
                reached[w] = v
                queue.put(w)

    path = [v]
    while v in reached:
        v = reached[v]
        path.append(v)

    path.reverse()
    return path

#deep first search
def dfs(start, target):
    global v

    stack = [start]
    reached = {start: None}

    while stack:
        v = stack.pop()
        if v == target:
            break

        #for every way in possible moves
        for w in get_moves(v):
            #if we havent discovered this way yet, we put it on the stack of reached
            if w not in reached:
                reached[w] = v
                stack.append(w)

    path = [v]
    while v in reached:
        v = reached[v]
        path.append(v)

    path.reverse()
    return path


def misplaced_tiles(current,target):
    #Admissible Heuristics missplaced tiles

    counter = 0
    for x in range (3):
        for y in range (3):
            if(current[x][y]!= target[x][y]):
               counter+= 1
    return counter

def distance(current, target):
    #manhatten distance to determine distance beetween target and goal
    global current_0, target_0

    for x in range(3):
        for y in range(3):
            if current[x][y] == 0:
                current_0 = (x, y)

    for x in range(3):
        for y in range(3):
            if target[x][y] == 0:
                target_0 = (x, y)

    #targetX - currentX + targetY- current Y
    return abs(target_0[0] - current_0[0]) + abs(target_0[1] - current_0[1])


def a_star(start, target):
#a star search algorithm
    global v

    queue = PriorityQueue()
    queue.put((0, start))

    reached = {start: (None, 0)}

    while queue:
        v = queue.get()[1]

        if v == target:
            break

        for w in get_moves(v):
            if w not in reached:
                reached[w] = (v, reached[v][1] + 1)
                print("cost to reach path: ",reached[v][1] + 1," distance to goal: ",distance(w, target))
                print("f(n) = ",reached[w][1] + distance(w, target), w)
                print("misplaced tiles heuristic",misplaced_tiles(w,target))
                queue.put((reached[w][1] + distance(w, target), w))

    path = [v]
    while v in reached:
        v = reached[v][0]
        path.append(v)

    path.reverse()
    return path


def main():
    start = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
    target = ((1, 2, 3), (8, 0, 4), (7, 6, 5))


    ##To change method (line 197); a_star or dfs or bfs
    #print path
    path = dfs(start, target)
    for node in path:
        print(node)


main()

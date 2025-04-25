import sys
from collections import deque

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        sys.exit(1)

    with open(sys.argv[2], 'r', encoding="utf-8") as file: #open file for reading
        cols = int(file.readline().strip()) #parse columns
        rows = int(file.readline().strip()) #parse rows

        robot = tuple() #starting position
        dirty = set() #set of dirty coordinates
        blocked = set() #set of blocked coordinates

        #parse grid
        for y in range(rows):
            line = file.readline().strip()
            for x in range(cols):
                coords = line[x]
                if (coords == '@'):
                    robot = (x, y) #assign start position
                elif (coords == '*'):
                    dirty.add((x, y)) #add coordinate to dirty set
                elif (coords == '#'):
                    blocked.add((x,y)) #add coordinate to blocked set

        initialState = (robot[0], robot[1], frozenset(dirty)) #state tracks robot position and dirty coordinates

    if (sys.argv[1] == "uniform-cost"): #uniform-cost search
        frontier = deque() #initialize queue
        frontier.append((initialState, [])) #push initial state and path into queue
        explored = set()
        expandedNodes = 0
        genNodes = 1

        while frontier: #while frontier is not empty
            state, path = frontier.popleft() #dequeue
            expandedNodes += 1

            if (len(state[2]) == 0): #no more dirty coordinates
                return expandPath(path, genNodes, expandedNodes) #return path
            
            actions = expandState(state, rows, cols, blocked) #expand state and get all successors from possible actions

            for childState, action in actions: #loop over all actions
                if (childState not in explored): #check if state has already been explored
                    explored.add(state)
                    frontier.append((childState, path + [action]))
                    genNodes += 1

    # elif (sys.argv[1] == "depth-first"): #depth-first search
    #     frontier = deque() #initialize stack
    #     frontier.append(initialState) #push initial state on stack
    #     explored = set() #set for explored states
    #     path = []

    #     while (len(frontier) != 0):
    #         state = frontier.pop() #pop 

    #         if (len(state[2]) == 0): #no more dirty coordinates
    #             return expandPath(path, genNodes, expandedNodes) #return path (should prob have a diff function)

    #         explored.add(state)
    #         actions = expandState(state, rows, cols, blocked)

    #         for action in actions:

    else:
        print("Incorrect algorithm inputted")
        sys.exit(1)



def expandState(state: tuple, rows: int, cols: int, blocked: set):
    posX, posY, dirty = state #unpack the robot location and current dirty coordinates

    if (posX, posY) in dirty: #check if current position is dirty               (maybe move this back to the end)
        updatedDirty = dirty - {(posX, posY)} #remove from dirty set
        yield ((posX, posY, updatedDirty), 'V') #vacuuming the position
        return

    for (changeX, changeY, direction) in [(0, -1, 'N'), (0, 1, 'S'), (-1, 0, 'W'), (1, 0, 'E')]: #loop over all directions
        successor = (posX + changeX, posY + changeY) #calculate new coordinates
        if inBounds(successor, rows, cols) and successor not in blocked: #check if new coordinates are in bounds and not blocked
            yield ((successor[0], successor[1], dirty), direction) #return new state and action to get to that state

def expandPath(path: list, genNodes: int, expandedNodes: int): #print path and stats
    for s in path:
        print(s)
    print(genNodes, "nodes generated")
    print(expandedNodes, "nodes expanded")

def inBounds(position: tuple, rows: int, cols: int): #checks if position is in bounds of the grid
    x, y = position
    return 0 <= x < cols and 0 <= y < rows

if __name__ == "__main__":
    main()
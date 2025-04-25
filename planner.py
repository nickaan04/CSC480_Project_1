import sys
from collections import deque

CARD_DIRECTIONS = [(0,-1,'N'), (0,1,'S'), (-1,0,'W'), (1,0,'E')]

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        sys.exit(1)

    with open(sys.argv[2], 'r', encoding="utf-8") as file: #open file for reading
        cols = int(file.readline().strip()) #parse columns
        rows = int(file.readline().strip()) #parse rows

        startPos = tuple() #starting position
        dirty = set() #set of dirty coordinates
        blocked = set() #set of blocked coordinates

        #parse grid
        for y in range(rows):
            line = file.readline().strip()
            for x in range(cols):
                coords = line[x]
                if (coords == '@'):
                    startPos = (x, y) #assign start position
                elif (coords == '*'):
                    dirty.add((x, y)) #add coordinate to dirty set
                elif (coords == '#'):
                    blocked.add((x,y)) #add coordinate to blocked set

        initialState = (startPos[0], startPos[1], frozenset(dirty)) #state tracks position and dirty coordinates

    search(initialState, rows, cols, blocked, sys.argv[1]) #call search function

def search(initialState: tuple, rows: int, cols: int, blocked: set, algorithm: str): #carry out the specified search algorithm
    expandedNodes, genNodes = 0, 1
    explored = set() #initialize explored set
    frontier = deque() #initialize queue or stack
    frontier.append((initialState, [])) #add initial state to frontier
    frontierStates = {initialState} #set of states in frontier

    while frontier: #while frontier is not empty
        if (algorithm == "uniform-cost"): #uniform-cost search
            state, path = frontier.popleft() #dequeue from queue
        elif (algorithm == "depth-first"): #depth-first search
            state, path = frontier.pop() #pop from stack
        else:
            print("Incorrect algorithm inputted")
            sys.exit(1)

        frontierStates.remove(state) #remove state from frontier
        expandedNodes += 1

        if (len(state[2]) == 0): #no more dirty coordinates
            return printPath(path, genNodes, expandedNodes) #return path

        explored.add(state) #mark state as explored

        for childState, action in expandState(state, rows, cols, blocked): #expand state and get all successors from possible actions
            if (childState not in explored and childState not in frontierStates): #check if state has already been explored
                #add new state to frontier and update path
                frontier.append((childState, path + [action]))
                frontierStates.add(childState)
                genNodes += 1

def expandState(state: tuple, rows: int, cols: int, blocked: set):
    posX, posY, dirty = state #unpack the robot location and current dirty coordinates

    if (posX, posY) in dirty: #check if current position is dirty
        updatedDirty = dirty - {(posX, posY)} #remove from dirty set
        yield ((posX, posY, updatedDirty), 'V') #vacuuming the position
        return

    for (changeX, changeY, direction) in CARD_DIRECTIONS: #loop over all directions
        childX, childY = posX + changeX, posY + changeY #calculate new coordinates
        if (0 <= childX < cols and 0 <= childY < rows and (childX, childY) not in blocked): #check if new coordinates are in bounds and not blocked
            yield ((childX, childY, dirty), direction) #return new state and action to get to that state

def printPath(path: list, genNodes: int, expandedNodes: int): #print path and stats
    for action in path:
        print(action)
    print(f"{genNodes} nodes generated")
    print(f"{expandedNodes} nodes expanded")

if __name__ == "__main__":
    main()
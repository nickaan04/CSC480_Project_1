import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        sys.exit(1)
    if sys.argv[1] not in ("uniform-cost", "depth-first"):
        print("Incorrect algorithm inputted")
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

        initialState = (robot[0], robot[1], dirty) #state tracks robot position and dirty coordinates



def expandState(state: (tuple), rows: int, cols: int, blocked: set):
    posX, posY, dirty = state #unpack the robot location and current dirty coordinates
    for (changeX, changeY, direction) in [(0, -1, 'N'), (0, 1, 'S'), (-1, 0, 'W'), (0, 1, 'E')]: #loop over all directions
        successor = (posX + changeX, posY + changeY) #calculate new coordinates
        if inBounds(successor, rows, cols) and successor not in blocked: #check if new coordinates are in bounds and not blocked
            yield ((successor[0], successor[1]), direction) #return new coordinates and direction
    
    if (posX, posY) in dirty: #check if current position is dirty
        updatedDirty = dirty - {(posX, posY)} #remove from dirty set
        yield ((posX, posY, updatedDirty), 'V') #vacuuming the position


def inBounds(position: tuple, rows: int, cols: int): #checks if position is in bounds of the grid
    if (position[0] < 0 or position[0] >= cols):
        return False
    if (position[1] < 0 or position[1] >= rows):
        return False
    return True


if __name__ == "__main__":
    main()
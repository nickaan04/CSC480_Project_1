import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        sys.exit(1)

    with open(sys.argv[2], 'r', encoding="utf-8") as file: #open file for reading
        cols = int(file.readline().strip()) #parse columns
        rows = int(file.readline().strip()) #parse rows

        start = tuple() #starting position
        dirty = set() #set of dirty coordinates
        blocked = set() #set of blocked coordinates

        for y in range(rows):
            line = file.readline().strip()
            for x in range(cols):
                coords = line[x]
                if (coords == '@'):
                    start = (x, y) #assign start position
                elif (coords == '*'):
                    dirty.add((x, y)) #add coordinate to dirty set
                elif (coords == '#'):
                    blocked.add((x,y)) #add coordinate to blocked set

        



if __name__ == "__main__":
    main()
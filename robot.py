with open("room1.txt") as f:
    lines = f.read().splitlines()

    room = []

    for r in lines:
        row = []
        for c in r:
            row.append(c)
        room.append(row)

start = ()
robot = {"row": 0,"col": 0,"heading": "E","battery": 100,"path":[start],"visited":{start},"collected":[],"moves":0,"bumps":0}
HEADINGS = ["N","E","S","W"] # clockwise order
MOVES = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)} # moves
ARROWS = {"N": "^", "E": ">","S": "v","W": "<"}



def turn_right(robot):
    current_heading = robot["heading"]
    index = HEADINGS.index(current_heading)
    if index != 3:
        new_heading = index+1
    else:
        new_heading = 0
    robot["heading"] = HEADINGS[new_heading]

def turn_left(robot):
    current_heading = robot["heading"]
    index = HEADINGS.index(current_heading)
    if index != 0:
        new_heading = index-1
    else:
        new_heading = 3
    robot["heading"] = HEADINGS[new_heading]

def move_forward(robot,room,items):
    direction = robot["heading"]
    row, col = MOVES[direction]


    new_row = row + robot["row"]
    new_col = col + robot["col"]
    pos = (new_row,new_col)

    if new_row >= len(room) or new_row < 0 or new_col >= len(room[0]) or new_col < 0:
        print("Bump!")
        return False
    elif room[new_row][new_col] == "#":
        print("bump!")
        return False
    else:
        robot["row"] = new_row
        robot["col"] = new_col
        robot["path"].append(pos)
        robot["visited"].add(pos)

        if pos in items:
            items.remove(pos)
            robot["collected"].append(pos)
            room[new_row][new_col] = "."
            print("Collected item at", pos)

    
def parse(text):
    parsed_text = []

    new_text = text.split()
    for t in new_text:
        letter = t[0]
        num = t[1:]

        if num == "":
            num = "1"
        
        parsed_text.append((letter,int(num)))
    return parsed_text
        

    

def run(robot,commands,room,items):
    command = parse(commands)
    bumps = robot["bumps"]
    for cmd in command:
        first_cmd = cmd[0] #maked first_cmd the letter
        second_cmd = cmd[1] #makes second_cmd the number of times it should do it
        for c in range(second_cmd):

            if robot["battery"] <= 0:
                print("battery dead at (",{robot["row"]}, "," ,{robot["col"]}, ")")
                break

            
            #forward
            if first_cmd == "F":
                if robot["battery"] < 5:
                    robot["battery"] = 0
                    print("battery dead at (",{robot["row"]}, "," ,{robot["col"]}, ")")
                    break

                robot["battery"] -= 5

                if not move_forward(robot,room,items):
                    bumps += 1
                    print("RUN--BUMPED INTO WALL---")
                    robot["bumps"] +=1
                else:
                    robot["moves"] +=1
                    

            # right
            elif first_cmd == "R":
                if robot["battery"] < 1:
                    robot["battery"] = 0
                    print("battery dead at (",{robot["row"]}, "," ,{robot["col"]}, ")")
                    break

                robot["battery"] -= 1
                turn_right(robot)

            # left
            elif first_cmd == "L":
                if robot["battery"] < 1:
                    robot["battery"] = 0
                    print("battery dead at (",{robot["row"]}, "," ,{robot["col"]}, ")")
                    break

                robot["battery"] -= 1
                turn_left(robot)

            # error
            else:
                print("error, unkown letter")


        print("RUN-----------------------")
        print(" ")
        print("FINAL POS || (", {robot["row"]} , "," ,{robot["col"]}, ")")
        print("HEADING || ",{robot["heading"]})
        print("BATTERY ||" , {robot["battery"]}, "%")
        print("NUM OF BUMPS || ",{bumps})
        print(" ")
        print("--------------------------")

def show(room, robot):
    for r in range(len(room)):
        row_display = ""
        for c in range(len(room[r])):
            if r == robot["row"] and c == robot["col"]:
                row_display += ARROWS[robot["heading"]]
            else:
                row_display += room[r][c]


        print(row_display)

def coverage(robot,room):
    free_cells = 0
    visited_num = len(robot["visited"])

    for r in range(len(room)):
        for c in range(len(room[r])):
            if room[r][c] != "#":
                
                free_cells += 1

    perecent = (visited_num / free_cells) * 100
    return perecent

#with open("room1.txt") as f:
    #lines = f.read().splitlines() # list of rows as strings
#with open("r1.txt","w") as f:
   # f.write("Mission success\n")

def load_map(filename, robot):
    with open(filename) as f:
        lines = f.read().splitlines()

    grid = []
    start = None
    goal = None
    items = set()

    row_length = len(lines[0]) if lines else 0

    for r, line in enumerate(lines):
        if len(line) != row_length:
            raise ValueError("rows are not equal in length")

        grid_row = []

        for c, char in enumerate(line):
            grid_row.append(char)

            if char == 'S':
                start = (r, c)
            elif char == 'G':
                goal = (r, c)
            elif char == '*':
                items.add((r, c))

        grid.append(grid_row)

    if start is None or goal is None:
        raise ValueError("map should have start and end")

    # Reset robot
    robot.clear()
    robot.update({
        "row": start[0],
        "col": start[1],
        "heading": "E",
        "battery": 100,
        "path": [start],
        "visited": {start},
        "collected":[],
        "moves":0,
        "bumps":0
    })

    return grid, start, goal, items



    
def run_mission(robot, filename, room, items, goal):
    with open(filename) as f:
        commands = f.read().splitlines()

    for cmd in commands:

        run(robot, cmd, room, items)

        if robot["battery"] <= 0:
            break

    # Check mission result
    position = (robot["row"], robot["col"])

    if position == goal and robot["battery"] > 0:
        print("MISSION SUCCESS!")
        return "SUCCESS"
    else:
        print("MISSION FAILED!")
        return "FAILED"

def write_report(robot, room, result, filename):
    report_map = []


    for row in room:
        new_row = row.copy()
        report_map.append(new_row)

    row = robot["row"]
    col = robot["col"]


    direction = robot["heading"]
    arrow = ARROWS[direction]
    report_map[row][col] = arrow

    with open(filename, "w") as f:
        f.write("MISSION REPORT\n")
        f.write("---------------------------------\n")

        f.write("RESULT || " + result + "\n")

        f.write("\nMAP:\n")
        for row in report_map:
            f.write("".join(row) + "\n")

        f.write("\nMOVES || " + str(robot["moves"]) + "\n")
        f.write("BUMPS || " + str(robot["bumps"]) + "\n")
        f.write("BATTERY LEFT  || " + str(robot["battery"]) + "%\n")

        f.write("\nITEMS COLLECTED:\n")
        for item in robot["collected"]:
            f.write(str(item) + "\n")

        f.write("\nCOVERAGE: " + str(coverage(robot, room)) + "%\n")

        f.write("\nFULL PATH:\n")
        f.write(str(robot["path"]) + "\n")




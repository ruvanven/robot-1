import robot
grid, start, goal, items = robot.load_map("room1.txt",robot.robot)


while True:
    cmd = input("Command> ")
    
    if cmd == 'q': #quits
        print("quiting")
        break
    elif cmd == "load room2": #loads the map
        try:
            grid, start, goal, items = robot.load_map("room2.txt", robot.robot)
            robot.room = grid
            robot.start = start

        except FileNotFoundError:
            print("file not found")

    elif cmd == "status": #shows status of robot
        row = robot.robot["row"]
        col = robot.robot["col"]

        heading = robot.robot["heading"]
        battery = robot.robot["battery"]

        coverage = robot.coverage(robot.robot,robot.room)
        items_left = len(items)

        print("STATUS || pos:",row,col," || heading:",heading," || battery",battery,"% || cov:",coverage,"% || items",items_left)
    elif cmd == "undo":
        robot.robot["path"].pop()
    elif cmd == "m1":
        mission_name = "m1.txt"

        try:
            robot.run_mission(robot.robot,mission_name,robot.room,items,goal)

        except FileNotFoundError:
            print("file not found")
    elif cmd == "r1":
        mission_name = "m1.txt"

        try:

            result = robot.run_mission(robot.robot,mission_name,robot.room,items,goal)

            report_file = "r1.txt"

            robot.write_report(robot.robot,robot.room,result,report_file)

            print("Report saved!")

        except FileNotFoundError:
            print("Mission file not found!")
            
    else: #run command
        robot.run(robot.robot,cmd,robot.room,items)
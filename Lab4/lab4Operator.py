from lab4Server import *
print("******************************")
print("*\t\t\t     *")
print("*Land Mine Detection Program!*")
print("*\t\t\t     *")
print("*\t\t\t     *")
print("******************************")
print("By: Mahir Faisal")
print("\n")
print("1) Get map")
print("2) Resize map")
print("3) Get mine list")
print("4) Get a mine")
print("5) Delete mine")
print("6) Create a mine")
print("7) Update a mine")
print("8) Get rover list")
print("9) Get a rover")
print("10) Create a rover")
print("11) Delete a rover")
print("12) Send commands to a rover")
print("13) Dispatch a rover")
print("14) Quit application")

landMap = []
updatedMap = []
mapUpdated = False
request = input("Please enter the option number noted above that you would like to execute: ")
while(request.isdigit() and int(request) >= 1 and int(request) < 14):
    if int(request) == 1 and mapUpdated == False:
        landMap = getMap()
        if 404 in landMap:
            print("Unable to find map file. Please add the map file in the directory before invoking this command")
        else:
            print("Map data retrieved successfully, below is a preview of what the map looks like.")
            for x in range(len(landMap)):
                for y in range(len(landMap[0])):
                    print('{:4}'.format(landMap[x][y]),end=""),
                print()
    elif int(request) == 1 and mapUpdated == True:
        landMap = updatedMap
        if 404 in landMap:
            print("Unable to find map file. Please add the map file in the directory before invoking this command")
        else:
            print("Map data retrieved successfully, below is a preview of what the map looks like.")
            for x in range(len(landMap)):
                for y in range(len(landMap[0])):
                    print('{:4}'.format(landMap[x][y]),end=""),
                print()
    elif int(request) == 2:
        new_height = input("Please enter the new height for the land map: ")
        new_width = input("Please enter the new width for the land map: ")
        choice2 = updateDimensions(landMap,int(new_height),int(new_width))
        if choice2[0] == True:
            mapUpdated = choice2[0]
            updatedMap = choice2[1]
        else:
            print("Unable to update the map. this program will use the original non-updated map data")
    elif int(request) == 3:
        print("Mine list retrieval successful! The information for each mine object can be seen below")
        mineData = getMineData()
        for x in range(len(mineData)):
            print(mineData[x].serialNum + " " + mineData[x].xCoordinate + " " + mineData[x].yCoordinate)
    elif int(request) == 4:
        mineNum = input("Please enter the ID number for the mine that you wish to retrieve: ")
        mineResult = getMineFromID(int(mineNum))
        if 404 in mineResult:
            print("Unable to retrieve mine object with the provided ID value")
        else:
            print("Mine retrieval successful. Here is the available information for this mine object")
            print(*mineResult, sep=" ")
    elif int(request) == 5:
        deleteMineID = input("Please enter the ID of the mine that you wish to delete: ")
        deletedMineResult = delete_mine(int(deleteMineID))
        if deletedMineResult == status.HTTP_404_NOT_FOUND:
            print("Unable to delete mine object.")
        else:
            print("Mine object deletion successful!")
    elif int(request) == 6 and mapUpdated == False:
        mineXcoordinate = input("Please enter the x-coordinate of the mine object that you wish to add: ")
        mineYcoordinate = input("Please enter the y-coordinate of the mine object that you wish to add: ")
        mineSerialNumber = input("Please enter the serial number of the mine object that you wish to add: ")
        mineToAdd = Mine(xCoordinate=mineXcoordinate, yCoordinate=mineYcoordinate, serialNum=mineSerialNumber)
        landMap = getMap()
        createMineResult = create_mine(mineToAdd,landMap)
        if type(createMineResult) is list and 400 in createMineResult:
            print("Could not create mine")
        else:
            print("Mine created successfully. The mine is assigned an ID number of " + str(createMineResult))
    elif int(request) == 6 and mapUpdated == True:
        mineXcoordinate = input("Please enter the x-coordinate of the mine object that you wish to add: ")
        mineYcoordinate = input("Please enter the y-coordinate of the mine object that you wish to add: ")
        mineSerialNumber = input("Please enter the serial number of the mine object that you wish to add: ")
        mineToAdd = Mine(xCoordinate=mineXcoordinate, yCoordinate=mineYcoordinate, serialNum=mineSerialNumber)
        landMap = updatedMap
        createMineResult = create_mine(mineToAdd,landMap)
        if type(createMineResult) is list and 400 in createMineResult:
            print("Could not create mine")
        else:
            print("Mine created successfully. The mine is assigned an ID number of " + str(createMineResult))
    elif int(request) == 7:
        updateId = input("Please enter the ID of the mine that you wish to update: ")
        paramtoUpdate = input("Please enter the name of the parameter that you wish to update: ")
        paramValue = input("Please enter the new value of the parameter to be updated: ")
        updatedMineRes = update_mine(int(updateId),paramtoUpdate,paramValue)
        if 404 in updatedMineRes or 400 in updatedMineRes:
            print("Unable to update mine object")
        else:
            print("Mine object updated successfully. Below are the newly updated details")
            print(updatedMineRes.xCoordinate + " " + updatedMineRes.yCoordinate + " " + updatedMineRes.serialNum)
    elif int(request) == 8:
        roverList = getrovList()
        print("Rover list retrieval successful! The information for each rover in the list can be shown below")
        for x in range(len(roverList)):
            print(str(x) + " " + roverList[x].rovStatus)
    elif int(request) == 9:
        rovID = input("Please enter the ID number of the rover that you wish to retrieve: ")
        roverRes = getRovFromID(int(rovID))
        if 404 in roverRes:
            print("Unable to retrieve rover")
        else:
            print("Rover retrieval successful")
            print(*roverRes,sep=" ")
    elif int(request) == 10:
        roverCommandStr = input("Please enter the coommand string that you would like to assign to the rover: ")
        roverCommandStr = roverCommandStr.replace(" ","")
        roverToAdd = Rover(rovCommands=roverCommandStr)
        roverCreateRes = create_rover(roverToAdd)
        if type(roverCreateRes) is list and 400 in roverCreateRes:
            print("Unable to create rover")
        else:
            print("Rover is created successfully with rover ID number " + str(roverCreateRes))
    elif int(request) == 11:
        rovertoDelete = input("Please enter the ID of the rover that you wish to delete: ")
        roverDeletedRes = delete_rover(int(rovertoDelete))
        if roverDeletedRes == status.HTTP_404_NOT_FOUND:
            print("Rover unable to be deleted")
        else:
            print("Rover successfully deleted")
    elif int(request) == 12:
        commandID = input("Please enter the ID of the rover that you wish to send a command string to: ")
        commandsToSend = input("Please enter the command string that you would like to send to this rover: ")
        commandsToSend = commandsToSend.replace(" ","")
        commandSent = send_commands(int(commandID),commandsToSend)
        if type(commandSent) is int and commandSent == status.HTTP_404_NOT_FOUND:
            print("Rover does not exist")
        elif type(commandSent) is int and commandSent == status.HTTP_400_BAD_REQUEST:
            print("Failure")
        else:
            print("Rover commands have been updated to the following: ")
            print(rovList[int(commandID)].rovCommands)
    elif int(request) == 13 and mapUpdated == False:
        dispatchID = input("Please enter the ID of the rover that you wish to dispatch: ")
        landMap = getMap()
        roverDispatched = dispatch_rover(int(dispatchID),landMap)
        if 404 in roverDispatched:
            print("Rover cannot be dispatched!")
        else:
            for x in range(len(roverDispatched)):
                if x == 0:
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in roverDispatched[x]]))
                else:
                    print(str(roverDispatched[x]) + " ",end="")
                    if x == len(roverDispatched) - 1:
                        print()
                        break
    elif int(request) == 13 and mapUpdated == True:
        dispatchID = input("Please enter the ID of the rover that you wish to dispatch: ")
        landMap = updatedMap
        roverDispatched = dispatch_rover(int(dispatchID),landMap)
        if 404 in roverDispatched:
            print("Rover cannot be dispatched!")
        else:
            for x in range(len(roverDispatched)):
                if x == 0:
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in roverDispatched[x]]))
                else:
                    print(str(roverDispatched[x]) + " ",end="")
                    if x == len(roverDispatched) - 1:
                        print()
                        break      
    request = input("Please enter the option number noted above that you would like to execute: ")

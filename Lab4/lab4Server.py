from fastapi import FastAPI, status 
from typing import Optional
from pydantic import BaseModel
import random
from hashlib import sha256
import copy
import os


class Mine(BaseModel):
    xCoordinate: str
    yCoordinate: str
    serialNum: str

class Rover(BaseModel):
    rovStatus: str = "Not Started"
    rovCommands: str
    rovPosition: str = "00"
mineList = []
rovList = []
def returnErrorCodes():
    errorCode = []
    errorCode.append(status.HTTP_404_NOT_FOUND)
    errorCode.append(status.HTTP_400_BAD_REQUEST)
    errorCode.append("Request not found")
    errorCode.append("Request failed")
    return errorCode
def digProces(id):
    validPin = False
    pin = 0
    while not validPin:
        mineKey = str(pin) + id
        hashedValue = sha256(mineKey.encode('utf-8')).hexdigest()
        if hashedValue[0:6] == "000000":
            validPin = True
        else:
            pin = pin + 1
    return validPin 

def directionChange(command,currentDirection):
    # LEFT COMMAND CASES
    if command == "L" and currentDirection == "S":
        currentDirection = "E"
    elif command == "L" and currentDirection == "E":
        currentDirection = "N"
    elif command == "L" and currentDirection == "N":
        currentDirection = "W"
    elif command == "L" and currentDirection == "W":
        currentDirection = "S"
    # RIGHT COMMAND CASES
    elif command == "R" and currentDirection == "S":
        currentDirection = "W"
    elif command == "R" and currentDirection == "W":
        currentDirection = "N"
    elif command == "R" and currentDirection == "N":
        currentDirection = "E"
    elif command == "R" and currentDirection == "E":
        currentDirection = "S"
    return currentDirection

def createPath(rov_id, landMat, commandMat):
    executed = []
    rovList[rov_id].rovStatus = "Moving"
    mineMatchcount = 0
    mineLoc = ""
    disarmed = False
    destroyed = False
    mines = mineList
    pathMat = copy.deepcopy(landMat)
    pathRows = len(pathMat)
    pathCols = len(pathMat[0])
    currentFacing = "S"
    x = int(rovList[rov_id].rovPosition[0])
    y = int(rovList[rov_id].rovPosition[1])
    for command in commandMat:
        if x > pathRows - 1 or y > pathCols - 1 or x < 0 or y < 0: #Check if the rover goes out of bounds for the land space
            break
        else:
            # Cases where command is M
            if currentFacing == "S" and command == "M":
                if pathMat[x][y] == "1": #Rover is on a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                    destroyed = True
                    break
                elif pathMat[x][y] == "0": # you can move and the rover is not over a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                if x < pathRows - 1: 
                    x = x + 1
            elif currentFacing == "N" and command == "M":
                if pathMat[x][y] == "1": #Rover is on a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                    destroyed = True
                    break
                elif pathMat[x][y] == "0": # you can move and the rover is not over a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                if x > 0: 
                    x = x - 1
            elif currentFacing == "E" and command == "M":
                if pathMat[x][y] == "1": #Rover is on a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                    destroyed = True
                    break
                elif pathMat[x][y] == "0": # you can move and the rover is not over a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                if y < pathCols - 1: 
                    y = y + 1
            elif currentFacing == "W" and command == "M":
                if pathMat[x][y] == "1": #Rover is on a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                    destroyed = True
                    break
                elif pathMat[x][y] == "0": # you can move and the rover is not over a mine
                    pathMat[x][y] = "*"
                    executed.append(command)
                if y > 0: 
                    y = y - 1
            # If command is D and the rover does NOT hit a mine, write a * at that location
            elif command == "D" and pathMat[x][y] == "0":
                pathMat[x][y] = "*"
                executed.append(command)
            elif command == "D" and pathMat[x][y] == "1": # If command is D and the rover does hit a mine, initiate the digging process for that mine
                for j in range(len(mines)):
                    mineLoc = mines[j].xCoordinate + mines[j].yCoordinate
                    if mineLoc == str(x) + str(y):
                        mineMatchcount = mineMatchcount + 1 # Counter which keeps track of the total number of mine serial location matches
                        disarmed = digProces(mines[j].serialNum)
                        if disarmed == True:
                            print("Mine located at x-coordinate " + mines[j].xCoordinate + " and y-coordinate " + mines[j].yCoordinate + " has been disarmed successfully!")
                            pathMat[x][y] = "#" # If mine is successfully disarmed place a # character at that location
                            executed.append(command)
                            break
                    elif mineMatchcount == 0 and j == len(mines) - 1:
                        print("Mine cannot be disarmed. Unable to identify the mine's serial number.")
                        pathMat[x][y] = "*" #Error handling scenario where the function is unable to identify the mine's serial number
                        executed.append(command)
                    else:
                        continue
            # If command is L or R, change direction of rover
            elif command == "L" or command == "R":
                currentFacing = directionChange(command,currentFacing)
    
    if destroyed == False  and len(commandMat) == len(executed):
        rovList[rov_id].rovStatus = "Finished"
    elif destroyed == False and len(executed) != len(commandMat):
        rovList[rov_id].rovStatus = "Moving"
    else:
        rovList[rov_id].rovStatus = "Eliminated"
    position = str(x) + str(y)
    results = [pathMat, rov_id, rovList[rov_id].rovStatus, position, executed]
    return results
app = FastAPI()

@app.get("/map/")
def getMap(file: str = "map.txt"):
    if not os.path.exists("map.txt"):
        errors = returnErrorCodes()
        return errors
    landSpace = []
    count = 0
    with open(file,"r") as f:
        lineList = f.readlines()
        for line in lineList:
            count = count + 1
            if count >= 2:
                mat = [item.strip() for item in line.split()]
                landSpace.append(mat)
    return landSpace

@app.put("/map/")
def updateDimensions(map: list, height: int, width: int):
    returnData = []
    newField = []
    updated = False
    if(height > 0 and width > 0):
        field = map
        for x in range(height):
            sub = []
            for y in range(width):
                if x > len(field) - 1 or y > len(field[0]) - 1:
                    sub.append(str(random.randint(0,1)))
                else:
                    sub.append(field[x][y])
            newField.append(sub)
        updated = True
        returnData.append(updated)
        returnData.append(newField)
        return returnData
    else:
        results = returnErrorCodes()
        results.append(updated)
        return results
 
@app.get("/mines")
def getMineData(mines: list = mineList):
    return mines
@app.get("/mines/{mine_id}")
def getMineFromID(mine_id: int):
    try:
        if mineList[mine_id] not in mineList:
            errors = returnErrorCodes()
            return errors
        else:
            results = [mineList[mine_id].serialNum, mineList[mine_id].xCoordinate, mineList[mine_id].yCoordinate]
            return results
    except IndexError:
        errors = returnErrorCodes()
        return errors
@app.delete("/mines/{mine_id}")
def delete_mine(mine_id: int):
    try:
        if mineList[mine_id] not in mineList:
            error = status.HTTP_404_NOT_FOUND
            return error
        mineList.remove(mineList[mine_id])
        return status.HTTP_200_OK
    except IndexError:
        error = status.HTTP_404_NOT_FOUND
        return error
@app.post("/mines")
def create_mine(mine: Mine, field: list):
    if mine in mineList or int(mine.xCoordinate) > len(field) - 1 or int(mine.yCoordinate) > len(field[0]) - 1 or int(mine.xCoordinate) < 0 or int(mine.yCoordinate) < 0:
        errors = returnErrorCodes()
        return errors
    else:
        mineList.append(mine)
        mineID = len(mineList) - 1
        return mineID      
@app.put("/mines/{mine_id}")
def update_mine(mine_id: int, parameterToUpdate: str, value: str):
    try:
        validInput = False
        if parameterToUpdate == "x" and int(value) < 0 or parameterToUpdate == "y" and int(value) < 0:
            errors = returnErrorCodes()
            return errors 
        elif mineList[mine_id] not in mineList:
            errors = returnErrorCodes()
            return errors
        else:
            while(validInput == False):
                if parameterToUpdate == "x":
                    mineList[mine_id].xCoordinate = value
                    validInput = True
                elif parameterToUpdate == "y":
                    mineList[mine_id].yCoordinate = value
                    validInput = True
                elif parameterToUpdate == "serial":
                    mineList[mine_id].serialNum = value
                    validInput = True
                else:
                    errors = returnErrorCodes()
                    break
            if validInput == False:
                return errors
            else:
                return mineList[mine_id]
    except IndexError:
        errors = returnErrorCodes()
        return errors
@app.get("/rovers")
def getrovList(rovers: list = rovList):
    return rovList

@app.get("/rovers/{rov_id}")
def getRovFromID(rov_id: int):
    try:
        if rovList[rov_id] not in rovList:
            errors = returnErrorCodes
            return errors
        else:
            results = [rov_id, rovList[rov_id].rovStatus, rovList[rov_id].rovPosition, rovList[rov_id].rovCommands]
            return results
    except IndexError:
        errors = returnErrorCodes()
        return errors

@app.post("/rovers")
def create_rover(rover: Rover):
    if rover in rovList:
        errors = returnErrorCodes()
        return errors
    else:
        rovList.append(rover)
        rovID = len(rovList) - 1
        return rovID

@app.delete("/rovers/{rov_id}")
def delete_rover(rov_id: int):
    try:
        if rovList[rov_id] not in rovList:
            error = status.HTTP_404_NOT_FOUND
            return error
        else:
            rovList.remove(rovList[rov_id])
            return status.HTTP_200_OK
    except IndexError:
        error = status.HTTP_404_NOT_FOUND
        return error

@app.put("/rover/{rov_id}")
def send_commands(rov_id: int, commands: str):
    try:
        updatedCommands = ""
        if rovList[rov_id] not in rovList:
            errors = returnErrorCodes()
            return errors
        elif rovList[rov_id].rovStatus == "Moving" or rovList[rov_id].rovStatus == "Eliminated":
            error = status.HTTP_400_BAD_REQUEST
            return error
        else:
            initCommands = rovList[rov_id].rovCommands
            updatedCommands = initCommands + commands
            rovList[rov_id].rovCommands = updatedCommands
            result = status.HTTP_200_OK
            return result
    except IndexError:
        errors = returnErrorCodes()
        return errors 
@app.post("/rovers/{rov_id}/dispatch")
def dispatch_rover(rov_id: int, field: list):
    try:
        if rovList[rov_id] not in rovList:
            errors = returnErrorCodes()
            return errors
        elif rovList[rov_id].rovStatus == "Moving" or rovList[rov_id].rovStatus == "Eliminated":
            errors = returnErrorCodes()
            return errors
        else:
            results = createPath(rov_id,field,list(rovList[rov_id].rovCommands))
            return results
    except IndexError:
        errors = returnErrorCodes()
        return errors
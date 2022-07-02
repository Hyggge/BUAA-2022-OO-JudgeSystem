from colorfulPrint import ColorfulPrint

STATE_OPEN = 0
STATE_CLOSE = 1
MAX_FLOOR = 10
MIN_FLOOR = 1
MAX_NUM = 6
MIN_NUM = 0
# 常规的纵向电梯
ELEVATOR_FLOOR = 1
# 反人类的横向电梯
ELEVATOR_TOWER = 2

reqDic = {}
elevators = {}
flag = [0]
lastOpTime = [0.0]

class Req:
    def __init__(self, req):
        eles = self.parseReq(req)
        self.id = int(eles[0])
        self.ft = eles[2]
        self.ff = int(eles[3])
        self.tt = eles[5]
        self.tf = int(eles[6])
    def parseReq(self, req):
        req = req.replace('\n', '')
        index = req.index(']')
        req = req[index + 1:]
        return req.split('-')
    def getId(self):
        return self.id
    def getFromTower(self):
        return self.ft
    def getFromFloor(self):
        return self.ff
    def getToTower(self):
        return self.tt
    def getToFloor(self):
        return self.tf

class Elevator:
    def __init__(self, str):
        eles = str.split('-')
        if eles[1] == 'floor':
            self.type = ELEVATOR_TOWER
            self.floor = int(eles[3])
            self.tower = 0
        elif eles[1] == 'building':
            self.type = ELEVATOR_FLOOR
            self.floor = 1
            self.tower = getTower(eles[3], -1)
        else:
            ColorfulPrint.colorfulPrint('??? Unknow elevator type ???', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        self.id = int(eles[2])
        self.state = STATE_CLOSE
        self.lastMoveTime = -10.0
        self.lastOpenTime = -10.0
        self.passengers = []
    def checkArrive(self, eles, lineNum, opTime):
        if self.state != STATE_CLOSE:
            printError('Elevator moved when the door is not closed!', lineNum)
        if self.type == ELEVATOR_FLOOR:
            if opTime - self.lastMoveTime < 0.4 - 0.00001:
                printError('Floor elevator moved too fast!', lineNum)
            self.lastMoveTime = opTime
            if self.tower != getTower(eles[1], lineNum):
                printError('Floor elevator shouldn\'t move among bulidings!', lineNum)
            if self.floor > MAX_FLOOR or self.floor < MIN_FLOOR:
                printError('Floor elevator in a not-exist floor!', lineNum)
            if self.floor - int(eles[2]) != 1 and self.floor - int(eles[2]) != -1:
                printError('Illegal floor elevator movement!', lineNum)
            self.floor = int(eles[2])
        else:
            if opTime - self.lastMoveTime < 0.2 - 0.00001:
                printError('Building elevator moved too fast!', lineNum)
            self.lastMoveTime = opTime
            if self.floor != int(eles[2]):
                printError('Building elevator shouldn\'t move among floors!', lineNum)
            if self.tower < 0 or self.tower > 4:
                printError('Building elevator in a not-exist building!', lineNum)
            temp = self.tower - getTower(eles[1], lineNum)
            if temp < 0:
                temp += 5
            if temp != 1 and temp != 4:
                printError('Illegal building elevator movement!', lineNum)
            self.tower = getTower(eles[1], lineNum)
    def checkOpen(self, eles, lineNum, opTime):
        if self.state != STATE_CLOSE:
            printError('Elevator door is not closed before open!', lineNum)
        self.state = STATE_OPEN
        self.lastOpenTime = opTime
        if int(eles[2]) != self.floor:
            printError('Elevator floor error!', lineNum)
        if getTower(eles[1], lineNum) != self.tower:
            printError('Elevator building error!', lineNum)
    def checkClose(self, eles, lineNum, opTime):
        if self.state != STATE_OPEN:
            printError('Elevator door is not opened before close!', lineNum)
        self.state = STATE_CLOSE
        if opTime - self.lastOpenTime < 0.4 - 0.00001:
            printError('Close too fast!', lineNum)
        if int(eles[2]) != self.floor:
            printError('Elevator floor error!', lineNum)
        if getTower(eles[1], lineNum) != self.tower:
            printError('Elevator building error!', lineNum)
        self.lastMoveTime = opTime
    def checkIn(self, eles, lineNum, opTime):
        if self.state != STATE_OPEN:
            printError('Passengers can\'t in when the door is closed!', lineNum)
        passengerID = int(eles[1])
        self.passengers.append(passengerID)
        req = reqDic.get(passengerID)
        if req == None:
            printError('Passenger not exist!', lineNum)
        else:
            if req.getFromFloor() != int(eles[3]) or req.getFromTower() != eles[2]:
                printError('\'IN\' message unmatched request!', lineNum)
        if len(self.passengers) > MAX_NUM:
            printError('Elevator overload!', lineNum)
        if int(eles[3]) != self.floor:
            printError('Elevator floor error!', lineNum)
        if getTower(eles[2], lineNum) != self.tower:
            printError('Elevator building error!', lineNum)
    def checkOut(self, eles, lineNum, opTime):
        if self.state != STATE_OPEN:
            printError('Passengers can\'t out when the door is closed!', lineNum)
        passengerID = int(eles[1])
        if passengerID not in self.passengers:
            printError('Passenger is not in elevator!', lineNum)
        else:
            self.passengers.remove(passengerID)
        req = reqDic.get(passengerID)
        if req == None:
            printError('Passenger not exist!', lineNum)
        else:
            if req.getToFloor() != int(eles[3]) or req.getToTower() != eles[2]:
                printError('\'OUT\' message unmatched request!', lineNum)
            reqDic.pop(passengerID)
        if int(eles[3]) != self.floor:
            printError('Elevator floor error!', lineNum)
        if getTower(eles[2], lineNum) != self.tower:
            printError('Elevator building error!', lineNum)
    def getPassengerNum(self):
        return len(self.passengers)
    def getID(self):
        return self.id
    def getState(self):
        return self.state


def arrive(eles, lineNum, opTime):
    eleID = int(eles[3])
    if elevators.get(eleID) == None:
        printError('Unknow elevator ID!', lineNum)
        return
    elevator = elevators.get(eleID)
    elevator.checkArrive(eles, lineNum, opTime)
def elevatorOpen(eles, lineNum, opTime):
    eleID = int(eles[3])
    if elevators.get(eleID) == None:
        printError('Unknow elevator ID!', lineNum)
        return
    elevator = elevators.get(eleID)
    elevator.checkOpen(eles, lineNum, opTime)
def elevatorClose(eles, lineNum, opTime):
    eleID = int(eles[3])
    if elevators.get(eleID) == None:
        printError('Unknow elevator ID!', lineNum)
        return
    elevator = elevators.get(eleID)
    elevator.checkClose(eles, lineNum, opTime)
def passengerIn(eles, lineNum, opTime):
    eleID = int(eles[4])
    if elevators.get(eleID) == None:
        printError('Unknow elevator ID!', lineNum)
        return
    elevator = elevators.get(eleID)
    elevator.checkIn(eles, lineNum, opTime)
def passengerOut(eles, lineNum, opTime):
    eleID = int(eles[4])
    if elevators.get(eleID) == None:
        printError('Unknow elevator ID!', lineNum)
        return
    elevator = elevators.get(eleID)
    elevator.checkOut(eles, lineNum, opTime)

def printError(msg, l = 0):
    if l == 0:
        msg = ' ***** ' + msg + ' ***** '
    else:
        msg = ' ***** ' + msg + ' In line: ' + str(l) + ' ***** '
    ColorfulPrint.colorfulPrint(msg, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    flag[0] = 0

def initElevator():
    reqDic.clear()
    elevators.clear()
    flag[0] = 1
    lastOpTime[0] = -1.0
    elevators[1] = Elevator('ADD-building-1-A')
    elevators[2] = Elevator('ADD-building-2-B')
    elevators[3] = Elevator('ADD-building-3-C')
    elevators[4] = Elevator('ADD-building-4-D')
    elevators[5] = Elevator('ADD-building-5-E')

def processInput():
    with open('stdin.txt', 'r') as f:
        tot = f.readlines()
        for ele in tot:
            ele = ele.replace('\n', '')
            if 'ADD' in ele:
                temp = ele.split('-')
                elevators[int(temp[2])] = Elevator(ele)
            else:
                req = Req(ele)
                reqDic[req.getId()] = req

def checkOutput(fileName):
    initElevator()
    processInput()
    with open(fileName, 'r') as f:
        tot = f.readlines()
        count = 1
        for line in tot:
            process(line, count)
            count += 1
    if len(reqDic) != 0:
        printError('Some requests are not satisfied!')
        print('Not satisfied requests ID:')
        for num in reqDic:
            print(num)
    for elevator in elevators.values():
        if elevator.getPassengerNum() != 0:
            printError('Some is trapped in elevator! Elevator id: ' + str(elevator.getID()))
        if elevator.getState() != STATE_CLOSE:
            printError('Elevator is not closed! Elevator id: ' + str(elevator.getID()))
    if flag[0] == 1:
        ColorfulPrint.colorfulPrint(' ===== Accepted ===== ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
        return True
    else:
        printError('Wrong answer!')
        return False

def process(read, lineNum):
    read = read.replace('\n', '')
    index = read.index(']')
    opTime = float(read[1:index - 1])
    read = read[index + 1:]
    eles = read.split('-')
    if opTime < lastOpTime[0]:
        printError('Incorrect output order!', lineNum)
    lastOpTime[0] = opTime
    if eles[0] == 'ARRIVE':
        arrive(eles, lineNum, opTime)
    elif eles[0] == 'OPEN':
        elevatorOpen(eles, lineNum, opTime)
    elif eles[0] == 'CLOSE':
        elevatorClose(eles, lineNum, opTime)
    elif eles[0] == 'IN':
        passengerIn(eles, lineNum, opTime)
    elif eles[0] == 'OUT':
        passengerOut(eles, lineNum, opTime)
    else:
        printError('Unknow option!', lineNum)

def getTower(tower, lineNum):
    if tower == 'A':
        return 0
    elif tower == 'B':
        return 1
    elif tower == 'C':
        return 2
    elif tower == 'D':
        return 3
    elif tower == 'E':
        return 4
    else:
        printError('UNKNOW TOWER!', lineNum)

if __name__ == "__main__":
    fileName = 'stdout2.txt'
    checkOutput(fileName)
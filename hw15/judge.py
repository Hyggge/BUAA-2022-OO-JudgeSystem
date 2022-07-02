from colorfulPrint import ColorfulPrint
import time
import os
import random
import sys

player = ['xjh', 'czh', 'xyy']
playerNum = 3
maxErrorNum = 10
errorList = [0] * 9

def merge(fileName1, fileName2, tarFileName):
    with open(fileName1, 'r') as f:
        con1 = f.readlines()
    with open(fileName2, 'r') as f:
        con2 = f.readlines()
    conNew = []
    l1 = len(con1)
    l2 = len(con2)
    p1 = 0
    p2 = 0
    while con1[p1] != 'END_OF_MODEL\n' or con2[p2] != 'END_OF_MODEL\n':
        if con1[p1] == 'END_OF_MODEL\n':
            conNew.append(con2[p2])
            p2 += 1
        elif con2[p2] == 'END_OF_MODEL\n':
            conNew.append(con1[p1])
            p1 += 1
        elif random.randint(0, 1) == 0:
            conNew.append(con1[p1])
            p1 += 1
        else:
            conNew.append(con2[p2])
            p2 += 1
    p1 += 1
    p2 += 1
    conNew.append('END_OF_MODEL\n')
    while p1 < l1 or p2 < l2:
        if p1 == l1:
            conNew.append(con2[p2])
            p2 += 1
        elif p2 == l2:
            conNew.append(con1[p1])
            p1 += 1
        elif random.randint(0, 1) == 0:
            conNew.append(con1[p1])
            p1 += 1
        else:
            conNew.append(con2[p2])
            p2 += 1
    with open(tarFileName, 'w') as f:
        f.writelines(conNew)
    
def showError(lineNum, inStr, exceptStr, readStr, name):
    ColorfulPrint.colorfulPrint('***** ' + name + ' ERROR IN LINE: ' + str(lineNum) + ' *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('Input: ' + inStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('We excepted: ' + exceptStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('Your output: ' + readStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)

def makeLog(num, size, tle = False):
    if tle == False:
        with open('input.txt', 'r') as f:
            con = f.read()
        with open('./logWA/input' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'output' + str(i + 1) + '.txt'
            name2 = './logWA/output' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)
    else:
        with open('input.txt', 'r') as f:
            con = f.read()
        with open('./logTLE/input' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'output' + str(i + 1) + '.txt'
            name2 = './logTLE/output' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)

def runAndCmp(inputFile):
    ColorfulPrint.colorfulPrint('>>>>> use ' + inputFile + ' <<<<<', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
    countError = 0
    if playerNum <= 1:
        ColorfulPrint.colorfulPrint('***** TOO LESS! *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        return
    for i in range(playerNum):
        begTime = time.time()
        cmd = 'java -jar ' + player[i] + '.jar < ' + inputFile + ' > output' + str(i + 1) + '.txt'
        os.system(cmd)
        ColorfulPrint.colorfulPrint('>>>>> ' + player[i] + ' use time: ' + str(time.time() - begTime) + 's <<<<<', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
    with open(inputFile, 'r') as f:
        stdin = f.readlines()
        count  = 0
        while stdin[count] != 'END_OF_MODEL\n':
            count += 1
        stdin = stdin[count + 1:]
    stdout = []
    for i in range(playerNum):
        with open('output' + str(i + 1) + '.txt', 'r') as f:
            stdout.append(f.readlines())
    for j in range(len(stdout[0])):
        for i in range(playerNum):
            if i == 0:
                continue
            if stdout[0][j] != stdout[i][j]:
                if countError >= maxErrorNum:
                    return False
                countError += 1
                showError(j + 1, stdin[j][:-1], stdout[0][j][:-1], stdout[i][j][:-1], player[i])
    if countError == 0:
        return True
    else:
        return False

def runTest(testNum):
    ColorfulPrint.colorfulPrint('>>>>>>>>>> Test ' + str(testNum) + ' <<<<<<<<<<', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
    os.system('python3 generate.py')
    os.system('./gen > input2.txt')

    #merge('input1.txt', 'input2.txt', 'input.txt')

    if runAndCmp('input1.txt') == True:
        ColorfulPrint.colorfulPrint('===== ACCEPTED =====', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
        with open('output1.txt', 'r') as f:
            temp = f.readlines()
            if len(temp) == 1:
                errorList[int(temp[0][21]) - 1] += 1
                ColorfulPrint.colorfulPrint(temp[0][:-1], ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_YELLOW)
    else:
        assert False
        ColorfulPrint.colorfulPrint('***** WRONG ANSWER *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        makeLog(testNum, playerNum)
    
    if runAndCmp('input2.txt') == True:
        ColorfulPrint.colorfulPrint('===== ACCEPTED =====', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
        with open('output1.txt', 'r') as f:
            temp = f.readlines()
            if len(temp) == 1:
                errorList[int(temp[0][21]) - 1] += 1
                ColorfulPrint.colorfulPrint(temp[0][:-1], ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_YELLOW)
    else:
        assert False
        ColorfulPrint.colorfulPrint('***** WRONG ANSWER *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        makeLog(testNum, playerNum)

if __name__ == '__main__':
    for i in range(20):
        runTest(i + 1)
    for i in range(9):
        print('R00' + str(i + 1) + ':' + str(errorList[i]))

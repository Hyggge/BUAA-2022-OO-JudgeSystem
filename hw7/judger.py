import re
import time
import os
import subprocess
from outputChecker import checkOutput
from colorfulPrint import ColorfulPrint

playerName = ['Saber', 'Lancer', 'Archer', 'Rider', 'Caster', 'Assassin', 'Berserker']

def getFileName(i = 0):
    if i == 0:
        return 'stdout.txt'
    elif i > 0:
        return 'stdout' + str(i) + '.txt'
    else:
        ColorfulPrint.colorfulPrint('Can\'t get the file name!', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        return None

def makeLog(num, size, aboutTime = False):
    if aboutTime == False:
        with open('stdin.txt', 'r') as f:
            con = f.read()
        with open('./logWA/stdin' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'stdout' + str(i + 1) + '.txt'
            name2 = './logWA/stdout' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)
    else:
        with open('stdin.txt', 'r') as f:
            con = f.read()
        with open('./logTLE/stdin' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'stdout' + str(i + 1) + '.txt'
            name2 = './logTLE/stdout' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)

# return a String
def getTime(fileName):
    with open(fileName, 'r') as f:
        read = f.readlines()
    read = read[-1]
    read = re.findall(r"\d+\.?\d*", read)
    if len(read) > 0:
        return read[0]
    else:
        ColorfulPrint.colorfulPrint('Can\'t get time from ' + fileName + '!', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        return None    

if __name__ == "__main__":
    # set running parameters here
    playerNum = 9
    useMaker = True
    testNum = 200
    displayDetail = False
    special = True

    cmd = 'chmod u+x datainput_student_linux_x86_64'
    if displayDetail:
        print('Executing: ' + cmd)
    os.system(cmd)

    if playerNum == 1:
        if useMaker:
            waCount = 0
            ColorfulPrint.colorfulPrint(' Test point num: ' + str(testNum), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            for i in range(testNum):
                ColorfulPrint.colorfulPrint(' >>>>>>>>>>>>>>>>>>>>>>>>> Test {} <<<<<<<<<<<<<<<<<<<<<<<<< '.format(i + 1), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                cmd = 'python3 generate.py > stdin.txt'
                if displayDetail:
                    print('Executing: ' + cmd)
                os.system(cmd)
                beginTime = time.time()
                cmd = './datainput_student_linux_x86_64 | timeout 150 java -jar ' + playerName[0] + '.jar > stdout.txt'
                if displayDetail:
                    print('Executing: ' + cmd)
                os.system(cmd)
                endTime = time.time()
                if endTime - beginTime > 150.0:
                    ColorfulPrint.colorfulPrint(' Program can\'t end normaly! ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
                ColorfulPrint.colorfulPrint(' ---------- Use time: ' + getTime(getFileName()) + 's ---------- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                ans = checkOutput(getFileName())
                if ans == False:
                    waCount += 1
                    makeLog(i + 1, playerNum)
            if waCount == 0:
                ColorfulPrint.colorfulPrint(' ========== You have passed all testpoint! ========== ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
            else:
                ColorfulPrint.colorfulPrint(' ********** You have not passed all testpoint! ********** ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
                ColorfulPrint.colorfulPrint(' Passed: ' + str(testNum - waCount) + '/' + str(testNum), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_YELLOW)
        else:
            ColorfulPrint.colorfulPrint(' >>>>>>>>>>>>>>>>>>>>>>>>> Test begin <<<<<<<<<<<<<<<<<<<<<<<<< ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            beginTime = time.time()
            cmd = './datainput_student_linux_x86_64 | timeout 150 java -jar ' + playerName[0] + '.jar > stdout.txt'
            if displayDetail:
                print('Executing: ' + cmd)
            os.system(cmd)
            endTime = time.time()
            if endTime - beginTime > 150.0:
                ColorfulPrint.colorfulPrint(' Program can\'t end normaly! ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
            ColorfulPrint.colorfulPrint(' ---------- Use time: ' + getTime(getFileName()) + 's ---------- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            checkOutput(getFileName())

    elif playerNum > 1 and playerNum <= len(playerName):
        times = []
        thread = [None] * playerNum
        for i in range(playerNum):
            times.append("")
        if useMaker:
            waCount = 0
            ColorfulPrint.colorfulPrint(' Test point num: ' + str(testNum), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            for i in range(testNum):
                ColorfulPrint.colorfulPrint(' >>>>>>>>>>>>>>>>>>>>>>>>> Test {} <<<<<<<<<<<<<<<<<<<<<<<<< '.format(i + 1), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                cmd = 'python3 generate.py > stdin.txt'
                ans = True
                if displayDetail:
                    print('Executing: ' + cmd)
                os.system(cmd)
                beginTime = time.time()
                for j in range(playerNum):
                    cmd = './datainput_student_linux_x86_64 | timeout 150 java -jar ' + playerName[j] + '.jar > ' + getFileName(j + 1)
                    if displayDetail:
                        print('Executing: ' + cmd)
                    thread[j] = subprocess.Popen(cmd, shell = True)
                for j in range(playerNum):
                    returnCode = thread[j].wait()
                endTime = time.time()
                if endTime - beginTime > 150.0:
                    ColorfulPrint.colorfulPrint(' Program can\'t end normaly! ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
                    ans = False
                for j in range(playerNum):
                    times[j] = getTime(getFileName(j + 1))
                    ColorfulPrint.colorfulPrint(' >>>>> Checking: ' + playerName[j] + ' <<<<< ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                    ans &= checkOutput(getFileName(j + 1))
                tempSum = 0.0
                for j in range(playerNum):
                    times[j] = getTime(getFileName(j + 1))
                    tempSum += float(times[j])
                aveTime = tempSum / playerNum
                flagTime = False
                for j in range(playerNum):
                    if float(times[j]) > 1.25 * aveTime:
                        ColorfulPrint.colorfulPrint(' ----- ' + playerName[j] + ' use time: ' + times[j] + 's TLE! ----- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
                        flagTime = True
                    else:
                        ColorfulPrint.colorfulPrint(' ----- ' + playerName[j] + ' use time: ' + times[j] + 's ----- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                if ans == False:
                    waCount += 1
                    makeLog(i + 1, playerNum)
                if flagTime:
                    makeLog(i + 1, playerNum, True)
                toAdd = ''
                for j in range(playerNum):
                    if j != 0:
                        toAdd = toAdd + ',' + str(float(times[j]) / aveTime)
                    else:
                        toAdd = toAdd + str(float(times[j]) / aveTime)
                toAdd = toAdd + '\n'
                with open('time.txt', 'a') as f:
                    f.write(toAdd)
            if waCount == 0:
                ColorfulPrint.colorfulPrint(' ========== All passed! ========== ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
            else:
                ColorfulPrint.colorfulPrint(' ********** Some one not passed all testpoint! ********** ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        else:
            ColorfulPrint.colorfulPrint(' >>>>>>>>>>>>>>>>>>>>>>>>> Test begin <<<<<<<<<<<<<<<<<<<<<<<<< ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            beginTime = time.time()
            for j in range(playerNum):
                cmd = './datainput_student_linux_x86_64 | timeout 150 java -jar ' + playerName[j] + '.jar > ' + getFileName(j + 1)
                if displayDetail:
                    print('Executing: ' + cmd)
                thread[j] = subprocess.Popen(cmd, shell = True)
            for j in range(playerNum):
                returnCode = thread[j].wait()
            endTime = time.time()
            if endTime - beginTime > 150.0:
                ColorfulPrint.colorfulPrint(' Program can\'t end normaly! ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
            for j in range(playerNum):
                times[j] = getTime(getFileName(j + 1))
                ColorfulPrint.colorfulPrint(' >>>>> Checking: ' + playerName[j] + ' <<<<< ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
                checkOutput(getFileName(j + 1))
            tempSum = 0.0
            for j in range(playerNum):
                times[j] = getTime(getFileName(j + 1))
                tempSum += float(times[j])
            aveTime = tempSum / playerNum
            for j in range(playerNum):
                if float(times[j]) > 1.25 * aveTime:
                    ColorfulPrint.colorfulPrint(' ----- ' + playerName[j] + ' use time: ' + times[j] + 's TLE! ----- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
                else:
                    ColorfulPrint.colorfulPrint(' ----- ' + playerName[j] + ' use time: ' + times[j] + 's ----- ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
            toAdd = ''
            for j in range(playerNum):
                if j != 0:
                    toAdd = toAdd + ',' + str(float(times[j]) / aveTime)
                else:
                    toAdd = toAdd + str(float(times[j]) / aveTime)
            toAdd = toAdd + '\n'
            with open('time.txt', 'a') as f:
                f.write(toAdd)
    else:
        ColorfulPrint.colorfulPrint('Illegal players num!', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)

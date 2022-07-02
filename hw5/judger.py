import re
import os
from outputChecker import checkOutput
from colorfulPrint import ColorfulPrint
times = []

def checkTime():
    with open('stdout.txt', 'r') as f:
        read = f.readlines()
    read = read[-1]
    yourTime = re.findall(r"\d+\.?\d*", read)
    yourTime = yourTime[0]
    with open('time.txt', 'r') as f:
        read = f.readlines()
    read = read[0]
    times = re.findall(r"\d+\.?\d*", read)
    if float(yourTime) > float(times[1]) + 0.25:
        ColorfulPrint.colorfulPrint(' ***** TLE ***** ' + 'Your time: ' + yourTime + ', Max time: ' + times[1], ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        return 2
    elif float(yourTime) > float(times[0]) + 0.25:
        ColorfulPrint.colorfulPrint(' ##### BAD PERFORMANCE ##### ' + 'Your time: ' + yourTime + ', Base time: ' + times[0], ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_YELLOW)
        return 1
    else:
        ColorfulPrint.colorfulPrint(' ===== TIME ACCEPTED ===== ' + 'Your time: ' + yourTime + ', Base time: ' + times[0], ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
        return 0

if __name__ == "__main__":
    waCount = 0
    accCount = 0
    badCount = 0
    tleCount = 0
    passCount = 0
    failCount = 0
    x = 50
    cmd = 'chmod u+x datainput_student_linux_x86_64'
    os.system(cmd)
    cmd = 'chmod u+x datacheck1_linux'
    os.system(cmd)
    for i in range(x) :
        ColorfulPrint.colorfulPrint(' >>>>>>>>>>>>>>>>>>>>>>> TEST {} <<<<<<<<<<<<<<<<<<<<<<<< '.format(i + 1), ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
        cmd = 'python3 generate.py > stdin.txt' 
        os.system(cmd)
        cmd = './datainput_student_linux_x86_64 | java -jar code.jar > stdout.txt'
        os.system(cmd)
        cmd = './datacheck1_linux > time.txt'
        os.system(cmd)
        temp = checkTime()
        if temp == 2:
            with open('stdin.txt', 'r') as f:
                con = f.read()
            with open('./logTime/stdin' + str(i + 1) + '.txt', 'w') as f:
                f.write(con)
            with open('stdout.txt', 'r') as f:
                con = f.read()
            with open('./logTime/stdout' + str(i + 1) + '.txt', 'w') as f:
                f.write(con)
            tleCount += 1
            waCount += 1
            res = False
        elif temp == 1:
            badCount += 1
            res = True
        else:
            accCount += 1
            res = True
        temp = checkOutput()
        if temp:
            passCount += 1
        else:
            failCount += 1
            waCount += 1
            with open('stdin.txt', 'r') as f:
                con = f.read()
            with open('./logWA/stdin' + str(i + 1) + '.txt', 'w') as f:
                f.write(con)
            with open('stdout.txt', 'r') as f:
                con = f.read()
            with open('./logWA/stdout' + str(i + 1) + '.txt', 'w') as f:
                f.write(con)
    if waCount == 0:
        ColorfulPrint.colorfulPrint(' ===== YOU HAVE PASSED ALL TESTPOINT ===== ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
        ColorfulPrint.colorfulPrint(' ===== TESTPOINT PASSED: ' + str(x) + '/' + str(x) + ' ===== ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
    else:
        ColorfulPrint.colorfulPrint(' ***** YOU HAVE NOT PASSED ALL TESTPOINT ***** ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        ColorfulPrint.colorfulPrint(' ***** TESTPOINT PASSED: ' + str(x - waCount) + '/' + str(x) + ' ***** ', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint(' ===== Time accept: ' + str(accCount) + '/' + str(x) + ' rate: ' + str(accCount * 100 / x) + '% =====', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
    ColorfulPrint.colorfulPrint(' ##### Bad performance: ' + str(badCount) + '/' + str(x) + ' rate: ' + str(badCount * 100 / x) + '% #####', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_YELLOW)
    ColorfulPrint.colorfulPrint(' ***** Tle: ' + str(tleCount) + '/' + str(x) + ' rate: ' + str(tleCount * 100 / x) + '% *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint(' ===== Output correct: ' + str(passCount) + '/' + str(x) + ' rate: ' + str(passCount * 100 / x) + '% =====', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
    ColorfulPrint.colorfulPrint(' ***** Output incorrect: ' + str(failCount) + '/' + str(x) + ' rate: ' + str(failCount * 100 / x) + '% *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)

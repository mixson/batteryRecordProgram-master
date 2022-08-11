import copy
import time
import os, sys

import datetime

currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
batteryDir = os.path.join(currentDir, "batteryRecord")

sys.path.insert(0, currentDir)

from utils.logTool import exception_handler
from utils.comboFun import getOnlineAGVDictList, getAGVFullList
from utils.General_Function import generateTimeIntervalList




@exception_handler
def getRegularBatteryInfo():
    print("")


@exception_handler
def writeDataIntoFile(dataStr, fileAbsolutePath):
    with open(fileAbsolutePath, "a+") as file:
        file.write(dataStr)


def getCurrentTimeInterval(timeIntervalList):
    currentTime = datetime.datetime.now()
    for i in range(len(timeIntervalList) - 1):
        if currentTime >= timeIntervalList[i] and currentTime < timeIntervalList[i + 1]:
            return timeIntervalList[i]
    return None

def getOfflineAGVList(agvDictDataList, agvFullDataList):
    agvDictSet = set([agvDict["robotCode"] for agvDict in agvDictDataList])
    agvFullLSet = set([agvDict["code"] for agvDict in agvFullDataList])

    return list(agvFullLSet.difference(agvDictSet))



def addOfflineAGVIntoAGVDictList(offlineAGVList, agvDictDataList, rowList):
    for agvCode in offlineAGVList:
        addDict = {key: None for key in rowList}
        addDict["robotCode"] = agvCode

        agvDictDataList.append(addDict)
    print("success added : {}".format(str(offlineAGVList)))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    rowList = ["robotCode", "robotIp", "statusStr", "battery", "excludeStr", "posX", "posY", "taskCode", "taskStatus"]

    colStr = "recordTime\t"
    colStr += "\t".join(rowList)
    colStr += "\n"



    while True:
        currentTime = datetime.datetime.now()
        startTime = currentTime.replace( hour=0, minute=0, second=0, microsecond=0)
        endTime = startTime + datetime.timedelta(days=1)
        timeInterval = datetime.timedelta(minutes=1)
        timeIntervalList = generateTimeIntervalList(startTime, endTime, timeInterval)

        month = startTime.month
        day = startTime.day

        currentTimeInterval = getCurrentTimeInterval(timeIntervalList)

        agvFullList = getAGVFullList()
        agvStatusDictList = getOnlineAGVDictList("-1")
        offlineAGVList = getOfflineAGVList(agvStatusDictList, agvFullList)
        addOfflineAGVIntoAGVDictList(offlineAGVList, agvStatusDictList, rowList)


        for agvDict in agvStatusDictList:
            fileName = "{}_{}_{}.txt".format(agvDict["robotCode"], str(month), str(day))
            fileFullPath = os.path.join(batteryDir, fileName)
            isFileCreated = os.path.exists(fileFullPath)

            if not isFileCreated:
                with open(fileName, "a+") as file:
                    writeDataIntoFile(colStr, fileFullPath)

            agvStatusStr = "{}\t".format(currentTimeInterval.strftime("%Y-%m-%d %H:%M:%S"))
            for row in rowList:
                rowValue = "NA"
                if row in agvDict.keys():
                    rowValue = agvDict[row]
                agvStatusStr += "{}\t".format(rowValue)

            agvStatusStr += "\n"

            writeDataIntoFile(agvStatusStr, fileFullPath)


        print(datetime.datetime.now())
        # time.sleep(10)
        time.sleep(15* 60)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

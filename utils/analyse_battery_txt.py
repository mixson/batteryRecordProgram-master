import datetime
import os

from utils.General_Function import withInRange

def readTxtIntoDict(filePath):
    resultDict = {}
    rowList = ["recordTime","robotCode", "robotIp", "statusStr", "battery", "excludeStr", "posX", "posY", "taskCode", "taskStatus"]
    with open(filePath, "r+") as file:
        lines = file.readlines()

    colNameList = lines[0].replace("\n","").split("\t")

    for line in lines[1:]:
        rowDataList = line.split("\t")
        for colName in colNameList:
            dateTimeStr = rowDataList[0]
            resultDict[dateTimeStr] = {colNameList[i]: rowDataList[i] for i in range(len(colNameList))}

    return resultDict



def getRecordFileByAGVByDate(agvCode, startTime, endTime, batteryRecordDir):
    targetFilesFullPathList = []
    for fileDir,_,fileNameList in os.walk(batteryRecordDir):
        for fileName in fileNameList:
            fileInfoList = fileName.replace(".txt","").split("_")
            fileAGVCode = fileInfoList[0]
            fileDateTime = datetime.datetime(year=2022, month=int(fileInfoList[1]), day=int(fileInfoList[2]))
            if ((fileAGVCode == agvCode or agvCode == "-1")and withInRange(fileDateTime, startTime, endTime)):
                targetFilesFullPathList.append(os.path.join(fileDir, fileName))
                print(fileName)


    return targetFilesFullPathList

def getAGVStatusDictByAGVCode(agvCode, startTime, endTime, batteryRecordDir): # for agv battery tracking
    outputDict = {agvCode: {}}
    agvFileList = getRecordFileByAGVByDate(agvCode, startTime, endTime, batteryRecordDir)
    for agvFile in agvFileList:
        resultDict = readTxtIntoDict(agvFile)
        outputDict[agvCode].update(resultDict)
    return outputDict

def getAGVBatteryByDate(startTime, endTime, batteryRecordDir):
    agvFileList = getRecordFileByAGVByDate("-1", startTime, endTime, batteryRecordDir)

    outputDict = {}
    for agvFile in agvFileList:
        dataResultDict = readTxtIntoDict(agvFile)
        for dateTimeStr, dataLine in dataResultDict.items():
            if dateTimeStr not in outputDict.keys():
                outputDict[dateTimeStr] = []
            outputDict[dateTimeStr].append(dataLine)
    return outputDict

def getAverageBatteryByTimeList(timeDictList):
    validCount = 0
    validSum = 0
    for dataLine in timeDictList:
        batteryLevel = dataLine["battery"]
        if batteryLevel != 'None':
            validCount += 1
            validSum += int(batteryLevel)


    if validCount != 0:
        return {"total": len(timeDictList), "count": validCount, "level": validSum//validCount}
    else:
        return {"total": len(timeDictList), "count": validCount, "level": 0}

def getAverageBatteryResultDict(resultDict):
    pass




if __name__ == "__main__":
    print("Hello")
    batteryRecordDir = r"C:\Users\user\Desktop\Protek\Project\PnS\batteryRecordProgram-master\batteryRecord"
    endTime = datetime.datetime.now() - datetime.timedelta(days=7)
    startTime = endTime - datetime.timedelta(days=4)
    # agvFileList = getRecordFileByAGVByDate("7001", startTime, endTime, batteryRecordDir)
    # agvFileList = getAGVStatusDictByAGVCode("7005", startTime, endTime, batteryRecordDir)
    agvRecordByDateTime = getAGVBatteryByDate(startTime, endTime, batteryRecordDir)
    resultDict = {}
    for dateTimeStr, dateList in agvRecordByDateTime.items():
        resultDict[dateTimeStr] = getAverageBatteryByTimeList(dateList)

    # for agvFile in agvFileList:
    #     resultDict = readTxtIntoDict(agvFile)
    #     # resultDict = readTxtIntoDict(r"C:\Users\user\Desktop\Protek\Project\PnS\batteryRecordProgram-master\7006_8_8.txt")
    print(resultDict)
from utils.Web_Rcs import Web_RCS
import json

def getOnlineAGVDictList(agvStr):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    deviceStatusQueryService = Web_RCS.DeviceStatusQueryService()
    deviceStatusQueryService.setMapShortName("PnS")
    if agvStr == "-1" or agvStr == -1:
        deviceStatusQueryService.setRobotCode(agvStr)
    else:
        deviceStatusQueryService.setRobotList(agvStr)
    result = json.loads(deviceStatusQueryService.sendJSON().text)
    agvCloseList = result["data"]
    return agvCloseList

def getAGVFullList():
    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvListService = Web_RCS.AGVListService()
    agvListResult = json.loads(agvListService.sendJSON().text)
    return agvListResult["data"]
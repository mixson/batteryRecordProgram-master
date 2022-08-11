from utils.Web_Rcs import Web_RCS
import json

def getOnlineAGVDictList(agvStr):
    deviceStatusQueryService = Web_RCS.DeviceStatusQueryService()
    deviceStatusQueryService.setMapShortName("PnS")
    if agvStr == "-1" or agvStr == -1:
        deviceStatusQueryService.setRobotCode(agvStr)
    else:
        deviceStatusQueryService.setRobotList(agvStr)
    result = json.loads(deviceStatusQueryService.sendJSON().text)
    agvCloseList = result["data"]
    return agvCloseList

if __name__ == '__main__':
    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvList = getOnlineAGVDictList(-1)
    print("")
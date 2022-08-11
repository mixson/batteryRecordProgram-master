import logging
import datetime
import os
import traceback

currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
loggingDirPath = os.path.join(currentDir, "log")



def getLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("DailyRouteLog", "{}".format(todayStr))
    # config
    logging.captureWarnings(True)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(message)s')
    myLogger = logging.getLogger("py.warnings")
    myLogger.setLevel(logging.INFO)

    if not os.path.exists(loggingDirPath):
        os.makedirs(loggingDirPath)

    if str(os.path.join(loggingDirPath, fileName)) in [handler.baseFilename for handler in myLogger.handlers if hasattr(handler, "baseFilename")]:
        logger.handlers = []

    fileHandler = logging.FileHandler(os.path.join(loggingDirPath, fileName))
    fileHandler.setFormatter(formatter)
    myLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    myLogger.addHandler(consoleHandler)

    return myLogger

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = getLogger()
            tb = traceback.format_exc()
            logger.error(tb)
            logger.error(str(e))
    return inner_function

# singleton
logger = getLogger()
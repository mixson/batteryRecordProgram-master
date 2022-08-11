from utils.logTool import exception_handler

@exception_handler
def aFun():
    a = 0
    b = 1
    c = b/a

if __name__ == '__main__':
    aFun()
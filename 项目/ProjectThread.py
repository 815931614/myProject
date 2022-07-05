from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import threading
from threading import Lock
import time
import inspect
from Tool import Tool_Random
import ctypes
from PyQt5.QtWidgets import QPushButton
class ProjectThread(QThread):
    _tablePyqtSignal = pyqtSignal(dict)
    _successNumPyqtSignal = pyqtSignal(str)
    _btnPyqtSignal = pyqtSignal(QPushButton,bool)
    _consoleOutPyqtSignal = pyqtSignal(str,str)
    def __init__(self,data):
        super(QThread, self).__init__()

        # 项目名称
        self.projectName = data['项目名称']

        # 线程数量
        self.threadNum = int(data['线程数量'])

        # 间隔时间
        self.intervalTime = int(data['间隔时间'])

        # 注册数量
        self.runSuccessNum = int(data['注册数量'])

        # 邀请码
        self.inviteCode = data['邀请码']

        # 开始按钮
        self.btn = data['开始按钮']

        # 接码
        self.jiema = data['接码平台']

        # 打码
        self.dama = data['打码平台']

        # 代理
        self.proxiesApi = data['代理平台']

        # 实名
        self.idCardDoc = data['实名数据']

        # 账号密码
        self.accountPassword = data['账号密码']

        # 是否随机密码
        self.isRandomAccountPassword = data['是否随机账号密码']

        # 交易密码
        self.transactionPassword = data['交易密码']

        # 是否随机交易密码
        self.isRandomTransactionPassword = data['是否随机交易密码']

        # 工具类
        self.tool_random = Tool_Random()

        # 当前以注册完成的数量
        self.successNum = 0

        # 信号锁(界面表格)
        self.tablePyqtSignalMutex = QMutex()  # 创建线程锁

        # 信号锁(成功数量)
        self.successNumPyqtSignalMutex = QMutex()  # 创建线程锁

        # 信号锁(日志)
        self.consolePyqtSignalMutex = QMutex()  # 创建线程锁

        self.rowIndex = 0

        self.rowLock = Lock()  # 创建线程锁

        # 已创建的线程
        self.threadAll = []

        # 验证创建线程锁
        self.createLock = threading.RLock()

        self.flag = False

    def run(self):

        for r in range(int(self.threadNum)):
            self.createThread(False,int(self.intervalTime) * r)
            time.sleep(.1)


    def runMain(self,sleepTime):
        pass
    def createThread(self, flag,sleepTime = None):
        '''
               :param flag: 是否执行成功
               :param num:
               :return:
               '''
        self.createLock.acquire()

        if flag:
            self.successNum += 1
        aliveThread = self.getAliveThreadNum()
        self.updateSuccessNum(self.successNum)
        # 如果当前存活的线程数量，小于剩余的数量，则创建线程
        if not self.flag and aliveThread - 1 < self.runSuccessNum - self.successNum:
            if sleepTime == None:
                sleepTime = self.intervalTime
            t = threading.Thread(target=self.runMain, args=(sleepTime,))
            t.start()
            self.threadAll.append(t)
        elif aliveThread == 1 and (self.runSuccessNum == self.successNum or self.flag):
            self._btnPyqtSignal.emit(self.btn, True)
            self.addConsoleOut("运行完成")

        self.createLock.release()
    def getAliveThreadNum(self):
        aliveNum = 0
        for t in self.threadAll:
            if t.isAlive():
                aliveNum += 1
        return aliveNum


    def addConsoleOut(self, text,type=""):
        self.consolePyqtSignalMutex.lock()  # 加锁
        self._consoleOutPyqtSignal.emit(text,type)
        self.consolePyqtSignalMutex.unlock()  # 解锁


    def updateSuccessNum(self, num):
        self.successNumPyqtSignalMutex.lock()  # 加锁
        self._successNumPyqtSignal.emit(str(num))
        self.successNumPyqtSignalMutex.unlock()  # 解锁



    def updateTable(self,row,col,text):
        self.tablePyqtSignalMutex.lock()  # 加锁
        self._tablePyqtSignal.emit({
            'row' : row,
            'col' : col,
            'msg' : text
        })
        self.tablePyqtSignalMutex.unlock()  # 解锁

    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:

            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self,thread):
        try:
            self._async_raise(thread.ident, SystemExit)
        except Exception:
            pass
    def stopThreadAll(self):
        self.flag = True
        t = threading.Thread(target=self.stopThreadRun)
        t.start()
    def getRowIndex(self):
        with self.rowLock:
            self.rowIndex += 1
            return self.rowIndex - 1
    def stopThreadRun(self):
        self._btnPyqtSignal.emit(self.btn, True)
        self.addConsoleOut("运行完成")
        while 1:
            f = True
            for t in self.threadAll:
                if t.isAlive():
                    f = False
                    self.stop_thread(t)
                time.sleep(.1)
            if f:
                break
# api-06UfUlD0   abc123456  33498
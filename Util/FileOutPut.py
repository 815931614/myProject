import threading
import os
import json
import winreg
class FileOutPut:

    def __init__(self):
        self.desktopURI = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'), "Desktop")[0]


        self.createLock = threading.RLock()
        self.createLock2 = threading.RLock()


    def readFile(self):
        pass



    def appendFile(self,filename,text,fileType = "txt"):
        self.createLock.acquire()
        f = open(self.desktopURI + "\\" + filename  + "." + fileType, "a")
        f.write(text + "\n")
        f.close()
        self.createLock.release()



    def fileWrite(self,path,text):
        with open(path,"w") as f:
            f.write(text)

    def fileRead(self,path):
        with open(path, "r") as r:
            return r.read()

    def realNameCache(self,projectName,name,idcard):
        self.createLock2.acquire()
        fl = False
        userPath = "\\".join(self.desktopURI.split("\\")[0:-1])
        text = name + '-' + idcard
        filePath = userPath + "\\." + projectName
        rlist = []
        if os.path.exists(filePath):
            rlist = json.loads(self.fileRead(filePath))
        if text not in rlist:
            rlist.append(text)
            self.fileWrite(filePath, json.dumps(rlist))
            fl =  True
        self.createLock2.release()
        return fl



    def readInfo(self):
        userPath = "\\".join(self.desktopURI.split("\\")[0:-1])
        filePath = userPath + "\\.info"
        rlist = {
            "接码平台" : {},
            "打码平台"  : {},
            '代理平台' : {},
        }
        if os.path.exists(filePath):
            rlist = json.loads(self.fileRead(filePath))
        else:
            self.fileWrite(filePath,json.dumps(rlist))
        return rlist
    def updateInfo(self,rlist):
        userPath = "\\".join(self.desktopURI.split("\\")[0:-1])
        filePath = userPath + "\\.info"
        self.fileWrite(filePath,json.dumps(rlist))

if __name__ == '__main__':
    print(FileOutPut().readInfo())
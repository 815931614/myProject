import time
from ProjectThread import ProjectThread
from IGO import IGO
from FileOutPut import FileOutPut
import threading


class ProjectRunMain(ProjectThread):


    def __init__(self,data):
        super(ProjectRunMain, self).__init__(data)


        self.getSmsfrequency = 10  # 接码获取验证码次数

        self.getSmsTime = 5  # 接码获取验证码间隔秒数

        self.filOutPut = FileOutPut()

        self.fileName = self.projectName + ' ' + time.strftime('%Y-%m-%d %H{H}%M{M}%S{S}').format(H='点', M='分', S='秒')

        self.realNameIndex = 1

        self.realNameLock = threading.RLock()

    def runMain(self, sleepTime):
        time.sleep(sleepTime)
        row = self.getRowIndex()

        self.updateTable(row, 0, self.tool_random.getRandomPhoneNumber())
        time.sleep(1.5)
        self.updateTable(row, 1, self.tool_random.getRandomAccountPassword() + "/" + self.tool_random.getRandomTransactionPassword())
        time.sleep(1.5)
        self.updateTable(row, 2, "ok")
        time.sleep(.5)
        # projectObject = IGO()
        # phoneNum = self.idCardDoc[row + self.runSuccessNum][0]
        # self.updateTable(row, 0, phoneNum)
        # passWord = self.idCardDoc[row + self.runSuccessNum][1]
        # print(row + self.runSuccessNum)
        # self.updateTable(row, 1, passWord)
        # ipRes = self.getIp(row,projectObject) # 获取IP
        # if ipRes:
        #     loginres = self.login_Req(row,projectObject,phoneNum=phoneNum,passWord=passWord)
        #     if loginres:
        #         getMyGoods = self.getMyGoods(row,projectObject)
        #         if getMyGoods:
        #             self.filOutPut.appendFile(self.fileName,phoneNum + " " + passWord + " " + getMyGoods)
        self.createThread(True)


    def login_Req(self, row, obj, phoneNum, passWord):

        login_res = obj.login_Req(phoneNum=phoneNum, passWord=passWord)
        if login_res['code'] == 0:
            self.updateTable(row, 2, "登录成功")
            return True
        self.updateTable(row, 2, "登录失败：" + login_res['msg'])



    def getPhone(self,row):
        '''
        获取手机号
        :return:
        '''
        self.updateTable(row, 2, "获取手机号")
        phoneRes = self.jiema.getPhone()

        if phoneRes['code'] == 0:

            self.updateTable(row, 2, "获取成功")
            self.updateTable(row, 0, phoneRes['mobile'])
            return phoneRes['mobile']

        if "余额不足" in phoneRes['msg']:
            self.flag = True
            self.flag = True
            self.addConsoleOut(f"第{row + 1}行，接码余额不足，请充值，然后重新启动；", 'Error')
            return
        self.updateTable(row, 2, "获取失败")
        self.addConsoleOut(f"第{row + 1}行，获取手机号:{phoneRes['msg']}" , 'Error')


    def getSmsCode(self,row,phoneNum):
        '''
        获取验证码
        :param row:
        :param phoneNum:
        :return:
        '''
        self.updateTable(row, 2, "正在获取验证码")
        smsCodeRes = None
        for i in range(self.getSmsfrequency):
            smsCodeRes = self.jiema.getMessage(phoneNum)
            if smsCodeRes['code'] == 0:
                self.updateTable(row, 2, "获取成功")
                return smsCodeRes['smsCode']
            if i < self.getSmsfrequency-1:
                time.sleep(self.getSmsTime)
            if "余额不足" in smsCodeRes['msg']:
                self.flag = True
                self.addConsoleOut(f"第{row + 1}行，接码余额不足，请充值，然后重新启动；", 'Error')
                return
        self.jiema.addBlacklist(phoneNum)
        self.updateTable(row, 2, "验证码获取失败")
        self.addConsoleOut(f"第{row + 1}行，获取验证码:{smsCodeRes['msg']}", 'Error')



    def sendSms_Req(self,row,obj,phoneNum):
        """
           code
            0 : 发送成功
            1 : 此账号已注册
            2 : 需等待60秒后发送
            3 : 当日发送上限
            4 : 未知错误
           -1 : 异常


          code
           0 : 登录成功
           1 : 密码错误
           2 : 图形验证码错误
           3 : 该手机号未注册
           4 : 密码错误次数上限
           5 : 未知错误
          -1 : 异常
       """

        isr = obj.login_Req(phoneNum = phoneNum,passWord="123456yyy")
        if isr['code'] != 1:
            self.jiema.addBlacklist(phoneNum)
            self.updateTable(row, 2, "手机号已注册")
            return
        sendSms_res = obj.sendSms_Req(phoneNum = phoneNum)
        if sendSms_res['code'] == 0 or sendSms_res['code'] == 2:
            self.updateTable(row, 2, "发送成功")
            return True
        self.jiema.addBlacklist(phoneNum)
        self.updateTable(row, 2, "发送失败")
        self.addConsoleOut(f"第{row + 1}行，发送验证码:{sendSms_res['msg']}", 'Error')


    def register_Req(self, row, obj, phoneNum,smsCode):
        """
                   code
                    0 : 注册成功
                    1 : 此账号已注册
                    2 : 验证码错误
                    3 : 未知错误
                    4 : 图形验证码错误
                    5 : 邀请码不存在
                   -1 : 异常
        """
        '''
            'mobile': kwargs['phoneNum'],
            'password': kwargs['passWord'],
            'code': kwargs['smsCode'],
            'userId': '69770',
        
        '''
        register_res = obj.register_Req(phoneNum = phoneNum,smsCode = smsCode)
        if register_res['code'] == 0:
            self.updateTable(row, 2, "注册成功")
            return True
        self.updateTable(row, 2, "注册失败")
        self.addConsoleOut(f"第{row + 1}行，注册:{register_res['msg']}", 'Error')

    def setInviteCode(self,row,obj):
        '''
        设置邀请码
        :param row:
        :param obj:
        :return:
        '''
        setInviteCode_res = obj.setInviteCode(inviteCode=self.inviteCode)
        if setInviteCode_res['code'] == 0:
            return True
        self.updateTable(row, 2, "邀请码设置失败")
        self.addConsoleOut(f"第{row + 1}行，邀请码设置:{setInviteCode_res['msg']}", 'Error')


    def setLoginPassWord(self,row, obj,password):
        '''
        设置登录密码
        :param row:
        :param obj:
        :param password:
        :return:
        '''
        setLoginPassWord_res = obj.setLoginPassWord( passWord=password)
        if setLoginPassWord_res['code'] == 0:
            self.updateTable(row, 2, "密码设置成功")
            self.updateTable(row, 1, password)
            return True
        self.updateTable(row, 2, "密码设置失败")
        self.addConsoleOut(f"第{row + 1}行，设置密码:{setLoginPassWord_res['msg']}", 'Error')


    def setRealName(self, row, obj):
        '''
        实名
        :param row:
        :param obj:
        :return:
        '''
        card = self.getRealName(row)
        realNameAuthentication_Res = obj.realNameAuthentication_Req(name=card[0], idCard=card[1])
        if realNameAuthentication_Res['code'] == 0:
            self.updateTable(row, 2, "实名成功")
            return [card[0], card[1]]
        self.updateTable(row, 2, "实名失败")
        self.addConsoleOut(f"第{row + 1}行，实名失败:{realNameAuthentication_Res['msg']}", 'Error')


    def getIp(self,row,obj):
        '''
        设置IP
        :param row:
        :param obj:
        :return:
        '''
        if self.proxiesApi == None:
            return True
        while True:
            proxies = self.proxiesApi.getIp()
            if proxies['code'] == 0:
                obj.setProxies(proxies['IP']) # 设置iP
                self.addConsoleOut( f"第{row + 1}行，获取成功:{proxies['IP']}，剩余数量：{proxies['number']}")
                return proxies['IP']
            self.addConsoleOut(f"第{row + 1}行，IP获取失败:{proxies['msg']}，5秒后重新获取。", 'Error')
            time.sleep(5)



    def getRealName(self,row):
        '''
        获取身份证信息
        :param row:
        :return:
        '''
        self.realNameLock.acquire()
        n = None
        c = None
        for i in range(self.realNameIndex,len(self.idCardDoc)):
            self.realNameIndex = i + 1
            n = self.idCardDoc[i][0]
            c = self.idCardDoc[i][1]
            isCache = self.filOutPut.realNameCache(self.projectName,n,c)
            if isCache:
                self.realNameLock.release()
                return [n,c]
            self.addConsoleOut(f"第{row + 1}行，实名信息已使用,5秒后重新尝试", 'Error')
            time.sleep(5)
        if self.realNameIndex >= len(self.idCardDoc):
            self.addConsoleOut(f"第{row + 1}行，实名信息已使用完毕，请手动登录实名", 'Error')
            self.flag = True
            self.realNameLock.release()
            return None

    def getAccountPassword(self):
        '''
        获取账号密码
        :return:
        '''
        if self.isRandomAccountPassword:
            return self.tool_random.getRandomAccountPassword()
        return self.accountPassword



    def getTransactionPassword(self):
        '''
        获取交易密码
        :return:
        '''
        if self.isRandomTransactionPassword:
            return self.tool_random.getRandomTransactionPassword()
        return self.transactionPassword
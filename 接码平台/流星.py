import requests
import time
from requests import exceptions
import re
from JieMaParent import JieMaParent
class liuxing(JieMaParent):
    def __init__(self):
        """
        @param apiName: 接码平台的API账号
        @param passWord: 密码
        @param project_id: 项目ID
        """
        super(liuxing, self).__init__()

        self.money = None
        # 项目id
        self.project_id = None

        # token
        self.token = None

        # 开发者账号
        self.api_id = "108763"
        self.operator = ''
        # 域名api地址
        self.domainName = "http://api.lx967.com:9090/sms/api/"

    def login(self,apiName,passWord):

        """
        登录
        @return: 成功返回ok; 失败返回原因
        """
        self.token = None
        date = {
            'username': apiName,
            'password': passWord
        }
        res = self.requestsGet('login', date)
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['msg'] == "success":
            self.token = res['token']
            resdata['code'] = 0
            self.money = str(res['money'])
            resdata['money'] = self.money
        else:
            resdata['code'] = 1
        resdata['msg'] = res['msg']
        return resdata

    def getUserInfo(self):
        """
        @return: 返回当前账户的余额
        """
        date = {
            'token': self.token
        }
        res = self.requestsGet('userinfo', date)
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['msg'] == "success":
            resdata['code'] = 0
            self.money = str(res['money'])
            resdata['money'] = self.money
        else:
            resdata['code'] = 1
        resdata['msg'] = res['msg']
        return resdata

    def setOperator(self, operator):
        if operator != 0:
            self.operator = operator


    def getPhone(self):
        '''
        :param ascription:
        :return: ascription: 1:实卡；2:虚拟卡
        '''
        date = {
            'token': self.token,
            'sid': self.project_id,
            'ascription': self.operator
         }
        res = self.requestsGet('getPhone', date)

        # {"msg": "success", "code": 0, "phone": "13852137155"}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['code'] == 0:
             resdata['code'] = 0
             resdata['mobile'] = res["phone"]
        else:
            resdata['code'] = 1
        resdata['msg'] = res['msg']
        return resdata
    def getMessage(self,phone_num):

        date = {
            'token': self.token,
            'sid': self.project_id,
            'phone': phone_num,
            'tid': self.api_id
        }
        res = self.requestsGet('getMessage', date)


        # {"msg":"success","code":0,"sms":"您的短信为10083"}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['code'] == 0:
            resdata['code'] = 0
            resdata['smsCode'] = re.compile(r'([0-9]{4})', re.I).findall( res["sms"])[0]
        elif res['code'] == -1 or res['code'] == -4:
            resdata['code'] = 1
        else:
            resdata['code'] = 2

        resdata['msg'] = res['msg']
        return resdata

    def addBlacklist(self, phone_num):
        date = {
            'token': self.token,
            'sid': self.project_id,
            'phone': phone_num
        }
        res = self.requestsGet('addBlacklist', date)
        # {"msg":"success","code":0}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['code'] == 0:
            resdata['code'] = 0
        else:
            resdata['code'] = 1
        resdata['msg'] = res['msg']
        return resdata

    def cancelRecv(self, phone_num):
        date = {
            'token': self.token,
            'sid': self.project_id,
            'phone': phone_num
        }
        res = self.requestsGet('addBlacklist', date)
        # {"msg":"success","code":0}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['code'] == 0:
            resdata['code'] = 0
        else:
            resdata['code'] = 1

        resdata['msg'] = res['msg']
        return resdata

    def cancelRecvAll(self):
        date = {
            'token': self.token,
            'sid': self.project_id,
            'phone': "all"
        }
        res = self.requestsGet('addBlacklist', date)
        # {"msg":"success","code":0}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['code'] == 0:
            resdata['code'] = 0
        else:
            resdata['code'] = 1

        resdata['msg'] = res['msg']
        return resdata


if __name__ == '__main__':
    m  = liuxing()
    print(m.login("api-06UfUlD0","abc123456"))


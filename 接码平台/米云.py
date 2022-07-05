import requests
import time
from requests import exceptions
from JieMaParent import JieMaParent
class miyun(JieMaParent):
    def __init__(self):
        """
        @param apiName: 接码平台的API账号
        @param passWord: 密码
        @param project_id: 项目ID
        """
        super(miyun, self).__init__()
        self.money = None
        # 项目id
        self.project_id = None

        self.operator = 0

        # token
        self.token = None

        # 开发者账号
        self.api_id = "815931614"

        # 域名api地址
        self.domainName = "https://api.miyun999.live/api/"

    def login(self,apiName,passWord):

        """
        登录
        @return: 成功返回ok; 失败返回原因
        """
        self.token = None
        date = {
            'apiName': apiName,
            'password': passWord
        }
        res = self.requestsGet('login', date)

        resdata = {}
        if res['code'] == 999:
           return res
        elif res['message'] == "ok":
            self.token = res['token']
            resdata['code'] = 0
            resdata['token'] = res['token']
            userInfo = self.getUserInfo()
            if userInfo['code'] == 0:
                self.money = userInfo['money']
                resdata['money'] = self.money
            else:
                resdata['money'] = userInfo['msg']
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
        return resdata

    def getUserInfo(self):
        """
        @return: 返回当前账户的余额
        """
        date = {
            'token': self.token
        }
        res = self.requestsGet('get_myinfo', date)
        resdata = {}
        if res['code'] == 999:
           return res
        elif res['message'] == "ok":
            resdata['code'] = 0
            self.money =  str(res['money'])
            resdata['money'] = self.money
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
        return resdata

    def setOperator(self,operator):
        if operator == 0:
            self.operator = 0
        elif operator == 1:
            self.operator = 4
        elif operator == 2:
            self.operator = 5
    def getPhone(self):
        '''
        :param ascription:
        :return: ascription: 1:实卡；2:虚拟卡
        '''
        date = {
            'token': self.token,
            'project_id': self.project_id,
            'operator': self.operator,
            'api_id' : self.api_id
         }
        res = self.requestsGet('get_mobile', date)

        # {"msg": "success", "code": 0, "phone": "13852137155"}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['message'] == "ok":
             resdata['code'] = 0
             resdata['mobile'] = res["mobile"]
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
        return resdata

    def getMessage(self,phone_num):

        date = {
            'token': self.token,
            'project_id': self.project_id,
            'phone_num': phone_num
        }

        res = self.requestsGet('get_message', date)
        # {"msg":"success","code":0,"sms":"您的短信为10083"}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['message'] == "ok":
            resdata['code'] = 0
            resdata['smsCode'] = res["code"]
        elif res['message'] == "暂无消息..":
            resdata['code'] = 1
        else:
            resdata['code'] = 2
        resdata['msg'] = res['message']
        return resdata

    def addBlacklist(self, phone_num):
        date = {
            'token': self.token,
            'project_id': self.project_id,
            'phone_num': phone_num
        }
        res = self.requestsGet('add_blacklist', date)
        # {"msg":"success","code":0}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['message'] == "ok":
            resdata['code'] = 0
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
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
        elif res['message'] == "ok":
            resdata['code'] = 0
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
        return resdata


if __name__ == '__main__':
    m  = miyun()
    print(m.login("MY.2078223256","abc123456"))
    # mo = m.addBlacklist(16537639452)
    # print(mo)
    # while False:
    #     print(m.getMessage(mo))
    #     time.sleep(3)


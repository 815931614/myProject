import requests
import time
from requests import exceptions
from JieMaParent import JieMaParent
class yezhi(JieMaParent):
    def __init__(self):
        """
        @param apiName: 接码平台的API账号
        @param passWord: 密码
        @param project_id: 项目ID
        """
        super(yezhi, self).__init__()
        self.operator = 0

        # 项目id
        self.project_id = None

        self.money = None

        # token
        self.token = None

        # 开发者账号
        self.api_id = "498898"

        # 域名api地址
        self.domainName = "http://api.sqhyw.net:81/api/"

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
        res = self.requestsGet('logins', date)
        # {'code': 0, 'msg': '登录成功', 'money': '6.8000'}
        resdata = {}
        if res['code'] == 999:
           return res
        elif res['message'] == "登录成功":
            self.token = res['token']
            resdata['code'] = 0
            resdata['msg'] = "登录成功"
            self.money = res['data'][0]['money']
            resdata['money'] = self.money
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
        # {'message': 'ok', 'data': [{'money': '6.8000', 'money_1': '0.0000'}], 'code': 200}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['message'] == "ok":
            resdata['code'] = 0
            self.money = res['data'][0]['money']
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
        # {'code': 200, 'msg': '未收到验证码'}
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['message'] == "ok":
            resdata['code'] = 0
            resdata['smsCode'] = res["code"]
        elif res['message'] == "未收到验证码":
            resdata['code'] = 1
        else :
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


    def cancelRecv(self,phone_num):
         # :http://api.sqhyw.net:81/api/free_mobile?token=xxxxx&phone_num=xxxxx&project_id=xxxx&project_type=X
        date = {
            'token': self.token,
            'project_id': self.project_id,
            'phone_num': phone_num
        }
        res = self.requestsGet('free_mobile', date)
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



    def cancelRecvAll(self):
        date = {
            'token': self.token
        }
        res = self.requestsGet('free_mobile', date)
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
    m  = yezhi()
    print(m.login("yz815931614","Abc123456."))
    # m.project_id = '151771'
    # mo = m.getPhone()
    #
    # print(mo)
    # while True:
    #     print(m.getMessage(mo))
    #     time.sleep(3)


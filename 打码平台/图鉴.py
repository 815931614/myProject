import requests
import time
from requests import exceptions

class TuJian:
    def __init__(self):
        """
        @param apiName: 接码平台的API账号
        @param passWord: 密码
        @param project_id: 项目ID
        """

        self.username = None

        self.password = None

        self.money = None



        # 域名api地址
        self.domainName = "http://api.ttshitu.com/"
    def requestsGet(self,path,params):
        resdate = {'code': 999}
        try:
            res = requests.get(self.domainName + path, params=params,verify=False).json()
            if 'code' not in res.keys():
                res['code'] = 200

            return res

        except exceptions.Timeout:
            resdate['msg'] = '请求超时'
        except exceptions.HTTPError:
            resdate['msg'] = 'http请求错误'
        except exceptions.ConnectionError:  # 断网情况下
            resdate['msg'] = '网络异常'
        except Exception as e:
            resdate['msg'] = '未知异常'
        return resdate
    def requestsPost(self,path,data):
        resdate = {'code': 999}
        try:
            res = requests.post(self.domainName + path, json=data,verify=False).json()
            if 'code' not in res.keys():
                res['code'] = 200



            return res

        except exceptions.Timeout:
            resdate['msg'] = '请求超时'
        except exceptions.HTTPError:
            resdate['msg'] = 'http请求错误'
        except exceptions.ConnectionError:  # 断网情况下
            resdate['msg'] = '网络异常'
        except Exception as e:
            resdate['msg'] = '未知异常'
        return resdate
    def login(self,username,passWord):

        """
        登录
        @return: 成功返回ok; 失败返回原因
        """

        date = {
            'username': username,
            'password': passWord
        }
        res = self.requestsGet('queryAccountInfo.json', date)

        resdata = {}
        if res['code'] == 999:
           return res
        elif res['success']:
            resdata['code'] = 0
            self.money = res['data']['balance']
            resdata['money'] = self.money
            self.username = username
            self.password = passWord
        else:
            resdata['code'] = 1
        resdata['msg'] = res['message']
        return resdata
    def predict(self,typeid,image):
        """
        通用图片识别
        @return:
        """
        date = {
            'username': self.username,
            'password': self.password,
            'typeid' :  typeid,
            'image' : image   # 注意不含：data:image/jpg;base64,直接图片base64编码）。
        }
        res = self.requestsPost('predict', date)
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['success']:
            resdata['msg'] = "ok"
            resdata['result'] = res['data']['result']
            resdata['id'] = res['data']['id']
        else:
            resdata['msg'] = res['message']
        return resdata
    def reporterror(self,id):
        """
         报错接口
         @return:
         """
        date = {
            'id': id
        }
        res = self.requestsPost('reporterror.json', date)
        resdata = {}
        if res['code'] == 999:
            return res
        elif res['success']:
            resdata['msg'] = "ok"
        else:
            resdata['msg'] = res['message']
        return resdata

if __name__ == '__main__':
  tj = TuJian()
  print(tj.login("815931614","abc123456"))
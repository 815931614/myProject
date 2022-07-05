import requests
import time
from requests import exceptions

class JieMaParent:
    def __init__(self):
        """
        @param apiName: 接码平台的API账号
        @param passWord: 密码
        @param project_id: 项目ID
        """

        self.operator = 0

        # 项目id
        self.project_id = None

        self.money = None

        # token
        self.token = None

        # 开发者账号
        self.api_id = None

        # 域名api地址
        self.domainName = None


    def requestsGet(self,path,params):
        index = 0
        while True:
            resdate = {'code': 999}
            try:
                res = requests.get(self.domainName + path, params=params).json()
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
                resdate['msg'] = '未知请求异常'
            if index <= 1:
                index += 1
                time.sleep(.5)
                continue
            return resdate


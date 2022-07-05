from requests import exceptions
import requests
import time

class ProjectParent:

    def __init__(self):

        self.header_post = None

        self.header_get = None

        self.proxies = None


    def setProxies(self,ip):

        self.proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip
        }

    def login(self,**kwargs):
        """
        登录
        :param kwargs:
        :return:
        """
        """
           code
            0 : 登录成功
            1 : 密码错误
            2 : 图形验证码错误
            3 : 该手机号未注册
            4 : 密码错误次数上限
            5 : 未知错误
           -1 : 异常
        """
        return self.login_Req(**kwargs)



    def getImgCode(self,**kwargs):
        return  ""




    def sendSms(self,**kwargs):
        """
        发送验证码
         0 : 发送成功
         1 : 此账号已注册
         2 : 需等待60秒后发送
         3 : 当日发送上限
         4 : 图形验证码错误
         5 : 未知错误
        -1 : 异常
       """

        sendSms_res = self.sendSms_Req(**kwargs)
        return sendSms_res


    def register(self,**kwargs):
        """
        注册
         0 : 注册成功
         1 : 此账号已注册
         2 : 验证码错误
         3 : 未知错误
         4 : 图形验证码错误
         5 : 邀请码不存在
        -1 : 异常
       """
        register_req = self.register_Req(**kwargs)
        return register_req



    def realNameAuthentication(self,**kwargs):

        """
            实名认证
           code
            0 : 认证成功
            1 : 该账号已实名
            2 : 该证件已使用
            3 : 证件错误
            4 : 未知错误
           -1 : 异常
          """
        realNameAuthentication_req = self.realNameAuthentication_Req(**kwargs)
        return realNameAuthentication_req


    def requests(self,url, method="post", **kwargs):
        for i in range(3):
            resdate = {'code': 999}
            try:

                if "proxies" not in kwargs:
                    kwargs['proxies'] = self.proxies
                kwargs['timeout'] = 5

                res = None

                if method == "post":

                    res = requests.post(url, **kwargs,).json()
                else:
                    res = requests.get(url, **kwargs).json()

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

            if i >= 2:
                return resdate
            time.sleep(1.5)



    def login_Req(self,**kwargs):
        return {}
    def getImgCode_req(self,**kwargs):
        return {}
    def sendSms_Req(self,**kwargs):
        return {}
    def register_Req(self,**kwargs):
        return {}
    def realNameAuthentication_Req(self,**kwargs):
        return {}

if __name__ == '__main__':
    ProjectParent(None).login(a = "1")
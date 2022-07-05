# -*- coding:utf-8 -*-
import time
from urllib.parse import parse_qs, urlparse, urlencode, quote, unquote
from ProjectParent import ProjectParent

class IGO(ProjectParent):
    def __init__(self,userAgent):
        super(IGO, self).__init__()

        self.header_get = {

        }
        self.header_post = {


        }

        self.host = ""
        self.token =""

    def login_Req(self,**kwargs):
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

        pass

    def sendSms_Req(self,**kwargs):
        """
         code
          0 : 发送成功
          1 : 此账号已注册
          2 : 需等待60秒后发送
          3 : 当日发送上限
          4 : 未知错误
         -1 : 异常
        """
        pass



    def register_Req(self,**kwargs):
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

        pass



    def realNameAuthentication_Req(self,**kwargs):

        """
            实名认证
           code
            0 : 认证成功
            1 : 该账号已实名
            2 : 该证件已使用
            3 : 证件错误
            4:  手机号与身份证信息不一致
            5 : 未知错误
           -1 : 异常
          """
        pass

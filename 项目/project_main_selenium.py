# -*- coding:utf-8 -*-
import time
from urllib.parse import parse_qs, urlparse, urlencode, quote, unquote
from ProjectParent_Selenium import ProjectParent_Selenium
from requests_toolbelt import MultipartEncoder
import string
from selenium.webdriver.common.action_chains import ActionChains
import random
import requests
from LocalRecognition import LocalRecognition
import json
from Image_Dispose import Image_Dispose
from Tool import Tool_Random
import ddddocr
from PIL import Image
import traceback


class Project_Main(ProjectParent_Selenium):
    def __init__(self,ip = None):
        super(Project_Main, self).__init__(ip)

        self.image_Dispose = Image_Dispose()

        self.host = ""
        self.token = ""
        self.localRecognition = LocalRecognition()
        self.uuid = None
        self.ocr = ddddocr.DdddOcr()

    def login_Req(self, **kwargs):
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
        res = self.openUrl("https://nft.cizang.art/Login?BackUrl=https%3A%2F%2Fnft.cizang.art%2FMember", 'qui-col-ff',
                           '立即注册')
        msg = ""
        if res['code'] == 0:
            res = self.set_input_value_xpath('//*[@id="app"]/div/form/div[1]/input', kwargs['phoneNum'])
            if res['code'] == 0:
                res = self.set_input_value_xpath('//*[@id="app"]/div/form/div[2]/input', kwargs['passWord'])
                if res['code'] == 0:
                    time.sleep(1.5)
                    res = self.click_find_xpath('//*[@id="app"]/div/form/div[3]/input')
                    if res['code'] == 0:
                        while True:
                            res = self.waitFor_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]")
                            print(res)
                            if res['code'] == 0:


                                res = self.waitFor_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]")
                                print(1)
                                res2 = self.waitFor_xpath("/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/img")
                                print(2)
                                if res['code'] == 0 and res2['code'] == 0:
                                    try:
                                        time.sleep(1)
                                        keysImg = self.driver.find_element_by_xpath(
                                            '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]')
                                        # element.screenshot('./baiduyixia.png')     #图片会保存到当前目录下

                                        keysImg.screenshot(r'./keysImg.png')

                                        bigImg = self.driver.find_element_by_xpath(
                                            '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]')
                                        # element.screenshot('./baiduyixia.png')     #图片会保存到当前目录下

                                        import base64
                                        bigImg.screenshot(r'./bigImg.png')
                                        ocr_res = self.localRecognition.hanzi_location(
                                            base64.b64decode(bigImg.screenshot_as_base64),
                                            keyImg=base64.b64decode(keysImg.screenshot_as_base64))
                                        if ocr_res['msg'] != 'ok':
                                            self.click_find_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/a[2]')
                                            time.sleep(1)
                                            continue
                                        else:
                                            for p in ocr_res['words_result']:
                                                ActionChains(self.driver).move_to_element_with_offset(to_element=bigImg,
                                                                                                      xoffset=
                                                                                                      p['position'][0],
                                                                                                      yoffset=
                                                                                                      p['position'][
                                                                                                          1]).click().perform()
                                                # time.sleep(.5)
                                            self.click_find_xpath(
                                                '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[2]')
                                            self.waitFor_xpath(
                                                '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]')
                                            while True:
                                                code_msg = self.driver.find_element_by_xpath(
                                                    '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]').text
                                                if code_msg: break
                                            print(code_msg)
                                            if '秒的速度超过' not in code_msg:
                                                time.sleep(1)
                                                continue


                                            while True:
                                                waitFor_res = self.waitFor_xpath('/html/body/div[4]/div')
                                                if waitFor_res['msg'] != 'ok':
                                                    return {
                                                        'code' : -5,
                                                        'msg': '登录超时'
                                                    }
                                                res_data = self.driver.find_element_by_xpath('/html/body/div[4]/div').text
                                                if res_data:
                                                    break
                                                time.sleep(.2)
                                            if res_data == "登录成功":
                                                res['code'] = 0
                                                res['msg'] = "登录成功"
                                            else:
                                                res['code'] = 4
                                                res['msg'] = res_data

                                        break
                                    except:
                                        traceback.print_exc()
                                        return {
                                            'code': -6,
                                            'msg': "验证码图片加载失败！"
                                        }

        return res

    def getMyGoods(self, **kwargs):
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

    def sendSms_Req(self, **kwargs):
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

    def register_Req(self, **kwargs):
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

    def setInviteCode(self, **kwargs):
        pass

    def setLoginPassWord(self, **kwargs):
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

    def realNameAuthentication_Req(self, **kwargs):

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


if __name__ == '__main__':
    pass
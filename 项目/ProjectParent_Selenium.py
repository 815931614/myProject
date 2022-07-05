# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,WebDriverException
import warnings
import time
import traceback
from LocalStorage import LocalStorage
from selenium.webdriver.common.action_chains import ActionChains
warnings.filterwarnings('ignore')
class ProjectParent_Selenium:

    def __init__(self,ip = None):
        self.ip = ip
        self.header_post = None

        self.header_get = None

        self.proxies = None

        self.driver = webdriver.Chrome(executable_path='../Chromium/chromedriver', options=self.getOptions())

        self.storage = LocalStorage(self.driver)
        # 隐藏webdriver，防止被检测
        self.setHideWebdriver()
    

    def getOptions(self):
        options = webdriver.ChromeOptions()
        # 页面加载策略
        options.page_load_strategy = 'eager'

        # 禁止加载css样式表

        # 去掉浏览器提示自动化黄条:没什么用处，只是为了好看而已。(附加去掉控制台多余日志信息)
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable- logging'])
        options.add_experimental_option('useAutomationExtension', False)

        # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

        # 设置代理Ip
        if self.ip:
            options.add_argument("--proxy-server=http://" + self.ip)

        prefs = {"": ""}
        # 屏蔽'保存密码'提示框
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False

        # 屏蔽css
        prefs['profile.default_content_setting_values'] = {'css': 2}

        options.add_experimental_option("prefs", prefs)

        # options.add_argument('--headless')  # 浏览器不提供可视化页面（无头模式）. linux下如果系统不支持可视化不加这条会启动失败

        # options.add_argument(
        #   'User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')

        return options

    def setHideWebdriver(self):
        """
        设置window.navigator.webdriver为undefined，防止被检测
        :return:
        """
        # 方法1
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => false
            })
          """
        })

        # 方法二
        # with open('./js/stealth.min.js') as f:
        #     js = f.read()
        #
        # self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })

    def exceptionHandling(self, defName, **kwargs):
        resdata = {}
        try:
            return defName(**kwargs)
        except TimeoutException:
            resdata['code'] = -1
            resdata['msg'] = "连接超时"
        except NoSuchElementException:
            resdata['code'] = -2
            resdata['msg'] = "未匹配到该DOM节点"
        except WebDriverException as e:
            if "ERR_PROXY_CONNECTION_FAILED" in str(e.msg):
                resdata['code'] = -3
                resdata['msg'] = "代理IP连接失败"
            else:
                resdata['code'] = -4
                resdata['msg'] = "webdriver驱动加载失败"
        except Exception:
            resdata['code'] = -5
            resdata['msg'] = "未知错误"
            traceback.print_exc()
        return resdata

    def __openUrl__(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        self.driver.get(kwargs['url'])
        WebDriverWait(self.driver, 5, 0.5).until(
            EC.text_to_be_present_in_element(('class name', kwargs['className']), kwargs['text']))
        return {
            'code': 0,
            'msg': "页面加载成功"
        }

    def openUrl(self, url, className, text):
        '''
        打开链接
        :param url:
        :return:
        '''
        return self.exceptionHandling(self.__openUrl__, url=url, className=className, text=text,err="打开网页")

    def setInputValue(self, **kwargs):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__waitFor__, **kwargs,err="输入框赋值")
    def waitFor_xpath(self, path):
        '''
            等待空间出现
            :return:
        '''
        return self.exceptionHandling(self.__waitFor__, findType='xpath', path=path,err="输入框赋值")

    def waitFor_css(self, path):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__setInputValue__, findType='css', path=path,err="等待DOM出现")


    def set_input_value_xpath(self, path, text):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__setInputValue__, findType='xpath', path=path, text=text,err="等待DOM出现")

    def set_input_value_css(self, path, text):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__setInputValue__, findType='css', path=path, text=text,err="等待DOM出现")

    def click_find_xpath(self, path):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__click__, findType='xpath', path=path,err="点击失败")

    def click_find_css(self, path):
        '''
        输入框中设置手机号
        :param phoneNum: 手机号
        :return:
        '''
        return self.exceptionHandling(self.__click__, findType='css', path=path,err="点击失败")

    def __setInputValue__(self, **kwargs):
        resdata = {}
        self.driver.implicitly_wait(10)
        if kwargs['findType'] == "xpath":
            doc = self.driver.find_element_by_xpath(kwargs['path'])
        else:
            doc = self.driver.find_element_by_css_selector(kwargs['path'])
        doc.send_keys(kwargs['text'])
        if kwargs['text'] == doc.get_attribute("value"):
            resdata['code'] = 0
            resdata['msg'] = "设置成功"
        else:
            resdata['code'] = 1
            resdata['msg'] = "设置失败"
        return resdata

    def __click__(self, **kwargs):
        self.driver.implicitly_wait(10)
        if kwargs['findType'] == "xpath":
            doc = self.driver.find_element_by_xpath(kwargs['path'])
        else:
            doc = self.driver.find_element_by_css_selector(kwargs['path'])
        doc.click()
        return {
            'code': 0,
            'msg': "点击完成"
        }
    def __waitFor__(self,**kwargs):
        self.driver.implicitly_wait(10)
        if kwargs['findType'] == "xpath":
            doc = self.driver.find_element_by_xpath(kwargs['path'])
        else:
            doc = self.driver.find_element_by_css_selector(kwargs['path'])
        return {
            'code': 0,
            'msg': "ok"
        }


    # def is_Load_the_success(self,image_doc):
    #     '''
    #        首选获取image标签元素:
    #
    #        WebElement image = driver.findElement(By.cssSelector("div#media_container > img"));
    #        boolean isVisible = this.IsImageVisible(driver, image);
    #
    #        然后判断:
    #
    #        private boolean IsImageVisible(WebDriver driver,WebElement image){
    #        Boolean imageLoaded1 = (Boolean) ((JavascriptExecutor)driver).executeScript("return arguments[0].complete && typeof arguments[0].naturalWidth != "undefined" && arguments[0].naturalWidth > 0", image);
    #        if (!imageLoaded1)
    #        {
    #        return false;
    #        }
    #        return true;
    #        }
    #
    #        complete 属性判断有没有加载完成,naturalWidth 判断该图片是否存在
    #
    #        '''
    #
    #
    #     isVisible = this.IsImageVisible(driver, image);

    def getCookies(self):
        # [{'domain': 'mall.qingxi.art', 'httpOnly': True, 'name': 'SESSION', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '018bcb3b-3404-491f-8658-1e3336af6be0'}]
        print(self.driver.get_cookies())

    def getLocalStorage(self):
        # print(self.driver.execute_script('localStorage.setItem("wwwPassLogout", "2");'))
        print(self.storage)

if __name__ == '__main__':
   pass
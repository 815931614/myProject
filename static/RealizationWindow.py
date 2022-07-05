# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QFileDialog
from InitUi import InitUi
import warnings
from MyThread import ThirdPartyLogin,ProxiesTest,ReadIdCard


# 接码平台
from 米云 import miyun
from 流星 import liuxing
from 椰子 import yezhi

# 打码平台
from 图鉴 import TuJian

# 代理平台
from 易代理 import YiDaiLi

from ProjectRunMain import ProjectRunMain
warnings.filterwarnings("ignore")
class RealizationWindow(InitUi):

    def __init__(self,mainWindow):
        super(RealizationWindow, self).__init__(mainWindow)

        #  身份证数据
        self.idCardList = []

        # 接码对象
        self.jieMaList = [liuxing(),  yezhi() , miyun()]

        # 打码对象
        self.daMaList = [TuJian()]

        # 代理对象
        self.daiLiList = [YiDaiLi()]

        # 代理链接
        self.proxiesUrl = ""

        self.proxiesTest = None

        self.thirdPartyLogin = None

        self.readIdCard = None


        self.projectRunMain = None
        mainWindow.event_impor_idCard = self.impor_idCard


        self.platform = {
            '接码平台': {
                'count' : self.jiema_comboBox.currentIndex(),
                self.jiema_comboBox.currentText() : {'username' : self.jiema_input_username.text().strip(),'password':self.jiema_input_passWord.text().strip()}
            },
            '打码平台': {
                'count' : self.dama_comboBox.currentIndex(),
                self.dama_comboBox.currentText() : {'username' : self.dama_input_username.text().strip(),'password':self.dama_input_passWord.text().strip()}
            },
            '代理平台' : {
                'count': self.daili_comboBox.currentIndex(),
                self.daili_comboBox.currentText():  self.daili_input_apiurl.text().strip()
            }
        }


        # 接码平台选择切换
        self.jiema_comboBox.currentIndexChanged.connect(self.jieMaPlatformChanged)

        # 打码平台选择切换
        self.dama_comboBox.currentIndexChanged.connect(self.daMaPlatformChanged)

        # 代理平台选择切换
        self.daili_comboBox.currentIndexChanged.connect(self.daiLiPlatformChanged)

    def daiLiPlatformChanged(self,index):
        infodict = self.fileOutPut.readInfo()
        self.platform['代理平台'][self.daili_comboBox.itemText(self.platform['代理平台']['count'])] = self.daili_input_apiurl.text().strip()

        if self.daili_comboBox.currentText() in self.platform['代理平台'].keys() and  self.platform['代理平台'][self.daili_comboBox.currentText()]:
            self.daili_input_apiurl.setText(self.platform['代理平台'][self.daili_comboBox.currentText()])
        elif self.daili_comboBox.currentText() in infodict['代理平台'].keys():
            self.daili_input_apiurl.setText(infodict['代理平台'][self.dama_comboBox.currentText()])
        else:
            self.daili_input_apiurl.setText("")
        self.platform['代理平台']['count'] = index
        number = self.daiLiList[index].number
        if number:
            self.daili_input_number.setText(str(number))
        else:
            self.daili_input_number.setText('')

    def daMaPlatformChanged(self,index):
        infodict = self.fileOutPut.readInfo()
        self.platform['打码平台'][self.dama_comboBox.itemText(self.platform['接码平台']['count'])] = {
            'username': self.dama_input_username.text().strip(),
            'password': self.dama_input_passWord.text().strip()
        }
        if self.dama_comboBox.currentText() in self.platform['打码平台'].keys() and (
                self.platform['打码平台'][self.dama_comboBox.currentText()]['username'] or
                self.platform['打码平台'][self.dama_comboBox.currentText()]['password']):
            self.dama_input_username.setText(self.platform['打码平台'][self.dama_comboBox.currentText()]['username'])
            self.dama_input_passWord.setText(self.platform['打码平台'][self.dama_comboBox.currentText()]['password'])

        elif self.dama_comboBox.currentText() in infodict['打码平台'].keys():
            self.dama_input_username.setText(infodict['打码平台'][self.dama_comboBox.currentText()]['username'])
            self.dama_input_passWord.setText(infodict['打码平台'][self.dama_comboBox.currentText()]['password'])
        else:
            self.dama_input_username.setText("")
            self.dama_input_passWord.setText("")
        self.platform['接码平台']['count'] = index
        money = self.daMaList[index].money
        if money:
            self.dama_input_money.setText(str(money))
        else:
            self.dama_input_money.setText('')

    def jieMaPlatformChanged(self,index):
        infodict = self.fileOutPut.readInfo()
        self.platform['接码平台'][self.jiema_comboBox.itemText(self.platform['接码平台']['count'])] = {
            'username': self.jiema_input_username.text().strip(),
            'password': self.jiema_input_passWord.text().strip()
        }
        if self.jiema_comboBox.currentText() in self.platform['接码平台'].keys() and (self.platform['接码平台'][self.jiema_comboBox.currentText()]['username'] or self.platform['接码平台'][self.jiema_comboBox.currentText()]['password']):
            self.jiema_input_username.setText(self.platform['接码平台'][self.jiema_comboBox.currentText()]['username'])
            self.jiema_input_passWord.setText(self.platform['接码平台'][self.jiema_comboBox.currentText()]['password'])

        elif self.jiema_comboBox.currentText() in infodict['接码平台'].keys():
            self.jiema_input_username.setText(infodict['接码平台'][self.jiema_comboBox.currentText()]['username'])
            self.jiema_input_passWord.setText(infodict['接码平台'][self.jiema_comboBox.currentText()]['password'])
        else:
            self.jiema_input_username.setText("")
            self.jiema_input_passWord.setText("")
        self.platform['接码平台']['count'] = index
        money = self.jieMaList[index].money
        if money:
            self.jiema_input_money.setText(str(money))
        else:
            self.jiema_input_money.setText('')


    def third_party_login(self, username, password, index,btn,type):
        '''
        登录
        :param index:
        :return:
        '''

        function = None
        if type == 0:
            function = self.jieMaList[index].login
        else:
            function = self.daMaList[index].login
        self.thirdPartyLogin = ThirdPartyLogin(function, username, password, btn)
        self.thirdPartyLogin.loginRes.connect(self.login_res)
        self.thirdPartyLogin.start()


    def login_res(self,res,btn):
        '''
         登录响应
         :param index:
         :return:
         '''
        if res['code'] == 0:
            self.addConsoleLine("登录成功,账号余额" + res['money'])
            if btn.objectName() == "jiema_login_btn":
                self.jiema_input_money.setText(res['money'])
            elif btn.objectName() == "dama_login_btn":
                self.dama_input_money.setText(res['money'])

            self.messageWindow("登录", "登录成功,账号余额" + res['money'])

        else:
            self.addConsoleLine("登录失败," + res['msg'])
            self.messageWindow("登录", "登录失败," + res['msg'])
        btn.setEnabled(True)


    def apiTest_click(self, index, urlText,btn):
        '''
        代理API测试按钮
        :param index:
        :return:
        '''
        url = urlText.strip()
        if not url:
            self.messageWindow("测试", "请输入链接！")
            return

        uparse = self.daiLiList[index].isUrl(url)
        if not uparse:
            self.messageWindow("测试", "链接格式错误！")
            return
        btn.setEnabled(False)
        self.proxiesTest = ProxiesTest(self.daiLiList[index].getProxies,btn)
        self.proxiesTest.testRes.connect(self.apiTest_res)
        self.proxiesTest.start()

        # self.proxiesUrl

    def apiTest_res(self,res,btn):
        message = ""
        if res['code'] == 0:

            self.daili_input_number.setText(str(res['number']))
            message = "测试成功,剩余：" + str(res['number']) + "个;"
        elif res['code'] == 999:
            message = "测试失败，连接失败！"
        else:
            message = res['msg']
        self.addConsoleLine(message)
        self.messageWindow("测试",message)
        btn.setEnabled(True)


    def startBtn_click(self,interfaceDataAll,btn ):
        '''
        开始按钮点击
        :return:
        '''

        if interfaceDataAll['线程数量'] < interfaceDataAll['注册数量']:
            threadNum = interfaceDataAll['注册数量']

        jiema_currentIndex = self.jieMaList[interfaceDataAll['接码平台'][0]]
        dama_currentIndex  = self.daMaList[ interfaceDataAll['打码平台'][0]]
        daili_currentIndex = self.daiLiList[interfaceDataAll['代理平台'][0]]

        msg = None
        if self.config.isJieMa and not jiema_currentIndex.token:
            msg = "当前选择的接码平台未登录！"
        elif self.config.isDaMa and not dama_currentIndex.money:
            msg = "当前选择的打码平台未登录！"
        elif self.config.isDaiLi == 1 and not daili_currentIndex.number:
            msg = "选择的代理IP未测试！"
        elif self.config.isCard and len(self.idCardList) == 0:
            msg = "实名信息未导入！"
        elif not interfaceDataAll['邀请码'] and not interfaceDataAll['项目ID']:
            msg = "请输入邀请码和接码项目ID！"
        elif not interfaceDataAll['邀请码'] :
            msg = "请输入邀请码！"
        elif not interfaceDataAll['项目ID']:
            msg = "请输入接码项目ID！"
        else:
            if not  daili_currentIndex.number:
                daili_currentIndex = None
            btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.clearConsol()
            if jiema_currentIndex:
                jiema_currentIndex.setOperator(interfaceDataAll['接码号段'])   # 设置号段类型
                jiema_currentIndex.project_id = interfaceDataAll['项目ID']  # 设置接码项目ID

            if int(interfaceDataAll['线程数量']) > int(interfaceDataAll['注册数量']):
                interfaceDataAll['线程数量'] = interfaceDataAll['注册数量']
            intervalTime = 1
            if int(interfaceDataAll['线程数量']) == 1:
                intervalTime = 0
            self.tabWidget.setCurrentIndex(0)
            data = {
                '项目名称' : self.config.projectName,

                '接码平台' : jiema_currentIndex,

                '打码平台' : dama_currentIndex,

                '代理平台' : daili_currentIndex,

                '项目ID' : interfaceDataAll['项目ID'],

                '账号密码' : interfaceDataAll['账号密码'],

                '是否随机账号密码' : interfaceDataAll['是否随机账号密码'],

                '交易密码' : interfaceDataAll['交易密码'],

                '是否随机交易密码' : interfaceDataAll['是否随机交易密码'],

                '邀请码' : interfaceDataAll['邀请码'],

                '注册数量' : int(interfaceDataAll['注册数量']),

                '线程数量' : int(interfaceDataAll['线程数量']),

                '间隔时间' : intervalTime,

                '实名数据' : self.idCardList,

                '开始按钮' : btn
            }
            self.projectRunMain = ProjectRunMain(data)
            self.projectRunMain._successNumPyqtSignal.connect(self.setSuccessNum)
            self.projectRunMain._consoleOutPyqtSignal.connect(self.addConsoleLine)
            self.projectRunMain._tablePyqtSignal.connect(self.updateTable)
            self.projectRunMain._btnPyqtSignal.connect(self.setBtnEnabled)
            self.projectRunMain.start()

        if msg:
            # self.addConsoleLine(msg,"Error")
            self.messageWindow(" ", msg)
    def setBtnEnabled(self,btn,b):
        btn.setEnabled(b)
        self.stop_btn.setEnabled(False)

    def stopBtn_click(self):
        """
        终止按钮点击
        :return:
        """
        # self.stopBtn.setEnabled(False)
        # self.startBtn.setEnabled(True)
        self.projectRunMain.stopThreadAll()
        print(f'终止按钮')

    def setSuccessNum(self,num):
        self.successedNum_input.setText(str(num))

    def impor_idCard_click(self, cb):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self.mainWindow, "选取文件", "",  # 起始路径
                                                                "Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔
        self.impor_idCard(fileName_choose)
    def impor_idCard(self,fileName_choose):
        if fileName_choose:


            if type(fileName_choose) == list:
                if not fileName_choose:
                    self.messageWindow("错误", "文件读取失败！")
                    return
                if len(fileName_choose) != 1:
                    self.messageWindow("错误", "请勿拖拽多个文件。")
                    return
                fileName_choose = fileName_choose[0]
            if fileName_choose.split('.')[-1] != 'txt':
                self.messageWindow("错误", "格式错误，只能读取.txt文件。")
                return

            if self.materia_input_btn.isChecked():
                self.materia_input_btn.setChecked(False)
            self.tableView_Init_Card.clearConsol()
            self.idCardList = []
            r = open(fileName_choose, encoding='utf-8', mode='r')
            readText = r.read().strip()
            if not readText:
                self.addConsoleLine("该文本内容为空！", "Error")
                return
            r.close()
            readTextSplit = readText.split('\n')
            if len(readTextSplit) > 10000:
                self.messageWindow("错误", "该文本内容超出限制，最多只可读取一万行数据！")
                self.addConsoleLine("该文本内容超出限制，最多只可读取一万行数据！", "Error")
                return
            self.materia_input_btn.setText("正在读取")
            self.materia_input_btn.setStyleSheet("")
            self.idCardList = []
            self.frame_3.setVisible(True)
            self.tabWidget.setCurrentIndex(1)

            self.readIdCard = ReadIdCard(readTextSplit)
            self.readIdCard._idCardRead.connect(self.setTableIdCard)
            self.readIdCard._setProgressBarNum.connect(self.setProgressBarNum)
            self.readIdCard.start()

    def setTableIdCard(self,data):
        for r in data['rlist']:
            self.tableView_Init_Card.addTable(r)
            if r[2] == "成功":
                self.idCardList.append(r[1].split('/'))
        self.frame_3.setVisible(False)
        if len(self.idCardList) != 0:
            self.materia_input_btn.setStyleSheet("background:#4FC442;")
            self.materia_input_btn.setText(f"读取完成,共{len(self.idCardList)}条")
        else:
            self.materia_input_btn.setText("重新导入")
        self.materia_input_btn.setChecked(True)
        self.addConsoleLine(f"读取完成，成功读取数量:{len(self.idCardList)},失败数量：{data['errorLine']}；")
        self.messageWindow(" ", f"读取完成，成功读取数量:{len(self.idCardList)},失败数量：{data['errorLine']}；")

    def setProgressBarNum(self,num):
        if num == 100:
            self.label_3.setText("读取完成，正在渲染表格。")
        self.progressBar.setProperty("value", num)
























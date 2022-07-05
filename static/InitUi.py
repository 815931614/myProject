from LDCNumber_TimeView import LDCNumber_TimeView
from TableView_Init import TableView_Init
from TableView_Init_Card import TableView_Init_Card
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect
from SetQTextEdit import SetQTextEdit
from PyQt5.QtWidgets import QMessageBox,QFrame,QLabel,QProgressBar
from UI_MainWindow import Ui_MainWindow
from FileOutPut import FileOutPut
from config import Config

class InitUi(Ui_MainWindow,LDCNumber_TimeView,TableView_Init,SetQTextEdit,TableView_Init_Card):


    def __init__(self,mainWindow):
        # super(InitUi, self).__init__()
        self.mainWindow = mainWindow
        Ui_MainWindow.__init__(self)



        # 启动UI
        self.setupUi(mainWindow)

        # 时间渲染
        LDCNumber_TimeView.__init__(self, mainWindow, self.currentTime_lcd)

        self.fileOutPut = FileOutPut()

        # 初始化注册显示表格
        TableView_Init.__init__(self, self.registrationData_table)

        # 初始化料子显示表格
        self.tableView_Init_Card = TableView_Init_Card(self.material_table)

        # 初始化日志显示框
        SetQTextEdit.__init__(self, self.console_textEdit)

        self.config = Config()

        # 设置默认值
        self.setWindowDefault()

        # 设置缓存数据
        self.set_Catch()

        # 注册按钮点击事件
        self.btn_clicked_connect()

        # 初始化料子加载动画
        self.setloadGif()
    def setloadGif(self):
        self.frame_3 = QFrame(self.tab_2)
        self.frame_3.setGeometry(QRect(0, 0, 821, 738))
        self.frame_3.setStyleSheet("background-color:#fff;")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setGeometry(QRect(300, 240, 261, 31))
        font = QFont()
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("正在读取")
        self.progressBar = QProgressBar(self.frame_3)
        self.progressBar.setGeometry(QRect(260, 290, 351, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.frame_3.setVisible(False)
    def setWindowDefault(self):
        """
        设置界面默认值
        :return:
        """
        # 设置窗口标题
        self.mainWindow.setWindowTitle(self.config.projectName)

        self.runSuccessNum_input.setValue(self.config.runSuccessNum_input)

        self.threadNum_input.setValue(self.config.threadNum_input)

        if not self.config.isJieMa:
            self.tabWidget_2.removeTab(0)
            # self.jiema_input_username.setEnabled(False)
            # self.jiema_input_username.setPlaceholderText("该项目不需要接码")
            # self.jiema_input_username.setStyleSheet("color:blck;")
            # self.jiema_input_passWord.setEnabled(False)
            # self.jiema_comboBox.setEnabled(False)
            # self.jiema_login_btn.setEnabled(False)
        if not self.config.isDaMa:
            self.tabWidget_2.removeTab( self.tabWidget_2.count() - 2)


            # self.dama_input_username.setEnabled(False)
            # self.dama_input_username.setPlaceholderText("该项目不需要打码")
            # self.dama_input_username.setStyleSheet("color:blck;")
            # self.dama_input_passWord.setEnabled(False)
            # self.dama_comboBox.setEnabled(False)
            # self.dama_login_btn.setEnabled(False)

        if self.config.isDaiLi == 2:
            self.tabWidget_2.removeTab(self.tabWidget_2.count() - 1)
            # self.daili_input_apiurl.setEnabled(False)
            # self.daili_input_apiurl.setPlaceholderText("该项目不需要代理")
            # self.daili_input_apiurl.setStyleSheet("color:blck;")
            # self.daili_comboBox.setEnabled(False)
            # self.daili_test_btn.setEnabled(False)


    def set_Catch(self):

        infodict = self.fileOutPut.readInfo()

        if self.config.isJieMa and self.jiema_comboBox.currentText() in infodict['接码平台'].keys():

            self.jiema_input_username.setText( infodict['接码平台'][self.jiema_comboBox.currentText()]['username'])
            self.jiema_input_passWord.setText( infodict['接码平台'][self.jiema_comboBox.currentText()]['password'])
        if self.config.isDaMa and self.dama_comboBox.currentText() in infodict['打码平台'].keys():
            self.dama_input_username.setText(infodict['打码平台'][self.dama_comboBox.currentText()]['username'])
            self.dama_input_passWord.setText(infodict['打码平台'][self.dama_comboBox.currentText()]['password'])
        if self.config.isDaiLi != 2 and self.daili_comboBox.currentText() in infodict['代理平台'].keys():
            self.daili_input_apiurl.setText(infodict['代理平台'][self.daili_comboBox.currentText()])



    def btn_clicked_connect(self):
        # 接码平台登录按钮点击
        self.jiema_login_btn.clicked.connect(lambda :self.login_clicked(self.jiema_comboBox.currentIndex(),self.jiema_input_username.text().strip(),self.jiema_input_passWord.text().strip(),self.jiema_login_btn,0))


        # 打码平台登录按钮点击
        self.dama_login_btn.clicked.connect(lambda :self.login_clicked(self.dama_comboBox.currentIndex(),self.dama_input_username.text().strip(), self.dama_input_passWord.text().strip(), self.dama_login_btn,1))

        # 代理平台测试按钮点击
        self.daili_test_btn.clicked.connect(lambda: self.apiTest_click(self.daili_comboBox.currentIndex(),self.daili_input_apiurl.text(),self.daili_test_btn))

        # 开始按钮
        self.start_btn.clicked.connect(self.startBtn_clicked)

        # 终止按钮
        self.stop_btn.clicked.connect(self.stopBtn_click)

        # 实名信息导入
        self.materia_input_btn.clicked.connect(lambda: self.impor_idCard_click(self.materia_input_btn))






    def login_clicked(self, index,username,password,btn,type):

        if not username and not password:
            self.messageWindow("登录", "请输入账号和密码！")
        elif not username:
            self.messageWindow("登录", "请输入账号！")
        elif not password:
            self.messageWindow("登录", "请输入密码！")
        else:
            btn.setEnabled(False)
            self.addConsoleLine("正在登录")
            self.third_party_login(username, password, index,btn,type)


    def third_party_login(self,username, password,index, btn,type):
        '''
        登录
        :param index:
        :return:
        '''
        pass



    def apiTest_click(self, index, urlText,btn):
        '''
        代理API测试按钮
        :param index:
        :return:
        '''
        pass


    def startBtn_clicked(self):

        '''
        开始按钮点击
        :return:
        '''



        self.startBtn_click(self.getInterfaceDataAll(),self.start_btn)




    def startBtn_click(self, interfaceDataAll,btn):
        '''
        开始按钮点击
        :return:
        '''
        pass




    def stopBtn_click(self):
        """
        终止按钮点击
        :return:
        """
        pass


    def impor_idCard_click(self, cb):
        if cb.isChecked():
            cb.setChecked(False)
        pass
    def messageWindow(self,title,text):
        QMessageBox.about(self.mainWindow, title, text)


    def getInterfaceDataAll(self):
        data = {
            '接码平台': [self.jiema_comboBox.currentIndex(),self.jiema_comboBox.currentText()],
            '接码账号' : self.jiema_input_username.text().strip(),
            '接码密码' : self.jiema_input_passWord.text().strip(),

            '打码平台': [self.dama_comboBox.currentIndex(), self.dama_comboBox.currentText()],
            '打码账号' : self.dama_input_username.text().strip(),
            '打码密码' : self.dama_input_username.text().strip(),

            '代理平台' : [self.daili_comboBox.currentIndex(), self.daili_comboBox.currentText()],
            '代理链接' : self.daili_input_apiurl.text().strip(),

            '项目ID'  : self.project_input.text().strip(),
            '接码号段' : self.operator_comboBox.currentIndex(),

            '账号密码' : self.passward_input.text().strip(),
            '是否随机账号密码' : self.isRandom_input_password.isChecked(),

            '交易密码' : self.payPassward_input.text().strip(),
            '是否随机交易密码' : self.isRandom_input_payPassword.isChecked(),

            '邀请码' : self.invitation_input.text().strip(),

            '注册数量' : self.runSuccessNum_input.text().strip(),
            '线程数量' : self.threadNum_input.text().strip()
        }
        return data
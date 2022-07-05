from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow,QPushButton
from PyQt5.QtCore import Qt

class Wondow(QMainWindow):
    def __init__(self):
       super(Wondow, self).__init__()
       self.event_impor_idCard = None
       self.setAcceptDrops(True)
       # self.setWindowFlags(Qt.WindowMinimizeButtonHint)
    def dragEnterEvent(self, event):
       if event.mimeData().hasUrls:
           event.accept()
       else:
           event.ignore()
    def dropEvent(self, event):
       try:
           if event.mimeData().hasUrls:
               event.setDropAction(Qt.CopyAction)
               event.accept()
               links = []
               for url in event.mimeData().urls():
                   links.append(str(url.toLocalFile()))

               if self.event_impor_idCard:
                   self.event_impor_idCard(links)
           else:
               event.ignore()
       except Exception as e:
           pass
    def closeEvent(self, event):
        # 创建一个消息盒子(提示框)

        quitMsgBox = QMessageBox(self)

        # 设置提示框的标题

        quitMsgBox.setWindowTitle('确认窗口')

        # 设置提示框的内容

        quitMsgBox.setText('你确定退出吗？')

        # 创建两个点击的按钮，修改文本显示内容

        buttonY = QPushButton('确定')

        buttonN = QPushButton('取消')

        # 将两个按钮加到这个消息盒子中去，并指定yes和no的功能

        quitMsgBox.addButton(buttonY, QMessageBox.YesRole)

        quitMsgBox.addButton(buttonN, QMessageBox.NoRole)

        quitMsgBox.exec_()

        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件

        if quitMsgBox.clickedButton() == buttonY:

            event.accept()
        else:
            event.ignore()

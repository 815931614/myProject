
from PyQt5.QtWidgets import QLCDNumber
import time
from PyQt5.QtCore import QTimer
class LDCNumber_TimeView:
    def __init__(self,MainWindow,lcd):
        self.lcd = lcd
        # self.lcd.setMinimumHeight(60)
        # 设置数字位数
        self.lcd.setDigitCount(20)
        # 设置数字显示模式, 十进制
        self.lcd.setMode(QLCDNumber.Dec)
        # 设置数字屏显示样式
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        # 设置外观样式
        self.lcd.setStyleSheet("border:0;color: blue;")



        timer = QTimer(MainWindow)
        timer.setInterval(100)
        timer.timeout.connect(self.onRefresh)
        timer.start()

    def onRefresh(self):
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        self.lcd.display(t)




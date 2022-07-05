# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from RealizationWindow import RealizationWindow
from MainWindow import Wondow
import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow =Wondow()
    ui = RealizationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

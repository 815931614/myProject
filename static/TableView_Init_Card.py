
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QBrush,QColor
from PyQt5.QtWidgets import QApplication, QAction,QHeaderView
from PyQt5.QtCore import Qt


class TableView_Init_Card:
    def __init__(self,tableView):
        self.tableView_Card = tableView
        self.set_TableView()
    def set_TableView(self):
        self.tableView_Card.setContextMenuPolicy(Qt.ActionsContextMenu)  # 右键菜单
        self.tableView_Card.setEditTriggers(self.tableView_Card.NoEditTriggers)  # 禁止编辑
        self.tableView_Card.addAction(QAction("复制", self.tableView_Card, triggered=self.copy))
        self.myModel_Card = QStandardItemModel(40, 3)  # model
        self.tableView_Card.setModel(self.myModel_Card)
        self.initHeader()  # 初始化表头
        # self.myModel_Card.col
        qs = QStandardItem("")
        qs.setTextAlignment(Qt.AlignCenter)
        self.myModel_Card.setItem(
            1, 1, qs)
        # self.myModel_Card.rowCount()
    def selected_tb_text(self):
        try:
            indexes = self.tableView_Card.selectedIndexes()  # 获取表格对象中被选中的数据索引列表
            indexes_dict = {}
            for index in indexes:  # 遍历每个单元格
                row, column = index.row(), index.column()  # 获取单元格的行号，列号
                if row in indexes_dict.keys():
                    indexes_dict[row].append(column)
                else:
                    indexes_dict[row] = [column]

            # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
            text = ''
            for row, columns in indexes_dict.items():
                row_data = ''
                for column in columns:
                    data = self.tableView_Card.model().item(row, column).text()
                    if row_data:
                        row_data = row_data + '\t' + data
                    else:
                        row_data = data

                if text:
                    text = text + '\n' + row_data
                else:
                    text = row_data
            return text
        except BaseException as e:
            return ''

    def clearConsol(self):
        self.myModel_Card = QStandardItemModel(100, 3)  # model
        self.tableView_Card.setModel(self.myModel_Card)
        self.initHeader()
    def addTable(self, d):

        qs = QStandardItem(d[0])
        qs.setTextAlignment(Qt.AlignCenter)

        qs2 = QStandardItem(d[1])
        qs2.setTextAlignment(Qt.AlignCenter)

        qs3 = QStandardItem(d[2])
        qs3.setTextAlignment(Qt.AlignCenter)

        if not d[1]:
            qs.setBackground(QBrush(QColor(255, 0, 0)))
            qs2.setBackground(QBrush(QColor(255, 0, 0)))
            qs3.setBackground(QBrush(QColor(255, 0, 0)))
        self.myModel_Card.setItem(
            d[3], 0, qs)
        self.myModel_Card.setItem(
            d[3], 1, qs2)
        self.myModel_Card.setItem(
            d[3], 2, qs3)

    def copy(self):
        text = self.selected_tb_text()  # 获取当前表格选中的数据
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # pyperclip.copy(text) # 复制数据到粘贴板
    def initHeader(self):

        self.myModel_Card.setHorizontalHeaderLabels([ "原数据", "姓名/身份证号", "校验状态"])
        self.tableView_Card.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableView_Card.setColumnWidth(0, 360)
        self.tableView_Card.setColumnWidth(1, 280)
        self.tableView_Card.setColumnWidth(2, 120)


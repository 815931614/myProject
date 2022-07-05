
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QAction,QHeaderView
from PyQt5.QtCore import Qt

class TableView_Init:
    def __init__(self,tableView):
        self.tableView = tableView
        self.set_TableView()
    def set_TableView(self):
        self.tableView.setContextMenuPolicy(Qt.ActionsContextMenu)  # 右键菜单
        self.tableView.setEditTriggers(self.tableView.NoEditTriggers)  # 禁止编辑
        self.tableView.addAction(QAction("复制", self.tableView, triggered=self.copy))
        self.myModel = QStandardItemModel(16, 3)  # model

        self.tableView.setModel(self.myModel)
        self.initHeader()  # 初始化表头

        # self.myModel.col
        qs = QStandardItem("23122223")
        qs.setTextAlignment(Qt.AlignCenter)
        self.myModel.setItem(
            1, 1, qs)
        # self.myModel.rowCount()
    def selected_tb_text(self):
        try:
            indexes = self.tableView.selectedIndexes()  # 获取表格对象中被选中的数据索引列表
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
                    data = self.tableView.model().item(row, column).text()
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


    def copy(self):
        text = self.selected_tb_text()  # 获取当前表格选中的数据
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # pyperclip.copy(text) # 复制数据到粘贴板

    def updateTable(self,d):
        mi = self.myModel.item(d['row'], d['col'])
        if d['col'] == 2 and mi:
            d['msg'] = mi.text() + "|" + d['msg']
        qs = QStandardItem(d['msg'])
        qs.setTextAlignment(Qt.AlignCenter)
        self.myModel.setItem(
            d['row'], d['col'], qs)

    def clearConsol(self):
        self.myModel = QStandardItemModel(100, 3)  # model
        self.tableView.setModel(self.myModel)
        self.initHeader()



    def initHeader(self):

        self.myModel.setHorizontalHeaderLabels(["账号","密码/支付密码", "状态"])
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.setColumnWidth(1, 180)
        self.tableView.setColumnWidth(2, 490)


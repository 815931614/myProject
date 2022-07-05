
import time
class SetQTextEdit:
    def __init__(self,textEdit):
        self.textEdit = textEdit

        # 禁止编辑
        self.textEdit.setReadOnly(True)
        '''
        
        获取光标所在行的行号

        QTextCursor tc = ui->textEdit->textCursor(); //当前光标
        int rowNum = tc.blockNumber() + 1;//获取光标所在行的行号
        '''

    def addConsoleLine(self,text,type=""):
        htmled = self.textEdit.toHtml()
        html = ""
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        if type == "Error":
            html = f"<div style='font-weight:600;font-size:13px;width:100%;'>{t}:<font style='font-weight:0;color:red;font-size:13px;'>{text}</font></div>"
        else:
            html = f"<div style='font-weight:600;font-size:13px;width:100%;'>{t}:<font style='font-weight:0;font-size:13px;'>{text}</font></div>"
        self.textEdit.setHtml(htmled  +  html)


    def consoleClearAll(self):
        self.textEdit.setHtml("")
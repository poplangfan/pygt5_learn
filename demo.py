from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from threading import Thread


class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        # self.ui = QUiLoader().load('main.ui')
        self.ui = QUiLoader().load(r'C:\Users\Administrator\Desktop\demo.ui')

        self.ui.setWindowTitle('mdc硬件测试')


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()

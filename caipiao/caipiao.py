"""
-*- coding: utf-8 -*-
@Author  : blyang
@project : PythonCode
@Time    : 2022/6/12 21:57
"""
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from threading import Thread

# 一些全局变量的设置
red_num = [x for x in range(1, 34)]
blue_num = [x for x in range(1, 17)]
counts = 0
select_one_flag = 0
str_one_list = []


# 06 11 14 20 27 30 09
def data_check_one(str_list):
    """
    判断一注的数据是不是符合规范
    :param str_list:
    :return:
    """
    if len(str_list) != 7:
        # 后期改为弹窗提醒
        print("输入格式不对")
    elif len(str_list) == 7:
        for index, str_ in enumerate(str_list):
            if index < 6:
                if int(str_) not in red_num:
                    print("红色数据数值不对")
            else:
                if int(str_) not in blue_num:
                    print("蓝色数据数值不对")


def data_check(str_):
    """
    校验所有的彩票数据是否符合规范，包括个数对但是大小不对的判断
    :return:
    """
    # 分几种情况，如果只有一注，判断长度，数值对不对，如果带 * 号的，要进行分割，如果是多注的，拆分后判断
    if "*" not in str_ and "," not in str_:
        str_list = str_.split(' ')
        # 单注判断封装为函数
        data_check_one(str_list)
    elif "*" in str_:
        global counts
        str_, counts = str_.split('*')
        str_list = str_.split(' ')
        data_check_one(str_list)
    elif "," in str_:
        global str_one_list
        str_one_list = str_.split(",")
        for str_one in str_one_list:
            str_list = str_one.split(' ')
            data_check_one(str_list)
    elif str_ == " ":
        pass


class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        # self.ui = QUiLoader().load('main.ui')
        self.ui = QUiLoader().load(r'./caipiao.ui')
        # 把所有lineEdit元素放入一个列表，方便操作
        self.lineEdit_buy = [self.ui.lineEdit_3, self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6,
                             self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_11, self.ui.lineEdit_12,
                             self.ui.lineEdit_13]
        self.lineEdit_result = [self.ui.lineEdit_3, self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6,
                                self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_11, self.ui.lineEdit_12,
                                self.ui.lineEdit_13, self.ui.lineEdit_9]

        # 绑定按钮和函数
        self.ui.pushButton.clicked.connect(self.start_run)  # 此处不能加()， 否则会直接执行

        self.ui.setWindowTitle('彩票模拟器')
        self.ui.statusbar.showMessage("相信科学，尊重概率。")

        # 调用才会生效
        self.page_init()

    def page_init(self):
        """
        初始化页面,有些参数只允许脚本修改，不允许用户修改
        :return:
        """
        # 将所有开奖结果设置为不可修改
        for lineEdit in self.lineEdit_result:
            lineEdit.setReadOnly(True)

    def judge_par(self):
        """
        参数获取判断，不符合规范需提示报错
        :return:
        """
        # 依次接收设置的数据
        # 目标号码
        lineEdit = self.ui.lineEdit.text()
        data_check(lineEdit)
        # 守护号码，可不写
        textEdit = self.ui.textEdit.toPlainText()
        if textEdit:
            # 如果自选号码只有一注
            if "*" not in textEdit and "," not in textEdit:
                global select_one_flag
                select_one_flag = 1
            data_check(textEdit)
        # 随机注数,可不写，不写所有金额用来购买守护号，写了则应大于0
        lineEdit_2 = self.ui.lineEdit_2.text()
        if lineEdit_2:
            # 如果此项写了，判断格式是否正确
            if int(lineEdit_2) <= 0:
                print("购买注数应大于0")

        # 花费金额,设置为不可更改，由计算得出
        sum_ = 0
        if lineEdit_2:
            if int(lineEdit_2) >= 0:
                sum_ += int(lineEdit_2) * 2
        if textEdit:
            global counts, str_one_list
            sum_ += int(counts) * 2
            sum_ += len(str_one_list) * 2
        sum_ += select_one_flag * 2

        self.ui.lineEdit_9.setText(str(sum_))

        pass

    def start_run(self):
        """
        对应开始模拟按钮，开始运行脚本
        :return:
        """
        global counts, str_one_list, select_one_flag
        counts = 0
        select_one_flag = 0
        str_one_list = []
        self.judge_par()
        pass

    def data_display(self):
        """
        数据的展示
        :return:
        """
        pass

    def stop_run(self):
        """
        中途停止运行脚本
        :return:
        """
        pass

    def check_result(self):
        """
        查看中奖记录，中奖记录保存在当前文件夹下的result.log
        :return:
        """
        pass


if __name__ == "__main__":
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()

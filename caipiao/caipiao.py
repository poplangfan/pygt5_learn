"""
-*- coding: utf-8 -*-
@Author  : blyang
@project : PythonCode
@Time    : 2022/6/12 21:57
"""
import random
import time
import logging
import os
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal

# 获取初始路径
gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
# if os.path.exists(os.path.join(gen_path, "result.txt")):
#     os.remove(os.path.join(gen_path, "result.txt"))

# 初始化日志存取路径
logging.basicConfig(filename=os.path.join(gen_path, "result.txt"), level=logging.INFO)

# 一些全局变量的设置
red_num = [x for x in range(1, 34)]
blue_num = [x for x in range(1, 17)]
counts = 0
select_one_flag = 0
str_one_list = []
buy_first = []
# 中奖号码
result_list = []
# 花费总金额
sum_ = 0
# 购买总注数
buy_num = 0
# 数据结果汇总字典
result_dict = {"一等奖": 0, "二等奖": 0, "三等奖": 0, "四等奖": 0, "五等奖": 0, "六等奖": 0,
               "购买注数": 0, "花费": 0, "盈利": 0}
money = {"一等奖": 5000000, "二等奖": 1000000, "三等奖": 3000, "四等奖": 200, "五等奖": 10, "六等奖": 5}


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


def buy_one():
    """
    购买一注彩票
    :return:
    """
    # 规则1-5, 完全随机购买
    list1 = [i for i in range(1, 34)]
    list2 = [i for i in range(1, 17)]
    red1 = random.randint(0, 32)
    red2 = random.randint(0, 31)
    red3 = random.randint(0, 30)
    red4 = random.randint(0, 29)
    red5 = random.randint(0, 28)
    red6 = random.randint(0, 27)
    blue = random.randint(0, 15)
    rule5 = [list1.pop(red1), list1.pop(red2), list1.pop(red3), list1.pop(red4),
             list1.pop(red5), list1.pop(red6)]
    rule5.sort()
    rule5.append(list2.pop(blue))
    return rule5


# 判断是否中奖
def judge_lottery(list1, list2):
    """
    传入两组数据，一组中奖号码，一组自己买的号码，判断是否中奖
    :list1: 中奖号码
    :list2: 自己购买的号码
    :return:
    """
    count = 0
    for i in range(6):
        if list2[i] in list1[0:6]:
            count += 1
    if len(list1) == 7 and len(list2) == 7:
        if count == 6 and list1[-1] == list2[-1]:  # 6+1
            return '一等奖'
        elif count == 6:  # 6
            return '二等奖'
        elif count == 5 and list1[-1] == list2[-1]:  # 5+1
            return '三等奖'
        elif count == 5 or (count == 4 and list1[-1] == list2[-1]):  # 5 4+1
            return '四等奖'
        elif count == 4 or (count == 3 and list1[-1] == list2[-1]):  # 4 3+1
            return '五等奖'
        elif list1[-1] == list2[-1]:  # 1
            return '六等奖'
        else:
            return '没有中奖'
    else:
        return '格式错误'


def buy_and_judge(flag=0):
    """
    购买和判断是否中奖
    :return:
    """
    if flag:
        buy_list = buy_first
        print(f"购买彩票：{buy_first}")
    else:
        buy_list = buy_one()
        print(f"购买彩票：{buy_list}")
    rst = judge_lottery(result_list, buy_list)
    if rst == "一等奖":
        logging.info(f"中一等奖:{buy_list}")
        result_dict["一等奖"] += 1
    elif rst == "二等奖":
        logging.info(f"中二等奖:{buy_list}")
        result_dict["二等奖"] += 1
    elif rst == "三等奖":
        logging.info(f"中三等奖:{buy_list}")
        result_dict["三等奖"] += 1
    elif rst == "四等奖":
        logging.info(f"中四等奖:{buy_list}")
        result_dict["四等奖"] += 1
    elif rst == "五等奖":
        logging.info(f"中五等奖:{buy_list}")
        result_dict["五等奖"] += 1
    elif rst == "六等奖":
        logging.info(f"中六等奖:{buy_list}")
        result_dict["六等奖"] += 1
    else:
        pass
    result_dict["购买注数"] += 1
    result_dict["花费"] += 2
    result_dict["盈利"] += money.get(rst, 0)
    result_dict["盈利"] -= 2


# 继承QObject类
class NewThread(QThread):
    # 自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = Signal(str)

    # 带一个参数t
    def __init__(self, parent=None):
        super(NewThread, self).__init__(parent)

    # run函数是子线程中的操作，线程启动后开始执行
    # 当前一个线程，下个阶段开多线程，并行操作
    def run(self):
        while buy_num > 0:
            time.sleep(0.05)
            # 发射自定义信号
            # 通过emit函数将参数i传递给主线程，触发自定义信号
            self.finishSignal.emit(str(buy_num))  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        # self.ui = QUiLoader().load('main.ui')
        self.ui = QUiLoader().load(r'./caipiao.ui')
        # 守护号码
        self.buy_first_list = []
        # 把所有lineEdit元素放入一个列表，方便操作
        self.lineEdit_buy = [self.ui.lineEdit_3, self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6,
                             self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_11, self.ui.lineEdit_12,
                             self.ui.lineEdit_13]
        self.lineEdit_result = [self.ui.lineEdit_3, self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6,
                                self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_11, self.ui.lineEdit_12,
                                self.ui.lineEdit_13, self.ui.lineEdit_9]

        # 目标中奖号码
        self.lineEdit = self.ui.lineEdit.text()
        # 绑定按钮和函数
        self.ui.pushButton.clicked.connect(self.start_run)  # 此处不能加()， 否则会直接执行
        self.ui.pushButton_2.clicked.connect(self.check_result)  # 此处不能加()， 否则会直接执行
        self.ui.pushButton_3.clicked.connect(self.stop_run)  # 此处不能加()， 否则会直接执行

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
        global result_list, result_dict
        result_list = [int(x) for x in lineEdit.split(" ")]
        # 守护号码，可不写
        textEdit = self.ui.textEdit.toPlainText()
        if textEdit:
            # 如果自选号码只有一注
            if "*" not in textEdit and "," not in textEdit:
                global select_one_flag
                select_one_flag = 1
                data_check(textEdit)
                self.buy_first_list = textEdit.split(" ")
                self.buy_first_list = [int(x) for x in self.buy_first_list]
                # 暂不实现多个自选
            # elif "," in textEdit:
            #     buy_list = textEdit.split(",")
            #     print(buy_list)

        # 随机注数,可不写，不写所有金额用来购买守护号，写了则应大于0
        lineEdit_2 = self.ui.lineEdit_2.text()
        global buy_num
        buy_num = int(lineEdit_2)
        result_dict["number"] = int(lineEdit_2)
        if lineEdit_2:
            # 如果此项写了，判断格式是否正确
            if int(lineEdit_2) <= 0:
                print("购买注数应大于0")

        # 花费金额,设置为不可更改，由计算得出
        global sum_
        if lineEdit_2:
            if int(lineEdit_2) >= 0:
                sum_ += int(lineEdit_2) * 2
        if textEdit:
            global counts, str_one_list
            sum_ += int(counts) * 2
            sum_ += len(str_one_list) * 2
        sum_ += select_one_flag * 2

        self.ui.lineEdit_9.setText(str(sum_))
        return self.buy_first_list

    def start_run(self):
        """
        对应开始模拟按钮，开始运行脚本
        :return:
        """
        global counts, str_one_list, select_one_flag
        counts = 0
        select_one_flag = 0
        str_one_list = []
        global buy_first
        buy_first = self.judge_par()
        # 先购买自选号码
        if buy_first:
            buy_and_judge(1)
        # 开启一个线程，购买彩票，判断是否中奖，记录中奖结果，返回中奖信息给界面
        self.thread1 = NewThread()  # 实例化一个线程
        self.thread2 = NewThread()  # 实例化一个线程
        self.thread3 = NewThread()  # 实例化一个线程
        self.thread4 = NewThread()  # 实例化一个线程
        self.thread5 = NewThread()  # 实例化一个线程
        # 开启一个线程，购买彩票，判断是否中奖，记录中奖结果，返回中奖信息给界面
        self.thread6 = NewThread()  # 实例化一个线程
        self.thread7 = NewThread()  # 实例化一个线程
        self.thread8 = NewThread()  # 实例化一个线程
        self.thread9 = NewThread()  # 实例化一个线程
        self.thread10 = NewThread()  # 实例化一个线程
        # 将线程thread的信号finishSignal和UI主线程中的槽函数data_display进行连接
        self.thread1.finishSignal.connect(self.data_display)
        self.thread2.finishSignal.connect(self.data_display)
        self.thread3.finishSignal.connect(self.data_display)
        self.thread4.finishSignal.connect(self.data_display)
        self.thread5.finishSignal.connect(self.data_display)
        self.thread6.finishSignal.connect(self.data_display)
        self.thread7.finishSignal.connect(self.data_display)
        self.thread8.finishSignal.connect(self.data_display)
        self.thread9.finishSignal.connect(self.data_display)
        self.thread10.finishSignal.connect(self.data_display)
        # 启动线程，执行线程类中run函数
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()
        self.thread5.start()
        self.thread6.start()
        self.thread7.start()
        self.thread8.start()
        self.thread9.start()
        self.thread10.start()

    def data_display(self, str_):
        """
        数据的展示
        :return:
        """
        # 先买守护号，守护号买完了再随机买
        global buy_num
        buy_num -= 1
        if buy_num >= 0:
            buy_and_judge()
            self.ui.lineEdit_11.setText(str(result_dict["购买注数"]))
            self.ui.lineEdit_12.setText(str(result_dict["花费"]))
            self.ui.lineEdit_13.setText(str(result_dict["盈利"]))
            self.ui.lineEdit_3.setText(str(result_dict["一等奖"]))
            self.ui.lineEdit_4.setText(str(result_dict["二等奖"]))
            self.ui.lineEdit_5.setText(str(result_dict["三等奖"]))
            self.ui.lineEdit_6.setText(str(result_dict["四等奖"]))
            self.ui.lineEdit_7.setText(str(result_dict["五等奖"]))
            self.ui.lineEdit_8.setText(str(result_dict["六等奖"]))
        else:
            pass

    def stop_run(self):
        """
        中途停止运行脚本,暂未实现，弹窗提醒
        :return:
        """
        QMessageBox.information(self.ui, "标题", "此功能暂未实现，可直接点击右上角退出软件")

    def check_result(self):
        """
        查看中奖记录，中奖记录保存在当前文件夹下的result.log
        :return:
        """
        folder = os.path.join(gen_path, "result.txt")
        # 方法1：通过start explorer
        os.system("start explorer %s" % folder)
        # 方法2：通过startfile
        # os.startfile(folder)


if __name__ == "__main__":
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()

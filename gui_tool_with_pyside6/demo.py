# import psutil
#
#
# # cpu信息
# def get_cpu_info():
#     cpu_percent = psutil.cpu_percent(interval=1)
#     cpu_info = "CPU使用率：%i%%" % cpu_percent
#     print(cpu_info)
#     # return cpu_info
#
#
# # 内存信息
# def get_memory_info():
#     virtual_memory = psutil.virtual_memory()
#     used_memory = virtual_memory.used / 1024 / 1024 / 1024
#     free_memory = virtual_memory.free / 1024 / 1024 / 1024
#     memory_percent = virtual_memory.percent
#     memory_info = "内存使用：%0.2fG，使用率%0.1f%%，剩余内存：%0.2fG" % (used_memory, memory_percent, free_memory)
#     print(memory_info)
#     # return memory_info
#
#
# get_cpu_info()
# get_memory_info()

import sys
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QChart, QChartView, QLineSeries


class TestChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.series = QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)
        self.series.append(QPointF(11, 1))
        self.series.append(QPointF(13, 3))
        self.series.append(QPointF(17, 6))
        self.series.append(QPointF(18, 3))
        self.series.append(QPointF(20, 2))

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Simple line chart example")

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())
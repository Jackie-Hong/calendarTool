import sys
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QTextEdit, QPushButton

from dbMsg import dbMsg


class CalendarApp(QWidget):
    def __init__(self):
        super(CalendarApp, self).__init__()

        self.initUI()

        self.db = dbMsg()

        # 刷新展示所有日程的文本框
        self.showAllSchedules()
    def initUI(self):
        self.setWindowTitle('Calendar and Scheduler')
        self.setGeometry(100, 100, 1200, 1400)

        # 创建日历部件
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.showSchedule)


        # 创建文本编辑部件用于显示和编辑日程
        self.schedule_edit = QTextEdit(self)

        # 创建保存按钮
        self.save_button = QPushButton('Save Schedule', self)
        self.save_button.clicked.connect(self.saveSchedule)

        # 创建展示所有日程的文本框
        self.all_schedules_display = QTextEdit(self)
        self.all_schedules_display.setReadOnly(True)

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.schedule_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.all_schedules_display)

    def showSchedule(self, date):
        # 在这里可以添加具体的日程查询和显示逻辑
        # 在这个简单的例子中，我们将日期和已有的日程显示在文本编辑框中
        schedule_texts = self.loadSchedule(date)
        if schedule_texts:
            for text in schedule_texts[0]:
                self.schedule_edit.setPlainText(text)
        else:
            self.schedule_edit.setPlainText("")

        # 刷新展示所有日程的文本框
        self.showAllSchedules()

    def loadSchedule(self, date):
        # 在这里可以添加从文件或其他数据源加载日程的逻辑
        # 在这个简单的例子中，我们从文件中加载日程

        return self.db.get_data(date)
        # try:
        #     with open(self.getFileName(date), "r") as file:
        #         return file.read()
        # except FileNotFoundError:
        #     return ""


    def saveSchedule(self):
        # 获取当前选中日期
        selected_date = self.calendar.selectedDate()

        # 获取文本编辑框中的日程
        schedule_text = self.schedule_edit.toPlainText()

        # 保存日程到文件
        # filename = self.getFileName(selected_date)
        # with open(filename, "w") as file:
        #     file.write(schedule_text)
        if schedule_text == "":
            self.db.delete_data(selected_date)
        else:
            if self.db.get_data(selected_date):
                self.db.update_date(selected_date, schedule_text)
            else:
                self.db.insert_data(selected_date, schedule_text)

        # 刷新展示所有日程的文本框
        self.showAllSchedules()

    def showAllSchedules(self):
        # 获取当前选中月份的所有日期
        current_month = self.calendar.monthShown()
        current_year = self.calendar.yearShown()

        start_date = QDate(current_year, current_month, 1)
        end_date = start_date.addMonths(1).addDays(-1)

        # 逐天加载日程并展示
        all_schedules = ""
        current_date = start_date
        while current_date <= end_date:
            schedule_text = self.loadSchedule(current_date)
            if schedule_text:
                for text in schedule_text[0]:
                    all_schedules += "{}:\n{}\n\n".format(current_date.toString(Qt.ISODate), text)
            current_date = current_date.addDays(1)

        self.all_schedules_display.setPlainText(all_schedules)

    # def getFileName(self, date):
    #     # 生成以日期为名的文件名
    #     return date.toString(Qt.ISODate) + ".txt"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalendarApp()
    ex.show()
    sys.exit(app.exec_())

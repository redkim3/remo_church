import os
from PyQt5.QtCore import * # QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic

today = QDate.currentDate()
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/Quarter_report_start.ui")[0]

class Ge_quarterly_Report(QDialog, QWidget, form_class) : #QDialog
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        global b_year
        self.setWindowTitle("분기재정보고")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))        
        b_year = today.year()

        Quarterly_income_report_window = QPushButton("결산재정보고-수입내역")
        Quarterly_income_report_window.clicked.connect(self.Quarterly_income_report)
        Quarterly_cost_report_Button = QPushButton("결산재정보고-지출내역")
        Quarterly_cost_report_Button.clicked.connect(self.Quarterly_cost_report)
 
    def Quarterly_income_report(self):
        from report.income_report_window_numpy import Ge_quarterly_income_Report
        self.hide() # 메인 윈도우 숨김
        self.income_report = Ge_quarterly_income_Report()
        self.income_report.show() # exec()
        
        # self.show()

    def Quarterly_cost_report(self):
        # from report.cost_report_window import Ge_quarterly_cost_Report
        from report.cost_report_window import Ge_quarterly_cost_Report # 수정중
        self.hide() # 메인 윈도우 숨김 
        self.cost_report = Ge_quarterly_cost_Report()
        self.cost_report.show() # 현재 비모달창으로 열고 있는데 모달 창으로 하려면 show() 대신에 exec() 로 한다.
        # 모달 창으로 하면 다른창을 열 수가 없다.
        
        # self.show()
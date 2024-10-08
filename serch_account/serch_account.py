import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic, QtWidgets # QtCore, QtGui 
from PyQt5.QtCore import QRect
from PyQt5 import QtGui
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPainter, QFontMetrics
from basic.cost_select import *
from datetime import datetime
import configparser, hashlib

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()

form_class = uic.loadUiType(r"./ui/serch_account_form.ui")[0]

class serch_account(QtWidgets.QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("지출 계정별 검색")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        view_year = str(today.year())
        start_month = str(1)
        start_day = str(1)
        view_month = str(today.month())
        view_day = str(today.day())
        self.serch_year_widget.setText(view_year)
        # 수정된 부분
        self.start_month_combo.currentIndexChanged.connect(lambda: self.update_days("start"))
        self.start_month_combo.setCurrentIndex(-1)  # 존재하지 않는 인덱스로 설정
        self.start_month_combo.setCurrentText(start_month)
        self.end_month_combo.currentIndexChanged.connect(lambda: self.update_days("end"))
        self.serch_year_widget.editingFinished.connect(lambda: self.update_days("end"))
        
        self.start_day_combo.setCurrentText(start_day)
        self.end_month_combo.setCurrentText(view_month)
        self.end_day_combo.setCurrentText(view_day)
 
        self.load_gubun_combo()
        self.gubun_combo_widget.currentTextChanged.connect(self.load_hang_combo)
        self.hang_combo_widget.currentTextChanged.connect(self.load_mok_combo)
        self.mok_combo_widget.currentTextChanged.connect(self.load_semok_combo)
        self.result_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정
        
        self.mok_combo_items = {}
        self.semok_combo_items = {}

    def update_days(self, s_end):
        year = int(self.serch_year_widget.text())
        if s_end == "start":
            self.start_day_combo.clear()
            try:
                month = int(self.start_month_combo.currentText())
                days_in_month = QDate(year, month, 1).daysInMonth()
                self.start_day_combo.addItems([str(day) for day in range(1, days_in_month + 1)])
            except ValueError:
                pass  # 년도와 월이 유효하지 않을 경우 예외 처리
        else:
            self.end_day_combo.clear()
            try:
                month = int(self.end_month_combo.currentText())
                days_in_month = QDate(year, month, 1).daysInMonth()
                self.end_day_combo.addItems([str(day) for day in range(1, days_in_month + 1)])
                current_year = str(today.year())
                if int(year) < int(current_year):
                    self.end_month_combo.setCurrentText("12")
                    self.end_day_combo.setCurrentText("31")
            except ValueError:
                pass  # 년도와 월이 유효하지 않을 경우 예외 처리

    def load_gubun_combo(self):
        from basic.hun_name_2 import gubun_values_check
        confirm_data = self.user_confirm()
        Ge_check = int(confirm_data[1]) # 일반회계
        # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.

        self.hap_widget.clear()
        self.gubun_combo_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        self.gubun_combo_widget.clear()
        self.gubun_combo_widget.addItems(["선택"] + gubun_values_check(Ge_check))
        gubun = self.gubun_combo_widget.currentText()

    def load_hang_combo(self):
        from basic.cost_select import cost_hang_values
        self.hang_combo_items = {}
        self.hap_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        v_year = int(self.serch_year_widget.text())
        
        gubun = self.gubun_combo_widget.currentText()
        hang_s = cost_hang_values(v_year, gubun)
        hang_list = []
        for h in hang_s:
            hang, id = h
            hang_list.append(hang)
        if v_year not in self.hang_combo_items:
            hang_s = cost_hang_values(v_year, gubun)
            self.hang_combo_items[gubun] = ["선택"] + hang_list
            # self.hang_combo_items[gubun] = ["선택"] + list(cost_hang_values(v_year, gubun))
        self.hang_combo_widget.addItems(self.hang_combo_items[gubun])

    def load_mok_combo(self):
        from basic.cost_select import cost_mok_values
        self.hap_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        v_year = int(self.serch_year_widget.text())
  
        hang = self.hang_combo_widget.currentText()
        mok_s = cost_mok_values(v_year, hang)
        mok_list = []
        for mo in mok_s:
            mok, id = mo
            if mok != "보통예금":
                mok_list.append(mok)
        if hang not in self.mok_combo_items:
            self.mok_combo_items[hang] = ["선택"] + mok_list #list(cost_mok_values(v_year, hang))  # dictionary로 변경
        self.mok_combo_widget.addItems(self.mok_combo_items[hang])

    def load_semok_combo(self):
        from basic.cost_select import cost_semok_values
        self.hap_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        v_year = int(self.serch_year_widget.text())

        semok_list = []
        mok = self.mok_combo_widget.currentText()
        semok_s = cost_semok_values(v_year, mok)
        # cost_semok_values_list = []
        for se in semok_s:
            semok, id_se = se
            semok_list.append(semok)
        if mok not in self.semok_combo_items:
            self.semok_combo_items[mok] = ["선택"] + semok_list #list(cost_semok_values(v_year, mok))  # dictionary로 변경
        self.semok_combo_widget.addItems(self.semok_combo_items[mok])

    def serch_account_home(self):
        gubun = self.gubun_combo_widget.currentText()

        if gubun != '특별회계':
            self.serch_account_except_special(gubun)
        else:
            self.serch_account_special(gubun)

    def serch_account_except_special(self,gubun):
        from basic.cost_serch import serch_hang, serch_mok, serch_semok
        from basic.cost_serch import serch_hang_pre_date, serch_mok_pre_date, serch_semok_pre_date
        hap_total_1 = 0; hap_total_2 = 0; hap_total = 0
        cost_pre_amo = 0; c_jan_int = 0
        # 글꼴 설정
        # font = QtGui.QFont()
        # font.setPointSize(12)  # 글자 크기 설정
        # self.result_tableWidget.setFont(font)

        # 헤더 글꼴 설정
        header_font = QtGui.QFont()
        header_font.setPointSize(11) 
        self.result_tableWidget.horizontalHeader().setFont(header_font)

        self.result_tableWidget.clear()
        hang = self.hang_combo_widget.currentText()
        mok = self.mok_combo_widget.currentText()
        semok = self.semok_combo_widget.currentText()
        s_year = self.serch_year_widget.text()
        s_start_month = self.start_month_combo.currentText()
        s_start_day = self.start_day_combo.currentText()
        s_end_month = self.end_month_combo.currentText()
        s_end_day = self.end_day_combo.currentText()
        start_date = s_year + '-' + s_start_month + '-' + s_start_day
        end_date = s_year + '-' + s_end_month + '-' + s_end_day
    
        if hang != "선택" and mok != "선택" and  semok != "선택":  # 세목까지 선택하고 검색
            serch_semok_value = serch_semok(start_date, end_date, gubun, hang, mok, semok)
            self.result_tableWidget.setColumnCount(8)
            add_row = 0; c_jan_int = 0
            serch_semok_pre_date_value = serch_semok_pre_date(start_date, s_year, hang, mok, semok)
            
            for j1, passover_semok in enumerate(serch_semok_pre_date_value): # 전기이월 만들기
                cost_pre_amo += passover_semok[2] 

            hap_total_1 += cost_pre_amo
            c_jan = format(hap_total_1,",")

            if c_jan != '0':
                self.result_tableWidget.setRowCount(len(serch_semok_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_semok_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if c_jan != '0':
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 4, QTableWidgetItem(c_jan))
                if self.result_tableWidget.item(0, 4) != None:
                    self.result_tableWidget.item(0, 4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                add_row = 1

            for j, semok_data in enumerate(serch_semok_value):
                amo_int_1 = 0; amo_int_2 =0; amo_1 = ""; amo_2 = ""
                vdate = semok_data[0].strftime('%Y-%m-%d')
                cost_memo1 = semok_data[1]
                amo_int_1 = int(semok_data[2])
                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0
                    # amo_int_1 = int(semok_data[2])
                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                c_jan_int = hap_total_1 - hap_total_2
                c_jan = format(c_jan_int,",")
                payed_bank =  semok_data[3]
                semok_marks = semok_data[4]
                if len(semok_data) > 4:
                    id = str(semok_data[5])

                self.result_tableWidget.setItem(j + add_row, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + add_row, 1, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + add_row, 2, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + add_row, 3, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + add_row, 4, QTableWidgetItem(c_jan))
                self.result_tableWidget.setItem(j + add_row, 5, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + add_row, 6, QTableWidgetItem(semok_marks))
                self.result_tableWidget.setItem(j + add_row, 7, QTableWidgetItem(id))

                if self.result_tableWidget.item(j + add_row,0) != None:
                    self.result_tableWidget.item(j + add_row,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.result_tableWidget.item(j + add_row,1) != None:
                    self.result_tableWidget.item(j + add_row,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,2) != None:
                    self.result_tableWidget.item(j + add_row,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,3) != None:
                    self.result_tableWidget.item(j + add_row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,4) != None:
                    self.result_tableWidget.item(j + add_row,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,5) != None:
                    self.result_tableWidget.item(j + add_row,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,6) != None:
                    self.result_tableWidget.item(j + add_row,6).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(7, True)

        elif hang != "선택" and mok != "선택" and  semok == '선택':  # 목 까지 선택하고 검색
            serch_mok_value = serch_mok(start_date, end_date, gubun, hang, mok)
            serch_mok_pre_date_value = serch_mok_pre_date(start_date, s_year, hang, mok)
            self.result_tableWidget.setColumnCount(9)
            add_row = 0; c_jan_int = 0
            
            for j1, passover_semok in enumerate(serch_mok_pre_date_value): # 전기이월 만들기
                cost_pre_amo += passover_semok[3] 

            hap_total_1 += cost_pre_amo
            c_jan = format(hap_total_1,",")
            
            if c_jan != '0':
                self.result_tableWidget.setRowCount(len(serch_mok_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_mok_value))
            
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "세목", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if c_jan != '0':
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 5, QTableWidgetItem(c_jan))
                if self.result_tableWidget.item(0, 5) != None:
                    self.result_tableWidget.item(0, 5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                add_row = 1

            for j, mok_data in enumerate(serch_mok_value):
                amo_int_1 = 0; amo_int_2 =0; amo_1 = ""; amo_2 = ""
                vdate = mok_data[0].strftime('%Y-%m-%d')
                cost_semok = mok_data[1]
                cost_memo1 = mok_data[2]
                amo_int_1 = int(mok_data[3])
                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0

                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                c_jan_int = hap_total_1 - hap_total_2
                c_jan = format(c_jan_int,",")
                payed_bank = mok_data[4]
                mok_marks = mok_data[5] # if mok_data[5] != 'nan' else ''
                if len(mok_data) > 6:
                    id = str(mok_data[6])

                self.result_tableWidget.setItem(j + add_row, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + add_row, 1, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j + add_row, 2, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + add_row, 3, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + add_row, 4, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + add_row, 5, QTableWidgetItem(c_jan))
                self.result_tableWidget.setItem(j + add_row, 6, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + add_row, 7, QTableWidgetItem(mok_marks))
                self.result_tableWidget.setItem(j + add_row, 8, QTableWidgetItem(id))
                if self.result_tableWidget.item(j + add_row,0) != None:
                    self.result_tableWidget.item(j + add_row,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.result_tableWidget.item(j + add_row,1) != None:
                    self.result_tableWidget.item(j + add_row,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,2) != None:
                    self.result_tableWidget.item(j + add_row,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,3) != None:
                    self.result_tableWidget.item(j + add_row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,4) != None:
                    self.result_tableWidget.item(j + add_row,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,5) != None:
                    self.result_tableWidget.item(j + add_row,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,6) != None:
                    self.result_tableWidget.item(j + add_row,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,7) != None:
                    self.result_tableWidget.item(j + add_row,7).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(8, True)

        elif hang != '선택' and mok == '선택' and semok == '선택':
            serch_hang_value = serch_hang(start_date, end_date, gubun, hang)
            serch_hang_pre_date_value = serch_hang_pre_date(start_date, s_year, hang)
            self.result_tableWidget.setColumnCount(10)
            
            add_row = 0; c_jan_int = 0
            for j1, passover_semok in enumerate(serch_hang_pre_date_value): # 전기이월 만들기
                cost_pre_amo += passover_semok[4] 
                    
            hap_total_1 += cost_pre_amo
            c_jan = format(hap_total_1,",")

            if c_jan != '0':
                self.result_tableWidget.setRowCount(len(serch_hang_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_hang_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "목", "세목", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if c_jan != '0':
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 6, QTableWidgetItem(c_jan))
                if self.result_tableWidget.item(0, 6) != None:
                    self.result_tableWidget.item(0, 6).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                add_row = 1
            
            for j, hang_data in enumerate(serch_hang_value):
                amo_int_1 = 0; amo_int_2 =0
                vdate = hang_data[0].strftime('%Y-%m-%d')
                cost_mok = hang_data[1]
                cost_semok = hang_data[2]
                cost_memo1 = hang_data[3]
                amo_int_1 = int(hang_data[4])
                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0
                        
                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                c_jan_int = hap_total_1 - hap_total_2
                c_jan = format(c_jan_int,",")
                payed_bank = hang_data[5]
                hang_marks = hang_data[6] # if hang_data[6] != 'nan' else ''
                if len(hang_data) > 7:
                    id = str(hang_data[7])
                
                self.result_tableWidget.setItem(j + add_row, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + add_row, 1, QTableWidgetItem(cost_mok))
                self.result_tableWidget.setItem(j + add_row, 2, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j + add_row, 3, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + add_row, 4, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + add_row, 5, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + add_row, 6, QTableWidgetItem(c_jan))
                self.result_tableWidget.setItem(j + add_row, 7, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + add_row, 8, QTableWidgetItem(hang_marks))
                self.result_tableWidget.setItem(j + add_row, 9, QTableWidgetItem(id))
                
                if self.result_tableWidget.item(j + add_row,0) != None:
                    self.result_tableWidget.item(j + add_row,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.result_tableWidget.item(j + add_row,1) != None:
                    self.result_tableWidget.item(j + add_row,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,2) != None:
                    self.result_tableWidget.item(j + add_row,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,3) != None:
                    self.result_tableWidget.item(j + add_row,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,4) != None:
                    self.result_tableWidget.item(j + add_row,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,5) != None:
                    self.result_tableWidget.item(j + add_row,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,6) != None:
                    self.result_tableWidget.item(j + add_row,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + add_row,7) != None:
                    self.result_tableWidget.item(j + add_row,7).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + add_row,8) != None:
                    self.result_tableWidget.item(j + add_row,8).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                # if self.result_tableWidget.item(j,9) != None:
                #     self.result_tableWidget.item(j,9).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(9, True)

        c_jan = format(c_jan_int, ",")
        self.hap_widget.setText(c_jan)
    
    def serch_account_special(self,gubun):
        from basic.cost_serch import serch_hang_pre_year, serch_mok_pre_year, serch_semok_pre_year
        from basic.cost_serch import serch_hang, serch_mok, serch_semok

        hap_total_1 = 0; hap_total_2 = 0; jan_int = 0; pre_amo = 0; s_jan_int = 0
        # 글꼴 설정
        # font = QtGui.QFont()
        # font.setPointSize(12)  # 글자 크기 설정
        # self.result_tableWidget.setFont(font)

        # 헤더 글꼴 설정
        header_font = QtGui.QFont()
        header_font.setPointSize(11) 
        self.result_tableWidget.horizontalHeader().setFont(header_font)

        self.result_tableWidget.clear()
        hang = self.hang_combo_widget.currentText()
        mok = self.mok_combo_widget.currentText()
        semok = self.semok_combo_widget.currentText()
        s_year = self.serch_year_widget.text()
        s_start_month = self.start_month_combo.currentText()
        s_start_day = self.start_day_combo.currentText()
        s_end_month = self.end_month_combo.currentText()
        s_end_day = self.end_day_combo.currentText()
        start_date = s_year + '-' + s_start_month + '-' + s_start_day
        end_date = s_year + '-' + s_end_month + '-' + s_end_day
        
        if hang != "선택" and mok != "선택" and  semok != "선택":  # 세목까지 선택하고 검색
            asset = 0 ; s_jan = ""
            serch_semok_pre_year_value = serch_semok_pre_year(start_date, hang, mok, semok)
            serch_semok_value = serch_semok(start_date, end_date, gubun, hang, mok, semok)
            for j1, passover_semok in enumerate(serch_semok_pre_year_value): # 전기이월 만들기
                hang_a = passover_semok[1]
                balance = passover_semok[7]
                
                if hang_a == "예금자산":
                    if balance != "예금감소":
                        pre_amo += passover_semok[3] 
                    else:
                        pre_amo -= passover_semok[3] 
                if hang_a == "고정자산" :
                    if balance == "예금증가":
                        pre_amo -= passover_semok[3] 
                    else:
                        pre_amo += passover_semok[3] 
                if hang_a == "부채" :
                    if balance == "예금감소":
                        pre_amo -= passover_semok[3] 
                    else:
                        pre_amo += passover_semok[3] 
                    
            hap_total_1 += pre_amo
            s_jan_int += pre_amo
            s_jan = format(s_jan_int,",")
            
            # serch_semok_value = serch_semok(serch_year, hang, mok, semok)

            self.result_tableWidget.setColumnCount(8)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(5, 1)
            if hap_total_1 != 0:
                self.result_tableWidget.setRowCount(len(serch_semok_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_semok_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if s_jan != '0':
                asset = 1
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 4, QTableWidgetItem(s_jan))
                if self.result_tableWidget.item(0, 4) != None:
                    self.result_tableWidget.item(0, 4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            for j, semok_data in enumerate(serch_semok_value):
                amo_int_1 = 0; amo_int_2 =0; amo_1 = ""; amo_2 = ""
                vdate = semok_data[0].strftime('%Y-%m-%d')
                hang_a = semok_data[1]
                cost_memo1 = semok_data[2]
                balance = semok_data[7]
                
                if hang_a == "고정자산":
                    if balance == "예금증가":
                        amo_int_2 += int(semok_data[3])
                    else: 
                        if balance == "예금감소" or balance == "예금증감 없음":
                            amo_int_1 += int(semok_data[3])

                if hang_a == "부채":
                    if balance == "예금증가" or balance == "예금증감 없음":
                        amo_int_1 += int(semok_data[3])
                    else:
                        if balance == "예금감소" :
                            amo_int_2 += int(semok_data[3])
                
                if hang_a == "예금자산":
                    if balance == '예금증가' or balance == "예금증감 없음":
                        amo_int_1 += int(semok_data[3])
                    else:
                        if balance == "예금감소":
                            amo_int_2 += int(semok_data[3])

                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0
                
                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                jan_int = hap_total_1 - hap_total_2
                jan = format(jan_int,",")
                payed_bank =  semok_data[4]
                semok_marks = semok_data[5]
                if len(semok_data) > 4:
                    id = str(semok_data[6])
                
                
                self.result_tableWidget.setItem(j + asset, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + asset, 1, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + asset, 2, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + asset, 3, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + asset, 4, QTableWidgetItem(jan))
                self.result_tableWidget.setItem(j + asset, 5, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + asset, 6, QTableWidgetItem(semok_marks))
                self.result_tableWidget.setItem(j + asset, 7, QTableWidgetItem(id))
                if self.result_tableWidget.item(j + asset,0) != None:
                    self.result_tableWidget.item(j + asset,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.result_tableWidget.item(j + asset,1) != None:
                    self.result_tableWidget.item(j + asset,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,2) != None:
                    self.result_tableWidget.item(j + asset,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,3) != None:
                    self.result_tableWidget.item(j + asset,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,4) != None:
                    self.result_tableWidget.item(j + asset,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,5) != None:
                    self.result_tableWidget.item(j + asset,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,6) != None:
                    self.result_tableWidget.item(j + asset,6).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(7, True)

        elif hang != "선택" and mok != "선택" and  semok == '선택':  # 목 까지 선택하고 검색
            if hang == "예금자산" and mok == "보통예금":
                    QMessageBox.information(None, "오류","보통예금은 특별회계 예금보기에서 검색 하십시오.")
                    return
            asset = 0; s_jan = ""
            # serch_mok_value = serch_mok(serch_year, hang, mok)
            serch_mok_pre_year_value = serch_mok_pre_year(start_date, hang, mok)
            serch_mok_value = serch_mok(start_date, end_date, gubun, hang, mok)
            self.result_tableWidget.setColumnCount(9)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(6, 1) 
            for j1, passover_semok in enumerate(serch_mok_pre_year_value): # 전기이월 만들기
                hang_a = passover_semok[1]
                balance = passover_semok[9]
                
                if hang_a == "예금자산":
                    if balance != "예금증가":
                        pre_amo += passover_semok[5] 
                    else:
                        if balance == "예금감소":
                            pre_amo -= passover_semok[5] 
                
                if hang_a == "고정자산" :
                    if balance == "예금증가":
                        pre_amo -= passover_semok[5] 
                    else:
                        pre_amo += passover_semok[5] 
                
                if hang_a == "부채" :
                    if balance == "예금감소":
                        pre_amo -= passover_semok[5] 
                    else:
                        pre_amo += passover_semok[5] 
                    
            hap_total_1 += pre_amo
            s_jan_int += pre_amo
            pre_amo_T = format(pre_amo,",")
            s_jan = format(s_jan_int,",")
            
            if hap_total_1 != 0:
                self.result_tableWidget.setRowCount(len(serch_mok_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_mok_value))

            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "세목", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if hap_total_1 != 0:
                asset = 1
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 5, QTableWidgetItem(s_jan))
                if self.result_tableWidget.item(0, 5) != None:
                    self.result_tableWidget.item(0, 5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            for j, mok_data in enumerate(serch_mok_value):
                amo_int_1 = 0; amo_int_2 = 0; amo_1 = ""; amo_2 = ""
                vdate = mok_data[0].strftime('%Y-%m-%d')
                hang_a = mok_data[1]
                cost_semok = mok_data[2]
                cost_memo1 = mok_data[3]
                
                balance = mok_data[8]
                if hang_a == "고정자산":
                    if balance == "예금증가":
                        amo_int_2 += int(mok_data[4])
                    else: 
                        if balance == "예금감소" or balance == "예금증감 없음":
                            amo_int_1 += int(mok_data[4])
                if hang_a == "부채":
                    if balance == "예금증가" or balance == "예금증감 없음":
                        amo_int_1 += int(mok_data[4])
                    else:
                        if balance == "예금감소" :
                            amo_int_2 += int(mok_data[4])
                if hang_a == "예금자산":
                    if balance == '예금증가' or balance == "예금증감 없음":
                        amo_int_1 += int(mok_data[4])
                    else:
                        if balance == "예금감소":
                            amo_int_2 += int(mok_data[4])
                
                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0
                
                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                jan_int = hap_total_1 - hap_total_2
                jan = format(jan_int,",")
                payed_bank = mok_data[5]
                mok_marks = mok_data[6] # if mok_data[5] != 'nan' else ''

                if len(mok_data) > 6:
                    id = str(mok_data[7])

                self.result_tableWidget.setItem(j + asset, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + asset, 1, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j + asset, 2, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + asset, 3, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + asset, 4, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + asset, 5, QTableWidgetItem(jan))
                self.result_tableWidget.setItem(j + asset, 6, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + asset, 7, QTableWidgetItem(mok_marks))
                self.result_tableWidget.setItem(j + asset, 8, QTableWidgetItem(id))
                if self.result_tableWidget.item(j + asset,0) != None:
                    self.result_tableWidget.item(j + asset,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.result_tableWidget.item(j + asset,1) != None:
                    self.result_tableWidget.item(j + asset,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,2) != None:
                    self.result_tableWidget.item(j + asset,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,3) != None:
                    self.result_tableWidget.item(j + asset,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,4) != None:
                    self.result_tableWidget.item(j + asset,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,5) != None:
                    self.result_tableWidget.item(j + asset,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,6) != None:
                    self.result_tableWidget.item(j + asset,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,7) != None:
                    self.result_tableWidget.item(j + asset,7).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(8, True)

        elif hang != '선택' and mok == '선택' and semok == '선택':
            if hang == "예금자산":
                    QMessageBox.information(None, "오류","예금자산은 '목'을 선택하여 주세요.")
                    return
            asset = 0
            # serch_hang_value = serch_hang(serch_year, hang)
            serch_hang_value = serch_hang(start_date, end_date, gubun, hang)
            serch_hang_pre_year_value = serch_hang_pre_year(start_date, hang)
            self.result_tableWidget.setColumnCount(10)
            for j1, passover_semok in enumerate(serch_hang_pre_year_value): # 전기이월 만들기
                hang_a = passover_semok[1]
                balance = passover_semok[9]
                
                if hang_a == "고정자산" :
                    if balance == "예금증가":
                        pre_amo -= passover_semok[5] 
                    else:
                        pre_amo += passover_semok[5] 
                
                if hang_a == "부채" :
                    if balance == "예금감소":
                        pre_amo -= passover_semok[5] 
                    else:
                        pre_amo += passover_semok[5] 
                    
            hap_total_1 += pre_amo
            s_jan_int += pre_amo
            pre_amo_T = format(pre_amo,",")
            s_jan = format(s_jan_int,",")
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(7, 1)
            if hap_total_1 != 0:
                self.result_tableWidget.setRowCount(len(serch_hang_value)+1)
            else:
                self.result_tableWidget.setRowCount(len(serch_hang_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "목", "세목", "적요", "증가액", "감소액", "잔액", "지급계좌", "비고","id"])
            if hap_total_1 != 0:
                asset = 1
                self.result_tableWidget.setItem(0, 0, QTableWidgetItem('이월금액'))
                self.result_tableWidget.setItem(0, 6, QTableWidgetItem(s_jan))
                if self.result_tableWidget.item(0, 6) != None:
                    self.result_tableWidget.item(0, 6).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            for j, hang_data in enumerate(serch_hang_value):
                amo_int_1 = 0; amo_int_2 =0

                vdate = hang_data[0].strftime('%Y-%m-%d')
                cost_hang = hang_data[1]
                cost_mok = hang_data[2]
                cost_semok = hang_data[3]
                cost_memo1 = hang_data[4]
                
                balance = hang_data[9]
                
                if cost_hang == "고정자산":
                    if balance == "예금감소" or balance == "예금증감 없음":
                        amo_int_1 += int(hang_data[5])
                    else: 
                        if balance == "예금증가":
                            amo_int_2 += int(hang_data[5])
                        
                if cost_hang == "부채":
                    if balance == "예금증가" or balance == "예금증감 없음":
                        amo_int_1 += int(hang_data[5])
                    else:
                        if balance == "예금감소" :
                            amo_int_2 += int(hang_data[5])
                if hang_a == "예금자산":
                    if balance == '예금증가':
                        amo_int_1 += int(hang_data[5])
                    else:
                        if balance == "예금감소":
                            amo_int_2 += int(hang_data[5])

                if amo_int_1 < 0:
                    amo_int_2 = amo_int_1 * (-1)
                    amo_int_1 = 0
                        
                hap_total_1 += amo_int_1
                amo_1 = format(amo_int_1, ",")
                hap_total_2 += amo_int_2
                amo_2 = format(amo_int_2, ",")
                jan_int = hap_total_1 - hap_total_2
                jan = format(jan_int,",")
                payed_bank = hang_data[5]
                hang_marks = hang_data[6] # if hang_data[6] != 'nan' else ''

                if len(hang_data) > 7:
                    id = str(hang_data[7])
                self.result_tableWidget.setItem(j + asset, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j + asset, 1, QTableWidgetItem(cost_mok))
                self.result_tableWidget.setItem(j + asset, 2, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j + asset, 3, QTableWidgetItem(cost_memo1))
                if amo_1 != '0':
                    self.result_tableWidget.setItem(j + asset, 4, QTableWidgetItem(amo_1))
                if amo_2 != '0':
                    self.result_tableWidget.setItem(j + asset, 5, QTableWidgetItem(amo_2))
                self.result_tableWidget.setItem(j + asset, 6, QTableWidgetItem(jan))
                self.result_tableWidget.setItem(j + asset, 7, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j + asset, 8, QTableWidgetItem(hang_marks))
                self.result_tableWidget.setItem(j + asset, 9, QTableWidgetItem(id))

                self.result_tableWidget.item(j + asset,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j + asset,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j + asset,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j + asset,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,4) != None:
                    self.result_tableWidget.item(j + asset,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,5) != None:
                    self.result_tableWidget.item(j + asset,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,6) != None:
                    self.result_tableWidget.item(j + asset,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j + asset,7) != None:
                    self.result_tableWidget.item(j + asset,7).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if self.result_tableWidget.item(j + asset,8) != None:
                    self.result_tableWidget.item(j + asset,8).setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                # if self.result_tableWidget.item(j,9) != None:
                #     self.result_tableWidget.item(j,9).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(9, True)
        
        jan = format(jan_int, ",")
        self.hap_widget.setText(jan)

    def edit_cost(self): #cell_changed
        from modify.cost_modify_reg import Cost_modify_register
        from modify.special_balance_modi_reg import Special_modify_register
        gubun = self.gubun_combo_widget.currentText()
        hang = self.hang_combo_widget.currentText()
        mok = self.mok_combo_widget.currentText()
        semok = self.semok_combo_widget.currentText()
        # serch_year = int(self.year_combo_widget.currentText())
        v_year = today.year()
        sel_row = self.result_tableWidget.currentRow()
        # if v_year == serch_year:
        if sel_row >= 0:
            if hang != "선택" and mok != "선택" and  semok != "선택":
                id_row = 7
            if hang != "선택" and mok != "선택" and  semok == "선택":
                id_row = 8
            if hang != "선택" and mok == "선택" and  semok == "선택":
                id_row = 9
            # 선택한 셀이 존재하는 경우에만 진행 
            id = self.result_tableWidget.item(sel_row, id_row).text()
        else:
            QMessageBox.information(None, "완료","선택한 행이 없습니다.")
            return
        if gubun != "특별회계":
            self.cost_modify_register = Cost_modify_register(str(id))
            self.cost_modify_register.exec()
            self.show()
            self.serch_account_home()
        else:
            self.cost_modify_register = Special_modify_register(str(id))
            self.cost_modify_register.exec()
            self.show()
            self.serch_account_home()
        # else:
        #     QMessageBox.information(None, "완료", "금년의 지출내역만 수정할 수 있습니다.")
        
    def reset(self):
        self.hap_widget.clear()
        self.gubun_combo_widget.setCurrentText("선택")
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.setRowCount(0)
        self.result_tableWidget.setRowCount(1)
        # self.gubun_combobox()

    def serch_close(self):
        self.reset()
        self.close()
    
    def closeEvent(self, event):
        self.reset()
        event.accept()

    def user_confirm(self):
        from user.for_user_sql import user_infor_sql
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        user_id = config['user']['user_id']

        user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
        user_name_infor = user_info[0]        # 이름을 가져오고
        user_name_hash = self.user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
        user_name = user_name_infor[0]
        Ge_value = str(user_name_infor[1])       # user_reg_check의 권한을 가져와서
        # # sun_value = str(user_name_infor[2])       # user_reg_check의 권한을 가져와서
        # # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
        # Ge_check = self.user_infor_hash(Ge_value)  # user_reg_check를 hash화 한다.
        # # sun_check = self.user_infor_hash(sun_value)
        config['user'][user_name] = user_name_hash # 해시화된 이름을 저장한다.
        # config['user'][Ge_check] = Ge_check
        # config['user'][sun_check] = sun_check
        
        return user_name_infor  # , sun_check

    def user_infor_hash(self,data):
        # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
        hasher = hashlib.sha256()
        # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
        hasher.update(data.encode('utf-8'))
        # 해시된 결과 반환
        return hasher.hexdigest()
    
    def serch_account_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.serch_year_widget.text()
            year_text = year_int + '년도'
            hang = self.hang_combo_widget.currentText()
            mok = self.mok_combo_widget.currentText()
            semok = self.semok_combo_widget.currentText()
            
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)
            # font = painter.font()
            x_margin = 35; y_margin = 70
            current_x = x_margin
            current_y = y_margin

            # 페이지 크기 계산
            page_rect = printer.pageRect()
            available_width = page_rect.width() - (2 * x_margin) # 양 옆의 여백을 제외한 크기가 인쇄가능 넓이
            available_height = page_rect.height() - current_y - y_margin


            if year_int != '선택' and hang != '선택':
                # year_text 출력
                painter.setFont(font1)
                self.adjust_font_size(painter, year_text, available_width)
                painter.drawText(current_x, current_y, year_text)
                year_int_width = painter.fontMetrics().width(year_text)
                current_x += year_int_width + 10

                # hang 출력
                painter.setFont(font1)
                self.adjust_font_size(painter, hang, available_width)
                painter.drawText(current_x, current_y, hang)
                hang_width = painter.fontMetrics().width(hang)
                current_x += hang_width + 10

                if mok != '선택':
                    # mok 출력
                    painter.setFont(font1)
                    self.adjust_font_size(painter, mok, available_width)
                    painter.drawText(current_x, current_y, mok)
                    mok_width = painter.fontMetrics().width(mok)
                    current_x += mok_width + 20  #painter.fontMetrics().height() + 20  # 20은 제목과 테이블 간 간격
                    if semok != '선택':
                        # semok 출력
                        painter.setFont(font1)
                        self.adjust_font_size(painter, semok, available_width)
                        painter.drawText(current_x, current_y, semok)
                        mok_width = painter.fontMetrics().width(semok)
                        current_x += painter.fontMetrics().height() + 20 # title_width + 10  # 10은 라벨 간 간격

                # # 페이지 크기 계산
                # page_rect = printer.pageRect()
                # available_width = page_rect.width() - 2 * x_margin
                # available_height = page_rect.height() - current_y - y_margin
                
                # 초기 좌표 설정
                x = x_margin
                y = current_y + 20
                
                
                # 각 행과 열의 높이와 너비 계산
                row_height = 35  # 기본 행 높이
                painter.setFont(font2)
                col_widths = [self.result_tableWidget.columnWidth(col) for col in range(self.result_tableWidget.columnCount())]
                col_count = self.result_tableWidget.columnCount() - 1
                # 테이블 헤더 출력
                for col in range(self.result_tableWidget.columnCount() - 1):
                    header_text = self.result_tableWidget.horizontalHeaderItem(col).text()
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    self.adjust_font_size(painter, header_text, col_width)
                    painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, self.result_tableWidget.horizontalHeaderItem(col).text())
                    painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                    x += col_width

                y += row_height
                x = x_margin
                
                # 테이블 내용 출력
                for row in range(self.result_tableWidget.rowCount()):
                    if y + row_height > page_rect.bottom() - y_margin:
                        printer.newPage()
                        y = y_margin  # 새로운 페이지에서 y 좌표 초기화
                    x = x_margin
                    for col in range(col_count):
                        col_width = int(col_widths[col] * available_width / sum(col_widths))
                        painter.drawRect(x, y, col_width, row_height)
                        # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                        item = self.result_tableWidget.item(row, col)

                        if item and item.text():
                            cell_text = item.text()
                            self.adjust_font_size(painter, cell_text, col_width)
                            # align = Qt.AlignLeft if col <= 3 else (Qt.AlignRight if col == 4 else Qt.AlignRight)
                            # painter.drawText(QRect(x, y, col_width, row_height), align | Qt.AlignVCenter, cell_text)
                            if col_count == 9:
                                if col == 0:
                                    # 중앙 맞춤
                                    text_rect = QRect(x, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, cell_text)
                                elif 4 <= col <= 6:
                                    # 우측 맞춤 우측여백 5
                                    text_rect = QRect(x, y, col_width - 3, row_height)
                                    painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, cell_text)
                                else:
                                    # 좌측 맞춤 띄우기
                                    text_rect = QRect(x + 2, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, cell_text)
                            elif col_count == 8:
                                if col == 0:
                                    # 중앙 맞춤
                                    text_rect = QRect(x, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, cell_text)
                                elif 3 <= col <= 5:
                                    # 우측 맞춤 우측여백 5
                                    text_rect = QRect(x, y, col_width - 5, row_height)
                                    painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, cell_text)
                                else:
                                    # 좌측 맞춤 띄우기
                                    text_rect = QRect(x + 2, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, cell_text)
                            else:
                                if col == 0:
                                    # 중앙 맞춤
                                    text_rect = QRect(x, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, cell_text)
                                elif 2 <= col <= 4:
                                    # 우측 맞춤 우측여백 5
                                    text_rect = QRect(x, y, col_width - 5, row_height)
                                    painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, cell_text)
                                else:
                                    # 좌측 맞춤 띄우기
                                    text_rect = QRect(x + 5, y, col_width, row_height)
                                    painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, cell_text)
                                
                        x += col_width
                        # x += col_widths[col]
                    y += row_height

                painter.end()
            else:
                QMessageBox.about(self,'내용없음','출력할 사항이 없습니다.')
    
    def adjust_font_size(self,painter, text, max_width):
        """
        텍스트가 주어진 폭에 맞도록 폰트 크기를 조정합니다.
        """
        font = painter.font()
        font_metrics = QFontMetrics(font) # QFontMetrics는 특정 측정정보를 계산하는데 쓰이는Qt 클래스중 하나
        while font_metrics.boundingRect(text).width() > max_width: # boundingRect는 QFontMetrics 클래스에서 제공하는 메서드 사각형으로 텍스트가 화면에 렌더링될때 차지하는 공간을 나타냄
            font_size = font.pointSize()  # 현재의 폰트 크기를 가져옴
            if font_size <= 1:  # 최소 폰트 크기 제한
                break
            font.setPointSize(font_size - 1) # QFont 객체의 글꼴 크기를 한 포인트 줄이는 코드
            painter.setFont(font)
            font_metrics = QFontMetrics(font)
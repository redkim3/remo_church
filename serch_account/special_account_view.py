import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic, QtWidgets # QtCore, QtGui 
from PyQt5.QtCore import QRect
from PyQt5 import QtGui
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPainter
from basic.cost_select import *
import configparser, hashlib

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()

form_class = uic.loadUiType(r"./ui/serch_account_form.ui")[0]

class special_serch_account(QtWidgets.QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("특별회계 계정별 검색")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))

        self.load_year_combo()
        self.year_combo_widget.currentTextChanged.connect(self.load_gubun_combo)
        self.gubun_combo_widget.currentTextChanged.connect(self.load_hang_combo)
        self.hang_combo_widget.currentTextChanged.connect(self.load_mok_combo)
        self.mok_combo_widget.currentTextChanged.connect(self.load_semok_combo)
        self.result_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정
        self.hang_combo_items = {}
        self.mok_combo_items = {}
        self.semok_combo_items = {}

    def load_year_combo(self):
        today = QDate.currentDate()
        view_year = str(today.year())
        combo_year = ["선택"]
        for y in range(1, 6):
            combo_year.append(str(int(view_year) + 1 - y))
        self.year_combo_widget.addItems(combo_year)
        self.year_combo_widget.currentTextChanged.connect(self.reset)
        self.reset()

    def load_gubun_combo(self):
        from basic.hun_name_2 import gubun_values_check
        confirm_data = self.user_confirm()
        special_check = int(confirm_data[3]) # 특별회계
        # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.

        self.hap_widget.clear()
        self.gubun_combo_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        self.gubun_combo_widget.clear()
        self.gubun_combo_widget.addItems(["선택","특별회계"]) # + gubun_values_check(special_check))
        gubun = self.gubun_combo_widget.currentText()

    def load_hang_combo(self):
        from basic.cost_select import cost_hang_values
        self.hap_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        v_year = str(today.year())
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
        v_year = str(today.year())
        hang = self.hang_combo_widget.currentText()
        mok_s = cost_mok_values(v_year, hang)
        mok_list = []
        for mo in mok_s:
            mok, id = mo
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
        v_year = str(today.year())
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

    def special_serch_account(self):
        from basic.special_acc_sql import serch_hang, serch_mok, serch_semok
        hap_total = 0
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
        serch_year = self.year_combo_widget.currentText()
        # s_date = self.start_date_widget.text() #date().toPyDate()
        # e_date = self.end_date_widget.text() #date().toPyDate()

        if hang != "선택" and mok != "선택" and  semok != "선택":  # 세목까지 선택하고 검색
            serch_semok_value = serch_semok(serch_year, hang, mok, semok)

            self.result_tableWidget.setColumnCount(6)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(5, 1)
            self.result_tableWidget.setRowCount(len(serch_semok_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "적요", "증가액","감소액", "계좌은행", "비고","id"])
            for j, semok_data in enumerate(serch_semok_value):
                vdate = semok_data[0].strftime('%Y-%m-%d')
                cost_memo1 = semok_data[1]
                balance1 = semok_data[2]
                amo_int_1 = int(semok_data[3])
                hap_total += amo_int_1
                amo_1 = format(amo_int_1, ",")
                bank_account =  semok_data[4]
                semok_marks = semok_data[5]
                if len(semok_data) > 5:
                    id = str(semok_data[6])
                self.result_tableWidget.setItem(j, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j, 1, QTableWidgetItem(cost_memo1))
                if balance1 ==  "예금증가":
                    self.result_tableWidget.setItem(j, 2, QTableWidgetItem(amo_1))
                else:
                    self.result_tableWidget.setItem(j, 3, QTableWidgetItem(amo_1))
                self.result_tableWidget.setItem(j, 4, QTableWidgetItem(bank_account))
                self.result_tableWidget.setItem(j, 5, QTableWidgetItem(semok_marks))
                self.result_tableWidget.setItem(j, 6, QTableWidgetItem(id))
                
                self.result_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j,2) is not None:
                    self.result_tableWidget.item(j,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j,3) is not None:
                    self.result_tableWidget.item(j,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.result_tableWidget.item(j,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,5).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(6, True)

        elif hang != "선택" and mok != "선택" and  semok == '선택':  # 목 까지 선택하고 검색
            serch_mok_value = serch_mok(serch_year, hang, mok)
            self.result_tableWidget.setColumnCount(7)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(6, 1)
            self.result_tableWidget.setRowCount(len(serch_mok_value))

            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "세목", "적요", "증가액","감소액", "계좌은행", "비고","id"])
            for j, mok_data in enumerate(serch_mok_value):
                vdate = mok_data[0].strftime('%Y-%m-%d')
                cost_semok = mok_data[1]
                cost_memo1 = mok_data[2]
                balance2 = mok_data[3]
                amo_int_1 = int(mok_data[4])
                hap_total += amo_int_1
                amo_1 = format(amo_int_1, ",")
                payed_bank = mok_data[5]
                mok_marks = mok_data[6] if mok_data[5] != 'nan' else ''
                if len(mok_data) > 7:
                    id = str(mok_data[7])
                self.result_tableWidget.setItem(j, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j, 1, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j, 2, QTableWidgetItem(cost_memo1))
                if balance1 ==  "예금증가":
                    self.result_tableWidget.setItem(j, 3, QTableWidgetItem(amo_1))
                else:
                    self.result_tableWidget.setItem(j, 4, QTableWidgetItem(amo_1))
                
                self.result_tableWidget.setItem(j, 5, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j, 6, QTableWidgetItem(mok_marks))
                self.result_tableWidget.setItem(j, 7, QTableWidgetItem(id))
                self.result_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j,3) is not None:
                    self.result_tableWidget.item(j,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j,4) is not None:
                    self.result_tableWidget.item(j,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.result_tableWidget.item(j,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,6).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,7).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(7, True)

        elif hang != '선택' and mok == '선택' and semok == '선택':
            serch_hang_value = serch_hang(serch_year, hang)
            self.result_tableWidget.setColumnCount(8)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(7, 1)
            self.result_tableWidget.setRowCount(len(serch_hang_value))
            self.result_tableWidget.setHorizontalHeaderLabels(["일자", "목", "세목", "적요", "증가액","감소액", "계좌은행", "비고","id"])
            for j, hang_data in enumerate(serch_hang_value):
                vdate = hang_data[0].strftime('%Y-%m-%d')
                cost_mok = hang_data[1]
                cost_semok = hang_data[2]
                cost_memo1 = hang_data[3]
                balance_1 = hang_data[4]
                amo_int_1 = int(hang_data[5])
                hap_total += amo_int_1
                amo_1 = format(amo_int_1, ",")
                payed_bank = hang_data[6]
                hang_marks = hang_data[7] if hang_data[6] != 'nan' else ''
                if len(hang_data) > 8:
                    id = str(hang_data[8])
                self.result_tableWidget.setItem(j, 0, QTableWidgetItem(vdate))
                self.result_tableWidget.setItem(j, 1, QTableWidgetItem(cost_mok))
                self.result_tableWidget.setItem(j, 2, QTableWidgetItem(cost_semok))
                self.result_tableWidget.setItem(j, 3, QTableWidgetItem(cost_memo1))
                if balance1 ==  "예금증가":
                    self.result_tableWidget.setItem(j, 4, QTableWidgetItem(amo_1))
                else:
                    self.result_tableWidget.setItem(j, 5, QTableWidgetItem(amo_1))
                self.result_tableWidget.setItem(j, 6, QTableWidgetItem(payed_bank))
                self.result_tableWidget.setItem(j, 7, QTableWidgetItem(hang_marks))
                self.result_tableWidget.setItem(j, 8, QTableWidgetItem(id))
                self.result_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if self.result_tableWidget.item(j,4) is not None:
                    self.result_tableWidget.item(j,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                if self.result_tableWidget.item(j,5) is not None:
                    self.result_tableWidget.item(j,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.result_tableWidget.item(j,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.result_tableWidget.item(j,7).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.result_tableWidget.item(j,8).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.resizeColumnsToContents()
            self.result_tableWidget.setColumnHidden(8, True)

        hap_total = format(hap_total, ",")
        self.hap_widget.setText(hap_total)

    def edit_cost(self): #cell_changed
        from modify.cost_modify_reg import Cost_modify_register
        hang = self.hang_combo_widget.currentText()
        mok = self.mok_combo_widget.currentText()
        semok = self.semok_combo_widget.currentText()
        serch_year = int(self.year_combo_widget.currentText())
        v_year = today.year()
        sel_row = self.result_tableWidget.currentRow()
        if v_year == serch_year:
            if sel_row >= 0:
                if hang != "선택" and mok != "선택" and  semok != "선택":
                    id_row = 5
                if hang != "선택" and mok != "선택" and  semok == "선택":
                    id_row = 6
                if hang != "선택" and mok == "선택" and  semok == "선택":
                    id_row = 7
                # 선택한 셀이 존재하는 경우에만 진행
                id = self.result_tableWidget.item(sel_row, id_row).text()
            else:
                QMessageBox.information(None, "완료","선택한 행이 없습니다.")
                return
            self.cost_modify_register = Cost_modify_register(str(id))
            self.cost_modify_register.exec()
            self.show()
            self.serch_account()
        else:
            QMessageBox.information(None, "완료", "금년의 지출내역만 수정할 수 있습니다.")

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
        user_name_infor = user_info[0]         # 이름을 가져오고
        user_name_hash = self.user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
        user_name = user_name_infor[0]
        Ge_value = str(user_name_infor[1])       # user_reg_check의 권한을 가져와서
        sun_value = str(user_name_infor[2])       # user_reg_check의 권한을 가져와서
        special_value = str(user_name_infor[3])       # user_reg_check의 권한을 가져와서
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
            year_int = self.year_combo_widget.currentText()
            year_text = year_int + '년도'
            hang = self.hang_combo_widget.currentText()
            mok = self.mok_combo_widget.currentText()
            semok = self.semok_combo_widget.currentText()
            
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)
            # font = painter.font()
            x_margin = 50; y_margin = 100
            current_x = x_margin
            current_y = y_margin
            if year_int != '선택' and hang != '선택':
                # year_text 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, year_text)
                year_int_width = painter.fontMetrics().width(year_text)
                current_x += year_int_width + 10

                # hang 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, hang)
                hang_width = painter.fontMetrics().width(hang)
                current_x += hang_width + 10

                if mok != '선택':
                    # mok 출력
                    painter.setFont(font1)
                    painter.drawText(current_x, current_y, mok)
                    mok_width = painter.fontMetrics().width(mok)
                    current_x += mok_width + 20  #painter.fontMetrics().height() + 20  # 20은 제목과 테이블 간 간격
                    if semok != '선택':
                        # semok 출력
                        painter.setFont(font1)
                        painter.drawText(current_x, current_y, semok)
                        mok_width = painter.fontMetrics().width(semok)
                        current_x += painter.fontMetrics().height() + 20 # title_width + 10  # 10은 라벨 간 간격

                # 페이지 크기 계산
                page_rect = printer.pageRect()
                available_width = page_rect.width() - 2 * x_margin
                available_height = page_rect.height() - current_y - y_margin
                
                # 초기 좌표 설정
                x = x_margin
                y = current_y + 30
                
                # 각 행과 열의 높이와 너비 계산
                row_height = 35  # 기본 행 높이
                painter.setFont(font2)
                col_widths = [self.result_tableWidget.columnWidth(col) for col in range(self.result_tableWidget.columnCount())]
                
                # 테이블 헤더 출력
                for col in range(self.result_tableWidget.columnCount() - 1):
                    painter.drawText(x, y, col_widths[col], row_height, Qt.AlignCenter | Qt.AlignVCenter, self.result_tableWidget.horizontalHeaderItem(col).text())
                    painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    x += col_widths[col]
                y += row_height
                x = x_margin
                
                # 테이블 내용 출력
                for row in range(self.result_tableWidget.rowCount()):
                    if y + row_height > page_rect.bottom() - y_margin:
                        printer.newPage()
                        y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                    x = x_margin
                    for col in range(self.result_tableWidget.columnCount() - 1):
                        painter.drawRect(x, y, col_widths[col], row_height)
                        # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                        item = self.result_tableWidget.item(row, col)
                        if item and item.text():
                            if col <= 3:
                                # 중앙 맞춤
                                text_rect = QRect(x, y, col_widths[col], row_height)
                                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, item.text())
                            elif col == 4 :
                                # 좌측 맞춤 및 우측에서 여백(20) 띄우기
                                text_rect = QRect(x, y, col_widths[col] - 10, row_height)
                                painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, item.text())
                            else:
                                # 좌측 맞춤 및 우측에서 여백(20) 띄우기
                                text_rect = QRect(x, y, col_widths[col], row_height)
                                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, item.text())
                            
                        x += col_widths[col]
                    y += row_height

                painter.end()
            else:
                QMessageBox.about(self,'내용없음','출력할 사항이 없습니다.')
    
   
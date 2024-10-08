import pymysql, os, configparser
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic       # QtCore, QtGui, QtWidgets, 
from PyQt5.QtWidgets import *
from datetime import datetime
from PyQt5.QtGui import QIcon

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
now = today.toString(Qt.ISODate) 
hun_year = today.year()

imsi = []; Bank = ''; hap_total = 0 ; j = 0

form_class = uic.loadUiType("ui/other_reg_form.ui")[0]

class OtherIncomeRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('기타소득 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.other_date = QDateEdit()
        self.other_date_widget.setDate(today)
        year_widget = str(today.year())
        month_widget = str(today.month())
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)
        # self.other_income_tableWidget.clearContents()
        self.other_income_tableWidget.setRowCount(0)  # 0으로 하면 라인 추가에 문제가 발생함
        self.year_widget.setText(year_widget)      # = QLabel(order_sign1)
        self.month_widget.setText(month_widget)

        self.month_widget.setFocus()
        self.year_widget.editingFinished.connect(self.year_compare)
        self.week_widget.editingFinished.connect(self.gubun_combobox)
        self.amount_widget.textChanged.connect(self.on_amount_changed)
        # self.amount_widget.editingFinished.connect(self.amount_format)   #금액을 넣을때 다시 확인
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.other_income_tableWidget.itemChanged.connect(self.on_item_changed)
        self.gubun_name_combo_widget.currentTextChanged.connect(self.other_name_combo)
        self.other_income_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정

    def other_page_button(self):
        add_other_input = QPushButton("등록")
        add_other_input.clicked.connect(self.other_input)
        re_calculate_button = QPushButton("합계 재계산")
        re_calculate_button.clicked.connect(self.re_calculate)
        remove_row_button = QPushButton("행삭제 버튼")
        remove_row_button.clicked.connect(self.remove_row)
        other_save_button = QPushButton("저장")
        other_save_button.clicked.connect(self.file_save)

        file_close_button = QPushButton("종료(저장취소)")
        file_close_button.clicked.connect(self.file_close)
    
    def showEvent(self, event):
        super(OtherIncomeRegister, self).showEvent(event)
        self.set_cursor_position()

    def set_cursor_position(self):
        # 커서를 특정 위치로 설정합니다 (예: QLineEdit)
        self.month_widget.setFocus()
        self.month_widget.setCursorPosition(0)  # 커서를 맨 앞에 위치시킵니다
        # self.counter_name_widget.setEnabled(False)
        self.amount_widget.setEnabled(False)
        self.marks_widget.setEnabled(False)
        self.add_other_input.setEnabled(False)
        self.other_save_button.setEnabled(False)
        self.re_calculate_button.setEnabled(False)
        self.remove_row_button.setEnabled(False)
    
    def on_amount_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        amount_value_text = self.amount_widget.text()
        if amount_value_text != ''and amount_value_text != '-':
            try:
                amount_value = int(amount_value_text.replace(",", ""))
                self.amount_widget.setText(f"{amount_value:,}")  # 숫자를 쉼표로 포맷팅
            except ValueError:
                QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")
                self.amount_widget.clear()
                self.amount_widget.setFocus()
                return

    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if col == 0:  # 8번째 열
            try:
                value = int(item.text().replace(",", ""))
                item.setText(f"{value:,}")  # 숫자를 쉼표로 포맷팅
            except ValueError:
                QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")

    def user_confirm(self):
        from user.for_user_sql import user_infor_sql
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        user_id = config['user']['user_id']
        
        user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
        user_name_infor = user_info[0]        # 이름을 가져오고
        user_name = user_name_infor[0]
        # user_reg = str(user_name_infor[5])       # user_reg_check의 권한을 가져와서
        # # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
        # user_reg_check = user_infor_hash(user_reg)  # user_reg_check를 hash화 한다.
        
        config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
        return user_name
    
    def gubun_combobox(self):
        from basic.hun_name_2 import gubun_values
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
        self.gubun_name_combo_widget.clear()
        self.other_name_combo_widget.clear()        
        selec = gubun_values()
        self.gubun_name_combo_widget.addItems(['선택'] + selec)
        self.gubun_name_combo_widget.currentText()
       
    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(today.year()):
            return False  # 현재 년도와 같으면 False 반환
        else:
            QMessageBox.about(self, '', "'지출년도'가 현재의 '년도'와 같아야 합니다. ")
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환

    def other_name_combo(self):
        from basic.hun_name_2 import other_hun_mok_values
        # self.counter_name_widget.setEnabled(True)
        self.amount_widget.setEnabled(True)
        self.marks_widget.setEnabled(True)
        self.add_other_input.setEnabled(True)
        self.other_name_combo_widget.clear()
        self.hap_total_widget.clear()
        # self.other_income_tableWidget.clearContents()  
        self.other_income_tableWidget.setRowCount(0)
        Y1 = self.year_widget.text()
        gubun_mok = self.gubun_name_combo_widget.currentText()
        if gubun_mok != '선택' and gubun_mok != "":
            mok = other_hun_mok_values(Y1, gubun_mok)
            self.other_name_combo_widget.addItems(["선택"] + mok)
        else:
            self.gubun_name_combo_widget.setFocus()
            return

    def other_input(self):
        global hap_total, Bank, j
        try:
            if j != 0:
                self.other_income_tableWidget.insertRow(j)
            else:
                self.other_income_tableWidget.setRowCount(0)  # 0으로 하면 라인 추가에 문제가 발생함
                self.other_income_tableWidget.setRowCount(1)  # 0으로 하면 라인 추가에 문제가 발생함
            # counter_part = self.counter_name_widget.text()  # 거래상대방 
            amo_str = self.amount_widget.text()
            int_amo = int(amo_str.replace(',','')) #콤마제거 후 정수로 받음

            if int_amo != '':
                amount = format(int_amo,",")
                self.amount_widget.setText(amount)
            marks = self.marks_widget.text()
            if self.Bankincome_check.isChecked() == True: # text()
                Bank = '통장예입'
            else:
                Bank = ''
            
            # self.other_income_tableWidget.setItem(j,0,QTableWidgetItem(counter_part))
            self.other_income_tableWidget.setItem(j,0,QTableWidgetItem(amount))
            self.other_income_tableWidget.setItem(j,1,QTableWidgetItem(Bank))
            self.other_income_tableWidget.setItem(j,2,QTableWidgetItem(marks))
            self.other_income_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            if self.other_income_tableWidget.item(j, 0) != None:
                self.other_income_tableWidget.item(j, 0).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)

            hap_total = hap_total + int_amo
            hap_total_view = format(hap_total,',')
            self.hap_total_widget.setText(hap_total_view)
            self.other_income_tableWidget.scrollToBottom()   # 자동 스크롤
            self.Bankincome_check.setChecked(False)
            self.other_save_button.setEnabled(True)
            self.re_calculate_button.setEnabled(True)
            self.remove_row_button.setEnabled(True)
            # self.counter_name_widget.clear()  # 성도명 코드를 대체함
            self.amount_widget.clear()
            self.marks_widget.clear()
            j += 1

        except ValueError:
            QMessageBox.about(self,'입력오류','헌금 금액 또는 년,월,몇째주에 대한 입력을 확인하세요!!')
        
    # def amount_format(self):
    #     amo_str = self.amount_widget.text()
    #     int_amo = int(amo_str.replace(',','')) #콤마제거 후 정수로 받음
    #     if int_amo != '':
    #         amount = format(int_amo,",")
    #         self.amount_widget.setText(amount)

    def re_calculate(self):
        global hap_total
        hap_total = 0
        row_count = self.other_income_tableWidget.rowCount()
        if row_count == 0:
            self.hap_total_widget.setText('0')
        for i in range(row_count):
            imsi_amo = self.other_income_tableWidget.item(i,0).text()
            table_amo = int(imsi_amo.replace(',',''))
            amount = format(table_amo,',')
            self.other_income_tableWidget.setItem(i,0,QTableWidgetItem(amount))
            self.other_income_tableWidget.item(i,0).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            hap_total += table_amo
            hap_total_view = format(hap_total,',')
            self.hap_total_widget.setText(hap_total_view)
    
    def other_reg_reset(self):
        global hap_total,j
        hap_total = 0; j = 0
        self.week_widget.clear()
        self.hap_total_widget.clear()
        self.gubun_name_combo_widget.setCurrentText('선택')
        self.other_name_combo_widget.clear()
        self.other_income_tableWidget.setRowCount(0)
        # self.other_income_tableWidget.setRowCount(1)
        
        # self.counter_name_widget.clear()
        self.amount_widget.clear()
        self.marks_widget.clear()
        try:
            self.gubun_name_combo_widget.currentTextChanged.disconnect(self.other_name_combo)
        except TypeError:
            pass  # 연결되어 있지 않을 경우 발생하는 예외 무시
        # 시그널 다시 연결
        self.gubun_name_combo_widget.currentTextChanged.connect(self.other_name_combo)

    def file_close(self):
        self.other_reg_reset()
        self.close()
    
    def closeEvent(self,event):
        self.other_reg_reset()
        event.accept()

    def remove_row(self):
        global j
        selectedRows = set()
        for item in self.other_income_tableWidget.selectedItems():
            selectedRows.add(item.row())

        for row in sorted(selectedRows, reverse=True):
            self.other_income_tableWidget.removeRow(row)
            j -= 1
        
        self.re_calculate()
    
    def file_save(self):
        global hap_total, Bank,j
        hap_total = 0; data2 = []
        from register.register_sql import other_register
        from basic.hun_name_2 import other_hun_mokhang_values
        #try:
        
        if self.other_income_tableWidget.rowCount() > 0 :
            for row in range(self.other_income_tableWidget.rowCount()):
                v_date = datetime.strptime(now,'%Y-%m-%d')
                v_year = int(self.year_widget.text())
                v_month = int(self.month_widget.text())
                user_name = self.user_widget.text()
                if not self.week_widget.text().isdigit():
                    QMessageBox.about(self, '오류', '주차는 숫자여야 합니다.')
                    self.week_widget.clear()
                    self.week_widget.setFocus()
                    return

                v_week = int(self.week_widget.text())
                v_gubun = self.gubun_name_combo_widget.currentText()
                view_data = self.other_income_tableWidget.item(row, 0)
                if view_data == None or view_data.text() == "":
                    self.week_widget.setFocus()
                    return
                # name_diff = self.other_income_tableWidget.item(row,0).text()
                hun_mok = self.other_name_combo_widget.currentText()
                if not hun_mok or hun_mok == '선택': # == today.month():
                    QMessageBox.about(self, '입력누락', "'기타소득 명칭'을 선택하여 주세요")
                    self.other_name_combo_widget.setFocus()
                    return
                hun_hang_list = other_hun_mokhang_values(v_year,hun_mok)
                hun_hang = str(hun_hang_list[0])
                amo_txt = self.other_income_tableWidget.item(row,0).text()
                amount = int(amo_txt.replace(',',''))
                Bank = self.other_income_tableWidget.item(row,1).text()
                marks = self.other_income_tableWidget.item(row,2).text()
                data2 = (v_date, v_year, v_month, v_week, None, None, v_gubun, hun_hang, hun_mok, amount, None, Bank, marks, user_name)
                # print(data2)
                other_register(data2)

            self.other_income_tableWidget.clearContents()  # 성도명 코드
            self.other_income_tableWidget.setRowCount(1)
            self.hap_total_widget.clear()
            # self.counter_name_widget.clear()
            self.amount_widget.clear()

            hap_total = 0; j = 0
            QMessageBox.about(self,'저장',"헌금 내역이 저장되었습니다.!!!")
            self.gubun_name_combo_widget.setFocus()
 
        else:
            QMessageBox.about(self,'저장',"저장할 내역이 없습니다.!!!")
            self.gubun_name_combo_widget.setFocus()
            return
        # except pymysql.Error as e: #ValueError:
        #         QMessageBox.about(self, "입력오류", f"에러 발생: {e}")

                
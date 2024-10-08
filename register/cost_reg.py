import pymysql
import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QTableWidget, QDialog, QPushButton, QAbstractItemView
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from datetime import datetime
import configparser, hashlib

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 
j = 1
cost_imsi = []

form_class = uic.loadUiType("./ui/cost_reg_form.ui")[0]

class Cost_register(QDialog, QTableWidget, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.setWindowTitle('일일 지출내역 등록')
        
        # Initialize widgets and variables
        self.initialize_widgets()
        self.initialize_variables()

    def initialize_widgets(self):

        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.year_widget.editingFinished.connect(self.handle_year_editing)
        self.month_widget.editingFinished.connect(self.gubun_combobox)
        self.week_widget.textChanged.connect(self.gubun_combobox)
        self.gubun_combo_widget.currentTextChanged.connect(self.hang_combobox)
        self.hang_combo_widget.currentTextChanged.connect(self.mok_combobox)
        self.mok_combo_widget.currentTextChanged.connect(self.semok_combobox)
        # self.semok_combo_widget.currentTextChanged.connect(self.cost_detail_set)
        self.amount_widget.textChanged.connect(self.on_amount_changed)
        self.amount_widget.editingFinished.connect(self.banks_combobox)
        self.cost_tableWidget.itemChanged.connect(self.on_item_changed)
        self.marks_widget.editingFinished.connect(self.data_append)
        self.cost_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정

    def initialize_variables(self):
        global gubun, hap_total
        hap_total = 0
        self.new_input = False
        self.cost_tableWidget.setRowCount(0)
        self.cost_date_widget.setDate(today)

        self.year_widget.setText(str(today.year())) # = QLabel(order_sign1)
        self.month_widget.setText(str(today.month()))
        self.user_widget.setText(self.user_confirm()[0])
        # self.month_widget.setFocus()
        
    def showEvent(self, event):
        super(Cost_register, self).showEvent(event)
        self.set_cursor_position()

    def set_cursor_position(self):
        # 커서를 특정 위치로 설정합니다 (예: QLineEdit)
        self.month_widget.setFocus()
        self.month_widget.setCursorPosition(0)  # 커서를 맨 앞에 위치시킵니다

    def cost_reg_button(self):
        precost_data_call_Button = QPushButton("이전비용 불러오기")
        precost_data_call_Button.clicked.connect(self.pre_cost_data_call)
        addpum_button = QPushButton("비용등록")
        addpum_button.clicked.connect(self.data_append)
        
        hap_recalculator_button = QPushButton("합계_재계산")
        hap_recalculator_button.clicked.connect(self.re_calculate)

        pumsave_button = QPushButton("비용,저장")
        pumsave_button.clicked.connect(self.file_save)
        pumcancel_button = QPushButton("닫기(저장취소)")
        pumcancel_button.clicked.connect(self.file_close)
        remove_row_button = QPushButton("행삭제 버튼")
        remove_row_button.clicked.connect(self.remove_row)

        serch_cost_button = QPushButton("비용,저장")
        serch_cost_button.clicked.connect(self.serch_cost)
        cost_reset_button = QPushButton("비용리셋")
        cost_reset_button.clicked.connect(self.cost_reset)

    def handle_year_editing(self):
        self.gubun_combo_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        
    # def user_name_confirm(self):
    #     from user.for_user_sql import user_infor_sql
    #     config = configparser.ConfigParser()
    #     config.read(r"./register/config.ini")
    #     user_id = config['user']['user_id']
    #     user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
    #     user_name = user_info[0][0]
    #     # user_reg = str(user_name_infor[5])       # user_reg_check의 권한을 가져와서
    #     # # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
    #     # user_reg_check = user_infor_hash(user_reg)  # user_reg_check를 hash화 한다.
        
    #     config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    #     # config['user'][user_reg_check] = user_reg_check
    
    #     return user_name
    
    def on_amount_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        amount_value_text = self.amount_widget.text()
        try:
            if amount_value_text != "" and amount_value_text != "-" :
                amount_value = int(amount_value_text.replace(",", ""))
                self.amount_widget.setText(f"{amount_value:,}")  # 숫자를 쉼표로 포맷팅
        except ValueError:
            QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")
            self.amount_widget.clear()
            self.amount_widget.setFocus()
            return
    
    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if self.new_input != True:
            if col == 4:  # 8번째 열
                try:
                    if item.text() != '-':  # '-'를 입력한 경우에는 예외를 발생시키지 않고 넘어감
                        value = int(item.text().replace(",", ""))
                        item.setText(f"{value:,}")  # 숫자를 쉼표로 포맷팅
                except ValueError:
                        QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")

    def cost_reset(self):
        global hap_total, j
        self.cost_tableWidget.setRowCount(0)
        hap_total = 0
        self.cost_hap_widget.clear()
        self.amount_widget.clear()
        self.banks_combo_widget.clear()
        self.cost_detail_widget.clear()
        self.marks_widget.clear()
        self.month_widget.setFocus()
        j = 1
    
    def combo_reset(self):
        self.gubun_combo_widget.clear()
        self.hang_combo_widget.clear()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()

    def pre_cost_data_call(self): # 이전비용 가져오기
        global hap_total
        from basic.cost_call import pre_cost_call
        hap_total = 0

        self.cost_reset()
        
        Y1 = int(self.year_widget.text())
        M1 = int(self.month_widget.text())
        W1 = int(self.week_widget.text()) if self.week_widget.text().isdigit() else None
        if W1 == None:
            QMessageBox.about(self, '오류', '주 차는 숫자여야 합니다.')
            self.week_widget.clear()
            self.week_widget.setFocus()
            return
        gubun = self.gubun_combo_widget.currentText()
        if not gubun or gubun == '선택': # == today.month():
            QMessageBox.about(self, '입력누락', "'구분'을 선택하여 주세요")
            self.gubun_combo_widget.setFocus()
            return
        pre_cost = pre_cost_call(Y1,M1,W1,gubun)
        rowCount = len(pre_cost)
        self.cost_tableWidget.setRowCount(rowCount)
        if rowCount > 0:
            for j in range(rowCount):  # j는 행 c는 열
                hang, mo, sem, det, amo_int, bank, mar = pre_cost[j]
                amo = format(amo_int,",")
                
                self.cost_tableWidget.setItem(j,0,QTableWidgetItem(hang))
                self.cost_tableWidget.setItem(j,1,QTableWidgetItem(mo))
                self.cost_tableWidget.setItem(j,2,QTableWidgetItem(sem))
                self.cost_tableWidget.setItem(j,3,QTableWidgetItem(det))
                self.cost_tableWidget.setItem(j,4,QTableWidgetItem(amo))
                self.cost_tableWidget.setItem(j,5,QTableWidgetItem(bank))
                self.cost_tableWidget.setItem(j,6,QTableWidgetItem(mar))
                self.cost_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.cost_tableWidget.resizeColumnsToContents()
                if self.cost_tableWidget.item(j,4) != None:
                    self.cost_tableWidget.item(j,4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                # self.set_table_alignment(j)
                hap_total += amo_int
            self.cost_hap_widget.setText(format(hap_total,","))
        else:
            QMessageBox.about(self, "자료없음","지료가 없습니다.")
            self.cost_tableWidget.setRowCount(0)
            # self.cost_tableWidget.setRowCount(1)

    # def set_table_alignment(self, row):
    #     for col in range(7):
    #         item = self.cost_tableWidget.item(row, col)
    #         if item:
    #             if col == 4:
    #                 item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    #             elif col == 5 :
    #                 item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
    #             else :
    #                 item.setTextAlignment(Qt.AlignLeft | Qt.AlignHCenter)
                    

    def remove_row(self):
        global deleted_row_count
        deleted_row_count = 0
        selectedRows = set()
        for item in self.cost_tableWidget.selectedItems():
            selectedRows.add(item.row())

        for row in sorted(selectedRows, reverse=True):
            self.cost_tableWidget.removeRow(row)
            deleted_row_count += 1
        
        self.re_calculate()

        row_count = self.cost_tableWidget.rowCount()
        if row_count == 0:
            # self.cost_tableWidget.clearContents()
            self.cost_tableWidget.setRowCount(0)

    def gubun_combobox(self):
        from basic.hun_name_2 import gubun_values_check
        global gubun
        confirm_data = self.user_confirm()
        Ge_check = int(confirm_data[1]) # 일반회계
        # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
        
        # v_year = int(self.year_widget.text())
        # if v_year == today.year():
        self.gubun_combo_widget.clear()
        self.gubun_combo_widget.addItems(["선택"] + gubun_values_check(Ge_check))
        gubun = self.gubun_combo_widget.currentText()
         
    def hang_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자
        from basic.cost_select import cost_hang_values
        self.hang_combo_widget.clear()
        gubun = self.gubun_combo_widget.currentText()
        # hang_0 = ["선택"]
        v_year = self.year_widget.text()
        hang_list = []
        # self.hang_combo_widget.addItems(hang_0)
        hang_tuple = cost_hang_values(v_year,gubun)
        for hang in hang_tuple:
            cost1, id = hang
            hang_list.append(cost1)
        self.hang_combo_widget.addItems(["선택"] + hang_list)
        # self.hang_combo_widget.currentTextChanged.connect(self.mok_combobox)
        
    def mok_combobox(self):
        from basic.cost_select import cost_mok_values
        cost_hang = self.hang_combo_widget.currentText()
        self.mok_combo_widget.clear()
        self.semok_combo_widget.clear()
        self.cost_detail_widget.clear() # 적요
        self.amount_widget.clear()  # 금액
        self.marks_widget.clear() # 비고
        try:
            if cost_hang : #   len(cost_mok_values(cost_hang)) > 0: 
                v_year = self.year_widget.text()
                mok_list = []
                mok_tuple = cost_mok_values(v_year,cost_hang)
                for mok in mok_tuple:
                    mok_1, id = mok
                    mok_list.append(mok_1)
                self.mok_combo_widget.addItems(["선택"] + mok_list)
                # self.mok_combo_widget.currentTextChanged.connect(self.semok_combobox)
        except pymysql.Error as e: #ValueError:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            return

    def semok_combobox(self):
        from basic.cost_select import cost_semok_values
        mok = self.mok_combo_widget.currentText()
        v_year = self.year_widget.text()
        # hang = self.hang_combo_widget.currentText()
        self.semok_combo_widget.clear()
        self.cost_detail_widget.clear() # 적요
        self.amount_widget.clear()  # 금액
        self.marks_widget.clear() # 비고
        
        if len(cost_semok_values(v_year,mok)) > 0:
            semok_list = []
            semok_tuple = cost_semok_values(v_year,mok)
            for semok in semok_tuple:
                semok_1, id = semok
                semok_list.append(semok_1)
            self.semok_combo_widget.addItems(["선택"] + semok_list)
            # self.semok_combo_widget.currentTextChanged.connect(self.cost_detail_set)

    # def cost_detail_set(self):
    #     cost_semok = self.semok_combo_widget.currentText()
    #     self.cost_detail_widget.setText(cost_semok)

    def banks_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자 
        from payed_account.payed_account_sql import payed_account_values
        self.banks_combo_widget.clear()
        gubun = self.gubun_combo_widget.currentText()
        bank1 = payed_account_values('reg',gubun)
        self.banks_combo_widget.addItems(["선택"] + bank1)

        self.banks_combo_widget.currentTextChanged.connect(self.marks_input)
        
    def marks_input(self):
        from payed_account.payed_account_sql import payed_account_values
        payed_acc_name = self.banks_combo_widget.currentText()
        gubun = self.gubun_combo_widget.currentText()
        marks = payed_account_values(payed_acc_name, gubun) #payed_acc_name)
        marks_text = ''.join([f"{item[0]} {item[1]}" for item in marks]) # '.join(marks)  #  이 코드는 marks_text 변수가 리스트로 되었다고 함 ', '.join([payed_acc_name,marks])
        self.marks_widget.setText(marks_text)

    def data_append(self):
        global hap_total, j
        self.new_input = True
        try:
            re_count = self.cost_tableWidget.rowCount()
            idf_4 = self.hang_combo_widget.currentText()
            if idf_4 != '선택':
                idf_5 = self.mok_combo_widget.currentText()
                if idf_5 != '선택':
                    idf_6 = self.semok_combo_widget.currentText()
                    if idf_6 != '선택':
                        idf_7 = self.cost_detail_widget.text()
                        idf_8_s = self.amount_widget.text()
                        if idf_8_s == "":
                            self.amount_widget.text()
                            QMessageBox.about(self, "금액오류","금액이 없습니다.")
                            return
                        else: 
                            # idf_8_s != "" or idf_8_s != '-':
                            idf_8_amo = int(idf_8_s.replace(',',''))
                            idf_8 = int(idf_8_amo)
                            amount = format(idf_8,",")
                        idf_9 = self.banks_combo_widget.currentText()
                        if idf_9 != "선택":
                            idf_10 = self.marks_widget.text()
                            if re_count != 0 :
                                confirm = self.cost_tableWidget.item(re_count, 0)
                                if confirm == None:
                                    j = re_count + 1
                            else:
                                self.cost_tableWidget.setRowCount(1)
                            if j != 1:
                                self.cost_tableWidget.insertRow(j-1)
                            self.cost_tableWidget.setItem((j-1),0,QTableWidgetItem(idf_4))
                            self.cost_tableWidget.setItem((j-1),1,QTableWidgetItem(idf_5))
                            self.cost_tableWidget.setItem((j-1),2,QTableWidgetItem(idf_6))
                            self.cost_tableWidget.setItem((j-1),3,QTableWidgetItem(idf_7))
                            self.cost_tableWidget.setItem((j-1),4,QTableWidgetItem(amount))
                            self.cost_tableWidget.setItem((j-1),5,QTableWidgetItem(idf_9))
                            self.cost_tableWidget.setItem((j-1),6,QTableWidgetItem(idf_10))
                            self.cost_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                            if self.cost_tableWidget.item(j-1,4) != None:
                                self.cost_tableWidget.item(j-1,4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)

                            hap_total += idf_8
                            hap_view = format(hap_total,",")
                            self.cost_hap_widget.setText(hap_view)
                            self.cost_tableWidget.scrollToBottom()   # 자동 스크롤

                            self.hang_combo_widget.setCurrentText('선택')
                            self.mok_combo_widget.clear()
                            self.semok_combo_widget.clear()
                            self.cost_detail_widget.clear()
                            self.amount_widget.clear()
                            self.banks_combo_widget.clear()
                            self.marks_widget.clear()
                            j +=1
                            self.new_input = True
                            self.hang_combo_widget.setFocus()
                            return
                        else:
                            QMessageBox.about(self, "계좌선택오류","계좌 선택에 오류가 있습니다.")
                    else:
                        self.semok_combo_widget.setFocus()
                        return
                else:
                    self.mok_combo_widget.setFocus()
                    return
                # else:
                #     self.amount_widget.clear()
                #     QMessageBox.about(self, "금액 입력오류","숫자만 입력하여 주세요")
            else:
                self.hang_combo_widget.setFocus()
                return
        
        except pymysql.Error as e: #ValueError:  
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            self.registed_name.setFocus()
            return
        
    def re_calculate(self):
        global hap_total
        hap_total = 0
        row_count = self.cost_tableWidget.rowCount()
        for i in range(row_count):
            imsi_amo_Txt = self.cost_tableWidget.item(i,4)
            if imsi_amo_Txt and imsi_amo_Txt.text() != None:
                imsi_amo = imsi_amo_Txt.text()
                table_amo = int(imsi_amo.replace(',',''))
                amount = format(table_amo,',')
                self.cost_tableWidget.setItem(i,4,QTableWidgetItem(amount))
                if self.cost_tableWidget.item(i,4) != None:
                    self.cost_tableWidget.item(i,4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                hap_total += table_amo
            else:
                amount = '0'
                self.cost_tableWidget.setItem(i,4,QTableWidgetItem(amount))
                if self.cost_tableWidget.item(i,4) != None:
                    self.cost_tableWidget.item(i,4).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            hap_view = format(hap_total,',')
            self.cost_hap_widget.setText(hap_view)

    def serch_cost(self):
        from serch.cost_serch import cost_Serch
        self.co_serch = cost_Serch()
        self.co_serch.exec()
        
        self.show()
    
    def set_read_only(self, widget):
        widget.setReadOnly(True)

    def file_close(self):
        self.combo_reset()
        self.cost_reset()
        self.week_widget.clear()

        self.close()

    def closeEvent(self,event):
        self.combo_reset()
        self.cost_reset()
        self.week_widget.clear()
        event.accept()

    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(today.year()):
            return False  # 현재 년도와 같으면 False 반환
        else:
            if Y1 != today.year():
                reply = QMessageBox.question(self, '', "'지출 년도'가 현재의 '년도'와 다릅니다. 계속 진행하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 사용자가 OK를 클릭한 경우에만 진행
                    # 여기에 진행할 코드 작성
                    return True  # 현재 년도와 다르더라도 사용자가 OK를 했으므로 동의 False 반환,  동의 하지 않으면 True
                    # pass
                else:
                    # 사용자가 Cancel을 클릭한 경우
                    self.year_widget.setFocus()

                    return False
                
            # QMessageBox.about(self, '', "'지출년도'가 현재의 '년도'와 같아야 합니다. ")
            self.week_widget.clear()
            self.gubun_combo_widget.clear()
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환

    def file_save(self):
        from register.register_sql import cost_register
        global hap_total, j
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
        
        try:
            # if self.week_widget.text()!= '' :
            s_date = self.cost_date_widget.text()
            v_date = datetime.strptime(s_date,'%Y-%m-%d')
            v_year = self.year_widget.text()
            if s_date is None or v_year == "":
                self.year_widget.setFocus()
                return
            v_year = int(v_year)
            v_month = self.month_widget.text()
            if v_month is None or v_month == "":
                self.month_widget.setFocus()
                return
            v_month=int(v_month)
            user_name = self.user_widget.text()
            
            if v_month != today.month():
                reply = QMessageBox.question(self, '', "'지출월'이 현재의 '월'과 다릅니다. 계속 진행하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 사용자가 OK를 클릭한 경우에만 진행
                    # 여기에 진행할 코드 작성
                    pass
                else:
                    # 사용자가 Cancel을 클릭한 경우
                    self.month_widget.setFocus()
                    return
            # v_year == int(str(today.year()))
            v_week = self.week_widget.text()
            if v_week is None or v_week == '':
                QMessageBox.about(self, '입력누락', "'몇번째 '주' 인지 입력하여 주세요")
                self.week_widget.setFocus()
                return
            v_week = int(v_week)
            # if not v_week: # == today.month():
            #     QMessageBox.about(self, '입력누락', "'몇번째 '주' 인지 입력하여 주세요")
            #     self.week_widget.setFocus()
            
            v_gubun = self.gubun_combo_widget.currentText()
            if not v_gubun or v_gubun == '선택': # == today.month():
                QMessageBox.about(self, '입력누락', "'구분'을 선택하여 주세요")
                self.gubun_combo_widget.setFocus()
                return

            rowCount = self.cost_tableWidget.rowCount()
            if rowCount > 0 :
                for i in range(rowCount):
                    v_hang = self.cost_tableWidget.item(i, 0).text()
                    v_mok = self.cost_tableWidget.item(i, 1).text()
                    v_semok = self.cost_tableWidget.item(i, 2).text()
                    if v_semok == '':
                        v_semok = None
                    else:
                        v_semok = self.cost_tableWidget.item(i, 2).text()
                    v_memo = self.cost_tableWidget.item(i, 3).text()
                    amo_txt = self.cost_tableWidget.item(i, 4).text()
                    v_amount = int(amo_txt.replace(',',''))
                    v_bank = self.cost_tableWidget.item(i, 5).text()
                    if v_bank == '':
                        v_bank = None
                    else:
                        v_bank = self.cost_tableWidget.item(i, 5).text()

                    if self.cost_tableWidget.item(i, 6).text() == "" :
                        v_marks = None
                    else:
                        v_marks = self.cost_tableWidget.item(i, 6).text()
                    
                    # if any(cell_item == None for cell_item in [v_hang, v_mok, v_semok, v_memo, v_amount, v_bank, v_marks]):
                    #     QMessageBox.about(self, '에러', '저장할 데이터에 누락된 값이 있습니다.')
                    #     return
                    
                    data = (v_date,v_year,v_month,v_week,v_gubun,v_hang,v_mok,v_semok, v_memo, v_amount,v_bank,v_marks, user_name)
                    cost_register(data)
                    
                self.cost_hap_widget.clear()
                hap_total = 0
                # self.cost_tableWidget.clearContents()
                self.cost_tableWidget.setRowCount(0)  # 0으로 하면 라인 추가에 문제가 발생함
                cost_imsi.clear()
                j = 1
                QMessageBox.about(self,'',"저장이 완료되었습니다.!!!")
            else:
                QMessageBox.about(self,'',"저장할 내역이 없습니다.!!!")
 
        except pymysql.Error as e: #ValueError:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            self.week_widget.setFocus()
            return
    
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
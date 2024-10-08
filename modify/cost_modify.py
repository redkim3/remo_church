import configparser, os, hashlib
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic
from PyQt5.QtWidgets import *

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
m_today = QDate.currentDate()
m_today_ISO = m_today.toString(Qt.ISODate)
modi_year = m_today.year()

hun_imsi = []; hap_total = 0 ; n = 0

form_class = uic.loadUiType("./ui/cost_modi_form.ui")[0]

class Cost_Modify(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('지출내역 수정')
        global mok
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        m_year = str(m_today.year())
        m_month = str(m_today.month())
        self.modi_hun_table = QTableWidget()
        user_name = self.user_confirm()[0]
        self.user_widget.setText(user_name)
        self.year_widget.setText(m_year)
        self.month_widget.setText(m_month)
        self.week_widget.text()
        self.month_widget.setFocus()
        # 버튼을 인스턴스 변수로 정의합니다.
        self.new_input = False
        self.hap_recalculator_button.setEnabled(False)
        self.remove_row_Button.setEnabled(False)
        self.modi_row_save_button.setEnabled(False)
        self.accounting_change_button.setEnabled(False)

        self.cost_modi_tableWidget.itemChanged.connect(self.on_item_changed)
        self.month_widget.editingFinished.connect(self.gubun_combobox)
        self.month_widget.editingFinished.connect(self.modi_tablewidget_reset)
        self.gubun_combo_widget.currentTextChanged.connect(self.special_acc_eraser)
        self.cost_modi_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색 설정

    # def button_click(self):
    #     self.cost_serch_Button = QPushButton("검색")
    #     self.cost_serch_Button.clicked.connect(self.cost_serch)

    #     self.re_calculate_button = QPushButton("합계금액 재계산")
    #     self.re_calculate_button.clicked.connect(self.re_calculate)

    #     self.remove_row_Button = QPushButton("선택행 삭제")
    #     self.remove_row_Button.clicked.connect(self.remove_row)

    #     self.row_modi_save_Button = QPushButton("1행 부분수정")
    #     self.row_modi_save_Button.clicked.connect(self.row_modi_save)

    #     self.modi_cancel_button = QPushButton("종료(저장취소)")
    #     self.modi_cancel_button.clicked.connect(self.close)

    #     self.accounting_change_button = QPushButton("선택행 계정변경")
    #     self.accounting_change_button.clicked.connect(self.accounting_change)

    def special_acc_eraser(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        gubun_special = self.gubun_combo_widget.currentText()
        if gubun_special == '특별회계': # == today.month():
            self.gubun_combo_widget.setCurrentText("선택")
            QMessageBox.about(self, '입력제외', "'계정별 원장보기'를 이용하세요")
            self.week_widget.setFocus()
            return
        else:
            if gubun_special != "선택":
                self.cost_serch()
 
    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if self.new_input != True:
            if col == 3:  # 8번째 열
                try:
                    value = int(item.text().replace(",", ""))
                    item.setText(f"{value:,}")  # 숫자를 쉼표로 포맷팅
                except ValueError:
                    QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")

    def gubun_combobox(self):  # 검색기능 수행
        from basic.hun_name_2 import gubun_values_check
        confirm_data = self.user_confirm()
        Ge_check = int(confirm_data[1]) # 일반회계
        # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
        self.gubun_combo_widget.clear()
        # self.gubun_combo_widget.currentText()
        # gubun_select = ['선택']
        # gubun_list = [item[0] for item in gubun_values()]
        # self.gubun_combo_widget.addItems(gubun_select)
        self.gubun_combo_widget.addItems(['선택'] + gubun_values_check(Ge_check))  #  콤보 데이터 추가  
        self.gubun_combo_widget.currentText()
    
    def accounting_change(self):
        from modify.cost_modify_reg import Cost_modify_register
        sel_row = self.cost_modi_tableWidget.currentRow()
        id = self.cost_modi_tableWidget.item(sel_row,8).text()
        self.cost_modify_register = Cost_modify_register(str(id))
        self.cost_modify_register.exec()
        self.show()
        self.cost_serch()

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

    def cost_serch(self):
        from basic.cost_serch import week_cost_serch
        hap_total = 0
        self.modi_tablewidget_reset()
        self.new_input = True
        self.hap_recalculator_button.setEnabled(True)
        self.remove_row_Button.setEnabled(True)
        self.modi_row_save_button.setEnabled(True)
        self.accounting_change_button.setEnabled(True)

        # try:
        Y1=self.year_widget.text()
        M1=self.month_widget.text()
        W1=self.week_widget.text()
        if not Y1 : 
            # QMessageBox.about(self, "입력에러", "년도를 확인해 주세요.")
            self.year_widget.setFocus()
            return
        if not M1 :
            # QMessageBox.about(self, "입력에러", "월을 확인해 주세요.")
            self.month_widget.setFocus()
            return
        if not W1 :
            # QMessageBox.about(self, "입력에러", "주를 확인해 주세요.")
            self.week_widget.setFocus()
            return
        
        gubun = self.gubun_combo_widget.currentText()
        
        cost_list = week_cost_serch(Y1, M1, W1, gubun)
        if not cost_list:
            self.week_widget.setFocus()
            return

        for row, data in enumerate(cost_list):
            if row != 0:
                self.cost_modi_tableWidget.insertRow(row)
            date = data[0].strftime('%Y-%m-%d')
            cost_hang = data[1]
            cost_mok = data[2]
            cost_semok = data[3]
            cost_memo = data[4]
            amount = data[5]
            hap_total += int(amount)
            amount_T = format(amount,",")
            pay_banks = data[6] # 지급통장 분류
            marks= data[7]
            if marks == None:
                marks = ""
            id= data[8]

            self.cost_modi_tableWidget.setItem(row, 0,QTableWidgetItem(date))
            self.cost_modi_tableWidget.setItem(row, 1,QTableWidgetItem(cost_hang))
            self.cost_modi_tableWidget.setItem(row, 2,QTableWidgetItem(cost_mok))
            self.cost_modi_tableWidget.setItem(row, 3,QTableWidgetItem(cost_semok))
            self.cost_modi_tableWidget.setItem(row, 4,QTableWidgetItem(cost_memo))
            self.cost_modi_tableWidget.setItem(row, 5,QTableWidgetItem(amount_T))
            if self.cost_modi_tableWidget.item(row, 5) != None:
                self.cost_modi_tableWidget.item(row, 5).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.cost_modi_tableWidget.setItem(row, 6,QTableWidgetItem(pay_banks))
            self.cost_modi_tableWidget.setItem(row, 7,QTableWidgetItem(marks))
            self.cost_modi_tableWidget.setItem(row, 8,QTableWidgetItem(str(id)))
            self.cost_modi_tableWidget.resizeColumnsToContents()
            self.cost_modi_tableWidget.setColumnHidden(8, True)
        self.cost_modi_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        hap_total_view = format(hap_total,',')
        self.cost_hap_widget.setText(hap_total_view)
        self.new_input = False
        
    def row_modi_save(self): #cell_changed
        from modify.modifed_sql_save import update_cost_db_sql
        sel_row = None
        user = self.user_widget.text()
        change_data = []
        sel_row = self.cost_modi_tableWidget.currentRow()
        c_count = self.cost_modi_tableWidget.columnCount()
        for c_cnt in range(c_count):
            if self.cost_modi_tableWidget.item(sel_row,c_cnt) != None:
                if c_cnt == 5 or c_cnt == 8:
                    change_int = self.cost_modi_tableWidget.item(sel_row, c_cnt).text()
                    change_data_0 = int(change_int.replace(",",""))
                elif c_cnt >= 1 and c_cnt <= 3 :
                    continue
                else:
                    change_data_0 = self.cost_modi_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data_0 = None
            if c_cnt ==8:
                change_data.append(user)  # change_data_0에 테이이블 데이터를 하나씩 저장할때 테이블에 없는 user 삽입
                change_data.append(change_data_0)
            else:
                change_data.append(change_data_0)

        # 데이터베이스에 연결하여 값을 업데이트
        update_cost_db_sql(change_data)
        change_data = []
        # QMessageBox.information(None, "완료", "지출내역 정보가 변경 되었습니다.")
        self.cost_serch()
    
    # def cost_all_modi_save(self): #cell_changed  일괄수정 삭제
    #     from modify.modifed_sql_save import update_cost_db_sql
    #     user = self.user_widget.text()
    #     change_data = []
    #     r_count = self.cost_modi_tableWidget.rowCount()
    #     c_count = self.cost_modi_tableWidget.columnCount()

    #     for row in range(r_count):
    #         for col in range(c_count):
    #             if self.cost_modi_tableWidget.item(row, col) != None:
    #                 if col == 5 or col == 8:
    #                     change_int = self.cost_modi_tableWidget.item(row, col).text()
    #                     change_data_0 = int(change_int.replace(",",""))
    #                 else:
    #                     change_data_0 = self.cost_modi_tableWidget.item(row, col).text()
    #             else:
    #                 change_data_0 = None
                
    #             if col == 8:
    #                 change_data.append(user)
    #                 change_data.append(change_data_0)
    #             else:
    #                 change_data.append(change_data_0)

    #         update_cost_db_sql(change_data)
    #         change_data = []

    #     QMessageBox.information(None, "완료", "지출내역 정보가 변경 되었습니다.")
    #     self.cost_serch()
    
    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(m_today.year()):
            self.hun_gubun_combobox()
            return False  # 현재 년도와 같으면 False 반환
        else:
            QMessageBox.about(self, '', "'지출년도'가 현재의 '년도'와 같아야 합니다. ")
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환
    
    def remove_row(self):
        from modify.modifed_sql_save import cost_delete_row_from_database
        selected_rows = set(index.row() for index in self.cost_modi_tableWidget.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            id_item = self.cost_modi_tableWidget.item(row, 8)  # id 값을 나타내는 열
            if id_item != None:
                id_value = int(id_item.text())
                cost_delete_row_from_database(id_value)
            self.cost_modi_tableWidget.removeRow(row)

        self.re_calculate()
        QMessageBox.about(self, '', "'선택한 행이 삭제 되었습니다.")
        self.cost_serch()

    def re_calculate(self):
        global hap_total
        hap_total = 0
        self.cost_hap_widget.clear()
        
        row_count = self.cost_modi_tableWidget.rowCount()
        if row_count > 0:
            for i in range(row_count):
                imsi_amo = self.cost_modi_tableWidget.item(i,5).text()
                table_amo = int(imsi_amo.replace(',',''))
                amount = format(table_amo,',')
                self.cost_modi_tableWidget.setItem(i, 5, QTableWidgetItem(amount))
                if self.cost_modi_tableWidget.item(i, 5) != None:
                    self.cost_modi_tableWidget.item(i, 5).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                hap_total += table_amo
                hap_sum_view = format(hap_total,',')
                self.cost_hap_widget.setText(hap_sum_view)
        else:
            self.cost_hap_widget.clear()
            QMessageBox.about(self, '', "'테이터가 없습니다.. ")
    
    def modi_tablewidget_reset(self):
        self.cost_modi_tableWidget.setRowCount(0)
        self.cost_modi_tableWidget.setRowCount(1)
        self.cost_hap_widget.clear()
        self.hap_recalculator_button.setEnabled(False)
        self.remove_row_Button.setEnabled(False)
        self.modi_row_save_button.setEnabled(False)
        self.accounting_change_button.setEnabled(False)

    def file_close(self):
        self.modi_tablewidget_reset()
        self.close()

    def closeEvent(self,event):
        self.modi_tablewidget_reset()
        event.accept()


    def handle_item_edit(self, row, column):
        if column == 0:  # Assuming the column index of the 'Item' column
            # Get the current item text 
            current_text = self.cost_modi_tableWidget.item(row, column).text()

            # Display a combo box or a dialog to allow the user to select a new item
            new_item, ok = QInputDialog.getItem(self, "Edit Item", "Select an item:",
                                                items=['Item 1', 'Item 2', 'Item 3'], current=current_text)
            if ok:
                # Update the item in the table widget
                self.cost_modi_tableWidget.item(row, column).setText(new_item)

    def user_infor_hash(self,data):
        # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
        hasher = hashlib.sha256()
        # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
        hasher.update(data.encode('utf-8'))
        # 해시된 결과 반환
        return hasher.hexdigest()

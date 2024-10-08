import configparser, os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from basic.hun_name_2 import gubun_values

cur_fold = os.getcwd()
# from basic.hun_name import mok_select_reg #, semok_select, hang_select

m_today = QDate.currentDate()
m_today_ISO = m_today.toString(Qt.ISODate)
modi_year = m_today.year()

hun_imsi = []; hap_total = 0 ; n = 0

form_class = uic.loadUiType("./ui/hun_modi_form.ui")[0]

class Hun_modify(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('헌금내역 수정')
        global mok
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        
        self.hun_detail_combo.hide()     # 헌금세부 콤보
        m_year = str(m_today.year())
        m_month = str(m_today.month())
        # self.modi_hun_tableWidget = QTableWidget()
        self.year_widget.setText(m_year)      # = QLabel(order_sign1)
        self.month_widget.setText(m_month)
        self.month_widget.setFocus()
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)
        self.re_calculate_button.setEnabled(False)
        self.hun_row_modi_Button.setEnabled(False)
        self.hun_account_modi_Button.setEnabled(False)
        self.remove_row_Button.setEnabled(False)
        
        self.month_widget.editingFinished.connect(self.year_compare)
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.modi_hun_tableWidget.itemChanged.connect(self.on_item_changed)
        self.month_widget.editingFinished.connect(self.hun_gubun_combobox)
        self.week_widget.editingFinished.connect(self.hun_gubun_combobox)
        self.gubun_name_combo_widget.currentTextChanged.connect(self.hun_name_combo)
        self.hun_name_widget.currentTextChanged.connect(self.tablewidget_reset)
        self.modi_hun_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정
        
    # def button(self):
    #     serch_Button = QPushButton("검색")
    #     serch_Button.clicked.connect(self.hun_serch)
    #     re_calculate_button = QPushButton("합계금액 재계산")
    #     re_calculate_button.clicked.connect(self.re_calculate)
    #     remove_row_Button = QPushButton("선택행 삭제")
    #     remove_row_Button.clicked.connect(self.remove_row)
    #     hun_row_modi_Button = QPushButton("1행 수정,저장")
    #     hun_row_modi_Button.clicked.connect(self.row_modi_save)
    #     hun_account_modi_Button = QPushButton("선택행 계정수정 저장")
    #     hun_account_modi_Button.clicked.connect(self.hun_account_modi_save)
    #     modi_cancel_button = QPushButton("종료(저장취소)")
    #     modi_cancel_button.clicked.connect(self.close)

    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if col == 3:  # 8번째 열 
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
        
        return user_name
        
    def hun_gubun_combobox(self):  # 헌금명칭을 넣고 나면 진행하는것
        from basic.hun_name_2 import gubun_values
        # gubun_selec = []
        # gubun_list = gubun_values()
        self.gubun_name_combo_widget.clear()  # 헌금 명칭
        self.hun_name_widget.clear()
        self.tablewidget_reset()

        # self.gubun_name_combo_widget.currentText()
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
      
        # gubun_selec = ['선택']
        # gubun_select = gubun_selec + gubun_list
        self.gubun_name_combo_widget.addItems(['선택'] + gubun_values())
        self.gubun_name_combo_widget.currentText()
    
    def tablewidget_reset(self):
        self.hap_total_widget.clear()   # 헌금 합계액 
        self.modi_hun_tableWidget.setRowCount(0)
        self.modi_hun_tableWidget.setRowCount(1)
        self.re_calculate_button.setEnabled(False)
        self.hun_row_modi_Button.setEnabled(False)
        self.hun_account_modi_Button.setEnabled(False)
        self.remove_row_Button.setEnabled(False)

    def hun_name_combo(self):
        from basic.hun_name_2 import  gubun_mok_values
        self.hun_name_widget.clear()
        self.tablewidget_reset()
        
        try:
            Y1 = int(self.year_widget.text())
            gubun = self.gubun_name_combo_widget.currentText()
            if gubun ==None:
                self.gubun_name_combo_widget.setFocus()
                return

            # hun_select = ['선택']
            # hun_list_value = 
            # hun_list = hun_select + hun_list_value
            self.hun_name_widget.addItems(['선택'] + gubun_mok_values(Y1,gubun))  #  콤보 데이터 추가 
            self.modi_hun_tableWidget.setRowCount(0)
            self.modi_hun_tableWidget.setRowCount(1)
        # self.hun_name_widget.currentTextChanged.connect(self.hun_serch)
        except TypeError:
            pass
            # QMessageBox.about(self, "입력오류","입력내용을 확인 하세요")

    def hun_serch(self):  # 검색기능 수행
        from basic.hun_serch import week_hun_list
        hap_total = 0
        self.tablewidget_reset()
        self.re_calculate_button.setEnabled(True)
        self.hun_row_modi_Button.setEnabled(True)
        self.hun_account_modi_Button.setEnabled(True)
        self.remove_row_Button.setEnabled(True)

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
        
        gubun = self.gubun_name_combo_widget.currentText()
        if not gubun or gubun == '선택': # == today.month():
            QMessageBox.about(self, '입력누락', "'구분'을 선택하여 주세요")
            self.gubun_name_combo_widget.setFocus()
            return
        mok = self.hun_name_widget.currentText()
        if not mok or mok == '선택': # == today.month():
            QMessageBox.about(self, '입력누락', "'헌금'을 선택하여 주세요")
            self.hun_name_widget.setFocus()
            return
        
        hun_income = week_hun_list(Y1, M1, W1, gubun, mok)
        if not hun_income:
            QMessageBox.about(self, "", "검색 값이 없습니다..")

        for row, data in enumerate(hun_income):
            if row != 0:
                self.modi_hun_tableWidget.insertRow(row)
            
            date = data[0].strftime('%Y-%m-%d')
            code1= data[1]
            name_diff = data[2]
            amount = data[3]
            hap_total += int(amount)
            amount_T = format(amount,",")
            bank = data[4] # 통장예입여부
            if bank == None:
                bank = ""
            marks= data[5]
            if marks == None:
                marks = ""
            id= data[6]

            self.modi_hun_tableWidget.setItem(row, 0,QTableWidgetItem(date))
            self.modi_hun_tableWidget.setItem(row, 1,QTableWidgetItem(code1))
            self.modi_hun_tableWidget.setItem(row, 2,QTableWidgetItem(name_diff))
            self.modi_hun_tableWidget.setItem(row, 3,QTableWidgetItem(amount_T))
            if self.modi_hun_tableWidget.item(row, 3) != None:
                self.modi_hun_tableWidget.item(row, 3).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.modi_hun_tableWidget.setItem(row, 4,QTableWidgetItem(bank))
            self.modi_hun_tableWidget.setItem(row, 5,QTableWidgetItem(marks))
            self.modi_hun_tableWidget.setItem(row, 6,QTableWidgetItem(str(id)))
            self.modi_hun_tableWidget.setColumnHidden(6, True)
        self.modi_hun_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        hap_total_view = format(hap_total,',')
        self.hap_total_widget.setText(hap_total_view)

    def row_modi_save(self): #cell_changed
        from modify.modifed_sql_save import update_hun_db_sql
        sel_row = None
        user = self.user_widget.text()
        change_data = []
        sel_row = self.modi_hun_tableWidget.currentRow()
        c_count = self.modi_hun_tableWidget.columnCount()
        for col in range(c_count):
            if self.modi_hun_tableWidget.item(sel_row, col) != None:
                if col == 3 or col == 6:
                    change_int = self.modi_hun_tableWidget.item(sel_row, col).text()
                    change_data_0 = int(change_int.replace(",",""))
                else:
                    change_data_0 = self.modi_hun_tableWidget.item(sel_row, col).text()

            else:
                change_data_0 = None
            
            if col == 5:
                change_data.append(change_data_0)
                change_data.append(user)  # change_data_0에 테이이블 데이터를 하나씩 저장할때 테이블에 없는 user 삽입
            else:
                change_data.append(change_data_0)
        
        # 데이터베이스에 연결하여 값을 업데이트
        update_hun_db_sql(change_data)
        change_data = []
        
        QMessageBox.information(None, "완료", "헌금내역 정보가 변경 되었습니다.")
        self.hun_serch()
    
    def hun_account_modi_save(self):
        from modify.hun_modify_reg import hun_modify_Register
        sel_row = self.modi_hun_tableWidget.currentRow()
        id = self.modi_hun_tableWidget.item(sel_row,6).text()
        self.hun_modify_register = hun_modify_Register(str(id))
        self.hun_modify_register.exec()
        self.show()
        self.hun_serch()
    
    # def hun_all_modi_save(self): #cell_changed
    #     from modify.modifed_sql_save import update_hun_db_sql

    #     change_data = []
    #     r_count = self.modi_hun_tableWidget.rowCount()
    #     c_count = self.modi_hun_tableWidget.columnCount()

    #     for row in range(r_count):
    #         for col in range(c_count):
    #             if self.modi_hun_tableWidget.item(row, col) != None:
    #                 if col == 3 or col == 6:
    #                     change_int = self.modi_hun_tableWidget.item(row, col).text()
    #                     change_data_0 = int(change_int.replace(",",""))
    #                 else:
    #                     change_data_0 = self.modi_hun_tableWidget.item(row, col).text()
    #             else:
    #                 change_data_0 = None
                
    #             change_data.append(change_data_0)

    #         update_hun_db_sql(change_data)  # hun_db_save에 있는 쿼리 실행하기
    #         change_data = []

    #     QMessageBox.information(None, "완료", "헌금내역 정보가 변경 되었습니다.")
        
    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(m_today.year()):
            # self.hun_gubun_combobox()
            return False  # 현재 년도와 같으면 False 반환
        else:
            QMessageBox.about(self, '', "'당해년도의 헌금 내역만 수정이 가능합니다.")
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환
    
    def remove_row(self):
        from modify.modifed_sql_save import delete_row_from_database
        selected_rows = set(index.row() for index in self.modi_hun_tableWidget.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            id_item = self.modi_hun_tableWidget.item(row, 6)  # id 값을 나타내는 열
            if id_item != None:
                id_value = int(id_item.text())
                delete_row_from_database(id_value)   # hun_db_save에 있는 쿼리 실행하기
            self.modi_hun_tableWidget.removeRow(row)

        self.re_calculate()

    def re_calculate(self):
        global hap_total
        hap_total = 0
        self.hap_total_widget.clear()
        
        row_count = self.modi_hun_tableWidget.rowCount()
        if row_count > 0:
            for i in range(row_count):
                imsi_amo = self.modi_hun_tableWidget.item(i,3).text()
                table_amo = int(imsi_amo.replace(',',''))
                amount = format(table_amo,',')
                self.modi_hun_tableWidget.setItem(i, 3, QTableWidgetItem(amount))
                if self.modi_hun_tableWidget.item(i, 3) != None:
                    self.modi_hun_tableWidget.item(i, 3).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                hap_total += table_amo
                hap_sum_view = format(hap_total,',')
                self.hap_total_widget.setText(hap_sum_view)
        else:
            self.hap_total_widget.clear()
            QMessageBox.about(self, '', "'테이터가 없습니다.. ")

    def file_close(self):
        self.gubun_name_combo_widget.setCurrentText('선택')
        self.hun_name_widget.clear()
        self.tablewidget_reset()
        
        self.close()
    
    def closeEvent(self,event):
        self.gubun_name_combo_widget.setCurrentText('선택')
        self.hun_name_widget.clear()
        self.tablewidget_reset()
        event.accept()

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import *
from basic.hun_name_2 import gubun_values
import configparser, os

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())

imsi = []; n = 0

form_class = uic.loadUiType("ui/payed_account_view_form.ui")[0]
j = 1
class Payed_AccountView(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        gubun_value = gubun_values()
        self.gubun_comboBox.addItems(["선택"] + gubun_value)
        self.gubun_comboBox.currentTextChanged.connect(self.payed_account_review)

        self.setWindowTitle('지출 은행명칭 및 계좌 보기')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.registed_account_tableWidget.setEditTriggers(QTableWidget.DoubleClicked)

    # def registed_data(self):
    #     from payed_account.payed_account_sql import payed_account_values 
    #     gubun = self.gubun_combobox.currentText()
    #     account = payed_account_values('view',gubun)
    #     self.registed_account_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt 
    #     set_row = len(account)
    #     self.registed_account_tableWidget.setRowCount(set_row)
    #     self.registed_account_tableWidget.setColumnCount(1)
    #     for j in range(set_row): #set_row):  # j는
    #         registed_data = account[j]
    #         self.registed_account_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
    
    def payed_account_review(self):
        from payed_account.payed_account_sql import payed_account_values 
        gubun = self.gubun_comboBox.currentText()
        account_data = payed_account_values('view', gubun)
        # self.registed_account_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt 
        set_row = len(account_data)
        self.registed_account_tableWidget.setRowCount(set_row)
        self.registed_account_tableWidget.setColumnCount(4)
        # self.registed_account_tableWidget.setRowCount(len(account_data))
        for row, item in enumerate(account_data):
            for col, value in enumerate(item):
                self.registed_account_tableWidget.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.registed_account_tableWidget.resizeColumnsToContents()
        self.registed_account_tableWidget.setColumnHidden(3, True)

    def connect_button(self):
        account_review_button = QPushButton("등록 사항 보기")
        account_review_button.clicked.connect(self.payed_account_review)

        selected_row_edit_button = QPushButton("선택 행 수정")
        selected_row_edit_button.clicked.connect(self.selected_row_edit)

        selected_row_delete_button = QPushButton("선택행삭제")
        selected_row_delete_button.clicked.connect(self.selected_row_delete)

        account_view_close_button = QPushButton("종료(저장취소)")
        account_view_close_button.clicked.connect(self.account_view_close) 

    def selected_row_delete(self):
        from payed_account.payed_account_sql import payed_account_selected_row_delete
        selected_rows = set(index.row() for index in self.registed_account_tableWidget.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            id_item = self.registed_account_tableWidget.item(row, 3)  # id 값을 나타내는 열 
            if id_item != None:
                id = id_item.text()
                payed_account_selected_row_delete(id)
            self.registed_account_tableWidget.removeRow(row)

        self.payed_account_review()

    def selected_row_edit(self): #cell_changed
        from payed_account.payed_account_sql import update_payed_account_sql
        sel_row = None
        change_data = []
        sel_row = self.registed_account_tableWidget.currentRow()
        c_count = self.registed_account_tableWidget.columnCount()
        for c_cnt in range(c_count):
            if self.registed_account_tableWidget.item(sel_row,c_cnt) != None:
                change_data_0 = self.registed_account_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data_0 = None
            
            change_data.append(change_data_0)
      
        # 데이터베이스에 연결하여 값을 업데이트
        update_payed_account_sql(change_data)
        change_data = []

        QMessageBox.information(None, "완료", "지출내역 정보가 변경 되었습니다.")


    def account_view_close(self):
        self.registed_account_tableWidget.setRowCount(0)
        self.registed_account_tableWidget.setRowCount(1)
        self.gubun_comboBox.setCurrentText('선택')
        self.close()
    
    
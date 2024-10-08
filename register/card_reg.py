import pymysql, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from basic.bank_account import cardlist
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/card_account.ui")[0]

class Card_Register(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('사용카드 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
    
    def collect_button(self):
        add_card_list_Button = QPushButton("추가저장")
        add_card_list_Button.clicked.connect(self.carddata_append)

        delete_selected_Button = QPushButton("선택행삭제")
        delete_selected_Button.clicked.connect(self.delete_selected)

        modify_selected_Button = QPushButton("선택행 수정")
        modify_selected_Button.clicked.connect(self.modify_selected)

        card_view_Button = QPushButton("보기")
        card_view_Button.clicked.connect(self.card_view)

        close_Button = QPushButton("종료")
        close_Button.clicked.connect(self.addcard_close)
    
        cardaccount = cardlist()

        self.card_tableWidget.setRowCount(len(cardaccount))
        self.card_tableWidget.setColumnCount(len(cardaccount[0]))
        # self.bank_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 불능
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked) # 더블클릭으로 수정가능
        self.card_tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers) #클릭, 더블클릭 으로 수정가능
        self.card_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        for i, row in enumerate(cardaccount):
            for j, item in enumerate(row):
                self.card_tableWidget.setItem(i, j, QTableWidgetItem(item))
        for i, row in enumerate(cardaccount):
            for j, item in enumerate(row):
                self.card_tableWidget.setItem(i, j, QTableWidgetItem(item))    

    def carddata_append(self):
        try:
            conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
            with conn.cursor() as cur:
                bank_name = self.card_bank_name_widget.text()
                b_account = self.card_account_no_widget.text()
                use_dep = self.card_depart_widget.text()

                input_sql = "insert into card_list (bank_name, card_number, use_part) values (%s, %s, %s)"
                if bank_name != "" and b_account != "" and use_dep != "":
                    cur.execute(input_sql, (bank_name, b_account, use_dep))
                    # 새로 추가된 데이터 가져오기
                    cur.execute("select bank_name, card_number, use_part from card_list order by id desc limit 1")
                    new_data = cur.fetchone()
                    # 새로운 행 추가
                    row_position = self.card_tableWidget.rowCount()
                    self.card_tableWidget.insertRow(row_position)
                    # 데이터 설정
                    for j, item in enumerate(new_data):
                        self.card_tableWidget.setItem(row_position,j, QTableWidgetItem(str(item)))
            
                    conn.commit()
                    conn.close()

            self.card_bank_name_widget.clear()
            self.card_account_no_widget.clear()
            self.card_depart_widget.clear()
            
        except pymysql.Error as e:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            

    def addcard_close(self):
        self.card_bank_name_widget.text()
        self.card_account_no_widget.text()
        self.card_depart_widget.text()

        # self.card_tableWidget.clearContents()
        # self.card_tableWidget.setRowCount(1)
        self.close()

    def card_view(self):
        from basic.bank_account import cardlist
        cardaccount = cardlist()

        self.card_tableWidget.setRowCount(len(cardaccount))
        self.card_tableWidget.setColumnCount(len(cardaccount[0]))
        self.card_tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers) #클릭, 더블클릭 으로 수정가능
        self.card_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i, row in enumerate(cardaccount):
            for j, item in enumerate(row):
                self.card_tableWidget.setItem(i, j, QTableWidgetItem(item))    

    def delete_selected(self):
        selected_item = self.card_tableWidget.currentItem()
        if selected_item:
            row_index = self.card_tableWidget.row(selected_item)

            # 선택된 행의 데이터를 가져옴
            selected_data = self.card_tableWidget.item(row_index,1).text() 

            # 데이터베이스 연결
            conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            cursor = conn.cursor()

            # 데이터 삭제 쿼리 실행
            cursor.execute("DELETE FROM card_list where card_number=%s",(selected_data,))

            # 테이블 위젯에서 선택된 행 삭제
            self.card_tableWidget.removeRow(row_index)

            # self.card_view()

            # 변경사항을 데이터베이스에 반영
            conn.commit()

            # 데이터베이스 연결 해제
            conn.close()
    
    def modify_selected(self): #cell_changed
        from register.for_card_bank_modi_sql import card_update_row_sql
        sel_row = None
        change_data = []
        sel_row = self.card_tableWidget.currentRow()
        c_count = self.card_tableWidget.columnCount()
        for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
            if self.card_tableWidget.item(sel_row, c_cnt) != None:
                change_data_0 = self.card_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data = None
            change_data.append(change_data_0)
        change_data.append(change_data[1])

        # 데이터베이스에 연결하여 값을 업데이트
        card_update_row_sql(change_data)
        change_data = []
        QMessageBox.about(self,'저장',"카드정보가 변경 되었습니다.!!!")
        self.card_view()

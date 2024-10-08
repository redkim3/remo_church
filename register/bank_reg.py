import pymysql, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
# from basic.bank_account import banklist
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/bank_account.ui")[0]

class Bank_Register(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('거래은행 등록')
        self.bank_view()
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.Bank_name_widget.editingFinished.connect(self.gubun_combo)

    def collect_button(self):
        add_bank_list_Button = QPushButton("추가저장")
        add_bank_list_Button.clicked.connect(self.bankdata_append)

        delete_selected_Button = QPushButton("선택행삭제")
        delete_selected_Button.clicked.connect(self.delete_selected_row)

        modify_selected_Button = QPushButton("선택행수정")
        modify_selected_Button.clicked.connect(self.modify_selected)

        bank_view_Button = QPushButton("보기")
        bank_view_Button.clicked.connect(self.bank_view)

        close_Button = QPushButton("종료")
        close_Button.clicked.connect(self.addbank_close)

        bankaccount = self.bank_view()

        # 여기에서 self.bank_tableWidget을 찾아 초기화
        # self.bank_tableWidget = self.findChild(QTableWidget, "bank_list_tableWidget")  # 수정된 부분
        self.bank_tableWidget.setRowCount(len(bankaccount))
        self.bank_tableWidget.setColumnCount(len(bankaccount[0]))
        self.bank_tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.bank_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i, row in enumerate(bankaccount):
            for j, item in enumerate(row):
                self.bank_tableWidget.setItem(i, j, QTableWidgetItem(item))
    def gubun_combo(self):
        from basic.hun_name_2 import gubun_values
        gubun_com = []
        gubun_com = gubun_values()
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_com)

    def bankdata_append(self):
        try:
            conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            with conn.cursor() as cur:
                b_name = self.Bank_name_widget.text()
                b_account = self.account_no_widget.text()
                use_part = self.depart_widget.text()
                gubun = self.gubun_comboBox_widget.currentText()
                in_use = '사용중'

                bank_sql = """INSERT INTO bank_acc (bank_name, bank_account, use_part, gubun, in_use) VALUES (%s, %s, %s, %s, %s)"""
                if b_name != "":
                    if b_account != "" :
                        if use_part != "":
                            cur.execute(bank_sql, (b_name, b_account, use_part, gubun, in_use))
                            # 새로 추가된 데이터 불러오기
                            cur.execute("""select bank_name, bank_account, use_part, gubun, in_use from bank_acc order by id desc limit 1""")
                            new_data = cur.fetchone()
                            # 새로운 행 추가
                            row_position = self.bank_tableWidget.rowCount()
                            self.bank_tableWidget.insertRow(row_position)
                            # 데이터 설정
                            for j, item in enumerate(new_data):
                                self.bank_tableWidget.setItem(row_position,j, QTableWidgetItem(str(item)))
                            conn.commit()
                            conn.close()
                        else:
                            QMessageBox.about(self, "입력오류", " '사용부서'가 없습니다.")
                            self.depart_widget.setFocus()
                            return
                    else:
                        QMessageBox.about(self, "입력오류", " '계좌번호'가 없습니다.")
                        self.account_no_widget.setFocus()
                        return
                else:
                    QMessageBox.about(self, "입력오류", " '은행명'이 없습니다.")
                    self.Bank_name_widget.setFocus()
                    return


            self.Bank_name_widget.clear()
            self.account_no_widget.clear()
            self.depart_widget.clear()
            self.gubun_comboBox_widget.clear()
            self.bank_view()

        except pymysql.Error as e:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")

    def addbank_reset(self):
        self.Bank_name_widget.clear()
        self.account_no_widget.clear()
        self.depart_widget.clear()
        self.gubun_comboBox_widget.clear()
        

    def addbank_close(self):
        self.addbank_reset()
        self.close()
    
    def closeEvent(self,event):
        self.addbank_reset()
        event.accept()

    def bank_view(self):
        from register.bank_account_reg import banklist
        bankaccount = banklist()
        
        self.bank_tableWidget.setRowCount(len(bankaccount))
        self.bank_tableWidget.setColumnCount(len(bankaccount[0]))
        self.bank_tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.bank_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i, row in enumerate(bankaccount):
            for j, item in enumerate(row): 
                self.bank_tableWidget.setItem(i, j, QTableWidgetItem(item))

    def delete_selected_row(self):
        selected_item = self.bank_tableWidget.currentItem()
        if selected_item:
            row_index = self.bank_tableWidget.row(selected_item)

            # 선택된 행의 데이터를 가져옴
            selected_data = self.bank_tableWidget.item(row_index, 1).text()

            # 데이터베이스 연결
            conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            cursor = conn.cursor()

            # 데이터 삭제 쿼리 실행
            cursor.execute("DELETE FROM bank_acc where bank_account=%s", (selected_data,))

            # 테이블 위젯에서 선택된 행 삭제
            self.bank_tableWidget.removeRow(row_index)

            # 변경사항을 데이터베이스에 반영
            conn.commit()

            # 데이터베이스 연결 해제
            conn.close()
    
    def modify_selected(self): #cell_changed
        from register.for_card_bank_modi_sql import bank_update_row_sql
        sel_row = None
        change_data = []
        sel_row = self.bank_tableWidget.currentRow()
        c_count = self.bank_tableWidget.columnCount()
        for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
            if self.bank_tableWidget.item(sel_row, c_cnt) != None:
                change_data_0 = self.bank_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data = None
            change_data.append(change_data_0)
        change_data.append(change_data[1])

        # 데이터베이스에 연결하여 값을 업데이트
        bank_update_row_sql(change_data)
        change_data = []
        QMessageBox.about(self,'저장',"은행 계좌 리스트 정보가 변경 되었습니다.!!!")
        self.bank_view()

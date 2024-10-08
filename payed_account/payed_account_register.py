import pymysql, os
from PyQt5.QtCore import QDate
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import configparser
from basic.hun_name_2 import gubun_values
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())

imsi = []; n = 0

form_class = uic.loadUiType("ui/payed_account_reg_form.ui")[0]
j = 1
class payed_accountRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('지출 은행명칭 및 계좌 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        gubun_value = gubun_values()
        self.gubun_comboBox.addItems(["선택"] + gubun_value)
        self.gubun_comboBox.currentTextChanged.connect(self.registed_data)

        self.new_account_tableWidget.setRowCount(1)
        self.new_account_tableWidget.setColumnWidth(0, 125)
        self.new_account_widget.text()
    
    def connect_button(self):
        add_account_button = QPushButton("신규등록 추가")
        add_account_button.clicked.connect(self.account_reg_input)
        
        account_view_button = QPushButton("다시보기")
        account_view_button.clicked.connect(self.registed_data)
        delete_selected_row_button = QPushButton("선택행삭제")
        delete_selected_row_button.clicked.connect(self.delete_selected_row)

        account_save_button = QPushButton("저장")
        account_save_button.clicked.connect(self.file_save)
        account_close_button = QPushButton("종료(저장취소)")
        account_close_button.clicked.connect(self.file_save_cancel) 

    def registed_data(self):
        from payed_account.payed_account_sql import payed_account_values 
        # account = payed_account_values('reg')
        # self.registed_account_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        # set_row = len(account)
        # self.registed_account_tableWidget.setRowCount(set_row)
        # self.registed_account_tableWidget.setColumnCount(1)
        # for j in range(set_row): #set_row):  # j는
        #     registed_data = account[j]
        #     item = QTableWidgetItem(str(registed_data))
        #     self.registed_account_tableWidget.setItem(j,0,item)
        gubun = self.gubun_comboBox.currentText()
        account = payed_account_values('reg',gubun)
        self.registed_account_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt 
        set_row = len(account)
        self.registed_account_tableWidget.setRowCount(set_row)
        self.registed_account_tableWidget.setColumnCount(1)
        for j in range(set_row): #set_row):  # j는
            registed_data = account[j]
            self.registed_account_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))

    def delete_selected_row(self):
        global j
        #self.registed_hang_tableWidget.clicked.connect(self.handle_table_click)
        selected_items = self.registed_account_tableWidget.selectedItems()
        table_name = 'payed_account'
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_account_tableWidget.row(selected_items[0])
            if row_index != -1 and self.registed_account_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_account_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            cur = conn.cursor()

            try:
                # 데이터 삭제 쿼리 실행
                delete_account_sql = 'delete from {} where account_name = %s'.format(table_name)
                cur.execute(delete_account_sql,(selected_data,))

                # 테이블 위젯에서 선택된 행 삭제
                self.registed_account_tableWidget.removeRow(row_index)

                # 변경사항을 데이터베이스에 반영
                conn.commit()
                QMessageBox.about(self, '삭제', '데이터가 성공적으로 삭제되었습니다.')
            except pymysql.Error as e:
                QMessageBox.critical(self, '에러', f'데이터 삭제 중 오류 발생: {e}')
            finally:

                # 데이터베이스 연결 해제
                conn.close()
        self.registed_data()

    def account_reg_input(self):
        global j
        try:
            if j != 1:
                self.new_account_tableWidget.insertRow(j-1)
            accou_name = self.account_name_widget.text()
            bank_name = self.bank_name_widget.text()
            accou_no = self.new_account_widget.text()  # 구분
            if accou_name =='':
                QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
                if j != 1:
                    j -= 1
            self.new_account_tableWidget.setItem((j-1),0,QTableWidgetItem(accou_name))
            self.new_account_tableWidget.setItem((j-1),1,QTableWidgetItem(bank_name))
            self.new_account_tableWidget.setItem((j-1),2,QTableWidgetItem(accou_no))
            
            self.account_name_widget.clear()
            self.bank_name_widget.clear()
            self.new_account_widget.clear()
            j += 1
            self.account_name_widget.setFocus()
            return
       
        except ValueError:
            QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
            self.account_name_widget.setFocus()
            return
        
    def file_save_cancel(self):
        self.new_account_tableWidget.clearContents()
        self.close()
    
    def closeEvent(self, event):
        self.new_account_tableWidget.clearContents()
        event.accept()

    def file_save(self):
        global j
        rowCount = self.new_account_tableWidget.rowCount()
        conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
        cur = conn.cursor()
        # 데이터 설정
        db_name = 'payed_account' # 테이블 명칭임
        # 테이블이 존재하지 않으면 생성
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {db_name} (id int NOT NULL AUTO_INCREMENT, account_name VARCHAR(10) NOT NULL, bank_name VARCHAR(10), account_no VARCHAR(20) NOT NULL);"
        cur.execute(create_table_sql)

        rowCount = self.new_account_tableWidget.rowCount()
        # try:
        if rowCount > 0:
            for i in range(rowCount):
                    gubun = self.gubun_comboBox.currentText()
                    accou_name = self.new_account_tableWidget.item(i, 0).text()
                    bank_name = self.new_account_tableWidget.item(i, 1).text()
                    accou_no = self.new_account_tableWidget.item(i, 2).text()
                    imsi.append([gubun,accou_name,bank_name,accou_no,])

            for data in imsi:
                input_account = data
                account_sql = "INSERT INTO {} (gubun, account_name, bank_name, account_no) VALUES (%s, %s, %s, %s);".format(db_name)
                cur.execute(account_sql, (input_account))
            QMessageBox.about(self,'저장',"'지급계좌가 저장되었습니다.!!!")
            self.new_account_tableWidget.clearContents()
            j = 1
            self.new_account_tableWidget.setRowCount(j)
            conn.commit()
            conn.close()
            self.new_account_widget.setFocus()
        else:
            QMessageBox.about(self,'저장',"저장할 내용이 없습니다.!!!")
        # except pymysql.Error as e:
        #         QMessageBox.critical(self, '에러', f'데이터 삭제 중 오류 발생: {e}')

        self.registed_data()
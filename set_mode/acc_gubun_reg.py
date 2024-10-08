import os,pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import *
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()

today = QDate.currentDate()
v_year = str(today.year())

imsi = []; n = 0

form_class = uic.loadUiType("ui/acc_gubun_form.ui")[0]
j = 1
class acc_gubunRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('회계구분 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.registed_data()
        self.registed_gubun_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        self.new_gubun_tableWidget.setRowCount(1)
        self.new_gubun_tableWidget.setColumnWidth(0, 125)
        self.new_gubun_widget.text()
    
    def acc_button(self):
        addgubun_button = QPushButton("신규등록 추가")
        addgubun_button.clicked.connect(self.gubun_reg_input)
        
        gubun_view_button = QPushButton("다시보기")
        gubun_view_button.clicked.connect(self.registed_data)
        delete_selected_row_button = QPushButton("선택행삭제")
        delete_selected_row_button.clicked.connect(self.delete_selected_row)

        file_save_button = QPushButton("저장")
        file_save_button.clicked.connect(self.file_save)
        gubuncancel_button = QPushButton("종료(저장취소)")
        gubuncancel_button.clicked.connect(self.file_save_cancel)

    def registed_data(self):
        from basic.hun_name_2 import gubun_values
        gubun = gubun_values()
        self.registed_gubun_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        set_row = len(gubun)
        self.registed_gubun_tableWidget.setRowCount(set_row)
        for j in range(set_row): #set_row):  # j는
            registed_data = gubun[j]
            self.registed_gubun_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))

    def delete_selected_row(self):
        global j

        selected_items = self.registed_gubun_tableWidget.selectedItems()
        table_name = 'gubun'
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_gubun_tableWidget.row(selected_items[0])
            
            if row_index != -1 and self.registed_gubun_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_gubun_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            cur = conn.cursor()

            try:
                # 데이터 삭제 쿼리 실행
                delete_gubun_sql = 'delete from {} where gubun = %s'.format(table_name)
                cur.execute(delete_gubun_sql,(selected_data,))

                # 테이블 위젯에서 선택된 행 삭제
                self.registed_gubun_tableWidget.removeRow(row_index)

                # 변경사항을 데이터베이스에 반영
                conn.commit()
                QMessageBox.about(self, '삭제', '데이터가 성공적으로 삭제되었습니다.')
            except pymysql.Error as e:
                QMessageBox.critical(self, '에러', f'데이터 삭제 중 오류 발생: {e}')
            finally:
                # 데이터베이스 연결 해제
                conn.close()

    def gubun_reg_input(self):
        global j
        try:
            if j != 1:
                self.new_gubun_tableWidget.insertRow(j-1)
            gubun_name = self.new_gubun_widget.text()  # 구분
            if gubun_name =='':
                QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
                if j != 1:
                    j -= 1
            self.new_gubun_tableWidget.setItem((j-1),0,QTableWidgetItem(gubun_name))
            self.new_gubun_widget.clear() 
            self.new_gubun_widget.setFocus()
            j += 1
        
        except ValueError:
            QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')

    def file_save_cancel(self):
        self.new_gubun_tableWidget.clearContents()
        self.close()
    
    def closeEvent(self, event):
        self.new_gubun_tableWidget.clearContents()
        event.accept()
        
    def file_save(self):
        rowCount = self.new_gubun_tableWidget.rowCount()
    
        conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
        cur = conn.cursor()

        # 데이터 설정
        db_name = 'gubun' # 테이블 명칭임
        # 테이블이 존재하지 않으면 생성
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {db_name} (gubun VARCHAR(6));"
        cur.execute(create_table_sql)

        rowCount = self.new_gubun_tableWidget.rowCount()
        #try:
        if rowCount > 0:
            for i in range(rowCount):

                    gubun = self.new_gubun_tableWidget.item(i, 0).text()
                    imsi.append([gubun])

            for data in imsi:
                gubun = data
                gubun_sql = "INSERT INTO {} (gubun) VALUES (%s);".format(db_name)
                cur.execute(gubun_sql, (gubun))
            QMessageBox.about(self,'저장',"'구분이 저장되었습니다.!!!")
            self.new_gubun_tableWidget.clearContents()
            j = 1
            self.new_gubun_tableWidget.setRowCount(j)
            conn.commit()
            conn.close()
            self.new_gubun_widget.setFocus()
        else:
            QMessageBox.about(self,'저장',"저장할 내용이 없습니다.!!!")
     
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from datetime import datetime
import configparser, hashlib
import pymysql, os
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 

# # MySQL 연결 설정
# conn = pymysql.connect(host=host_name, user = 'root', password= '0000', db = 'isbs2024', charset = 'utf8')
# # MySQL 커서 생성
# cur = conn.cursor()

form_class = uic.loadUiType("ui/user_regist_form.ui")[0]

class userRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        global gubun, reg_no
        self.reg_date_widget.setDate(today)
        # self.name_widget.editingFinished.connect(self.hap_code_make)
        self.setWindowTitle('사용자 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))

    def button_select(self):
        user_view_Button = QPushButton("사용자보기")
        user_view_Button.clicked.connect(self.user_view)
        add_user_Button = QPushButton("등록")
        add_user_Button.clicked.connect(self.add_user_save)
        save_cancel_Button = QPushButton("종료")
        save_cancel_Button.clicked.connect(self.close_exit)
        row_delete_Button = QPushButton("선택생 삭제")
        row_delete_Button.clicked.connect(self.row_delete)
        row_edit_Button = QPushButton("선택행 수정")
        row_edit_Button.clicked.connect(self.row_edit)

    def close_reset(self):
        self.name_widget.clear()
        self.ID_regist_widget.clear()
        self.password_widget.clear()
        self.user_tableWidget.setRowCount(0)
        # 체크박스를 체크안된 상태로 초기화
        self.Ge_checkBox.setChecked(False)
        self.sun_checkBox.setChecked(False)
        self.spe_checkBox.setChecked(False)
        self.hun_detail_checkBox.setChecked(False)
        self.user_checkBox.setChecked(False)
    
    def close_exit(self):
        self.close_reset()
        self.close()
    
    def closeEvent(self,event):
        self.close_reset()
        event.accept()
    
    def user_review(self):
        from user.for_user_sql import user_view_sql
        account_data = user_view_sql()
        # self.registed_account_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt 
        set_row = len(account_data)
        self.user_tableWidget.setRowCount(set_row)
        self.user_tableWidget.setColumnCount(10)
        # self.registed_account_tableWidget.setRowCount(len(account_data)) 
        for row, item in enumerate(account_data):
            for col, value in enumerate(item):
                self.user_tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

        self.user_tableWidget.resizeColumnsToContents()
        

    def add_user_save(self):
        from basic.member import code1_select, name_diff_select
        from user.for_user_sql import add_user_sql
        imsi_user_data = []
        # if j != 0:
        #     self.user_tableWidget.insertRow(j)
        s_date=self.reg_date_widget.text()
        reg_date_1 = datetime.strptime(s_date,'%Y-%m-%d')
        reg_date = datetime.date(reg_date_1)
        N_code = name_diff_select()
        user_name=self.name_widget.text()
        if (user_name != '' and user_name in N_code) :
            code1 = str(code1_select(user_name))
            code1 = code1.strip("[',']")
        else :
            QMessageBox.about(self,'입력오류 !!!','성도 명단에 등록되지 않은 이름 입니다. 확인하여 주십시오')
            self.name_widget.setFocus()
            return
        user_id=self.ID_regist_widget.text()
        user_password=self.password_widget.text()
        hashed_password = self.hash_password(user_password)
        
        Ge_right=self.Ge_checkBox.isChecked()
        sun_right=self.sun_checkBox.isChecked()
        spe_right=self.spe_checkBox.isChecked()
        hun_view_right=self.hun_detail_checkBox.isChecked()
        regist_right=self.user_checkBox.isChecked()
        # imsi_user_data.append([user_id, reg_date, code1,user_name,user_password,Ge_right,sun_right,spe_right,hun_view_right,regist_right])
        imsi_user_data.append([user_id, reg_date, code1,user_name,hashed_password,Ge_right,sun_right,spe_right,hun_view_right,regist_right])
                
        record = add_user_sql(imsi_user_data)
        self.user_review()
        if record == 'record':
            self.name_widget.clear()
            self.ID_regist_widget.clear()
            self.password_widget.clear()
            # 체크박스를 체크안된 상태로 초기화
            self.Ge_checkBox.setChecked(False)
            self.sun_checkBox.setChecked(False)
            self.spe_checkBox.setChecked(False)
            self.hun_detail_checkBox.setChecked(False)
            self.user_checkBox.setChecked(False)
            imsi_user_data =[]
        else:
            self.ID_regist_widget.clear()
            self.ID_regist_widget.setFocus()
            return
    def hash_password(self,user_password):
        # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
        hasher = hashlib.sha256()
        # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
        hasher.update(user_password.encode('utf-8'))
        # 해시된 결과 반환
        return hasher.hexdigest()
    
    def row_edit(self): #cell_changed
        from user.for_user_sql import update_row_sql
        sel_row = None
        change_data = []
        sel_row = self.user_tableWidget.currentRow()
        c_count = self.user_tableWidget.columnCount()
        for c_cnt in range(1, c_count - 1): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
            if self.user_tableWidget.item(sel_row, c_cnt) != None:
                if c_cnt == 3:
                    # 비밀번호를 해시 처리한 값을 리스트로 감싸서 저장합니다. 
                    change_data_hash = self.hash_password(self.user_tableWidget.item(sel_row, c_cnt).text())
                    change_data_0 = str(change_data_hash)
                else:
                    if c_cnt == 0:
                        change_data_0 = (self.user_tableWidget.item(sel_row, c_cnt).text(),)
                    else:
                        # 날짜와 그 외의 값들은 그대로 리스트에 저장합니다.
                        change_data_0 = self.user_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data_0 = None
                
            change_data.append(change_data_0)

        # 날짜 값은 리스트로 감싸서 저장합니다.
        change_data_0 = self.user_tableWidget.item(sel_row, 0).text()
        change_data.append(change_data_0)
        # 데이터베이스에 연결하여 값을 업데이트
        update_row_sql(change_data)
        change_data = []
        QMessageBox.about(self,'저장',"사용자 정보가 변경 되었습니다.!!!")
        self.user_review()

    def row_delete(self):
        from user.for_user_sql import delete_row_from_database
        selected_rows = set(index.row() for index in self.user_tableWidget.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            id_item = self.user_tableWidget.item(row, 0)  # id 값을 나타내는 열
            if id_item != None:
                id_value = id_item.text()
                delete_row_from_database(id_value)   # hun_db_save에 있는 쿼리 실행하기
            self.user_tableWidget.removeRow(row)
        QMessageBox.about(self,'삭제',"사용자 정보가 삭제 되었습니다.!!!")
        self.user_review()

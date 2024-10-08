from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import configparser, os

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
email_imsi = []; delete_email = []
form_class = uic.loadUiType("./ui/email_account.ui")[0]
j = 0; row_s = 0

class email_Register(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('발송대상 이메일 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        global email_int, row_s

        # self.email_list_tableWidget.clearContents()
        self.email_list_tableWidget.setRowCount(0)
        self.email_list_tableWidget.setColumnCount(2)
        self.email_append_tableWidget.setRowCount(0)
        self.email_append_tableWidget.setRowCount(1)
        self.email_append_tableWidget.setColumnCount(2)

        # self.email_list_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 불능 
        self.email_list_tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers) #클릭, 더블클릭 으로 수정가능
        self.email_list_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        

    def button(self):
        add_email_list_Button = QPushButton("추가하기")
        add_email_list_Button.clicked.connect(self.email_append)
        email_save_Button = QPushButton("저장하기")
        email_save_Button.clicked.connect(self.email_save)
        email_view_Button = QPushButton("보기")
        email_view_Button.clicked.connect(self.registed_email_view)

        email_close_Button = QPushButton("종료(저장취소)")
        email_close_Button.clicked.connect(self.addemail_close)
    
        remove_row_Button = QPushButton("선택행 삭제하기)")
        remove_row_Button.clicked.connect(self.remove_row)

        modify_email_Button = QPushButton("선택행 수정하기)")
        modify_email_Button.clicked.connect(self.modify_email)

    def email_append(self):
        global j
        email_name = self.email_name_widget.text()
        email_add = self.email_add_widget.text()
        if email_name == "" and email_add == "":
            QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
        else:
            if j != 0:
                self.email_append_tableWidget.insertRow(j)
            self.email_append_tableWidget.setItem(j,0,QTableWidgetItem(email_name))
            self.email_append_tableWidget.setItem(j,1,QTableWidgetItem(email_add))
            self.email_append_tableWidget.resizeColumnsToContents()
            self.email_name_widget.clear()
            self.email_add_widget.clear()
            self.email_name_widget.setFocus()
            j += 1
    
    def registed_email_view(self):
        from outside.email_list import email_list_view
        emaillist = email_list_view()
        email_int = len(emaillist)
        self.email_list_tableWidget.setRowCount(email_int)
        for j in range(email_int):
            name, email = emaillist[j]
            self.email_list_tableWidget.setItem(j, 0, QTableWidgetItem(name))
            self.email_list_tableWidget.setItem(j, 1, QTableWidgetItem(email))
        self.email_list_tableWidget.resizeColumnsToContents()
        
    def remove_row(self):
        from outside.email_list import remome_email
        sel_row = None
        sel_row = self.email_list_tableWidget.currentRow()
        c_count = self.email_list_tableWidget.columnCount()
        for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
            if self.email_list_tableWidget.item(sel_row, c_cnt) != None:
                change_data_0 = self.email_list_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data = None
            delete_email.append(change_data_0)

        remome_email(delete_email)
        
        self.email_list_tableWidget.removeRow(sel_row)

    def email_save(self):
        from outside.email_list import email_regist
    
        rowCount = self.email_append_tableWidget.rowCount()
        for i in range(rowCount):
            email_name = self.email_append_tableWidget.item(i, 0).text()
            email_imsi.append(email_name)
            email_addr1 = self.email_append_tableWidget.item(i, 1).text()
            email_imsi.append(email_addr1)
        self.email_append_tableWidget.resizeColumnsToContents()

        email_regist(email_imsi)
        QMessageBox.about(self,'저장',"'새로운 발송대상 이메일이 저장되었습니다.!!!")

        # 다시보기
        self.registed_email_view()
        self.email_append_tableWidget.setRowCount(0)
        self.email_append_tableWidget.setRowCount(1)
        self.email_name_widget.setFocus()

    def modify_email(self): 
        from outside.email_list import modify_email
        sel_row = None
        change_data = []; modify_data=[]
        sel_row = self.email_list_tableWidget.currentRow()
        c_count = self.email_list_tableWidget.columnCount()
        for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
            if self.email_list_tableWidget.item(sel_row, c_cnt) != None:
                change_data_0 = self.email_list_tableWidget.item(sel_row, c_cnt).text()
            else:
                change_data = None
            
            change_data.append(change_data_0)

        modify_data.append(change_data[1])
        modify_data.append(change_data[0])
        
        modify_data = tuple(modify_data)
        # print(change_data)
        # 데이터베이스에 연결하여 값을 업데이트
        modify_email(modify_data)
        
        change_data = []; modify_data = []
        QMessageBox.about(self,'저장',"발송 이메일 주소가 수정 되었습니다.!!!")
        self.registed_email_view()


    def addemail_close(self):
        self.email_name_widget.text()
        self.email_add_widget.text()

        # self.email_list_tableWidget.clearContents()
        self.email_list_tableWidget.setRowCount(0)
        self.email_append_tableWidget.setRowCount(0)
        self.email_append_tableWidget.setRowCount(1)
        self.close()

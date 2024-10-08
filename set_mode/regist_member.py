import configparser, os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 

form_class = uic.loadUiType("./ui/reg_member_form.ui")[0]

class memberRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        global v_year
        self.setWindowTitle('성도등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        # 직접 함수 호출로 변경 
        self.reg_date_widget.setDate(today)
        v_year = QDate.currentDate().year()
        # self.reg_date_widget.editingFinished.connect(self.get_last_member_code)
        self.name_widget.editingFinished.connect(self.code1_make)
        # self.name_diff_widget.editingFinished.connect(self.name_diff_compare_serch)
    
    def button_reg(self):
        add_mem_Button = QPushButton("등록")
        add_mem_Button.clicked.connect(self.member_append)
        member_serch_Button = QPushButton("성도검색")
        member_serch_Button.clicked.connect(self.member_serch)
    
    def code1_make(self):
        from basic.member import name_diff_compare
        from basic.member_information import member_code
        s_name = self.name_widget.text()
        v_year = QDate.currentDate().year()
        same_name = name_diff_compare(s_name)
        if same_name != []:
            QMessageBox.about(self, "동일이름", "동명을 가진 사람이 있습니다. 동명구분란에 구분기호를 넣어 주세요")
        self.name_diff_widget.setText(s_name)        
        last_code = member_code(v_year)
        last_no = int(last_code) + 1
        last_no_form = '{:03d}'.format(last_no)
        code1 = str(v_year) +'-' + last_no_form
        self.code1_widget.setText(code1)
        self.hap_code_widget.setText(code1)
        
    def member_serch(self):
        from serch.serch_member import Serch_Member
        self.ser_member = Serch_Member()
        self.ser_member.exec()
        
        self.show()
 
    def member_append(self):
        from basic.member_information import new_member_append
        from basic.member import name_diff_compare
        new_data = []
        try:
            dat = self.reg_date_widget.text()
            code_1 = self.code1_widget.text()
            s_name = self.name_widget.text()
            name_diff = self.name_diff_widget.text()
            position = self.position_widget.text()
            hap_code = self.hap_code_widget.text()
            juso = self.addr_widget.text()
            marks = self.marks_widget.text()
            same_name_diff = name_diff_compare(name_diff)
            if same_name_diff == []:

                if dat != "" and code_1 != "" and s_name != "" and name_diff != "" and hap_code != "":
                    # 새로운 행 추가
                    row_position = self.regist_member_tableWidget.rowCount()
                    self.regist_member_tableWidget.insertRow(row_position)

                    # 데이터 설정
                    for j, item in enumerate([dat, code_1, name_diff, s_name, hap_code, position, juso, marks]):
                        self.regist_member_tableWidget.setItem(row_position, j, QTableWidgetItem(str(item)))
                        new_data.append(item)
                    new_member_append(new_data)

                    self.name_widget.clear()
                    self.code1_widget.clear()
                    self.name_diff_widget.clear()
                    self.position_widget.clear()
                    self.hap_code_widget.clear()
                    self.addr_widget.clear()
                    self.marks_widget.clear()

                else:
                    QMessageBox.about(self, "입력오류", "필수 입력사항이 누락되었습니다.")
            else:
                QMessageBox.about(self, "입력오류", "동일이름이 있습니다. 구분기호를 넣어 주세요.")
                self.name_diff_widget.setFocus()
                return

        except ValueError: #ValueError:
            QMessageBox.about(self, "입력오류", "입력사항을 확인하세요")
            self.registed_name.setFocus()
            return

    def closeEvent(self, event):
        self.name_widget.clear()
        self.code1_widget.clear()
        self.name_diff_widget.clear()
        self.position_widget.clear()
        self.hap_code_widget.clear()
        self.addr_widget.clear()
        self.marks_widget.clear()
        self.regist_member_tableWidget.clearContents()
        event.accept()

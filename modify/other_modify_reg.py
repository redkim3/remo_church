import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from datetime import datetime
from basic.hun_name_2 import gubun_values
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 

form_class = uic.loadUiType("./ui/sp_hun_modify_reg_form.ui")[0]

class Other_modify_Register(QDialog, form_class) :
    def __init__(self, id) :
        super().__init__()
        self.id = id
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        global gubun, selec1
        self.setWindowTitle('기타소득 상세보기 수정 등록')
        self.selected_row_data_call()
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
 
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)

        self.selected_row_data_call()
        self.month_widget.setFocus()
        self.amount_widget.editingFinished.connect(self.amount_QSpin)
 
        v_year = int(self.year_widget.text())
        self.gubun_name_combo_widget.addItems(["선택"] + gubun_values())
        self.gubun_name_combo_widget.currentTextChanged.connect(self.hun_name_combobox)

    def cost_reg_button(self):
        
        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.close)
        
        cost_save_button = QPushButton("수정 저장")
        cost_save_button.clicked.connect(self.accounting_change)

    def user_confirm(self):
        from user.for_user_sql import user_infor_sql
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        user_id = config['user']['user_id']
        user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
        user_name_infor = user_info[0]        # 이름을 가져오고
        user_name = user_name_infor[0]
        
        config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    
        return user_name

    def selected_row_data_call(self): # sql문으로 데이터 불러오기 방법은 id
        from modify.hun_modify_sql_save import selected_row_data_call
        # from basic.hun_name_2 import gubun_values
        from basic.cost_select import cost_hang_values, cost_mok_values, cost_semok_values
        from payed_account.payed_account_sql import payed_account_values
        id_value = int(self.id)
        gubun_combo = ["선택"] + gubun_values()
        selected_hun_data = selected_row_data_call(id_value)

        date_object = selected_hun_data[0][1]  # 날짜
        date_string = date_object.strftime("%Y-%m-%d")
        self.hun_date_widget.setDate(date_object) #
        self.year_widget.setText(str(selected_hun_data[0][2]))  # 년
        self.month_widget.setText(str(selected_hun_data[0][3]))  # 월
        self.week_widget.setText(str(selected_hun_data[0][4]))  # 주
        v_year = self.year_widget.text()
         # 사용 예시
        # self.code1_widget.setText(str(selected_hun_data[0][5]))
        # self.registed_name.setText(str(selected_hun_data[0][6]))
        selected_gubun = selected_hun_data[0][5] # 구분

        i1 = self.set_value_in_combo(gubun_combo, selected_gubun)
        
        # if i1 != -1:
        self.gubun_name_combo_widget.setItemText(i1, selected_gubun)
        amo_txt = selected_hun_data[0][10]
        amount = format(amo_txt,(","))
        self.amount_widget.setText(amount)
        # self.hun_detail_combo.setText(selected_hun_data[0][11])
        if selected_hun_data[0][12] == '통장예입':
            self.Bankincome_check.setChecked(True)
        else:
            self.Bankincome_check.setChecked(False)
        self.marks_widget.setText(selected_hun_data[0][13])
    
    # 콤보 상자에 특정 값을 설정하는 함수
    def set_value_in_combo(self, combo_box, value):
        for index in range(len(combo_box)):
            if combo_box[index] == value:
                # combo_box.setCurrentIndex(index)
                return index
        # 원하는 값이 콤보 상자에 없는 경우에 대비하여 -1 반환
        return -1

    def hun_name_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자
        from basic.hun_name_2 import  other_gubun_mok_values
        global selec1
        gubun = self.gubun_name_combo_widget.currentText()
        hun_mok_list = []   
        v_year = self.year_widget.text()
        # hang_0 = 
        hun_mok_tuple = other_gubun_mok_values(v_year,gubun)
        if hun_mok_tuple == None:
            self.week_widget.setFocus()
            return
        else:
            self.hun_name_widget.addItems(["선택"] + hun_mok_tuple)
        

    def name_input(self):
        from basic.member import code1_select, name_diff_select
        N_code = name_diff_select()
        mok = self.hun_name_widget.currentText()
        namecode = self.registed_name.text()

        if mok != "주일헌금": 
            if (namecode != '' and namecode in N_code) :
                code1 = str(code1_select(namecode))
                code1 = code1.strip("[',']")
                self.code1_widget.setText(code1)
            else :
                QMessageBox.about(self,'입력오류 !!!','등록되지 않은 이름 입니다. 확인하여 주십시오')
                self.registed_name.setFocus()
                return

    def file_close(self):
        global hap_total, j
        self.hun_name_widget.clear()
        self.week_widget.clear()

        self.close()
    
    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(today.year()):
            return False  # 현재 년도와 같으면 False 반환 
        else:
            QMessageBox.about(self, '', "'지출년도'가 현재의 '년도'와 같아야 합니다. ")
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환

    def file_save(self):
        from basic.hun_name_2 import  mok_hang_values
        from modify.hun_modify_sql_save import update_hun_db_sql
        selected_data = []
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
        j = 1; data = []
       
        s_date = self.hun_date_widget.text()
        v_date = datetime.strptime(s_date,'%Y-%m-%d')
        v_year = int(self.year_widget.text())
        v_month = int(self.month_widget.text())
        user_name = self.user_widget.text()
        if not self.week_widget.text().isdigit():
            QMessageBox.about(self, '오류', '"주"는 숫자여야 합니다.')
            self.week_widget.clear()
            self.week_widget.setFocus()
            return
        v_week = int(self.week_widget.text())
        v_gubun = self.gubun_name_combo_widget.currentText()
        hun_mok = self.hun_name_widget.currentText()
        mok_hang = mok_hang_values(v_year, hun_mok,v_gubun)[0]
        amo_txt = self.amount_widget.text()
        if amo_txt == None:
            QMessageBox.about(self, '오류', '금액이 없어 저장할 수 없습니다.')
            self.registed_name.setFocus()
            return
        amount = int(amo_txt.replace(',',''))

        if mok_hang != '기타소득':
            name_diff = "무명" # self.registed_name.text()
            code1 = "무명" #self.code1_widget.text()
            hun_detail = None #str(self.hun_detail_combo.currentText())   # 헌금 세부 즉 헌금세목
        else:
            name_diff = None
            code1 = None
            hun_detail = None

        if self.Bankincome_check.isChecked() == True: # text()
            Bank = '통장예입'
        else:
            Bank = None
        marks = self.marks_widget.text()
        id_value = int(self.id)
        data = (v_date, v_year, v_month, v_week, code1, name_diff, v_gubun, mok_hang, hun_mok, amount, hun_detail, Bank, marks, user_name, id_value)

        update_hun_db_sql(data)

        # self.registed_name.clear()  # 성도명 코드
        self.amount_widget.clear()
        # self.code1_widget.clear() # 개별코드
        self.marks_widget.clear()
        QMessageBox.about(self,'저장',"헌금 내역이 변경되었습니다.!!!")
        self.close()

    def amount_QSpin(self) :
        re_amount = self.amount_widget.text()
        amount = re_amount.replace(',','')
        # if not self.amount_widget.text().isdigit():
        if amount != ''and amount != '-':  # if not amount.isdigit():
            amount_int = int(amount)
            amount_txt = format(amount_int,(','))
            self.amount_widget.setText(amount_txt)
        else:
            QMessageBox.about(self, '오류', '금액란은 숫자만 입력하세요.')
            self.amount_widget.setFocus()
            return


       
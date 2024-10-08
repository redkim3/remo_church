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

form_class = uic.loadUiType("./ui/hun_modify_reg_form.ui")[0]

class hun_modify_Register(QDialog, form_class) :
    def __init__(self, id) :
        super().__init__()
        self.id = id
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        global gubun, selec1
        self.setWindowTitle('헌금계정 수정 등록')
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        
        self.hun_date_widget.setDate(today)
        # test = self.cost_date_widget.text() 
        year_widget = str(today.year())
        self.year_widget.setText(year_widget) # = QLabel(order_sign1)
        month_widget = str(today.month())
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)
        self.month_widget.setText(month_widget)
        self.selected_row_data_call()
        self.month_widget.setFocus()
        self.amount_widget.editingFinished.connect(self.amount_QSpin)
        # self.year_widget.editingFinished.connect(self.handle_year_editing)
        # self.week_widget.editingFinished.connect(self.handle_week_editing)

        v_year = int(self.year_widget.text())
        gubun_combo = []
        selec = ["선택"]
        item1 = gubun_values()
        gubun_combo = selec + item1
        self.gubun_name_combo_widget.addItems(gubun_combo)
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

    # def handle_week_editing(self):
    #     self.gubun_combobox()

    def selected_row_data_call(self): # sql문으로 데이터 불러오기 방법은 id
        from modify.hun_modify_sql_save import selected_row_data_call
        from basic.hun_name_2 import gubun_values
        from basic.cost_select import cost_hang_values, cost_mok_values, cost_semok_values
        from payed_account.payed_account_sql import payed_account_values
        id_value = int(self.id)
        selec = ["선택"]
        item1 = gubun_values()
        gubun_combo = selec + item1
        selected_hun_data = selected_row_data_call(id_value)
        # date_object, call_year, call_month, call_week, call_gubun, call_hang, call_mok, call_semok, call_cost_detail, call_amount, call_bank, call_marks in selected_hun_data
        # date_object = datetime.date(2024, 2, 4)
        date_object = selected_hun_data[0][1]
        date_string = date_object.strftime("%Y-%m-%d")
        self.hun_date_widget.setDate(date_object) #
        self.year_widget.setText(str(selected_hun_data[0][2]))
        self.month_widget.setText(str(selected_hun_data[0][3]))
        self.week_widget.setText(str(selected_hun_data[0][4]))
        v_year = self.year_widget.text()
         # 사용 예시
        self.code1_widget.setText(str(selected_hun_data[0][5]))
        self.registed_name.setText(str(selected_hun_data[0][6]))
        selected_gubun = selected_hun_data[0][5]

        i1 = self.set_value_in_combo(gubun_combo, selected_gubun)
        
        # if i1 != -1:
        self.gubun_name_combo_widget.setItemText(i1, selected_gubun)
        # self.gubun_name_combo_widget.setCurrentText(selected_gubun)
            # self.gubun_name_combo_widget.itemText(i1,selected_gubun)
        # else:
        #     QMessageBox.about(self, "에러", "구분 리스트에 없습니다. 확인해 주세요")
        # gubun = self.gubun_name_combo_widget.itemText(i1)
        # print(gubun)
        # item2 = cost_hang_values(v_year,gubun)
        # print(item2)
        # hang_combo = selec + item2
        # selected_hang = selected_hun_data[0][6]
        # i2 = self.set_value_in_combo(hang_combo, selected_hang)
        # if i2 != -1:
        #     self.hang_combo_widget.itemText(i2,selected_hang)
        # else:
        #     QMessageBox.about(self, "에러", "항 리스트에 없습니다. 확인해 주세요")
        # hang = self.hang_combo_widget.currentText()
        # item3 = cost_mok_values(v_year,hang)
        # mok_combo = selec + item3
        # selected_mok = selected_hun_data[0][7]
        # i3 = self.set_value_in_combo(mok_combo, selected_mok)
        # if i3 != -1:
        #     self.mok_combo_widget.itemText(i3,selected_mok)
        # else:
        #     QMessageBox.about(self, "에러", "목 리스트에 없습니다. 확인해 주세요")
        # mok = self.mok_combo_widget.currentText()
        # item4 = cost_semok_values(v_year,mok)
        # semok_combo = selec + item4
        # selected_semok = selected_hun_data[0][8]
        # i4 = self.set_value_in_combo(semok_combo, selected_mok)
        # if i4 != -1:
        #     self.hang_combo_widget.itemText(i4,selected_semok)
        # else:
        #     QMessageBox.about(self, "에러", "세목 리스트에 없습니다. 확인해 주세요")
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

    # def gubun_combobox(self):
    #     from basic.hun_name_2 import gubun_values
    #     global gubun, selec1
    #     v_year = int(self.year_widget.text())
    #     gubun_combo = []
    #     if v_year == today.year():
    #         # self.gubun_name_combo_widget.clear()
    #         selec = ["선택"]
    #         item1 = gubun_values()
    #         gubun_combo = selec + item1
    #         # self.gubun_name_combo_widget.addItems(selec)
    #         self.gubun_name_combo_widget.addItems(gubun_combo)
    #         # gubun = self.gubun_name_combo_widget.currentText()
    #         self.gubun_name_combo_widget.currentTextChanged.connect(self.hun_name_combobox)
    #     return gubun_combo
       
    def hun_name_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자
        from basic.hun_name_2 import  other_gubun_mok_values
        global selec1
        gubun = self.gubun_name_combo_widget.currentText()
        hun_mok_list = []   
        v_year = self.year_widget.text()
        hang_0 = ["선택"]
        hun_mok_tuple = other_gubun_mok_values(v_year,gubun)
        hun_mok_list = hang_0 + hun_mok_tuple
        # for hang in hang_tuple:
        #     cost1, id = hang
        #     hang_list.append(cost1)
        self.hun_name_widget.addItems(hun_mok_list)
        self.hun_name_widget.currentTextChanged.connect(self.hun_combobox)

        # self.hun_name_widget_widget.currentTextChanged.connect(self.mok_combobox)
        
    def hun_combobox(self):  # 헌금명칭을 넣고 나면 진행하는것
        from basic.hun_name_2 import  hun_semok_values
        global mok, j
        j = 1
        Hun_detail_list = []
        mok = self.hun_name_widget.currentText()
        self.hun_detail_combo.clear()
        hun_detail_select = ['선택']
        v_year = self.year_widget.text()
        hun_semok = hun_semok_values(v_year,mok)
        H_semok = []
        for H_se in hun_semok:
            h_s, id = H_se
            H_semok.append(h_s)
        Hun_detail_list = hun_detail_select + H_semok
        self.hun_detail_combo.addItems(Hun_detail_list) 
        self.fix_hun_detail.text()
        self.hun_detail_combo.currentText()
        if mok == '주일헌금':
            self.registed_name.clear()
            self.code1_widget.clear()
            self.registed_name.hide()
            self.name_1.hide()
        else:
            self.registed_name.show()
            self.name_1.show()

        if mok == '목적헌금' :
            self.fix_hun_detail.setText('목적세부')
            self.hun_detail_combo.show()
        else:
            self.fix_hun_detail.clear()
            self.hun_detail_combo.clear()
            self.hun_detail_combo.hide()

        # self.registed_name.setText('')
        # self.amount_widget.clear()
        # self.code1_widget.clear()
        # self.marks_widget.clear()
        self.registed_name.editingFinished.connect(self.name_input)

    def name_input(self):
        from basic.member import code1_select, name_diff_select
        N_code = name_diff_select()
        mok = self.hun_name_widget.currentText()
        namecode = self.registed_name.text()

        if mok != "주일헌금" and mok != "이자소득" and mok != "타회계이월":
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
        hun_mok = self.hun_name_widget.currentText()
            
        v_gubun = self.gubun_name_combo_widget.currentText()
        mok_hang = mok_hang_values(v_year,hun_mok,v_gubun)
        hun_hang = ', '.join(map(str, mok_hang))  # 헌금명칭
        amo_txt = self.amount_widget.text()
        if amo_txt == None:
            QMessageBox.about(self, '오류', '금액이 없어 저장할 수 없습니다.')
            self.registed_name.setFocus()
            return
        amount = int(amo_txt.replace(',',''))
        name_diff = self.registed_name.text()
        if name_diff == '':
            name_diff = None
        else:
            name_diff = self.registed_name.text()
        code1 = self.code1_widget.text()
        if code1 == '':
            code1 = None
        else:
            code1 = self.code1_widget.text()
        hun_detail = str(self.hun_detail_combo.currentText())   # 헌금 세부 즉 헌금세목
        if hun_detail == '':
            hun_detail = None
        else:
            hun_detail = str(self.hun_detail_combo.currentText())   # 헌금 세부 즉 헌금세목

        if self.Bankincome_check.isChecked() == True: # text()
            Bank = '통장예입'
        else:
            Bank = None
        marks = self.marks_widget.text()
        id_value = int(self.id)
        data = (v_date, v_year, v_month, v_week, code1, name_diff, v_gubun, hun_hang, hun_mok, amount, hun_detail, Bank, marks, user_name, id_value)

        update_hun_db_sql(data)

        self.registed_name.clear()  # 성도명 코드
        self.amount_widget.clear()
        self.code1_widget.clear() # 개별코드
        self.marks_widget.clear()
        QMessageBox.about(self,'저장',"헌금 내역이 변경되었습니다.!!!")
        self.close()

    def amount_QSpin(self) :
        re_amount = self.amount_widget.text()
        amount = re_amount.replace(',','')
        # if not self.amount_widget.text().isdigit():
        if not amount.isdigit():
            QMessageBox.about(self, '오류', '금액란은 숫자만 입력하세요.')
            self.amount_widget.setFocus()
            return

        amount_int = int(amount)
        amount_txt = format(amount_int,(','))
        self.amount_widget.setText(amount_txt)
       
import pymysql, os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다 
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QDoubleValidator
from datetime import datetime
from basic.hun_name_2 import gubun_values
from payed_account.payed_account_sql import payed_account_values
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 

form_class = uic.loadUiType("./ui/special_modify_reg_form.ui")[0]

class Special_modify_register(QDialog, form_class) :
    def __init__(self, id) :
        super().__init__()
        self.id = id
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        global gubun, selec1
        self.setWindowTitle('특별회계 계정수정 등록')
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        
        self.cost_date_widget.setDate(today)
        # test = self.cost_date_widget.text() 
        year_widget = str(today.year())
        self.year_widget.setText(year_widget) # = QLabel(order_sign1)
        month_widget = str(today.month())
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)
        self.month_widget.setText(month_widget)
        self.special_selected_row_data_call()
        self.month_widget.setFocus()
        # self.amount_widget.editingFinished.connect(self.amount_QSpin)
        # self.year_widget.editingFinished.connect(self.handle_year_editing)
        # self.week_widget.editingFinished.connect(self.handle_week_editing)
        self.amount_widget.editingFinished.connect(self.amount_confirm)


        # selec = ["선택"]
        # item1 = gubun_values()
        # gubun_combo = selec + item1
        # self.gubun_combo_widget.addItems(gubun_combo)
        self.hang_combobox()
        # self.gubun_combo_widget.currentTextChanged.connect(self.hang_combobox)
        self.amount_widget.editingFinished.connect(self.banks_combobox)
        
    def cost_reg_button(self):
        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.cost_reg_file_close)
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
        # config['user'][user_reg_check] = user_reg_check
    
        return user_name

    # def handle_week_editing(self):
    #     self.hang_combobox()

    def special_selected_row_data_call(self): # sql문으로 데이터 불러오기 방법은 id
        from modify.modifed_sql_save import special_selected_row_data_call
        id_value = int(self.id)
        selected_cost_data = special_selected_row_data_call(id_value)

        date_object = selected_cost_data[0][1]
        date_string = date_object.strftime("%Y-%m-%d")
        self.cost_date_widget.setDate(date_object) #
        self.year_widget.setText(str(selected_cost_data[0][2]))
        self.month_widget.setText(str(selected_cost_data[0][3]))
        self.week_widget.setText(str(selected_cost_data[0][4]))
        v_year = self.year_widget.text()
        
        self.cost_detail_widget.setText(selected_cost_data[0][9])
        amo_txt = selected_cost_data[0][11]
        amount = format(amo_txt,(","))
        self.amount_widget.setText(amount)
       
        self.marks_widget.setText(selected_cost_data[0][13])
    
    # 콤보 상자에 특정 값을 설정하는 함수
    def set_value_in_combo(self, combo_box, value):
        for index in range(len(combo_box)):
            if combo_box[index] == value:
                # combo_box.setCurrentIndex(index)
                return index
        # 원하는 값이 콤보 상자에 없는 경우에 대비하여 -1 반환
        return -1
       
    def hang_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자
        from basic.cost_select import cost_hang_values
        gubun = "특별회계"
        hang_list1 = []
        v_year = self.year_widget.text()
        hang_tuple = cost_hang_values(v_year,gubun)
        for hang in hang_tuple:
            cost1, id = hang
            hang_list1.append(cost1)
        
        self.hang_combo_widget.addItems(["선택"] + hang_list1)
        self.hang_combo_widget.currentTextChanged.connect(self.mok_combobox)
        self.semok_combo_widget.currentTextChanged.connect(self.banks_combobox)
        
    def mok_combobox(self):
        from basic.cost_select import cost_mok_values
        cost_hang = self.hang_combo_widget.currentText()

        try:
            if cost_hang : #   len(cost_mok_values(cost_hang)) > 0: 
                v_year = self.year_widget.text()
                self.mok_combo_widget.clear()
                mok_tuple = cost_mok_values(v_year,cost_hang)
                mok_item = ["선택"]
                mok_list_1 = []
                for mok in mok_tuple:
                    mok_1, id = mok
                    mok_list_1.append(mok_1)
                mok_list = mok_item + mok_list_1
                self.mok_combo_widget.addItems(mok_list)
                self.mok_combo_widget.currentTextChanged.connect(self.semok_combobox)
        except pymysql.Error as e: #ValueError:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            return

    def semok_combobox(self):
        from basic.cost_select import cost_semok_values
        mok = self.mok_combo_widget.currentText()
        v_year = self.year_widget.text()
        self.semok_combo_widget.clear()
        try:
            if len(cost_semok_values(v_year,mok)) > 0:
                semok_item = ["선택"]
                # self.semok_combo_widget.addItems(semok_item)
                semok_list_1 = []
                semok_tuple = cost_semok_values(v_year,mok)
                for semok in semok_tuple:
                    semok_1, id = semok
                    semok_list_1.append(semok_1)
                semok_list = semok_item + semok_list_1
                self.semok_combo_widget.addItems(semok_list)
                
        except:
            pass

    def balance_combobox(self):
        self.balance_combo_widget.clear()
        increment = ['선택','예금증가','예금감소','예금증감 없음']
        self.balance_combo_widget.addItems(increment)


    # def cost_detail_set(self):
    #     cost_semok = self.semok_combo_widget.currentText()
        # self.special_account_detail_widget.setText(cost_semok) 

    def banks_combobox(self):   #  항 콤보를 만들고 이후 목,세목의 콤보를 만들자 
        from register.bank_account_reg import bank_name_list
        self.banks_combo_widget.clear()
        bank1 = bank_name_list('특별회계')
        self.banks_combo_widget.addItems(bank1 + ['일반회계에서','선교회계에서'])
        self.banks_combo_widget.currentTextChanged.connect(self.balance_combobox)

    
    # def bank_combobox(self):
    #     from basic.special_acc_sql import select_bank
    #     confirm_data = self.user_confirm()
    #     special_check = int(confirm_data[3]) # 특별회계
    #     # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
    #     self.bank_combo_widget.clear()
    #     self.result_tableWidget.clearContents()
    #     self.result_tableWidget.setRowCount(1)
    #     self.bank_combo_widget.addItems(["선택"] + select_bank("특별회계"))
        

    def amount_confirm(self):
        validator = QDoubleValidator(-1e+100, 1e+100, 0)  # 범위와 소수점 자릿수 설정
        self.amount_widget.setValidator(validator)
        # re_amount = self.amount_widget.text()
 
        # # if not self.amount_widget.text().isdigit():
        # if  amount != "" or amount != '-': # not amount.isdigit():
        #     QMessageBox.about(self, '오류', '금액란은 숫자만 입력하세요.')
        #     return
        
        amount_pre = ''
        amount_pre = self.amount_widget.text()
        amount_pre =int(amount_pre.replace(',','')) #콤마제거 후 정수로 받음
        pri_int = int(amount_pre)
        price_2 = format(pri_int,(','))
        self.amount_widget.setText(price_2)

    def data_call(self):
        global hap_total, j
        
        hang = self.hang_combo_widget.currentText()
        mok = self.mok_combo_widget.currentText()
        semok = self.semok_combo_widget.currentText()
        cost_detail = self.cost_detail_widget.text()
        amount = self.amount_widget.text()
        if amount != "":
            idf_8_amo = int(amount.replace(',',''))
            idf_8 = int(idf_8_amo)
            amount = format(idf_8,",")
        paid_banks = self.banks_combo_widget.currentText()
        marks = self.marks_widget.text()
        self.hang_combo_widget.setFocus()
        self.registed_name.setFocus()
        return
        
    def cost_reg_file_close(self):
        self.close()

    def year_compare(self):
        Y1 = self.year_widget.text()
        if Y1 == str(today.year()):
            return False  # 현재 년도와 같으면 False 반환
        else:
            QMessageBox.about(self, '', "'지출년도'가 현재의 '년도'와 같아야 합니다. ")
            # self.week_widget.clear()
            # self.gubun_combo_widget.clear()
            self.year_widget.setFocus()
            return True  # 현재 년도와 다르면 True 반환

    def accounting_change(self):
        from modify.modifed_sql_save import balance_db_row_modify
        global record
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
        if self.week_widget.text()!= '' :
            s_date = self.cost_date_widget.text()
            v_date = datetime.strptime(s_date,'%Y-%m-%d')
            v_year = int(self.year_widget.text())
            v_month = int(self.month_widget.text())
            user_name = self.user_widget.text()
            v_week = int(self.week_widget.text())
            v_gubun = "특별회계"
            v_hang = self.hang_combo_widget.currentText()
            v_mok = self.mok_combo_widget.currentText()
            v_semok = self.semok_combo_widget.currentText()
            v_memo = self.cost_detail_widget.text()
            v_bank = self.banks_combo_widget.currentText()
            amo_txt = self.amount_widget.text()
            v_amount = int(amo_txt.replace(',',''))
            balance = self.balance_combo_widget.currentText()
            v_marks = self.marks_widget.text()
            id_value = self.id

            if any(cell_item == None for cell_item in [v_hang, v_mok, v_semok, v_memo, v_bank, v_amount, balance, v_marks]):
                QMessageBox.about(self, '에러', '저장할 데이터에 누락된 값이 있습니다.')
                return
                
            data = (v_date,v_year,v_month,v_week,v_gubun,v_hang,v_mok,v_semok, v_memo, v_bank, v_amount, balance, v_marks, user_name, id_value)
            
            balance_db_row_modify(data)
            QMessageBox.information(None, "완료", "지출내역 정보가 변경 되었습니다.")
           
            self.close()
            
        else:
            QMessageBox.about(self,'',"상단의 '지출일자','년도',월,주 는 기본 저장사항입니다. 지우지 마십시오.!!!")    
            self.week_widget.setFocus()    
        
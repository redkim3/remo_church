import pymysql, os
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import  uic # QtCore, QtGui, QtWidgets,
from PyQt5.QtWidgets import *
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
cur_fold = os.getcwd()
host_name = config['MySQL']['host']

today = QDate.currentDate()
#now = today.toString(Qt.ISODate) 
now = datetime.now().strftime('%Y-%m-%d')

hun_imsi = []; Bank = ''; hap_total = 0 ; j = 1

form_class = uic.loadUiType("ui/hun_reg_form.ui")[0]

class HungumRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        global mok
        self.setWindowTitle('헌금등록')
        self.hun_detail_combo.hide()     # 헌금세부 콤보
        self.hun_date = QDateEdit()   
        self.hun_date_widget.setDate(today)  # 헌금일자
        year_widget = str(today.year())
        month_widget = str(today.month())
        user_name = self.user_confirm()
        self.user_widget.setText(user_name)
        self.new_input = False
        
        # self.hun_detail_combo.hide()     # 헌금세부 콤보      
        self.year_widget.setText(year_widget)      # 헌금 반영 년도
        self.month_widget.setText(month_widget)    # 헌금 반영 월
        self.addhun_input.setEnabled(False)
        self.hunsave_button.setEnabled(False)
        self.re_calculate_button.setEnabled(False)
        self.remove_row_button.setEnabled(False)
        self.registed_name.setEnabled(False)
        self.amount_widget.setEnabled(False)
        self.marks_widget.setEnabled(False)
        self.year_widget.editingFinished.connect(self.year_compare)
        self.week_widget.editingFinished.connect(self.hun_gubun_combobox)
        self.gubun_name_combo_widget.currentTextChanged.connect(self.hun_name_combo)
        self.hun_name_widget.currentTextChanged.connect(self.hun_combobox)
        self.year_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.month_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.week_widget.returnPressed.connect(lambda: self.focusNextChild())
        self.amount_widget.textChanged.connect(self.on_amount_changed)
        self.hun_tableWidget.itemChanged.connect(self.on_item_changed)
        self.registed_name.editingFinished.connect(self.select_code1)
        self.marks_widget.editingFinished.connect(self.hun_input)
        self.hun_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정

    def showEvent(self, event):
        super(HungumRegister, self).showEvent(event)
        self.set_cursor_position()

    def set_cursor_position(self):
        # 커서를 특정 위치로 설정합니다 (예: QLineEdit)
        self.end_close = False  # 닫기에서는 True
        self.month_widget.setFocus()
        self.month_widget.setCursorPosition(0)  # 커서를 맨 앞에 위치시킵니다

    def on_amount_changed(self):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        amount_value_text = self.amount_widget.text()
        try:
            if amount_value_text : #!= "" and amount_value_text != "-" :
                if '.' in amount_value_text:
                    amount_value = float(amount_value_text.replace(",", ""))
                else:
                    amount_value = int(amount_value_text.replace(",", ""))
                    self.amount_widget.setText(f"{amount_value:,}")  # 숫자를 쉼표로 포맷팅
            
            self.addhun_input.setEnabled(True)
        except ValueError:
            QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")
            self.amount_widget.clear()
            self.amount_widget.setFocus()
            return
    
    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if self.new_input != True:
            if col == 2:  # 8번째 열
                try:
                    if item.text() != '-':  # '-'를 입력한 경우에는 예외를 발생시키지 않고 넘어감
                        value = int(item.text().replace(",", ""))
                        item.setText(f"{value:,}")  # 숫자를 쉼표로 포맷팅 
                except ValueError:
                    QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")

    def hun_gubun_combobox(self):  # 헌금명칭을 넣고 나면 진행하는것
        from basic.hun_name_2 import gubun_values
        self.gubun_name_combo_widget.blockSignals(True)
        self.gubun_name_combo_widget.clear()  # 회계구분 명칭(선교회계,일반회계,특별회계)
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지

        gubun = gubun_values()
        self.gubun_name_combo_widget.addItems(['선택'] + gubun)
        self.gubun_name_combo_widget.blockSignals(False)

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

    def hun_name_combo(self):
        global hap_total
        from basic.hun_name_2 import  gubun_mok_values
        self.hun_name_widget.blockSignals(True)
        hap_total = 0
        self.hap_total_widget.clear()   # 헌금 합계액
        self.hun_tableWidget.clearContents()  # 헌금자 리스트 테이블 
        self.hun_name_widget.clear()  # 헌금 명칭 콤보
        try:
            Y1 = self.year_widget.text()
            gubun = self.gubun_name_combo_widget.currentText()
            self.hun_name_widget.addItems(['선택'] + gubun_mok_values(Y1,gubun))  #  콤보 데이터 추가 

        except TypeError:
            pass

        self.hun_name_widget.blockSignals(False)

    def hun_combobox(self):  # 헌금명칭을 넣고 나면 진행하는것 헌금세목/
        from basic.hun_name_2 import  hun_semok_values
        from basic.not_use_p_name import not_use_personal_name_hun
        global mok, hap_total
        hap_total = 0
        not_use_name_hun_name_data = not_use_personal_name_hun()
        self.hap_total_widget.clear()
        self.hun_tableWidget.setRowCount(0)  # 0으로 하면 라인 추가에 문제가 발생함 
        mok = self.hun_name_widget.currentText()
        self.hun_detail_combo.clear()
        
        v_year = self.year_widget.text()
        hun_semok = hun_semok_values(v_year,mok)
        H_semok = []
        if hun_semok:
            for H_se in hun_semok:
                h_s, id = H_se
                H_semok.append(h_s)
         
        self.hun_detail_combo.addItems(['선택'] +H_semok) 
        self.fix_hun_detail.text()
        
        if mok in not_use_name_hun_name_data:  # non_use_personal_name = 주일헌금
            self.registed_name.hide()
            self.name_1.hide()
        else:
            self.registed_name.show()
            self.name_1.show()

        if (mok == '목적헌금') :
            #if mok == '목적헌금':
            self.fix_hun_detail.setText('목적세부')
            self.hun_detail_combo.show()
        else:
            self.fix_hun_detail.clear()
            self.hun_detail_combo.clear()
            self.hun_detail_combo.hide()

        self.registed_name.setText('')
        self.registed_name.setEnabled(True)
        self.amount_widget.setEnabled(True)
        self.marks_widget.setEnabled(True)
        self.amount_widget.clear()
        self.code1_widget.clear()
        self.marks_widget.clear()

    def select_code1(self):
        from basic.member import code1_select #, name_diff_select
        registed_name = self.registed_name.text()
        name_code = str(code1_select(registed_name))
        if self.end_close == False:
            if name_code != "" :
                code1_list = str(code1_select(registed_name))
                code1 = code1_list.strip("[',']")
                if code1 == "":
                    QMessageBox.about(self,'입력오류 !!!','성도명을 확인하여 주십시오.')
                    self.registed_name.clear()
                    self.registed_name.setFocus()
                else:
                    self.code1_widget.setText(code1)
                    
            else:
                # QMessageBox.about(self,'입력오류 !!!','성도명을 확인하여 주십시오.')
                self.registed_name.clear()
                self.registed_name.setFocus()
                    
    def hun_input(self):
        from basic.not_use_p_name import not_use_personal_name_hun
        global hun_imsi, j, hap_total
        not_use_name_hun_name_data = not_use_personal_name_hun()
        self.new_input = True

        j = 1
        hun_mok = self.hun_name_widget.currentText()
        if mok in not_use_name_hun_name_data:
            try:
                re_count = self.hun_tableWidget.rowCount()
                if re_count != 0 :
                    confirm = self.hun_tableWidget.item(re_count-1, 2)
                    if confirm != None:
                        j = re_count + 1
                else:
                    self.hun_tableWidget.setRowCount(1)
                if j != 1:
                    self.hun_tableWidget.insertRow(j-1)

                marks = self.marks_widget.text()
                if self.Bankincome_check.isChecked() == True: # text()
                    Bank = '통장예입'
                else:
                    Bank = ''
                amo_str = self.amount_widget.text()
                if amo_str != None:
                    int_amo =(int(amo_str.replace(',',''))*1000) #콤마제거 후 정수로 받음
                if int_amo != '':
                    amount = format(int_amo,",")
                    self.amount_widget.setText(amount)
                
                # self.hun_tableWidget.setItem((j-1),0,QTableWidgetItem(code1))
                # self.hun_tableWidget.setItem((j-1),1,QTableWidgetItem(name_diff))
                self.hun_tableWidget.setItem((j-1),2,QTableWidgetItem(amount))
                self.hun_tableWidget.setItem((j-1),3,QTableWidgetItem(Bank))
                self.hun_tableWidget.setItem((j-1),4,QTableWidgetItem(marks))
                
                self.hun_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

                if self.hun_tableWidget.item(j-1, 2) != None:
                    self.hun_tableWidget.item(j-1, 2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                
                hap_total += int_amo
                hap_total_view = format(hap_total,',')
                self.hap_total_widget.setText(hap_total_view)
                self.hun_tableWidget.scrollToBottom()   # 자동 스크롤
                self.Bankincome_check.setChecked(False)
                self.new_input = False
                self.hunsave_button.setEnabled(True)
                self.re_calculate_button.setEnabled(True)
                self.remove_row_button.setEnabled(True)
                # self.registed_name.clear()  # 성도명 코드
                self.amount_widget.clear()
                # self.code1_widget.clear() #합산코드
                self.marks_widget.clear()
                self.amount_widget.setFocus()
                return

            except pymysql.Error as e: #ValueError:
                QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
                return
            except ValueError:
                self.amount_widget.setFocus()
                if j != 1:
                    self.hun_tableWidget.removeRow(j-1)
                return
            except UnboundLocalError:
                if j != 1:
                    self.hun_tableWidget.removeRow(j-1)
                self.amount_widget.setFocus()
                return
            
            
        else:
            if hun_mok == '선택':
                QMessageBox.about(self,'입력오류 !!!','헌금 명칭이 없습니다. 확인하여 주십시오')
                self.hun_name_widget.setFocus()
                return
            name_diff = self.registed_name.text()  # 성도명 코드

            if name_diff == "":  #hun_mok != non_use_personal_name and 
                self.registed_name.setFocus()
                return

            try:
                re_count = self.hun_tableWidget.rowCount()
                if re_count != 0 :
                    confirm = self.hun_tableWidget.item(re_count-1, 0)
                    if confirm != None:
                        j = re_count + 1
                else:
                    self.hun_tableWidget.setRowCount(1)
                if j != 1:
                    self.hun_tableWidget.insertRow(j-1)

                code1 = self.code1_widget.text() #개별코드
                marks = self.marks_widget.text()
                if self.Bankincome_check.isChecked() == True: # text()
                    Bank = '통장예입'
                else:
                    Bank = ''
                amo_str = self.amount_widget.text()
                if amo_str != None:
                    int_amo =int((float(amo_str.replace(',',''))*1000)) #콤마제거 후 정수로 받음
                if int_amo != '':
                    amount = format(int_amo,",")
                    self.amount_widget.setText(amount)
                
                self.hun_tableWidget.setItem((j-1),0,QTableWidgetItem(code1))
                self.hun_tableWidget.setItem((j-1),1,QTableWidgetItem(name_diff))
                self.hun_tableWidget.setItem((j-1),2,QTableWidgetItem(amount))
                self.hun_tableWidget.setItem((j-1),3,QTableWidgetItem(Bank))
                self.hun_tableWidget.setItem((j-1),4,QTableWidgetItem(marks))
                
                self.hun_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

                if self.hun_tableWidget.item(j-1, 2) != None:
                    self.hun_tableWidget.item(j-1, 2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                
                hap_total += int_amo
                hap_total_view = format(hap_total,',')
                self.hap_total_widget.setText(hap_total_view)
                self.Bankincome_check.setChecked(False)
                self.hun_tableWidget.scrollToBottom()  # 자동 스크롤
                self.new_input = False
                self.hunsave_button.setEnabled(True)
                self.re_calculate_button.setEnabled(True)
                self.remove_row_button.setEnabled(True)
                self.registed_name.clear()  # 성도명 코드
                self.amount_widget.clear()
                self.code1_widget.clear() #합산코드
                self.marks_widget.clear()
                self.registed_name.setFocus()
                return

            except pymysql.Error as e: #ValueError:
                QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
                return
            except ValueError:
                QMessageBox.about(self, "입력오류", '입력사항을 확인하세요')
            except UnboundLocalError:
                QMessageBox.about(self, "입력오류", '입력사항을 확인하세요')
            
        if j != 1:
            self.hun_tableWidget.removeRow(j-1)
        
    
    # def add_row_to_table(self, data):
    #     # 테이블에 새로운 행 추가
    #     row_position = self.hun_tableWidget.rowCount()
    #     self.hun_tableWidget.insertRow(row_position)

    #     # 데이터를 해당 행에 추가
    #     for column, value in enumerate(data):
    #         self.hun_tableWidget.setItem(row_position, column, QTableWidgetItem(value))

    #     # 행이 추가된 후, 스크롤바를 아래로 이동
    #     self.hun_tableWidget.scrollToBottom()
    
    def remove_row(self):   # 입력도중 삭제의 경우 공란이 생기거나 행에 문제가 생김
        global j, hap_total
        selectedRows = set()
        for item in self.hun_tableWidget.selectedItems():
            selectedRows.add(item.row())

        for row in sorted(selectedRows, reverse=True):
            self.hun_tableWidget.removeRow(row)
            j -= 1
        
        self.re_calculate()
        
        row_count = self.hun_tableWidget.rowCount()
        if row_count == 0:
            # self.hun_tableWidget.clearContents()
            self.hun_tableWidget.setRowCount(0)

    def re_calculate(self):
        global hap_total
        self.hun_tableWidget.blockSignals(True)
        hap_total = 0
        self.hap_total_widget.clear()
        row_count = self.hun_tableWidget.rowCount()
        for i in range(row_count):
            item = self.hun_tableWidget.item(i,2)
            if item is not None:  # 아이템이 None이 아닌지 확인
                imsi_amo = item.text()
                table_amo = int(imsi_amo.replace(',',''))
                amount = format(table_amo,',')
                self.hun_tableWidget.setItem(i,2,QTableWidgetItem(amount))
                self.hun_tableWidget.item(i,2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                hap_total += table_amo
                hap_sum_view = format(hap_total,',')
                self.hap_total_widget.setText(hap_sum_view)
        self.hun_tableWidget.blockSignals(False)

    def hun_register_reset(self):
        global hap_total, j
        hap_total = 0; j = 1
        self.hap_total_widget.clear()
        self.registed_name.clear()  # 성도명 코드
        self.amount_widget.clear()
        self.code1_widget.clear() #합산코드
        self.marks_widget.clear()
        self.gubun_name_combo_widget.clear()
        self.hun_tableWidget.setRowCount(0)
        self.hun_tableWidget.setRowCount(1)
        self.hun_name_widget.clear()
        self.week_widget.clear()
        self.hunsave_button.setEnabled(False)
        self.re_calculate_button.setEnabled(False)
        self.remove_row_button.setEnabled(False)
        self.registed_name.setEnabled(False)
        self.amount_widget.setEnabled(False)
        self.marks_widget.setEnabled(False)

    def file_close(self):
        self.end_close = True
        self.hun_register_reset()
        self.close()
    
    def closeEvent(self,event):
        self.end_close = True
        self.hun_register_reset()
        event.accept()

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
        from register.register_sql import hun_register
        from basic.not_use_p_name import not_use_personal_name_hun
        not_use_name_hun_name_data = not_use_personal_name_hun()
        if self.year_compare():  # year_compare()가 True를 반환했을 때만 실행
            return  # 현재 년도와 다르면 file_save() 메서드 실행 중지
        global j, hap_total
        j = 1; data = []
        in_date = now
        try:
            if self.hun_tableWidget.rowCount() > 0 :
                for row in range(self.hun_tableWidget.rowCount()):
                    # if self.hun_tableWidget.rowCount() > 0:
                    v_date = datetime.strptime(in_date,'%Y-%m-%d')
                    v_year = int(self.year_widget.text())
                    v_month = int(self.month_widget.text())
                    user_name = self.user_widget.text()
                    if not self.week_widget.text().isdigit():
                        QMessageBox.about(self, '오류', '주차는 숫자여야 합니다.')
                        self.week_widget.clear()
                        self.week_widget.setFocus()
                        return
                    v_week = int(self.week_widget.text())
                    hun_mok = self.hun_name_widget.currentText()
                    if hun_mok in not_use_name_hun_name_data:
                        view_data = self.hun_tableWidget.item(row, 2)
                        if view_data != None:
                            code1 = None
                            name_diff = None
                        else:
                            view_data = None
                        if view_data == None or view_data.text() == "":
                            self.registed_name.setFocus()
                            return
                    # if hun_mok != non_use_personal_name:  #'주일헌금':
                    else:
                        if self.hun_tableWidget.item(row, 0) != None:
                            view_data = self.hun_tableWidget.item(row, 0)
                            code1 = self.hun_tableWidget.item(row,0).text()
                            name_diff = self.hun_tableWidget.item(row,1).text()
                        else:
                            view_data = None

                        if view_data == None or view_data.text() == "":
                            self.registed_name.setFocus()
                            return

                    v_gubun = self.gubun_name_combo_widget.currentText()
                    my_hang = mok_hang_values(v_year,hun_mok,v_gubun)
                    hun_hang = ', '.join(map(str, my_hang))

                    amo_txt = self.hun_tableWidget.item(row,2).text()
                    if amo_txt == None:
                        QMessageBox.about(self, '오류', '금액이 없어 저장할 수 없습니다.')
                        self.registed_name.setFocus()
                        return
                    amount = int(amo_txt.replace(',',''))
                    hun_detail = str(self.hun_detail_combo.currentText())   # 헌금 세부 즉 헌금세목
                    Bank = self.hun_tableWidget.item(row,3).text()
                    marks = self.hun_tableWidget.item(row,4).text()
                    data = (v_date, v_year, v_month, v_week, code1, name_diff, v_gubun, hun_hang, hun_mok, amount, hun_detail, Bank, marks, user_name)
                    hun_register(data)
                
                hap_total = 0
                self.hap_total_widget.clear()
                self.hun_tableWidget.setRowCount(0)  # 0으로 하면 라인 추가에 문제가 발생함
                self.hun_tableWidget.setRowCount(1)
                self.registed_name.clear()  # 성도명 코드
                self.amount_widget.clear()
                self.code1_widget.clear() # 개별코드
                self.marks_widget.clear()
                self.hun_name_combo()
                QMessageBox.about(self,'저장',"헌금 내역이 저장되었습니다.!!!")
                self.hun_name_widget.setFocus()
            else:
                QMessageBox.about(self,'저장',"저장할 내역이 없습니다.!!!")
                self.registed_name.setFocus()
                return
        except pymysql.Error as e: #ValueError:
                QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
                self.registed_name.setFocus()
                return
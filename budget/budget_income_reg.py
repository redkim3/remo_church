import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from budget.budget_call_select import budget_mok_list
import configparser
today = QDate.currentDate()
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/budget_income_reg_form.ui")[0]
order_amo_hap = 0; jeolgi_amo_hap = 0; last_year_hap = 0
order_hap = ''; jeolgi_hap = ''

class BudgetIncome_Register(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.setWindowTitle("수입예산 등록")
        self.budget_year_widget.text()
        user_name = self.user_confirm()
        self.user_name.setText(user_name)
        self.this_order_tableWidget.setRowCount(1)
        self.last_order_tableWidget.setRowCount(1)
        self.this_jeol_tableWidget.setRowCount(1)
        self.last_jeol_tableWidget.setRowCount(1)
        self.block_changes = False
        self.jeol_block_changes = False
        self.this_order_tableWidget.itemChanged.connect(self.on_item_changed)
        self.this_jeol_tableWidget.itemChanged.connect(self.on_item2_changed)

    def button(self):
        #self.budget_year_widget.editingFinished.connect(self.serch_last_budget)
        last_year_budget_Button = QPushButton("전년도예산보기")
        last_year_budget_Button.clicked.connect(self.serch_last_budget)
        budget_save_Button = QPushButton("저장하기")
        budget_save_Button.clicked.connect(self.budget_save)
        budget_close_Button = QPushButton("종료하기")
        budget_close_Button.clicked.connect(self.budget_end_close)
        budget_list_Button = QPushButton("예산항목 가져오기")
        budget_list_Button.clicked.connect(self.budget_list)
        recalculate_Button = QPushButton("재계산")
        recalculate_Button.clicked.connect(self.re_calculate)
    
    def user_confirm(self):
        from user.for_user_sql import user_infor_sql
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        user_id = config['user']['user_id']
        user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
        user_name= user_info[0][0]        # 이름을 가져오고
        return user_name
    
    def serch_last_budget(self): # 지난해 예산 불러오기
        from budget.budget_call_select import income_order_budget, income_jeol_budget
        from basic.hun_name_2 import hun_hang_values, gubun_values
        global budg_year, order_amo_hap, jeolgi_amo_hap, last_year_hap, order_hap, jeolgi_hap
        order_amo_hap = 0; jeolgi_amo_hap = 0
        gubun = gubun_values()[1] # gubun[1]은 '일반회계'이다 향후 변경이 된다면 수정 이창이 일반회계 수입예산 등록이라 1로확정한다.
        budg_year_st = self.budget_year_widget.text() #budg_year_st는 예산년도 시작(start)
        if budg_year_st == "" or budg_year_st is None :
            self.budget_year_widget.setFocus()
            return
        else:
            if budg_year_st.isdigit():
                budg_year = int(budg_year_st)
                if budg_year < today.year():
                    QMessageBox.about(self, '입력오류', '수입 예산은 당해년도 이전자료는 수정할 수 없습니다..')
                    self.budget_year_widget.setFocus()
                    return
        self.last_order_tableWidget.setRowCount(1)
        self.last_jeol_tableWidget.setRowCount(1)
        self.last_year_order_amount.clear()
        self.last_year_jeolgi_amount.clear()
        self.last_order_tableWidget.clearContents()
        self.last_jeol_tableWidget.clearContents()
        try:
            last_serch_Y = budg_year - 1
            m_hang1 = hun_hang_values(last_serch_Y, gubun)[0][0]
            last_order_budget = income_order_budget(last_serch_Y, m_hang1)  # 전년도 예배헌금 수입예산 
            rCount = len(last_order_budget)
            self.last_order_tableWidget.setRowCount(rCount)
            ord_hun_list = budget_mok_list(budg_year-1,m_hang1)
            ord_Count = len(ord_hun_list)

            self.last_order_tableWidget.setRowCount(ord_Count)
            if ord_Count > 1:
                for j in range(ord_Count):  # j는 행 c는 열 목 리스트
                    o_mok = str(ord_hun_list[j][0])
                    
                    for jj in range(ord_Count):  # j는 행 c는 열
                        l_mok = str(last_order_budget[jj][0])
                        if o_mok == l_mok:
                            int_amo = int(last_order_budget[jj][1])
                            l_amo = format(int_amo,",")
                            order_amo_hap += int_amo
                            order_sum = format(order_amo_hap,",")

                        self.last_order_tableWidget.setItem(j,0,QTableWidgetItem(o_mok))
                        self.last_order_tableWidget.setItem(j,1,QTableWidgetItem(l_amo))

                        self.last_order_tableWidget.resizeColumnsToContents()
                        self.last_order_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                        self.last_order_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            last_jeol_budget = income_jeol_budget(last_serch_Y)
            rjCount = len(last_jeol_budget)
            self.last_jeol_tableWidget.setRowCount(rjCount)

            m_hang2 = hun_hang_values(last_serch_Y, "일반회계")[1][0]
            jeol_hun_list = budget_mok_list(budg_year-1,m_hang2)
            je_Count = len(jeol_hun_list)
            self.last_jeol_tableWidget.setRowCount(je_Count)
            if je_Count > 1:
                for i in range(je_Count):  # j는 행 c는 열
                    je_mok = str(jeol_hun_list[i][0])
            
                    for ii in range(je_Count):  # j는 행 c는 열
                        j_mok = str(last_jeol_budget[ii][0])
                        if je_mok == j_mok :
                            int_j_amo = int(last_jeol_budget[ii][1])
                            j_amo = format(int_j_amo,",")
                            jeolgi_amo_hap += int_j_amo
                            jeolgi_sum = format(jeolgi_amo_hap,",")

                            self.last_jeol_tableWidget.setItem(i,0,QTableWidgetItem(je_mok))
                            self.last_jeol_tableWidget.setItem(i,1,QTableWidgetItem(j_amo))

                            self.last_jeol_tableWidget.resizeColumnsToContents()
                            self.last_jeol_tableWidget.item(i,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                            self.last_jeol_tableWidget.item(i,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                
            self.last_year_order_amount.setText(order_sum)
            self.last_year_jeolgi_amount.setText(jeolgi_sum)
            last_year_sum = order_amo_hap + jeolgi_amo_hap
            last_year_hap = format(last_year_sum,",")
            self.last_year_hun_hap.setText(last_year_hap)

        except ValueError:
            QMessageBox.about(self, "자료없음","전년도 자료가 없습니다.")
        except IndexError:
            QMessageBox.about(self, "자료없음","전년도 자료가 없습니다.")
        except UnboundLocalError:
            QMessageBox.about(self, "항목없음","헌금 항 목에 대한 데이터가 없습니다.")
        
    def re_calculate(self):  # 재계산
        global hap_total
        last_amo_0 = None ; last_amo2 = None
        this_year_order_amount = 0; this_year_jeol_amount = 0
        order_row_count = self.this_order_tableWidget.rowCount()
        jeol_row_count = self.this_jeol_tableWidget.rowCount()
        last_year = self.last_jeol_tableWidget.rowCount()
        if last_year > 1:
            try:
                for i in range(order_row_count):
                    last_amo_0 = self.last_order_tableWidget.item(i,1).text()
                    last_amo = int(last_amo_0.replace(",",''))
                    imsi_amo_T = self.this_order_tableWidget.item(i,1).text()
                    imsi_amo = int(imsi_amo_T.replace(",",""))
                    amount = format(imsi_amo,",")
                    if last_amo != 0 and imsi_amo != 0 :
                        rate_or1 = (imsi_amo / last_amo) * 100
                        rate_or = "%.2f" % rate_or1  # 소수점 2자리 까지 표시 
                    else :
                        rate_or = 0

                    self.this_order_tableWidget.setItem(i,1,QTableWidgetItem(amount))
                    self.this_order_tableWidget.setItem(i,2,QTableWidgetItem(rate_or))
                    self.this_order_tableWidget.item(i,1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    self.this_order_tableWidget.item(i,2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    this_year_order_amount += imsi_amo
                    order_hap_view = format(this_year_order_amount,",")
                    self.this_year_order_amount.setText(order_hap_view)
                    self.this_order_tableWidget.resizeColumnsToContents()
                    last_order_amount_s = self.last_year_order_amount.text()
                    last_order_amount = int(last_order_amount_s.replace(",",""))
                    order_ratio_int = (this_year_order_amount / last_order_amount) * 100
                    order_ratio = "%.2f" % order_ratio_int
                    self.order_ratio_label.setText(order_ratio)

                for i in range(jeol_row_count):
                    last_amo2_1 = self.last_jeol_tableWidget.item(i,1).text()
                    last_amo2 = int(last_amo2_1.replace(",",""))
                    imsi_amo2_T = self.this_jeol_tableWidget.item(i,1).text()
                    imsi_amo2 = int(imsi_amo2_T.replace(",",""))
                    amount2 = format(imsi_amo2,',')
                    if last_amo2 != 0 and imsi_amo2 != 0 :
                        rate_jeol2 = (imsi_amo2 / last_amo2) * 100
                        rate_jeol = "%.2f" % rate_jeol2  # 소수점 2자리 까지 표시
                    else :
                        rate_jeol = 0
                    self.this_jeol_tableWidget.setItem(i,1,QTableWidgetItem(amount2))
                    self.this_jeol_tableWidget.setItem(i,2,QTableWidgetItem(rate_jeol))
                    self.this_jeol_tableWidget.item(i,1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    self.this_jeol_tableWidget.item(i,2).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    this_year_jeol_amount += imsi_amo2
                    jeol_hap_view = format(this_year_jeol_amount,',')
                    self.this_year_jeolgi_amount.setText(jeol_hap_view)
                    self.this_jeol_tableWidget.resizeColumnsToContents()
                    last_jeol_amount_s = self.last_year_jeolgi_amount.text()
                    last_jeol_amount = int(last_jeol_amount_s.replace(",",""))
                    jeol_ratio_int = (this_year_jeol_amount / last_jeol_amount) * 100
                    jeol_ratio = "%.2f" % jeol_ratio_int
                    self.jeol_ratio_label.setText(jeol_ratio)
                this_year_hun_hap = this_year_order_amount + this_year_jeol_amount
                this_year_hap = format(this_year_hun_hap,",")
                self.this_year_hun_hap.setText(this_year_hap)
            except:
                QMessageBox.about(self,'AttributeErro',"전년도 예산이 없습니다. !!!")  
        else:
            try:
                for i in range(order_row_count):
                    imsi_amo_T = self.this_order_tableWidget.item(i,1).text()
                    imsi_amo = int(imsi_amo_T.replace(",",""))
                    amount = format(imsi_amo,",")
                    self.this_order_tableWidget.setItem(i,1,QTableWidgetItem(amount))
                    self.this_order_tableWidget.item(i,1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    this_year_order_amount += imsi_amo
                    order_hap_view = format(this_year_order_amount,",")
                    self.this_year_order_amount.setText(order_hap_view)
                    self.this_order_tableWidget.resizeColumnsToContents()

                for i in range(jeol_row_count):
                    imsi_amo2_T = self.this_jeol_tableWidget.item(i,1).text()
                    imsi_amo2 = int(imsi_amo2_T.replace(",",""))
                    amount2 = format(imsi_amo2,',')
                    self.this_jeol_tableWidget.setItem(i,1,QTableWidgetItem(amount2))
                    self.this_jeol_tableWidget.item(i,1).setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    this_year_jeol_amount += imsi_amo2
                    jeol_hap_view = format(this_year_jeol_amount,',')
                    self.this_year_jeolgi_amount.setText(jeol_hap_view)
                    self.this_jeol_tableWidget.resizeColumnsToContents()
                this_year_hun_hap = this_year_order_amount + this_year_jeol_amount
                this_year_hap = format(this_year_hun_hap,",")
                self.this_year_hun_hap.setText(this_year_hap)
            except:
                QMessageBox.about(self,'AttributeErro',"전년도 예산이 없습니다. !!!")  
    def on_item2_changed(self, item):  # 절기헌금 테이블의 숫자값이 변경되고 ' , '  넣어주기
        if self.jeol_block_changes:
            return
        col = item.column()
        if col == 1:
            text = item.text()
            if text != '-':
                try:
                    value = int(text.replace(",", ""))
                    formatted_text = f"{value:,}"
                    if text != formatted_text:
                        self.jeol_block_changes = True
                        item.setText(formatted_text)
                        self.jeol_block_changes = False
                        self.re_calculate()
                        self.this_jeol_tableWidget.resizeColumnsToContents()
                except ValueError:
                    pass  # 숫자가 아닌 경우는 무시 
        self.this_jeol_tableWidget.resizeColumnsToContents()

    def on_item_changed(self,item):
        if self.block_changes:
            return
        col = item.column()
        if col == 1:
            text = item.text()
            if text != '-':
                try:
                    value = int(text.replace(",", ""))
                    formatted_text = f"{value:,}"
                    if text != formatted_text:
                        self.block_changes = True
                        item.setText(formatted_text)
                        self.block_changes = False
                        self.re_calculate()
                        self.this_order_tableWidget.resizeColumnsToContents()
                except ValueError:
                    pass  # 숫자가 아닌 경우는 무시 
        self.this_order_tableWidget.resizeColumnsToContents()
        
    def budget_end_close(self):  # 종료
        global order_amo_hap, jeolgi_amo_hap, last_year_hap
        order_amo_hap = 0
        jeolgi_amo_hap = 0
        last_year_hap = 0
        self.budget_reset()
        self.order_ratio_label.clear()
        self.jeol_ratio_label.clear()

        self.close()
    
    def closeEvent(self,event):
        global order_amo_hap, jeolgi_amo_hap, last_year_hap
        order_amo_hap = 0
        jeolgi_amo_hap = 0
        last_year_hap = 0
        self.budget_reset()
        self.order_ratio_label.clear()
        self.jeol_ratio_label.clear()

        event.accept()

    def budget_list(self):  # 예산 만들어진 것이 있으면 지워야 한다.   안 그러면 중복 저장이 될 것이다. 수정은 별도로 만들어라
        from basic.hun_name_2 import hun_hang_values, gubun_values
        from budget.budget_call_select import budget_hun_call, delete_hun_budget
        budg_year_st = self.budget_year_widget.text() #budg_year_st는 예산년도 시작(start)
        if budg_year_st == "" or budg_year_st is None :
            self.budget_year_widget.setFocus()
            return
        budg_year = int(budg_year_st)
        confirm = budget_hun_call(budg_year)
        if not confirm :
            self.budget_income_hang_mok_call(budg_year)
            
        else:
            reply = QMessageBox.question(self, '질문', '기존의 데이터를 삭제하고 새로이 진행하시겠습니까?', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # 사용자가 '예'를 선택한 경우
            if reply == QMessageBox.Yes:
                delete_hun_budget(budg_year)
                self.budget_income_hang_mok_call(budg_year)

            else: # 기존 예산 데이터 유지하고 수정하기
                self.budget_income_hang_mok_call(budg_year)
                
                # 기존 데이터 가져오기
                gubun = gubun_values()[1] # gubun[1]은 '일반회계'이다 향후 변경이 된다면 수정 이창이 일반회계 수입예산 등록이라 1로확정한다.
                m_hang1 = hun_hang_values(budg_year, gubun)[0][0]
                or_hun_list = budget_mok_list(budg_year,m_hang1)
                or_Count = len(or_hun_list)

                m_hang2 = hun_hang_values(budg_year, gubun)[1][0]
                jeol_hun_list = budget_mok_list(budg_year,m_hang2)
                je_Count = len(jeol_hun_list)
                self.this_jeol_tableWidget.setRowCount(je_Count)
            
                self.this_order_tableWidget.setRowCount(or_Count)
                being_data = budget_hun_call(budg_year)

                for row, bd in enumerate(being_data):
                    budg_hang = bd[0]
                    budg_mok = bd[1]
                    budg_amount_i = bd[2]
                    budg_amount = format(budg_amount_i,",")
                    budg_marks = bd[3]
                    id = bd[4]
                    
                    if budg_hang == '예배':
                        for j1 in range(or_Count):
                            mok = self.this_order_tableWidget.item(j1,0).text()
                            if mok :
                                if budg_mok == mok:
                                    self.this_order_tableWidget.setItem(j1,1,QTableWidgetItem(budg_amount))
                                    if self.this_order_tableWidget.item(j1,1) != None:
                                        self.this_order_tableWidget.item(j1,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    self.this_order_tableWidget.setItem(j1,3,QTableWidgetItem(budg_marks))
                                    self.this_order_tableWidget.setItem(j1,4,QTableWidgetItem(str(id)))
                    self.this_order_tableWidget.resizeColumnsToContents()
                    self.this_order_tableWidget.setColumnHidden(4, True)
                    if budg_hang == '절기헌금':
                        for j2 in range(je_Count):
                            mok = self.this_jeol_tableWidget.item(j2,0).text()
                            if mok :
                                if budg_mok == mok:
                                    self.this_jeol_tableWidget.setItem(j2,1,QTableWidgetItem(budg_amount))
                                    if self.this_jeol_tableWidget.item(j2,1) != None:
                                        self.this_jeol_tableWidget.item(j2,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    self.this_jeol_tableWidget.setItem(j2,3,QTableWidgetItem(budg_marks))
                                    self.this_jeol_tableWidget.setItem(j2,4,QTableWidgetItem(str(id)))
                
                    self.this_jeol_tableWidget.resizeColumnsToContents()
                    self.this_jeol_tableWidget.setColumnHidden(4, True)

                self.re_calculate()

    def budget_income_hang_mok_call(self,budg_year):
        from basic.hun_name_2 import hun_hang_values, gubun_values
        self.this_year_order_amount.clear()
        self.this_year_jeolgi_amount.clear()
        self.this_year_hun_hap.clear()
        self.this_order_tableWidget.clearContents()
        self.this_jeol_tableWidget.clearContents()
        gubun = gubun_values()[1] # gubun[1]은 '일반회계'이다 향후 변경이 된다면 수정 이창이 일반회계 수입예산 등록이라 1로확정한다.
        m_hang1 = hun_hang_values(budg_year, gubun)[0][0]
        or_hun_list = budget_mok_list(budg_year,m_hang1)
        or_Count = len(or_hun_list)
    
        self.this_order_tableWidget.setRowCount(or_Count)
        if or_Count > 1:
            for j in range(or_Count):  # j는 행 c는 열
                o_mok = str(or_hun_list[j][0])
                o_amo = '0'
                self.this_order_tableWidget.setItem(j,0,QTableWidgetItem(o_mok))
                self.this_order_tableWidget.setItem(j,1,QTableWidgetItem(o_amo))
                self.this_order_tableWidget.resizeColumnsToContents()
                if self.this_order_tableWidget.item(j,1) is not None:
                    self.this_order_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    
        m_hang2 = hun_hang_values(budg_year, gubun)[1][0] # 절기헌금
        jeol_hun_list = budget_mok_list(budg_year,m_hang2)
        je_Count = len(jeol_hun_list)
        self.this_jeol_tableWidget.setRowCount(je_Count)
        if je_Count > 1:
            for i in range(je_Count):  # j는 행 c는 열
                je_mok = str(jeol_hun_list[i][0])
                j_amo = '0'
                self.this_jeol_tableWidget.setItem(i,0,QTableWidgetItem(je_mok))
                self.this_jeol_tableWidget.setItem(i,1,QTableWidgetItem(j_amo))
                self.this_jeol_tableWidget.resizeColumnsToContents()
                if self.this_jeol_tableWidget.item(i,1) is not None:
                    self.this_jeol_tableWidget.item(i,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

    def budget_save(self):
        from budget.budget_call_select import budget_income_save

        hun_order_imsi = []; jeol_hun_imsi = []
        budg_year = self.budget_year_widget.text()        
        user_name = self.user_name.text()
        orderrow_Count = self.this_order_tableWidget.rowCount()
        jeolrow_Count = self.this_jeol_tableWidget.rowCount()
        
        try:
            for i in range(orderrow_Count):
                hun_hang = '예배'
                hun_mok = self.this_order_tableWidget.item(i, 0).text()
                hun_amount = self.this_order_tableWidget.item(i, 1).text()
                amount = hun_amount.replace(",","")
                if  self.this_order_tableWidget.item(i, 3):
                    hun_marks = self.this_order_tableWidget.item(i, 3).text()
                    if hun_marks == '':
                        hun_marks = None
                else:
                    hun_marks = None
                if self.this_order_tableWidget.item(i, 4):# == "":
                    id = self.this_order_tableWidget.item(i, 4).text()
                    d_type = "modi"
                    hun_order_imsi.append((amount,hun_marks,user_name,id,d_type))
                else:
                    id = None
                    d_type = "new"
                    hun_order_imsi.append((budg_year,hun_hang,hun_mok,amount,hun_marks,user_name,d_type))

                budget_income_save(hun_order_imsi) # ,orderrow_Count)
                hun_order_imsi = []
            
            for j in range(jeolrow_Count):
                jeol_hang = '절기헌금'
                jeol_mok = self.this_jeol_tableWidget.item(j, 0).text()
                jeol_amount_T = self.this_jeol_tableWidget.item(j, 1).text()
                jeol_amount = jeol_amount_T.replace(",","")
                if self.this_jeol_tableWidget.item(i, 3):
                    jeol_marks = self.this_jeol_tableWidget.item(j, 3).text()
                    if jeol_marks == '':
                        jeol_marks = None
                else:
                    jeol_marks = None

                if self.this_jeol_tableWidget.item(j, 4):
                    id = self.this_jeol_tableWidget.item(j, 4).text()
                    d_type = "modi"
                    jeol_hun_imsi.append((jeol_amount,jeol_marks,user_name,id,d_type))
                else:
                    id = None
                    d_type = "new"
                    jeol_hun_imsi.append((budg_year,jeol_hang,jeol_mok,jeol_amount,jeol_marks,user_name,d_type))

                budget_income_save(jeol_hun_imsi) #,jeolrow_Count)
                jeol_hun_imsi = []
            
            QMessageBox.about(self,'저장',"'수입예산이 저장되었습니다.!!!")
            self.budget_reset()
            hun_order_imsi.clear()

        except AttributeError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            QMessageBox.about(self,'저장',"등록된 내용이 없습니다.!!!")

        except OSError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            hun_order_imsi.clear()
    
    def budget_reset(self):
        self.last_year_order_amount.clear()
        self.last_year_jeolgi_amount.clear()
        self.last_year_hun_hap.clear()
        self.this_year_order_amount.clear()
        self.this_year_jeolgi_amount.clear()
        self.this_year_hun_hap.clear()
        self.last_order_tableWidget.clearContents()
        self.last_jeol_tableWidget.clearContents()
        self.last_order_tableWidget.setRowCount(1)
        self.last_jeol_tableWidget.setRowCount(1)
        self.this_order_tableWidget.clearContents()
        self.this_jeol_tableWidget.clearContents()
        self.this_order_tableWidget.setRowCount(1)
        self.this_jeol_tableWidget.setRowCount(1)
        

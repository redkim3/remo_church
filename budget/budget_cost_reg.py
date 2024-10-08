from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import collections, os
import configparser
today = QDate.currentDate()
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/budget_cost_reg_form.ui")[0]
order_amo_hap = 0; jeolgi_amo_hap = 0; 
order_hap = ''; jeolgi_hap = ''

class BudgetCost_Register(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.setWindowTitle("지출예산 등록")
        self.budget_year_widget.text()
        user_name = self.user_confirm()
        self.user_name.setText(user_name)
        self.block_changes = False
        self.this_year_budg_tableWidget.itemChanged.connect(self.on_item_changed)

    def button_connect(self):
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
    
    def serch_last_budget(self):
        from budget.budget_cost_select import cost_budget_call
        global budg_year 
        row = 0
        budg_year_st = self.budget_year_widget.text()
        if budg_year_st == "" or budg_year_st == None:
            self.budget_year_widget.setFocus()
            return
        else:
            if budg_year_st.isdigit():
                budg_year = int(budg_year_st)
                if budg_year < today.year():
                    QMessageBox.about(self, '입력오류', '지출 예산은 당해년도 이전자료는 수정할 수 없습니다..')
                    self.budget_year_widget.setFocus()
                    return
            else:
                QMessageBox.about(self, '입력오류', '예산년도에 숫자를 확인해 주세요.')
                self.budget_year_widget.setFocus()
                return

        last_serch_Y = budg_year - 1
        self.last_year_tableWidget.clearContents()
        self.last_year_tableWidget.setRowCount(1)
        self.last_bud_hap_widget.clear()
        column_headers = ['항','목','세목','금액']
        self.last_year_tableWidget.setColumnCount(4)
        self.last_year_tableWidget.setRowCount(1)
        last_year_budget = cost_budget_call(last_serch_Y)  # 예산 내용 가져오기 
        self.last_year_tableWidget.setHorizontalHeaderLabels(column_headers)

        tree = collections.defaultdict(dict)

        # 결과 데이터를 트리로 변환합니다.
        for item in last_year_budget:
            hang, mok, semok, amount, marks, id = item
            if semok:
                if hang not in tree:
                    tree[hang] = {}
                if mok not in tree[hang]:
                    tree[hang][mok] = {}
                tree[hang][mok][semok] = amount
                
            elif mok:
                if mok in tree[hang]:
                    tree[hang][mok] = amount
                else:
                    tree[hang][mok] = amount
            else:
                tree[hang] = amount

        # 결과를 예시 형태로 출력합니다.
        # row_count = self.last_year_tableWidget.rowCount()  # 현재 행의 수 가져오기
        #self.last_year_tableWidget.insertRow(row_count)    # 새로운 행 추가

        row = 0; cost_sum = 0; s = 0; m = 0; mok_sum = 0
        for hang, mok_data in tree.items():
            hang_sum = 0
            if row != 0:
                self.last_year_tableWidget.insertRow(row)  # 행 삽입
            self.last_year_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입

            for mok, semok_data in mok_data.items():
                row += 1  # 행 인덱스 증가
                # mok_sum = 0  # 한 목의 합계 초기화
                self.last_year_tableWidget.insertRow(row)  # 행 삽입
                self.last_year_tableWidget.setItem(row, 1, QTableWidgetItem(mok))  # 행의 첫 번째 열에 항목 삽입
                  # 행 인덱스 증가;
                for semok, amount in semok_data.items():
                    if semok != '0':
                        row += 1 
                        s += 1; m += 1
                        self.last_year_tableWidget.insertRow(row)  # 행 삽입
                        amo_txt = format(amount,',')
                        self.last_year_tableWidget.setItem(row, 2, QTableWidgetItem(semok))  # 행의 첫 번째 열에 항목 삽입
                        self.last_year_tableWidget.setItem(row, 3, QTableWidgetItem(amo_txt))  # 행의 두 번째 열에 항목 삽입
                        if self.last_year_tableWidget.item(row, 3) != None:
                            self.last_year_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        mok_sum += amount  # 목의 합계 갱신
                        hang_sum += amount
                        cost_sum += amount
                        amount = 0
                    
                mok_sum += amount  # 목의 합계 갱신
                mok_sum_txt = format(mok_sum,',')
                self.last_year_tableWidget.setItem(row - s, 3, QTableWidgetItem(mok_sum_txt))  # 목의 합계 표시
                if self.last_year_tableWidget.item(row - s, 3) != None:
                    self.last_year_tableWidget.item(row - s, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                #hang_sum += mok_sum  # 행의 합계 갱신
                hang_sum += amount
                cost_sum += amount
                m += 1; s = 0; mok_sum = 0; amount = 0
            hang_sum_txt = format(hang_sum,',')
            self.last_year_tableWidget.setItem(row - m, 3, QTableWidgetItem(hang_sum_txt))  # 행의 합계 표시
            if self.last_year_tableWidget.item(row - m, 3) != None:
                self.last_year_tableWidget.item(row - m, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            m = 0; s = 0; row += 1
            
            cost_sum_txt = format(cost_sum,",")
            self.last_bud_hap_widget.setText(cost_sum_txt)

    def re_calculate(self):
        hap_total = 0
        this_year_count = self.this_year_budg_tableWidget.rowCount()
        last_year_count = self.last_year_tableWidget.rowCount()
        this_hang_amo_int = 0; this_mok_amo_int =0
        for a in range(this_year_count):
            this_hang_T1 = self.this_year_budg_tableWidget.item(a,0)  #a 는 0 부터
            this_hang_T2 = self.this_year_budg_tableWidget.item(a+1,0)
            this_semok_T1 = self.this_year_budg_tableWidget.item(a,2)
            this_semok_T2 = self.this_year_budg_tableWidget.item(a+1,2)
            this_mok_T1 = self.this_year_budg_tableWidget.item(a,1)
            this_mok_T2 = self.this_year_budg_tableWidget.item(a+1,1)
            if this_hang_T1 != None and this_hang_T2 != None : # 항이 현재항과 아래도 항의 있을때, 목이 없는 경우(현재는 이런 경우 없음)
                this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                this_amo_int = int(this_amo_T.replace(",",''))
                this_amo_f = format(this_amo_int,",")
                hap_total += this_amo_int
                self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            elif this_hang_T1 != None and this_hang_T2 == None : # 현재의 항에는 있고 아래의 항에는 없을때 즉 목에 있다(?)그러므로 목이 있는 항의 시작
                hang_c_adj = 0 ; this_hang_amo_int = 0  # 항의 차감 행의 수(hang_c_adj), 항의 합계(this_hang_amo_int)를 초기화 한다.
            elif this_hang_T1 == None and this_hang_T2 == None :  # 여기는 항의 목이 이어지는 형태이다.
                if this_mok_T1 != None and this_mok_T2 != None:   # 현재와 아래의 목에 값이있다. 목의 갑을 받아 넣는다. 항에 값에 더한다.
                    hang_c_adj += 1
                    this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                elif this_mok_T1 != None and this_mok_T2 == None: # 현재 목의 명칭은 있고 다음 목의 명칭은 없다.  세목이 있거나. 다음 항으로 간다.
                    if this_semok_T1 == None and this_semok_T2 != None: # 아래부터 세목이 있는 경우
                        mok_c_adj = 0
                        hang_c_adj += 1
                    elif this_semok_T1 == None and this_semok_T2 == None:
                        hang_c_adj += 1
                        this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_hang_amo_int += this_amo_int  # this_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        this_hang_amo = format(this_hang_amo_int,",")
                        hap_total += this_amo_int
                        self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))  # 목의 값이다.
                        self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.this_year_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))  # 목의 값이다.
                        self.this_year_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        hang_c_adj = 0; this_hang_amo_int =0
                    
                elif this_mok_T1 == None and this_mok_T2 == None:
                    if this_semok_T1 != None and this_semok_T2 != None:
                        mok_c_adj += 1
                        hang_c_adj += 1
                        this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_mok_amo_int += this_amo_int
                        this_hang_amo_int += this_amo_int  # this_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        hap_total += this_amo_int
                        self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))  # 목의 값이다.
                        self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        
                elif this_mok_T1 == None and this_mok_T2 != None :
                    if this_semok_T1 != None and this_semok_T2 == None :
                        mok_c_adj += 1
                        hang_c_adj += 1
                        this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_mok_amo_int += this_amo_int
                        this_mok_amo = format(this_mok_amo_int,",")
                        this_hang_amo_int += this_amo_int
                        this_hang_amo = format(this_hang_amo_int,",")
                        hap_total += this_amo_int
                        self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                        self.this_year_budg_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(this_mok_amo))
                        self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.this_year_budg_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.this_year_budg_tableWidget.setItem(a-mok_c_adj,6,QTableWidgetItem("id"))
                        self.this_year_budg_tableWidget.setItem(a-hang_c_adj,6,QTableWidgetItem("id"))
                        this_mok_amo_int = 0; mok_c_adj = 0
            
            elif this_hang_T1 == None and this_hang_T2 != None :
                if this_semok_T1 != None and this_semok_T2 == None :
                    mok_c_adj += 1
                    hang_c_adj += 1
                    this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_mok_amo_int += this_amo_int
                    this_mok_amo = format(this_mok_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.this_year_budg_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(this_mok_amo))
                    self.this_year_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))
                    self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.this_year_budg_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.this_year_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.this_year_budg_tableWidget.setItem(a-mok_c_adj,6,QTableWidgetItem("id"))
                    self.this_year_budg_tableWidget.setItem(a-hang_c_adj,6,QTableWidgetItem("id"))
                    mok_c_adj = 0; hang_c_adj = 0; this_hang_amo_int =0; this_mok_amo_int = 0
                if this_mok_T1 != None and this_mok_T2 == None :
                    hang_c_adj += 1
                    this_amo_T = self.this_year_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.this_year_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.this_year_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))  # 목으로만 분리된 항의 합계
                    self.this_year_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.this_year_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.this_year_budg_tableWidget.setItem(a-hang_c_adj,6,QTableWidgetItem("id"))

                    hang_c_adj = 0; this_hang_amo_int =0

        this_amo_f = format(this_amo_int,",")
        this_year_hap = format(hap_total,",")
        self.this_bud_hap_widget.setText(this_year_hap)
        # self.this_year_budg_tableWidget.setItem(a+1, 3, QTableWidgetItem(this_year_hap))  # 행의 합계 표시
        # if self.this_year_budg_tableWidget.item(a+1, 3) != None:
        #         self.this_year_budg_tableWidget.item(a+1, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

#여기부터는 증감율 계산
        if last_year_count > 1 and this_year_count > 1 :
            row_c = 0
            for i in range(this_year_count):
                this_hang_value = self.this_year_budg_tableWidget.item(i,0)
                if this_hang_value != None :
                    this_hang = self.this_year_budg_tableWidget.item(i,0).text()
                    row_c += 1
                    
                    for j in range(last_year_count):
                        last_hang_value = self.last_year_tableWidget.item(j,0)
                        if last_hang_value != None:
                            last_hang = self.last_year_tableWidget.item(j,0).text()
                            if this_hang == last_hang:
                                this_amo_t_value = self.this_year_budg_tableWidget.item(i,3)
                                last_amo_t_value = self.last_year_tableWidget.item(j,3)
                                if this_amo_t_value != None :
                                    this_amo_t = self.this_year_budg_tableWidget.item(i,3).text()
                                else:
                                    this_amo_t = '0'
                                if last_amo_t_value != None:
                                    last_amo_t = self.last_year_tableWidget.item(j,3).text()
                                else:
                                    last_amo_t = '0'
                                this_amo = int(this_amo_t.replace(",",''))
                                last_amo = int(last_amo_t.replace(",",''))
                                if this_amo != 0 and last_amo != 0:
                                    rate_comp = this_amo / last_amo * 100
                                    rate_comp = "%.2f" % rate_comp  # 소수점 2자리 까지 표시
                                    self.this_year_budg_tableWidget.setItem(i,4,QTableWidgetItem(rate_comp))
                                    self.this_year_budg_tableWidget.item(i,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                else:
                    this_mok_value = self.this_year_budg_tableWidget.item(i,1)
                    if this_mok_value != None:
                        this_mok = self.this_year_budg_tableWidget.item(i,1).text()
                      
                        for j in range(last_year_count):
                            last_mok_value = self.last_year_tableWidget.item(j,1)
                            if last_mok_value != None:
                                last_mok = self.last_year_tableWidget.item(j,1).text()
                                if last_mok != '':
                                    if this_mok == last_mok:
                                        this_amo_t_value = self.this_year_budg_tableWidget.item(i,3)
                                        last_amo_t_value = self.last_year_tableWidget.item(j,3)
                                        if this_amo_t_value != None :
                                            this_amo_t = self.this_year_budg_tableWidget.item(i,3).text()
                                        else:
                                            this_amo_t = '0'
                                        if last_amo_t_value != None:
                                            last_amo_t = self.last_year_tableWidget.item(j,3).text()
                                        else:
                                            last_amo_t = '0'
                                        this_amo = int(this_amo_t.replace(",",''))
                                        last_amo = int(last_amo_t.replace(",",''))
                                        if this_amo != 0 and last_amo != 0:
                                            rate_comp = this_amo / last_amo * 100
                                            rate_comp = "%.2f" % rate_comp  # 소수점 2자리 까지 표시
                                            self.this_year_budg_tableWidget.setItem(i,4,QTableWidgetItem(rate_comp))
                                            self.this_year_budg_tableWidget.item(i,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    
                    else:
                        this_semok_value = self.this_year_budg_tableWidget.item(i,2)
                        if this_semok_value != None:
                            this_semok = self.this_year_budg_tableWidget.item(i,2).text()
                            if this_semok != '':
                                for j in range(last_year_count):
                                    last_semok_value = self.last_year_tableWidget.item(j,2)
                                    if last_semok_value != None:
                                        last_semok = self.last_year_tableWidget.item(j,2).text()
                                        if last_semok != '':
                                            if this_semok == last_semok:
                                                this_amo_t_value = self.this_year_budg_tableWidget.item(i,3)
                                                last_amo_t_value = self.last_year_tableWidget.item(j,3)
                                                if this_amo_t_value != None :
                                                    this_amo_t = self.this_year_budg_tableWidget.item(i,3).text()
                                                else:
                                                    this_amo_t = '0'
                                                if last_amo_t_value != None:
                                                    last_amo_t = self.last_year_tableWidget.item(j,3).text()
                                                else:
                                                    last_amo_t = '0'
                                                this_amo = int(this_amo_t.replace(",",''))
                                                last_amo = int(last_amo_t.replace(",",''))
                                                if this_amo != 0 and last_amo != 0:
                                                    rate_comp = this_amo / last_amo * 100
                                                    rate_comp = "%.2f" % rate_comp  # 소수점 2자리 까지 표시
                                                    self.this_year_budg_tableWidget.setItem(i,4,QTableWidgetItem(rate_comp))
                                                    self.this_year_budg_tableWidget.item(i,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        else:
            for i in range(this_year_count):
                rate_comp = 0
                rate_comp = "%.2f" % rate_comp  # 소수점 2자리 까지 표시
                self.this_year_budg_tableWidget.setItem(i,4,QTableWidgetItem(rate_comp))
                self.this_year_budg_tableWidget.item(i,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.this_year_budg_tableWidget.resizeColumnsToContents()
        self.this_year_budg_tableWidget.setColumnHidden(6, True)
    
    def on_item_changed(self,item):
        if self.block_changes:
            return
        col = item.column()
        if col == 3:
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
                        self.this_year_budg_tableWidget.resizeColumnsToContents()
                except ValueError:
                    pass  # 숫자가 아닌 경우는 무시
        
    def budget_end_close(self):
        global order_amo_hap, jeolgi_amo_hap, last_year_hap
        order_amo_hap = 0
        jeolgi_amo_hap = 0
        last_year_hap = 0
        self.last_bud_hap_widget.clear()
        self.this_bud_hap_widget.clear()
        self.last_year_tableWidget.clearContents()
        self.this_year_budg_tableWidget.clearContents()
        self.last_year_tableWidget.setRowCount(1)
        self.this_year_budg_tableWidget.setRowCount(1)
        
        self.close()

    def budget_list(self):
        from budget.budget_call_select import budget_cost_call, delete_cost_budget
        budg_year_st = self.budget_year_widget.text() #budg_year_st는 예산년도 시작(start)
        if budg_year_st == "" or budg_year_st is None :
            self.budget_year_widget.setFocus()
            return
        budg_year = int(budg_year_st)
        budget_cost = budget_cost_call(budg_year)
        if len(budget_cost):
            confirm = "ok"
        
        if not confirm : # 기존의 데이터가 없으므로 신규,  그래서 항목을 그냥 가져오고 데이터를 입력할 준비를 한다.
            self.budget_cost_hang_mok_call(budg_year)
        else:
            reply = QMessageBox.question(self, '질문', '기존의 데이터를 삭제하고 새로이 진행하시겠습니까?', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             # 사용자가 '예'를 선택한 경우
            if reply == QMessageBox.Yes:
                delete_cost_budget(budg_year)
                self.budget_cost_hang_mok_call(budg_year)
            
            else: # No를 선택하게 되면 기존 예산 데이터 유지하고 수정한다. 그래서 항목을 가져오고 금액, 비고, id 까지 가져와서 수정저장한다.
                self.budget_cost_hang_mok_call(budg_year) # 항목 가져오기
                
                # 기존 데이터 가져오기
                # try:
                table_row_count = self.this_year_budg_tableWidget.rowCount()
                budg_cost_cnt = len(budget_cost)
                t_hang = None; t_mok = None; t_semok = None
                
                for row in range(table_row_count):
                    t_hang_T = self.this_year_budg_tableWidget.item(row,0)
                    t_mok_T = self.this_year_budg_tableWidget.item(row,1)
                    t_semok_T = self.this_year_budg_tableWidget.item(row,2)
                    if t_hang_T:
                        t_hang = t_hang_T.text()
                        t_mok = None
                        t_semok = None
                    if t_mok_T:
                        t_mok = t_mok_T.text()
                        t_semok = None
                    if t_semok_T:
                        t_semok = t_semok_T.text()
                    for r, data in enumerate(budget_cost):
                        bug_hang = data[0]
                        bug_mok = data[1]
                        bug_semok = data[2]
                        bug_amount_int = data[3]
                        bug_amount = format(bug_amount_int,",")
                        bug_marks = data[4]
                        id = data[5]
                        if t_hang == bug_hang and t_mok == bug_mok and t_semok == bug_semok :
                            self.this_year_budg_tableWidget.setItem(row, 3,QTableWidgetItem(bug_amount))
                            if self.this_year_budg_tableWidget.item(row, 3) != None:
                                self.this_year_budg_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                            self.this_year_budg_tableWidget.setItem(row, 5,QTableWidgetItem(bug_marks))
                            self.this_year_budg_tableWidget.setItem(row, 6,QTableWidgetItem(str(id)))
                self.this_year_budg_tableWidget.resizeColumnsToContents()
                self.this_year_budg_tableWidget.setColumnHidden(6, True)

                self.re_calculate()
                # except ValueError:
                #     self.budget_year_widget.setFocus() 
                #     return
        
    def budget_cost_hang_mok_call(self,budg_year):
        from basic.cost_hangmok_select import cost_budget_hang_list, cost_budget_mok_list, cost_budget_semok_list
        try:
            self.this_year_budg_tableWidget.clearContents()
            self.this_year_budg_tableWidget.setRowCount(1)
            gubun = "일반회계"
            co_this_hang_list = cost_budget_hang_list(budg_year,gubun)   # 계정 항 가져오기
            co_this_semok_tuple = cost_budget_semok_list(budg_year,'all')
            if co_this_semok_tuple != None:
                co_this_semok_mok_list = [item[0] for item in co_this_semok_tuple]
                co_this_Count = len(co_this_hang_list)
                self.this_year_budg_tableWidget.setRowCount(1)
            else:
                co_this_Count = 0

            row = 0
            
            if co_this_Count > 1:
                for j in range(co_this_Count):  # j는 행 c는 열
                    co_this_hang = co_this_hang_list[j][0]
                    co_amp = '0'
                    co_this_mok_list = cost_budget_mok_list(budg_year, co_this_hang)
                    if row != 0:
                        self.this_year_budg_tableWidget.insertRow(row)

                    if len(co_this_mok_list) == 0:
                        self.this_year_budg_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        self.this_year_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                        if self.this_year_budg_tableWidget.item(row,3) is not None:
                            self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        row += 1
                        
                    else:
                        self.this_year_budg_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        self.this_year_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                        self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        row += 1
                        for j2 in range(len(co_this_mok_list)):  # j는 행 c는 열
                            co_this_mok = str(co_this_mok_list[j2][0])
                            if row != 0:
                                self.this_year_budg_tableWidget.insertRow(row)
                                
                            if co_this_mok in co_this_semok_mok_list:
                                co_this_semok_list = cost_budget_semok_list(budg_year,co_this_mok)
                                self.this_year_budg_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                self.this_year_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                if self.this_year_budg_tableWidget.item(row,3) is not None:
                                    self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                row += 1

                                for j3 in range(len(co_this_semok_list)):  # j는 행 c는 열
                                    co_this_semok = str(co_this_semok_list[j3][0])
                                    if row != 0:
                                        self.this_year_budg_tableWidget.insertRow(row)
                                        self.this_year_budg_tableWidget.setItem(row,2,QTableWidgetItem(co_this_semok))
                                        self.this_year_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                        if self.this_year_budg_tableWidget.item(row,3) is not None:
                                            self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                        row += 1
                            else: # if len(co_this_semok_list) == 0:
                                self.this_year_budg_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                self.this_year_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                if self.this_year_budg_tableWidget.item(row,3) is not None:
                                    self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                row += 1

                        if self.this_year_budg_tableWidget.item(row,3) is not None:
                            self.this_year_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            self.this_year_budg_tableWidget.resizeColumnsToContents()
            self.this_year_budg_tableWidget.setColumnHidden(6, True)
            
        except ValueError:
            QMessageBox.about(self,'ValueError',"예산작성 년도를 입력하세요. !!!")
        except TypeError:
            QMessageBox.about(self,'TypeError',"데이터가 없습니다.")

    def budget_save(self):
        from budget.budget_call_select import budget_cost_save
        budget_cost_imsi = []
        budg_year_st = self.budget_year_widget.text() #budg_year_st는 예산년도 시작(start)
        if budg_year_st == "" or budg_year_st is None :
            self.budget_year_widget.setFocus()
            return
        budg_year = int(budg_year_st)
        user = self.user_name.text()
        thisyear_Count = self.this_year_budg_tableWidget.rowCount()
    
        # try:
        for i in range(thisyear_Count):
            hang_name = self.this_year_budg_tableWidget.item(i, 0)
            mok_name = self.this_year_budg_tableWidget.item(i, 1)
            semok_name = self.this_year_budg_tableWidget.item(i, 2)
            cost_amount_text = self.this_year_budg_tableWidget.item(i, 3)
            if cost_amount_text:
                cost_amount_T  = self.this_year_budg_tableWidget.item(i, 3).text()
                cost_amount = int(cost_amount_T.replace(",",''))     # 이전 항의 합 값을 숫자로
            if  self.this_year_budg_tableWidget.item(i, 5):
                cost_marks = self.this_year_budg_tableWidget.item(i, 5).text()
                if cost_marks == '':
                    cost_marks = None
            else:
                cost_marks = None
            
            hang_count = 0; mok_count = 0; semok_count = 0

            if hang_name != None:  # 항 이름에 뭔가 있으면, 데이터가 있을 수 있다.(없을 수도 있다)
                if hang_name.text() != '합   계':
                    hang_count += 1
                    hang = self.this_year_budg_tableWidget.item(i, 0).text()
                    next_hang_name = self.this_year_budg_tableWidget.item(i + 1, 0)  # next_hang_name 이 None 이 아니면 목과 세목이 없다
                    #if next_hang_name != None:  # 다음 행에 항이 있으면,
                    if cost_amount_text != None and cost_amount_text != 0:    # 항의 값이 있다, 그러면...  
                        if next_hang_name != None:  # 다음 행에 항이 있으면,
                            mok = None
                            semok = None
                            # cost_amount_T  = self.this_year_budg_tableWidget.item(i, 3).text()
                            # cost_amount = int(cost_amount_T.replace(",",''))     # 이전 항의 합 값을 숫자로
                            if self.this_year_budg_tableWidget.item(i, 6):
                                id = self.this_year_budg_tableWidget.item(i, 6).text()
                                d_type = "modi"
                                budget_cost_imsi.append((cost_amount, cost_marks, user, id, d_type))
                            else:
                                if cost_amount != '0' and cost_amount != None:
                                    id = None
                                    d_type = "new"
                                    budget_cost_imsi.append((budg_year,hang,mok,semok,cost_amount,cost_marks,user, id, d_type))
            else:
                if mok_name != None:  # mok 이름이 있으면 데이터 확인 해라!
                    mok_count += 1
                    mok  = self.this_year_budg_tableWidget.item(i, 1).text()  # mok 이름
                    next_mok_name = self.this_year_budg_tableWidget.item(i + 1, 2)  #다음 ㅡㅐㅏ
                    next_semok_name = self.this_year_budg_tableWidget.item(i + 1, 2)  #다음 ㅡㅐㅏ
                    # if next_mok_name != None:  # 다음 행에 목이 있으면,
                    if cost_amount_text != None and cost_amount_text != 0:  # 0 이 아닌 금액이 있으면...
                        # if next_mok_name != None :  # 다음 행에도 목이 있으면,
                        if next_semok_name == None:  # 세목이 없으면..
                            semok = None
                            cost_amount_T  = self.this_year_budg_tableWidget.item(i, 3).text()
                            cost_amount = int(cost_amount_T.replace(",",''))   # 해당 목의 금액이 된다.
                            if self.this_year_budg_tableWidget.item(i, 6):
                                id = self.this_year_budg_tableWidget.item(i, 6).text()
                                d_type = "modi"
                                budget_cost_imsi.append((cost_amount, cost_marks, user, id, d_type))
                                budget_cost_save(budget_cost_imsi)
                                budget_cost_imsi = []    
                            else:
                                if cost_amount != 0 and cost_amount != None:
                                    id = None
                                    d_type = "new"
                                    budget_cost_imsi.append((budg_year,hang,mok,semok,cost_amount,cost_marks,user, id, d_type))
                                    budget_cost_save(budget_cost_imsi)
                                    budget_cost_imsi = []    
                            
                else:
                    if semok_name != None:
                        semok_count += 1
                        semok = self.this_year_budg_tableWidget.item(i, 2).text()
                        # next_semok_name = self.this_year_budg_tableWidget.item(i + 1, 2)
                        if cost_amount_text != None:
                            cost_amount_T  = self.this_year_budg_tableWidget.item(i, 3).text()
                            cost_amount = int(cost_amount_T.replace(",",''))
                            if self.this_year_budg_tableWidget.item(i, 6):
                                id = self.this_year_budg_tableWidget.item(i, 6).text()
                                d_type = "modi"
                                budget_cost_imsi.append((cost_amount, cost_marks, user, id, d_type))
                                budget_cost_save(budget_cost_imsi)
                                budget_cost_imsi = []    
                            else:
                                if cost_amount != 0 and cost_amount != None:
                                    id = None
                                    d_type = "new"
                                    budget_cost_imsi.append((budg_year,hang,mok,semok,cost_amount,cost_marks,user, id, d_type))
                                    budget_cost_save(budget_cost_imsi)
                                    budget_cost_imsi = []
   
        QMessageBox.about(self,'저장',"지출예산이 저장되었습니다.!!!")
        self.budget_year_widget.clear()
        self.last_bud_hap_widget.clear()
        self.this_bud_hap_widget.clear()
        self.last_year_tableWidget.clearContents()
        self.this_year_budg_tableWidget.clearContents()
        self.last_year_tableWidget.setRowCount(0)
        self.this_year_budg_tableWidget.setRowCount(0)
            
        budget_cost_imsi.clear()
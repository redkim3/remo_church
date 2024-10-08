from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtGui import QPainter, QRegion
from PyQt5.QtGui import QIcon, QFontMetrics
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt, QPoint, QRect
import pandas as pd
import os, subprocess, collections

today = QDate.currentDate()
saved_file = r'./excel_view/분기보고_지출_보고서.xlsx'
cur_fold = os.getcwd()

form_secondclass = uic.loadUiType("./ui/Quarter_report_cost.ui")[0]

class Ge_quarterly_cost_Report(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(Ge_quarterly_cost_Report,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("분기지출 재정보고")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        global bogo_bungi
        bogo_year = today.year()
        self.bogo_year_widget.setText(str(bogo_year))
        self.bogo_year_widget.setFocus()

    def button_click(self):
        self.Quarter_cost_view_Button.clicked.connect(self.Quarterly_cost_view)
        self.Quarterly_cost_excel_save_Button.clicked.connect(self.Quarterly_cost_excel_save)
        self.Quarterly_cost_close_Button.clicked.connect(self.Quarterly_cost_close)
    
    def column_headers_set(self,bogo_year):
        column_headers = ['항','목','세목','년간누계','집행율']
        column_headers.insert(3,str(bogo_year)+'년도 예산')
        self.cost_tableWidget.setHorizontalHeaderLabels(column_headers)
        return column_headers
    
    def Quarterly_cost_view(self):
        from budget.budget_call_select import budget_cost_call
        bogo_year_st = self.bogo_year_widget.text()
        if bogo_year_st.isdigit():
            bogo_year = int(bogo_year_st)
            if bogo_year < 1000 or bogo_year > today.year():
                QMessageBox.about(self, '입력오류', '보고년도에 숫자를 확인해 주세요.')
                self.bogo_year_widget.setFocus()
                return
        else:
            QMessageBox.about(self, '입력오류', '보고년도를 확인해 주세요.')
            self.bogo_year_widget.setFocus()
            return
        bogo_bungi_st = self.Quarter_widget.text()
        if bogo_bungi_st.isdigit():
            bogo_bungi = int(bogo_bungi_st)
            if bogo_bungi < 0 or bogo_bungi > 4:
                QMessageBox.about(self, '입력오류', '분기는 1 부터 4 까지 입니다.')
                self.Quarter_widget.setFocus()
                return
        else:
            QMessageBox.about(self, '입력오류', '보고분기를 확인해 주세요.')
            self.Quarter_widget.setFocus()
            return

        budget_cost = budget_cost_call(bogo_year)
        
        if len(budget_cost):
            self.budget_cost_hang_mok_call(bogo_year) # 항목 가져오기

            table_row_count = self.cost_tableWidget.rowCount()
            t_hang = None; t_mok = None; t_semok = None
            
            for row in range(table_row_count):
                t_hang_T = self.cost_tableWidget.item(row,0)

                t_mok_T = self.cost_tableWidget.item(row,1)
                t_semok_T = self.cost_tableWidget.item(row,2)
                if t_hang_T:
                    t_hang = t_hang_T.text()
                    t_mok = None
                    t_semok = None
                
                if t_mok_T:
                    t_mok = t_mok_T.text()
                    t_semok = None
                else:
                    t_mok = t_mok
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
                    if t_hang == bug_hang and t_mok == bug_mok and t_semok == bug_semok:
                        self.cost_tableWidget.setItem(row, 3,QTableWidgetItem(bug_amount))
                        if self.cost_tableWidget.item(row, 3) != None:
                            self.cost_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

            self.cost_tableWidget.resizeColumnsToContents()
            self.budg_calculate()
            self.select_delete_rowcount()
            self.bungi_real_data_call()
            self.calculate_totals()
            

    def select_delete_rowcount(self):
        # 삭제대상열 선택하고 삭제하기
        del_select_row = self.cost_tableWidget.rowCount()
        # 역순으로 삭제해야 인덱스 문제 방지
        for row in reversed(range(del_select_row)):
            item = self.cost_tableWidget.item(row, 3)
            if item is not None:
                row_value = item.text()
                if row_value == '0':
                    self.cost_tableWidget.removeRow(row)
    
    def budget_cost_hang_mok_call(self,bogo_year):
        from basic.cost_hangmok_select import cost_budget_hang_list, cost_budget_mok_list, cost_budget_semok_list

        try:
            self.cost_tableWidget.clearContents()
            self.cost_tableWidget.setRowCount(1)
            self.cost_tableWidget.setColumnCount(5)
            self.cost_tableWidget.setRowCount(1)
            # bogo_budget = cost_budget_call(bogo_year)  # 예산 금액리스트
            self.cost_tableWidget.insertColumn(3) # 여기서 3은 추가되어야 할 열의 직전 열의 번호 
            self.column_headers_set(bogo_year)          

            gubun = "일반회계"
            co_this_hang_list = cost_budget_hang_list(bogo_year,gubun)   # 계정 항 가져오기
            co_this_semok_tuple = cost_budget_semok_list(bogo_year,'all')
            if co_this_semok_tuple != None:
                co_this_semok_mok_list = [item[0] for item in co_this_semok_tuple]
                co_this_Count = len(co_this_hang_list)
                self.cost_tableWidget.setRowCount(1)
            else:
                co_this_Count = 0

            row = 0
            if co_this_Count > 1:
                for j in range(co_this_Count):  # j는 행 c는 열
                    co_this_hang = co_this_hang_list[j][0]
                    co_amp = '0'
                    co_this_mok_list = cost_budget_mok_list(bogo_year, co_this_hang)
                    if row != 0:
                        self.cost_tableWidget.insertRow(row)

                    if len(co_this_mok_list) == 0:   # mok 이 없는 항의 경우
                        self.cost_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        self.cost_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                        if self.cost_tableWidget.item(row,3) is not None:
                            self.cost_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        row += 1
                        
                    else:  # mok 이 있는 항의 경우
                        self.cost_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        row += 1
                        for j2 in range(len(co_this_mok_list)):  # j는 행 c는 열
                            co_this_mok = str(co_this_mok_list[j2][0])
                            if co_this_mok in co_this_semok_mok_list:  # mok에 semok 이 있는경우
                                self.cost_tableWidget.insertRow(row)
                                co_this_semok_list = cost_budget_semok_list(bogo_year,co_this_mok)
                                self.cost_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                row += 1

                                for j3 in range(len(co_this_semok_list)):  # j는 행 c는 열
                                    co_this_semok = str(co_this_semok_list[j3][0])
                                    self.cost_tableWidget.insertRow(row)
                                    self.cost_tableWidget.setItem(row,2,QTableWidgetItem(co_this_semok))
                                    self.cost_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                    if self.cost_tableWidget.item(row,3) is not None:
                                        self.cost_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    row += 1
                            else: # if len(co_this_semok_list) == 0: # mok에 semok 이 없는경우
                                self.cost_tableWidget.insertRow(row)
                                self.cost_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                self.cost_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                if self.cost_tableWidget.item(row,3) is not None:
                                    self.cost_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                row += 1

                        if self.cost_tableWidget.item(row,3) is not None:
                            self.cost_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        except TypeError:
            QMessageBox.about(self,'TypeError',"예산데이터가 없습니다.")
    
    def budg_calculate(self):
        
        budg_hap_total = 0
        budg_count = self.cost_tableWidget.rowCount()
        budg_hang_amo_int = 0; budg_mok_amo_int =0
        for a in range(budg_count):
            budg_hang_T1 = self.cost_tableWidget.item(a,0)  #a 는 0 부터
            budg_hang_T2 = self.cost_tableWidget.item(a+1,0)
            this_semok_T1 = self.cost_tableWidget.item(a,2)
            budg_semok_T2 = self.cost_tableWidget.item(a+1,2)
            budg_mok_T1 = self.cost_tableWidget.item(a,1)
            budg_mok_T2 = self.cost_tableWidget.item(a+1,1)
            if budg_hang_T1 != None and budg_hang_T2 != None : # 항이 현재항과 아래도 항의 있을때, 목이 없는 경우(현재는 이런 경우 없음)
                budg_amo_T = self.cost_tableWidget.item(a,3).text()
                budg_amo_int = int(budg_amo_T.replace(",",''))
                budg_amo_f = format(budg_amo_int,",")
                budg_hap_total += budg_amo_int
                self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))
                self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            elif budg_hang_T1 != None and budg_hang_T2 == None : # 현재의 항에는 있고 아래의 항에는 없을때 즉 목에 있다(?)그러므로 목이 있는 항의 시작
                hang_c_adj = 0 ; budg_hang_amo_int = 0  # 항의 차감 행의 수(hang_c_adj), 항의 합계(budg_hang_amo_int)를 초기화 한다.
            elif budg_hang_T1 == None and budg_hang_T2 == None :  # 여기는 항의 목이 이어지는 형태이다.
                if budg_mok_T1 != None and budg_mok_T2 != None:   # 현재와 아래의 목에 값이있다. 목의 갑을 받아 넣는다. 항에 값에 더한다.
                    hang_c_adj += 1
                    budg_amo_T = self.cost_tableWidget.item(a,3).text()
                    budg_amo_int = int(budg_amo_T.replace(",",''))
                    budg_amo_f = format(budg_amo_int,",")
                    budg_hang_amo_int += budg_amo_int
                    budg_hang_amo = format(budg_hang_amo_int,",")
                    budg_hap_total += budg_amo_int
                    self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))
                    self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                elif budg_mok_T1 != None and budg_mok_T2 == None: # 현재 목의 명칭은 있고 다음 목의 명칭은 없다.  세목이 있거나. 다음 항으로 간다.
                    if this_semok_T1 == None and budg_semok_T2 != None: # 아래부터 세목이 있는 경우
                        mok_c_adj = 0
                        hang_c_adj += 1
                    elif this_semok_T1 == None and budg_semok_T2 == None:
                        hang_c_adj += 1
                        budg_amo_T = self.cost_tableWidget.item(a,3).text()
                        budg_amo_int = int(budg_amo_T.replace(",",''))
                        budg_amo_f = format(budg_amo_int,",")
                        budg_hang_amo_int += budg_amo_int  # budg_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        budg_hang_amo = format(budg_hang_amo_int,",")
                        budg_hap_total += budg_amo_int
                        self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))  # 목의 값이다.
                        self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.cost_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(budg_hang_amo))  # 목의 값이다.
                        self.cost_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        hang_c_adj = 0; budg_hang_amo_int =0
                    
                elif budg_mok_T1 == None and budg_mok_T2 == None:  # 현재의 항에도 없고, 다음 항에도 없다
                    if this_semok_T1 != None and budg_semok_T2 != None: # 현재와 다음 행에 세목이 있다.
                        mok_c_adj += 1
                        hang_c_adj += 1
                        budg_amo_T = self.cost_tableWidget.item(a,3).text()
                        budg_amo_int = int(budg_amo_T.replace(",",''))
                        budg_amo_f = format(budg_amo_int,",")
                        budg_mok_amo_int += budg_amo_int
                        budg_hang_amo_int += budg_amo_int  # budg_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        # budg_hang_amo = format(budg_hang_amo_int,",")
                        budg_hap_total += budg_amo_int
                        self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))  # 목의 값이다.
                        self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                elif budg_mok_T1 == None and budg_mok_T2 != None :
                    if this_semok_T1 != None and budg_semok_T2 == None :
                        mok_c_adj += 1
                        hang_c_adj += 1
                        budg_amo_T = self.cost_tableWidget.item(a,3).text()
                        budg_amo_int = int(budg_amo_T.replace(",",''))
                        budg_amo_f = format(budg_amo_int,",")
                        budg_mok_amo_int += budg_amo_int
                        budg_mok_amo = format(budg_mok_amo_int,",")
                        budg_hang_amo_int += budg_amo_int
                        budg_hang_amo = format(budg_hang_amo_int,",")
                        budg_hap_total += budg_amo_int
                        self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))
                        self.cost_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(budg_mok_amo))
                        self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.cost_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                        budg_mok_amo_int = 0; mok_c_adj = 0
            
            elif budg_hang_T1 == None and budg_hang_T2 != None :
                if this_semok_T1 != None and budg_semok_T2 == None :
                    mok_c_adj += 1
                    hang_c_adj += 1
                    budg_amo_T = self.cost_tableWidget.item(a,3).text()
                    budg_amo_int = int(budg_amo_T.replace(",",''))
                    budg_amo_f = format(budg_amo_int,",")
                    budg_mok_amo_int += budg_amo_int
                    budg_mok_amo = format(budg_mok_amo_int,",")
                    budg_hang_amo_int += budg_amo_int
                    budg_hang_amo = format(budg_hang_amo_int,",")
                    budg_hap_total += budg_amo_int
                    self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))
                    self.cost_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(budg_mok_amo))
                    self.cost_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(budg_hang_amo))
                    self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    
                    mok_c_adj = 0; hang_c_adj = 0; budg_hang_amo_int =0; budg_mok_amo_int = 0
                if budg_mok_T1 != None and budg_mok_T2 == None :
                    hang_c_adj += 1
                    budg_amo_T = self.cost_tableWidget.item(a,3).text()
                    budg_amo_int = int(budg_amo_T.replace(",",''))
                    budg_amo_f = format(budg_amo_int,",")
                    budg_hang_amo_int += budg_amo_int
                    budg_hang_amo = format(budg_hang_amo_int,",")
                    budg_hap_total += budg_amo_int
                    self.cost_tableWidget.setItem(a,3,QTableWidgetItem(budg_amo_f))
                    self.cost_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(budg_hang_amo))  # 목으로만 분리된 항의 합계
                    self.cost_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                    hang_c_adj = 0; budg_hang_amo_int =0

        # budg_amo_f = format(budg_amo_int,",")
        budg_hap = format(budg_hap_total,",")
        self.cost_tableWidget.insertRow(a + 1)
        self.cost_tableWidget.setItem(a + 1, 0, QTableWidgetItem("합   계"))  # 행의 합계 표시
        if self.cost_tableWidget.item(a + 1, 0) != None:
            self.cost_tableWidget.item(a + 1, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        
        # self.cost_tableWidget.setItem(a + 1, 1, QTableWidgetItem(''))  # 행의 합계 표시
        # self.cost_tableWidget.setItem(a + 1, 2, QTableWidgetItem(''))  # 행의 합계 표시
        self.cost_tableWidget.setItem(a + 1, 3, QTableWidgetItem(budg_hap))  # 행의 합계 표시
        if self.cost_tableWidget.item(a + 1, 3) != None:
            self.cost_tableWidget.item(a + 1, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        
        self.cost_tableWidget.resizeColumnsToContents()


    def Quarterly_cost_view_before_modify(self):

        from budget.budget_cost_select import cost_budget_call
        try: 
            bogo_year = int(self.bogo_year_widget.text())
            if bogo_year < 1000 or bogo_year > today.year() :
                QMessageBox.about(self, '입력오류', '보고년도를 확인해 주세요.')
                self.bogo_year_widget.setFocus()
                return
            bogo_bungi = int(self.Quarter_widget.text())
            if bogo_bungi < 0 or bogo_bungi > 4:
                QMessageBox.about(self, '입력오류', '분기는 1 부터 4 까지 입니다.')
                return
                self.Quarter_widget.setFocus()
            self.cost_tableWidget.clearContents()
            self.cost_tableWidget.setColumnCount(5)
            self.cost_tableWidget.setRowCount(1)
            bogo_budget = cost_budget_call(bogo_year)  # 예산 금액리스트
            self.column_headers_set(bogo_year)          
            self.cost_tableWidget.insertColumn(3) # 여기서 3은 추가되어야 할 열의 직전 열의 번호 

            tree = collections.defaultdict(dict)

            # 결과 데이터를 트리로 변환합니다.
            for item in bogo_budget:
                hang, mok, semok, amount, marks, id = item
                if hang != "타회계이월":
                    if semok:
                        if mok == None:
                            if hang not in tree:
                                tree[hang] = {}
                            if mok not in tree[hang]:
                                tree[hang][mok] = {}
                            tree[hang][mok][semok] = amount #[mok][semok]
                        else:
                            if mok in tree[hang]:
                                tree[hang][mok][semok] = amount
                            else:
                                tree[hang][mok] = {semok: amount}
                    elif mok:
                        if mok in tree[hang]:
                            tree[hang][mok] = amount
                        else:
                            tree[hang][mok] = amount
                    else:
                        tree[hang] = amount

            # 결과를 예시 형태로 출력합니다.
            row_count = self.cost_tableWidget.rowCount()  # 현재 행의 수 가져오기  여기의 row_count는 1
            self.cost_tableWidget.insertRow(row_count)    # 새로운 행 추가하기 시작
            
            row = 0; cost_sum = 0; s = 0; m = 0; mok_sum = 0
            for hang, mok_data in tree.items(): # 예산의 각 항,목,세목 금액 구하기
                hang_sum = 0
                if row != 0:
                    self.cost_tableWidget.insertRow(row)  # 행 삽입
                self.cost_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입
                for mok, semok_data in mok_data.items():
                    if mok:
                        row += 1  # 행 인덱스 증가
                        self.cost_tableWidget.insertRow(row)  # 행 삽입
                        self.cost_tableWidget.setItem(row, 1, QTableWidgetItem(mok))  # 행의 첫 번째 열에 항목 삽입
                        # 행 인덱스 증가;
                        for semok, amount in semok_data.items():
                            if semok != '0': # 세목이 있는 세목의 금액
                                row += 1 
                                s += 1; m += 1
                                self.cost_tableWidget.insertRow(row)  # 행 삽입
                                amo_txt = format(amount,',')
                                self.cost_tableWidget.setItem(row, 2, QTableWidgetItem(semok))  # 행의 첫 번째 열에 항목 삽입
                                self.cost_tableWidget.setItem(row, 3, QTableWidgetItem(amo_txt))  # 행의 두 번째 열에 항목 삽입
                                if self.cost_tableWidget.item(row, 3) != None:
                                    self.cost_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                mok_sum += amount  # 목의 합계 갱신
                                hang_sum += amount
                                cost_sum += amount
                                amount = 0
                        
                        mok_sum += amount  # 예산 목의 합계 갱신
                        mok_sum_txt = format(mok_sum,',')
                        
                        self.cost_tableWidget.setItem(row - s, 3, QTableWidgetItem(mok_sum_txt))  # 목의 합계 표시
                        if self.cost_tableWidget.item(row - s, 3) != None:
                            self.cost_tableWidget.item(row - s, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        #hang_sum += mok_sum  # 행의 합계 갱신
                        
                        hang_sum += amount
                        cost_sum += amount
                        m += 1; s = 0; mok_sum = 0; amount = 0
                    else:  # 목이 없으면
                        #self.cost_tableWidget.insertRow(row)  # 행 삽입
                        self.cost_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입
                        # 행 인덱스 증가;
                        for semok, amount in semok_data.items():
                            if semok != '0':
                                s += 1; m += 1
                            
                        mok_sum += amount  # 목의 합계 갱신
                        mok_sum_txt = format(mok_sum,',')
                        self.cost_tableWidget.setItem(row - s, 3, QTableWidgetItem(mok_sum_txt))  # 목의 합계 표시
                        if self.cost_tableWidget.item(row - s, 3) != None:
                            self.cost_tableWidget.item(row - s, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        
                        hang_sum += amount
                        cost_sum += amount
                        m += 1; s = 0; mok_sum = 0; amount = 0
                hang_sum_txt = format(hang_sum,',')
                self.cost_tableWidget.setItem(row - m, 3, QTableWidgetItem(hang_sum_txt))  # 행의 합계 표시
                if self.cost_tableWidget.item(row - m, 3) != None:
                    self.cost_tableWidget.item(row - m, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                
                m = 0; s = 0; row += 1
                cost_sum_txt = format(cost_sum,',')
                self.cost_tableWidget.setItem(row, 0, QTableWidgetItem("합   계"))  # 행의 합계 표시
                self.cost_tableWidget.setItem(row, 3, QTableWidgetItem(cost_sum_txt))  # 행의 합계 표시
                if self.cost_tableWidget.item(row, 3) != None:
                    self.cost_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                # # 수정대상은 여기까지
        except ValueError:
            QMessageBox.about(self, '누락', '분기 입력이 누락되었거나 올바른 형식이 아닙니다. 분기는 1부터 4까지의 값을 입력하세요.')
            self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
            return
        except UnboundLocalError:
            QMessageBox.about(self, '누락', '분기 입력이 누락되었거나 올바른 형식이 아닙니다. 분기는 1부터 4까지의 값을 입력하세요.')
            self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
            return
        except TypeError: 
            self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
            return

        self.bungi_real_data_call()
        self.calculate_totals()

    def bungi_real_data_call(self):  # 실 데이터 값 구하기
        from basic.hun_report_split import bungi_Ge_D_cost # bungi_Ge_M_cost # 예산의 내용과 지출비용의 실적
        bogo_year = int(self.bogo_year_widget.text())
        bogo_bungi = int(self.Quarter_widget.text())
        column_headers = self.column_headers_set(bogo_year)

        self.cost_tableWidget.setHorizontalHeaderLabels(column_headers)
        # 분기별 실적 넣기  # 분기 변동에 따른 열 추가
        r_amount_sum = 0; r_accu = 0
        for b1 in range(1, bogo_bungi + 1):  
            column_headers.insert(3 + b1, str(b1)+'/4 분기')
            self.cost_tableWidget.insertColumn(3 + b1) # 여기서 3은 추가되어야 할 열의 직전 열의 번호 
        self.cost_tableWidget.setHorizontalHeaderLabels(column_headers)
        # cell_count = self.cost_cost_tableWidget.rowCount()
        for bun in range(1, bogo_bungi + 1):  # 분기별 추가
            realcost = bungi_Ge_D_cost(bogo_year, bun)
            if realcost == '없음':
                self.bogo_year_widget.setFocus()
                return
            cost_hap = 0
            for r_hang, r_mok, r_semok, r_amount in realcost:
                cost_hap += r_amount
                # bun_total += r_amount
                # 비교 기준 열을 통해 이미 있는지 확인
                existing_item_row = self.find_existing_item(r_hang, r_mok, r_semok)
                # 이미 있는 경우 해당 위치에 값 삽입
                if existing_item_row:
                    if r_hang != '타회계이월':
                        # cost_hap += r_amount
                        row = existing_item_row
                        r_amount = format(r_amount, ',')  # 포맷팅
                        self.cost_tableWidget.setItem(row, bun + 3, QTableWidgetItem(r_amount))
                        if self.cost_tableWidget.item(row, bun + 3) != None:
                            self.cost_tableWidget.item(row, bun + 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    
                else:
                    if r_amount != 0 or r_amount != None:
                        r_amount_sum += r_amount
                        rowcount = self.cost_tableWidget.rowCount()
                        r_amount_sum_T = format(r_amount_sum,',')

                        if r_accu > 0:
                            self.cost_tableWidget.setItem(rowcount - 1, 3 + bun, QTableWidgetItem(r_amount_sum_T))
                            if self.cost_tableWidget.item(rowcount - 1, 3 + bun) != None:
                                self.cost_tableWidget.item(rowcount - 1, 3 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        else:
                            r_accu += 1
                            self.cost_tableWidget.insertRow(rowcount)
                            self.cost_tableWidget.setItem(rowcount, 0, QTableWidgetItem('예산외지출'))
                            self.cost_tableWidget.item(rowcount, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                            # self.cost_tableWidget.setItem(rowcount + 1, 0, QTableWidgetItem('총 합 계'))
                            self.cost_tableWidget.setItem(rowcount, 3 + bun, QTableWidgetItem(r_amount_sum_T)) #예산외지출 금액
                            if self.cost_tableWidget.item(rowcount, 3 + bun) != None:
                                self.cost_tableWidget.item(rowcount, 3 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            
            r_amount_sum = 0; cost_hap = 0 #; net_cost_hap = 0

    def calculate_totals(self):
        se_row = 0; m_row = 0
        bogo_bungi = int(self.Quarter_widget.text())
        for bun in range(1, bogo_bungi + 1):  # 1분기부터 3분기까지
            for row in range(self.cost_tableWidget.rowCount()):
                hang_item = self.cost_tableWidget.item(row, 0)
                mok_item = self.cost_tableWidget.item(row, 1)
                if mok_item != None:  # mok_item 에 값이 있으면.. 즉 목 이름이 있으면..
                    mok = mok_item.text()
                    m_row += 1; se_row = 0; parent_text = ""
                else:
                    mok = None
                semok_item = self.cost_tableWidget.item(row, 2)
                if semok_item != None:  # semok_item 에 값이 있으면.. 즉 세목 이름이 있으면..
                    semok = semok_item.text()
                    se_row += 1
                else:
                    semok = None
                real_value_text = self.cost_tableWidget.item(row, bun + 3).text() if self.cost_tableWidget.item(row, bun + 3) != None else ''

                if semok:
                    parent_item = self.cost_tableWidget.item(row - se_row, bun + 3)   # 세목의 값 합
                    if isinstance(parent_item, QTableWidgetItem):  # parent_item이 QTableWidgetItem 객체인지 확인
                        parent_text = parent_item.text()
                    else:
                        parent_text = '0'
                    parent_value = int(self.remove_commas(parent_text)) if parent_item else 0
                    current_value = int(self.remove_commas(real_value_text)) if real_value_text else 0
                    new_parent_value = parent_value + current_value
                    parent_item = format(new_parent_value, ",")
                    self.cost_tableWidget.setItem(row - se_row,bun + 3, QTableWidgetItem(parent_item))
                    if self.cost_tableWidget.item(row - se_row,bun + 3) != None:
                        self.cost_tableWidget.item(row - se_row,bun + 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        # mok 합 구하기
        for bun in range(1, bogo_bungi + 1):  # 1분기부터 3분기까지
            hap_sum = 0; ex_budget = 0
            for h_row in range(self.cost_tableWidget.rowCount()):
                hang_item = self.cost_tableWidget.item(h_row, 0)
                # 항목이 있는지 여부를 확인하여 설정
                if hang_item != None:   # 항의 이름 있으면...
                    # hang = hang_item.text()
                    se_row = 0; parent_text = "" ; m_row = 0; m_parent_text = ""
                else:
                    mok_item = self.cost_tableWidget.item(h_row, 1)
                    m_row += 1
                    if mok_item != None:  # 목 이름이 있으면..
                        mok = mok_item.text()
                    else:
                        mok = None

                real_value_2_text = self.cost_tableWidget.item(h_row, bun + 3).text() if self.cost_tableWidget.item(h_row, bun + 3) != None else ''

                if mok:
                    m_parent_item = self.cost_tableWidget.item(h_row - m_row, bun + 3)
                    m_parent_item_hang = self.cost_tableWidget.item(h_row - m_row, 0)
                    if isinstance(m_parent_item_hang, QTableWidgetItem):  # parent_item이 QTableWidgetItem 객체인지 확인
                        m_parent_hang_text = m_parent_item_hang.text()
                    if isinstance(m_parent_item, QTableWidgetItem):  # parent_item이 QTableWidgetItem 객체인지 확인
                        m_parent_text = m_parent_item.text()
                    else:
                        m_parent_text = '0'
                    
                    if m_parent_hang_text != '합   계' and m_parent_hang_text != '예산외지출' and m_parent_hang_text != '총 합 계':
                        m_parent_value = int(self.remove_commas(m_parent_text)) if m_parent_item else 0
                        current_m_value = int(self.remove_commas(real_value_2_text)) if real_value_2_text else 0
                        hap_sum += current_m_value

                        new_m_parent_value = m_parent_value + current_m_value  # 항의 합계를 계산하고
                        m_parent_item_text = format(new_m_parent_value, ",")
                        m_parent_item = QTableWidgetItem(m_parent_item_text)  # 수정된 값을 QTableWidgetItem으로 설정 항의 합을 입력한다.
                        self.cost_tableWidget.setItem(h_row - m_row, bun + 3, m_parent_item)
                        
                        if m_parent_item != None:
                            m_parent_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    else:
                        if m_parent_hang_text == '합   계':
                            hap = hap_sum - ex_budget
                            hap_T = format(hap,",")
                            hap_item = QTableWidgetItem(hap_T)
                            self.cost_tableWidget.setItem(h_row, bun + 3, hap_item)
        hs_row = self.cost_tableWidget.rowCount()
        self.cost_tableWidget.insertRow(hs_row)
        for bun in range(1, bogo_bungi + 1):  # 1분기부터 3분기까지
            hs_row = self.cost_tableWidget.rowCount()
            sum_total = 0
            for row_h in range(hs_row):
                sum_value_text = self.cost_tableWidget.item(row_h, bun + 3).text() if self.cost_tableWidget.item(row_h, bun + 3) != None else ''
                sum_value = int(self.remove_commas(sum_value_text)) if sum_value_text else 0  # 예산외지출
                sum_Text = self.cost_tableWidget.item(row_h, 0)
                if sum_Text :
                    if sum_Text.text() == '합   계' or sum_Text.text() == '예산외지출' :
                        sum_total += sum_value
                        sum_total_text = format(sum_total,",")
                        self.cost_tableWidget.setItem(hs_row - 1, 0, QTableWidgetItem("총 합 계"))
                        self.cost_tableWidget.item(hs_row - 1, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                        self.cost_tableWidget.setItem(hs_row - 1, bun + 3, QTableWidgetItem(sum_total_text))
            sum_total = 0

        # 년간 누적금액 및 집행율 계산
        accu_sum_value = 0
        sum_cell_count = self.cost_tableWidget.rowCount()
        for a in range(sum_cell_count): # 좌측헌금목록 행의 갯수
            accu_sum_value = 0; accu_value = '0'
            for k in range(1,bogo_bungi+1):
                accu_value = self.cost_tableWidget.item(a,3+k)
                if accu_value != None:
                    accu_value_T = accu_value.text()
                    accu_sum_value += int(accu_value_T.replace(",",""))
                else:
                    accu_sum_value += 0

            accu_sum_T = format(accu_sum_value,",")
            self.cost_tableWidget.setItem(a,4+k,QTableWidgetItem(accu_sum_T))
            if self.cost_tableWidget.item(a,4+k) != None:
                self.cost_tableWidget.item(a,4+k).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.cost_tableWidget.resizeColumnsToContents()

            try:
                budg_T = self.cost_tableWidget.item(a,3).text()
                budg_value = int(budg_T.replace(",",""))
            except:
                continue
            
            if budg_value != 0 and accu_sum_value != 0:
                rate_fine = (accu_sum_value / budg_value) * 100
                rate_T = format(rate_fine,".2f")
                self.cost_tableWidget.setItem(a,5+k,QTableWidgetItem(rate_T))
                if self.cost_tableWidget.item(a,5+k) != None:
                    self.cost_tableWidget.item(a,5+k).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                accu_sum_value = 0; budg_value = 0
    
        # #     QMessageBox.about(self,'입력에러','"누락된 부분을 확인하세요!!')
    
    def remove_commas(self, text):
        return text.replace(',', '')
   
    def find_existing_item(self, r_hang, r_mok, r_semok):
        serch_hang = 'not'; serch_mok = 'not'; serch_semok = 'not'
        
        for row2 in range(self.cost_tableWidget.rowCount()):
            hang = self.cost_tableWidget.item(row2, 0)  # 예산의 항
            mok = self.cost_tableWidget.item(row2, 1)
            semok = self.cost_tableWidget.item(row2, 2)
            if  hang and hang.text() == r_hang :  # r_hang는 text 임
                serch_hang = 'ok'
            if  mok and mok.text() == r_mok :  # r_hang는 text 임
                serch_mok = 'ok'
            if  semok and semok.text() == r_semok :  # r_hang는 text 임
                serch_semok = 'ok'
        if serch_hang == 'ok' and serch_mok == 'ok' and serch_semok == 'ok':
            for row in range(self.cost_tableWidget.rowCount()):
                semok = self.cost_tableWidget.item(row, 2)
                if semok and semok.text() == r_semok:
                    return row
        elif serch_hang == 'ok' and serch_mok == 'ok' and serch_semok == 'not':
            for row in range(self.cost_tableWidget.rowCount()):
                mok = self.cost_tableWidget.item(row, 1)
                if mok and mok.text() == r_mok:
                    return row
        else:
            if serch_hang == 'ok' and serch_mok == 'not' and serch_semok == 'not':
                for row in range(self.cost_tableWidget.rowCount()):
                    if hang and hang.text() == r_hang:
                        hang = self.cost_tableWidget.item(row, 0)
                        return row
                    
        return None  # 일치하는 항목이 없는 경우 None 반환

    def cost_report_print_button(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.bogo_year_widget.text()
            year_text = self.year_label.text()
            quarter_int = self.Quarter_widget.text() # quarter_text는 title_text에 포함되어 있음
            title_text = self.title_label.text()
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)

            x_margin = 35; y_margin = 70
            current_x = x_margin
            current_y = y_margin

            # 페이지 크기 계산
            page_rect = printer.pageRect()
            available_width = page_rect.width() - (2 * x_margin) # 양 옆의 여백을 제외한 크기가 인쇄가능 넓이
            available_height = page_rect.height() - current_y - y_margin
            
            # year_int 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_int, available_width)
            painter.drawText(current_x, current_y, year_int)
            year_int_width = painter.fontMetrics().width(year_int) # 년도의 숫자의 크기(폭) 즉 숫자 이다.
            current_x += year_int_width + 10  # 숫자의 폭에 10을 더한 값을 current_x 에 넣어라(년도 몇 분기 라고 쓸때 간격유지를 위해)

            # year_text('년도') 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, year_text)
            year_width = painter.fontMetrics().width(year_text)
            current_x += year_width + 15

            # quarter_int 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, quarter_int)
            quarter_width = painter.fontMetrics().width(quarter_int)
            current_x += quarter_width + 15  #painter.fontMetrics().height() + 20  # 20은 제목과 테이블 간 간격

            # title_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, title_text)
            title_width = painter.fontMetrics().width(title_text)
            current_x += title_width + 20  # 다음에 들어갈 내용이 없으므로 사용되지 않음
            
            # 초기 좌표 설정
            x = x_margin
            y = current_y + 20
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 30  # 기본 행 높이
            painter.setFont(font2)
            # 각 열의 열별 넓이의 리스트 만들기
            col_widths = [self.cost_tableWidget.columnWidth(col) for col in range(self.cost_tableWidget.columnCount())]
            # # 아래의 코드를 한줄로 표시한 것이 다
            # col_widths = []
            # for col in range(self.cost_tableWidget.columnCount()):
            #     width = self.cost_tableWidget.columnWidth(col)
            #     col_widths.append(width)
            
             # 테이블 헤더 출력
            for col in range(self.cost_tableWidget.columnCount()):
                header_text = self.cost_tableWidget.horizontalHeaderItem(col).text()
                col_width = int(col_widths[col] * available_width / sum(col_widths))
                self.adjust_font_size(painter, header_text, col_width)
                painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, self.cost_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                x += col_width

            # x = x_margin
            y += row_height
            
            # 테이블 내용 출력
            for row in range(self.cost_tableWidget.rowCount()):
                if y + row_height > page_rect.bottom() - y_margin:
                    printer.newPage()
                    y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                x = x_margin

                for col in range(self.cost_tableWidget.columnCount()):
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    painter.drawRect(x, y, col_width, row_height)
                    # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    item = self.cost_tableWidget.item(row, col)
                    if item and item.text():
                        cell_text = item.text()
                        self.adjust_font_size(painter, cell_text, col_width)
                        if col <= 2 :
                            if cell_text == '합   계' or cell_text == '총 합 계' or cell_text == '예산외지출':
                                rect = QRect(x, y, col_width, row_height)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 여백 7 픽셀 들여쓰기
                                rect = QRect(x + 5, y, col_width, row_height)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                        else:
                            # 우측 여백 7 픽셀 
                            rect = QRect(x, y, col_width - 5, row_height)
                            align = Qt.AlignRight | Qt.AlignVCenter

                        painter.drawText(rect, align, cell_text)
                    x += col_width
                    
                y += row_height

            painter.end()

    def adjust_font_size(self,painter, text, max_width):
        """
        텍스트가 주어진 폭에 맞도록 폰트 크기를 조정합니다.
        """
        font = painter.font()
        font_metrics = QFontMetrics(font) # QFontMetrics는 특정 측정정보를 계산하는데 쓰이는Qt 클래스중 하나
        while font_metrics.boundingRect(text).width() > max_width: # boundingRect는 QFontMetrics 클래스에서 제공하는 메서드 사각형으로 텍스트가 화면에 렌더링될때 차지하는 공간을 나타냄
            font_size = font.pointSize()  # 현재의 폰트 크기를 가져옴
            if font_size <= 1:  # 최소 폰트 크기 제한
                break
            font.setPointSize(font_size - 1) # QFont 객체의 글꼴 크기를 한 포인트 줄이는 코드
            painter.setFont(font)
            font_metrics = QFontMetrics(font)

    def Quarterly_cost_excel_save(self):  # 홈버튼

        #bun_cost_imsi = []; row_append_data = []
        r1_count = self.cost_tableWidget.rowCount()
        c1_count = self.cost_tableWidget.columnCount()
        
        cost_columnHeaders = []

        for j1 in range(c1_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.cost_tableWidget.horizontalHeaderItem(j1)
            if dat1:
                cost_columnHeaders.append(
                    self.cost_tableWidget.horizontalHeaderItem(j1).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                cost_columnHeaders.append('Null')
        df1 = pd.DataFrame(columns = cost_columnHeaders)

        # create dataframe object recordset
        for row1 in range(r1_count): #self.tbl_result.rowCount()):
            for col1 in range(c1_count): #self.tbl_result.columnCount()):
                try:
                    df1.at[row1, cost_columnHeaders[col1]] = self.cost_tableWidget.item(row1, col1).text()
                except:
                    continue

        # 저장
        try :
            df1.to_excel(excel_writer=saved_file, index=False, #) # f"{filename}.xlsx", index=False)
                #writer1,
                sheet_name='cost_report',
                startcol = 1,
                startrow = 2,
    #                encoding = 'utf-8',
                na_rep = '',      # 결측값을 ''으로 채우기
                inf_rep = '',     # 무한값을 ''으로 채우기
            )

            subprocess.Popen(["start", "excel.exe", os.path.abspath(saved_file)], shell=True)
            QMessageBox.about(self,'저장',"'분기보고_지출_보고서.xlsx'파일에 저장되었습니다.!!!")

        except OSError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            QMessageBox.about(self,'파일열기 에러',"'분기보고_지출_보고서'파일이 열려 있습니다. 파일을 닫고 다시 진행해 주세요. !!!")
    

    def Quarterly_cost_close(self):
        self.Quarter_widget.clear()
        self.close()
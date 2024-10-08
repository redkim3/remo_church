import os, subprocess, collections, re
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt, QRect, QSize
from PyQt5.QtGui import QFont, QIcon, QFontMetrics
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget # ,QApplication,  QMainWindow, QVBoxLayout, QPushButton
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter
import pandas as pd

# from basic.hun_report_split import bungi_Gecost, bungi_hungum_3, past_balance, year_Ge_hungum
cur_fold = os.getcwd()
today = QDate.currentDate()
saved_file = r'./excel_view/일반회계_분기보고_수입및요약.xlsx'
form_secondclass = uic.loadUiType("./ui/Quarter_report_income.ui")[0]

class Ge_quarterly_income_Report(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(Ge_quarterly_income_Report,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("분기 수입 및 수지 요약")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.bogo_date_widget.setDate(today)
        bogo_year = today.year()
        self.bogo_year_widget.setText(str(bogo_year))
        self.bogo_year_widget.setFocus()
    
    def connectFunction(self):
        self.Quarter_view_Button.clicked.connect(self.Quarterly_view)
        self.Quarterly_excel_save_Button.clicked.connect(self.Quarterly_excel_save)
        self.Quarterly_income_close_Button.clicked.connect(self.Quarterly_income_close)
    
    def Quarterly_view(self):
        global bogo_bungi, bogo_year
        # from basic.hun_name_2 import hun_mok_values
       
        from budget.budget_call_select import income_budget
        
        # v_year = str(today.year())
        self.income_tableWidget.clearContents()
        self.income_tableWidget.setColumnCount(4)
        # hang_list =['예배','절기헌금','지정헌금','기타소득']
        column_headers = ['항','목','연간누계','달성율']
        self.income_tableWidget.setRowCount(1)
        bogo_bungi = 0
        try:
            bogo_year_T = self.bogo_year_widget.text()
            if bogo_year_T != '':
                bogo_year = int(bogo_year_T)
                if bogo_year < 1000 or bogo_year > 9999:
                    QMessageBox.about(self, '누락', '보고년도는 1000부터 9999 사이의 4자리 수를 입력하세요.')
                    self.bogo_year_widget.setFocus()  # 해당 위젯으로 포커스 이동

            bogo_bungi_T = self.Quarter_widget.text()
            if bogo_bungi_T != '':
                bogo_bungi = int(bogo_bungi_T)
                if bogo_bungi < 1 or bogo_bungi > 4:
                    QMessageBox.about(self, '누락', '보고 분기는 1부터 4까지의 값을 입력하세요.')
                    self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
                    return
            else:
                QMessageBox.about(self, '누락', '보고 분기는 1부터 4까지의 값을 입력하세요.')
                self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
                return

            budgetvalue = income_budget(bogo_year)
            tree = collections.defaultdict(dict)
            # 결과 데이터를 트리로 변환합니다.
            for item in budgetvalue:
                hang, mok, amount = item
                if mok:
                    if mok in tree[hang]:
                        tree[hang][mok] = amount
                    else:
                        tree[hang][mok] = amount
                else:
                    tree[hang] = amount

            row_count = self.income_tableWidget.rowCount()  # 현재 행의 수 가져오기
            self.income_tableWidget.insertRow(row_count)    # 새로운 행 추가
            row = 0; hun_sum = 0; s = 0
            column_headers.insert(2,str(bogo_year)+'년도 예산')
            self.income_tableWidget.insertColumn(2)
            
            for c in range(1,bogo_bungi+1):
                column_headers.insert(2+c,str(c)+'/4분기')
                self.income_tableWidget.insertColumn(2+c) # 여기서 2는 항,목 예산 의 기본열 번호(0,1,2)
                self.income_tableWidget.setHorizontalHeaderLabels(column_headers)
            # r_count = self.income_tableWidget.rowCount()  # 예산 만 적용된 테이블 행 갯수

            for hang, mok_data in tree.items():
                hang_sum = 0
                if row != 0:
                    self.income_tableWidget.insertRow(row)  # 행 삽입
                self.income_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입
                
                # 행 인덱스 증가;
                for mok, amount in mok_data.items():
                    row += 1 ;  s += 1
                    self.income_tableWidget.insertRow(row)  # 행 삽입
                    amo_txt = format(amount,',')
                    self.income_tableWidget.setItem(row, 1, QTableWidgetItem(mok))  # 행의 첫 번째 열에 항목 삽입
                    self.income_tableWidget.setItem(row, 2, QTableWidgetItem(amo_txt))  # 행의 두 번째 열에 항목 삽입
                    if self.income_tableWidget.item(row, 2) != None:
                        self.income_tableWidget.item(row, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    hang_sum += amount
                    hun_sum += amount
                    amount = 0

                hang_sum += amount
                hun_sum += amount
                hang_sum_txt = format(hang_sum,',')
                self.income_tableWidget.setItem(row - s, 2, QTableWidgetItem(hang_sum_txt))  # 행의 합계 표시
                if self.income_tableWidget.item(row - s, 2) != None:
                    self.income_tableWidget.item(row - s, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                s = 0; row += 1; amount = 0

            hun_sum_txt = format(hun_sum,',')
            self.income_tableWidget.setItem(row, 0, QTableWidgetItem("합   계"))  # 행의 합계 표시
            self.income_tableWidget.setItem(row, 2, QTableWidgetItem(hun_sum_txt))  # 행의 합계 표시
            if self.income_tableWidget.item(row, 2) != None:
                self.income_tableWidget.item(row, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            # 실적 데이터 가져오기
            self.real_data_call()
            # 부분합 구하기
            self.part_hap_calculate()
            #비율 및 누계
            self.ratio_calculate()
            self.yoyak_view()
        except ValueError:
            QMessageBox.about(self, '누락', '분기 입력이 누락되었거나 올바른 형식이 아닙니다. 분기는 1부터 4까지의 값을 입력하세요.')
            self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
        except UnboundLocalError:
            QMessageBox.about(self, '누락', '분기 입력이 누락되었거나 올바른 형식이 아닙니다. 분기는 1부터 4까지의 값을 입력하세요.')
            self.Quarter_widget.setFocus()  # 해당 위젯으로 포커스 이동
    def real_data_call(self):
        from basic.hun_report_split import year_Ge_hun_bun_amount  #, year_Ge_hun_bun_hang_amount
       # 실적 가져오기
        # r1_count = 0
        for bun in range(1, bogo_bungi+1):
            real_hun = year_Ge_hun_bun_amount(bogo_year, bun)
            o_amount_sum = 0; f_amount_sum = 0
            f_amount = "" ; o_amount = ""
            bun_total = 0
            
            for r_hang, r_mok, r_amount in real_hun:
                if r_mok != '타회계이월':
                    bun_total += r_amount
                # 비교 기준 열을 통해 이미 있는지 확인
                existing_item_row = self.find_existing_item(r_mok)
                # 이미 있는 경우 해당 위치에 값 삽입
                if existing_item_row:
                    row = existing_item_row
                    r_amount_T = format(r_amount, ',')  # 포맷팅
                    self.income_tableWidget.setItem(row, bun + 2, QTableWidgetItem(str(r_amount_T)))
                    if self.income_tableWidget.item(row, bun + 2) != None:
                        self.income_tableWidget.item(row, bun + 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                # 없는 경우 맨 밑에 새로운 행 추가
                else:
                    if r_hang == '지정헌금': 
                        column_data1 = self.get_column_data(self.income_tableWidget, 0)
                        r1_count = self.income_tableWidget.rowCount()
                        f_amount_sum += r_amount   # 지정헌금의 누적금액 계산
                        f_amount = format(f_amount_sum,',')
                        if '지정헌금' in column_data1:
                            for jj in range(r1_count + 1):
                                jijeong = self.income_tableWidget.item(jj, 0)
                                if jijeong is not None and jijeong.text() == '지정헌금' :  # r_hang는 text 임
                                    self.income_tableWidget.setItem(jj, 2 + bun, QTableWidgetItem(f_amount))
                                    if self.income_tableWidget.item(jj, 2 + bun) != None:
                                        self.income_tableWidget.item(jj, 2 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        else:
                            for jj in range(r1_count + 1):
                                item = self.income_tableWidget.item(jj, 0)
                                if item is not None and item.text() == '합   계':
                                    self.income_tableWidget.insertRow(jj + 1)
                                    self.income_tableWidget.setItem(jj + 1, 0, QTableWidgetItem('지정헌금'))
                                    self.income_tableWidget.setItem(jj + 1, 2 + bun, QTableWidgetItem(f_amount))
                                    if self.income_tableWidget.item(jj + 1, 2 + bun) != None:
                                        self.income_tableWidget.item(jj + 1, 2 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                    if r_hang == '기타소득':
                        column_data2 = self.get_column_data(self.income_tableWidget, 0)
                        r2_count = self.income_tableWidget.rowCount()
                        if '기타소득' in column_data2:
                            if r_mok != '타회계이월':
                                o_amount_sum += r_amount
                                o_amount = format(o_amount_sum,',')
                                for jj in range(r2_count + 1):
                                    other = self.income_tableWidget.item(jj, 0)
                                    if other and other.text() == '기타소득' :  # r_hang는 text 임
                                        self.income_tableWidget.setItem(jj, bun + 2, QTableWidgetItem(o_amount))
                                        if self.income_tableWidget.item(jj, bun + 2) != None:
                                            self.income_tableWidget.item(jj, bun + 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        else:
                            if r_mok != '타회계이월':
                                o_amount_sum += r_amount
                                o_amount = format(o_amount_sum,',')
                                for j2 in range(r2_count + 1):
                                    item1 = self.income_tableWidget.item(j2, 0)
                                    item2 = self.income_tableWidget.item(j2+1, 0)
                                    if item1 is not None and item1.text() == '합   계':
                                        if item2 is not None and item2.text() == '지정헌금':
                                            self.income_tableWidget.insertRow(j2 + 2)
                                            self.income_tableWidget.setItem(j2 + 2, 0, QTableWidgetItem('기타소득'))
                                            self.income_tableWidget.setItem(j2 + 2, 2 + bun, QTableWidgetItem(o_amount))
                                            if self.income_tableWidget.item(j2 + 2, 2 + bun) != None:
                                                self.income_tableWidget.item(j2 + 2, 2 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                            self.income_tableWidget.insertRow(j2 + 3)
                                            self.income_tableWidget.setItem(j2 + 3, 0, QTableWidgetItem('총 합 계'))
                                        else:
                                            self.income_tableWidget.insertRow(j2 + 1)
                                            self.income_tableWidget.setItem(j2 + 1, 0, QTableWidgetItem('기타소득'))
                                            self.income_tableWidget.setItem(j2 + 1, 2 + bun, QTableWidgetItem(o_amount))
                                            if self.income_tableWidget.item(j2 + 1, 2 + bun) != None:
                                                self.income_tableWidget.item(j2 + 1, 2 + bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                            self.income_tableWidget.insertRow(j2 + 2)
                                            self.income_tableWidget.setItem(j2 + 2, 0, QTableWidgetItem('총 합 계'))
            f_amount_sum = 0; o_amount_sum = 0
    
    def part_hap_calculate(self):
        # 합 구하기
        for bun in range(1, bogo_bungi+1):
            r3_count = self.income_tableWidget.rowCount()
            bun_hap = 0; bun_hun_hap = 0; hang_hap = 0; hang_row = 0
            for i in range(r3_count + 1):
                hang_T = self.income_tableWidget.item(i ,0)
                if hang_T and hang_T.text() != None:
                    if hang_T.text() != '기타소득' and hang_T.text() != '지정헌금' and hang_T.text() != '총 합 계':
                        if self.income_tableWidget.item(i + 1, 0) == None:
                            hang_row = i
                            hang_hap = 0
                else:
                    mok_T = self.income_tableWidget.item(i ,1)
                    if mok_T and mok_T.text() != None:
                        amount_0 = self.income_tableWidget.item(i, bun + 2)
                        if amount_0 and amount_0.text() != None:
                            amount_1 = amount_0.text()
                            r1_amount = int(amount_1.replace(',',''))
                            hang_hap += r1_amount  # 항의 합계
                            bun_hun_hap += r1_amount  # 분기 예산된 헌금합
                            bun_hap += r1_amount       # 분기 총합 

                            hang_hap_T = format(hang_hap,',')
                            self.income_tableWidget.setItem(hang_row, 2 + bun, QTableWidgetItem(hang_hap_T))
                            if self.income_tableWidget.item(hang_row, 2 + bun) != None:
                                self.income_tableWidget.item(hang_row, 2 + bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    
                if hang_T and hang_T.text() != None:
                    if hang_T.text() == '기타소득' or hang_T.text() == '지정헌금':
                        amount_10 = self.income_tableWidget.item(i, bun + 2)
                        if amount_10 and amount_10.text() != None:
                            amount_11 = amount_10.text()
                            r2_amount = int(amount_11.replace(',',''))
                            bun_hap += r2_amount

                if  hang_T and hang_T.text() != None:
                    if hang_T.text() == '합   계':
                        bun_hun_hap_T = format(bun_hun_hap,",")
                        self.income_tableWidget.setItem(i, bun + 2, QTableWidgetItem(bun_hun_hap_T))
                        if self.income_tableWidget.item(i, bun + 2) != None:
                            self.income_tableWidget.item(i, bun + 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                if  hang_T and hang_T.text() != None:
                    if hang_T.text() == '총 합 계':
                        bun_total_T = format(bun_hap,",")
                        self.income_tableWidget.setItem(i, bun + 2, QTableWidgetItem(bun_total_T))
                        if self.income_tableWidget.item(i, bun + 2) != None:
                            self.income_tableWidget.item(i, bun + 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

    def ratio_calculate(self):
        # 개별항목 연간 합계 및 달성율
        r2_count = self.income_tableWidget.rowCount()
        for a in range(r2_count): # 좌측헌금목록 행의 갯수
            accu_sum_value = 0; accu_value = '0'
            for bun in range(1, bogo_bungi + 1):
                accu_value = self.income_tableWidget.item(a,2+bun)
                if accu_value != None:
                    a_value = accu_value.text()
                    accu_sum_value += int(a_value.replace(",",""))

            accu_sum_T = format(accu_sum_value,",")
            self.income_tableWidget.setItem(a,3+bun,QTableWidgetItem(accu_sum_T))
            if self.income_tableWidget.item(a,3+bun) != None:
                self.income_tableWidget.item(a,3+bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.income_tableWidget.resizeColumnsToContents()

            try:
                budg_T = self.income_tableWidget.item(a,2).text()
                budg_value = int(budg_T.replace(",",""))
            except:
                continue
            
            if accu_sum_value != 0 and budg_value != 0 :
                rate_fine = (accu_sum_value / budg_value) * 100
                rate_T = format(rate_fine,".2f")
                self.income_tableWidget.setItem(a,4+bun,QTableWidgetItem(rate_T))
                self.income_tableWidget.item(a,4+bun).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                accu_sum_value = 0; budg_value = 0
        header_font = QFont()
        header_font.setBold(True)
        self.income_tableWidget.horizontalHeader().setFont(header_font)

    def get_column_data(self, table_widget, column_index):
        row_count = table_widget.rowCount()
        column_data = []
        
        for row in range(row_count):
            item = table_widget.item(row, column_index)
            if item is not None:
                column_data.append(item.text())
            else:
                column_data.append('')  # 셀이 비어 있는 경우 빈 문자열 추가
        
        return column_data

    def find_existing_item(self, r_mok):
        serch_mok = 'not' # serch_hang = 'not'; 
        table_count = self.income_tableWidget.rowCount()
        for row2 in range(table_count):
            mok = self.income_tableWidget.item(row2, 1)
            if  mok and mok.text() == r_mok :  # r_hang는 text 임
                serch_mok = 'ok'
        
        if serch_mok == 'ok':
            for row in range(table_count):
                mok = self.income_tableWidget.item(row, 1)
                if mok and mok.text() == r_mok:
                    return row
        return None  # 일치하는 항목이 없는 경우 None 반환

    def yoyak_view(self):
        from basic.hun_report_split import past_hun, past_cost, year_cost_amount, year_Ge_hun_amount
        from basic.hun_report_split import year_othercost_amount, year_Ge_otherhun_amount   # 타회계이월 가져오기
        from budget.budget_call_select import income_budget_sum, cost_budget_sum
        self.balance_tableWidget.clearContents()
        self.balance_tableWidget.setRowCount(5)
        self.balance_tableWidget.setColumnCount(3)
        self.balance_tableWidget.clearContents()
        # column_headers = ['연간누계','집행율']
        column_headers = ['항  목','연간누계','집행율']
        bogo_year = int(self.bogo_year_widget.text())
        bogo_bungi = self.Quarter_widget.text()
        if bogo_bungi != '':
            bogo_Quarter = int(bogo_bungi)
            budgetincomesum =income_budget_sum(bogo_year)
            budgetcostsum = cost_budget_sum(bogo_year)
            # column_headers.insert(0,str(bogo_year)+'년도 예산')
            column_headers.insert(1,str(bogo_year)+'년도 예산')
            self.balance_tableWidget.insertColumn(1) # 여기서 3은 추가되어야 할 열의 직전 열의 번호 
            self.balance_tableWidget.setHorizontalHeaderLabels(column_headers)

            # 열 header 설정
            for c in range(1,bogo_Quarter+1):  #삽입 되는 열의 번호가 C 이다  '항목(0),연간누계(1)' 다음에 년도예산(1), 분기(2) 삽입
                column_headers.insert(c + 1,str(c)+'/4분기')
                self.balance_tableWidget.insertColumn(c + 1) # 여기서 3은 추가되어야 할 열의 직전 열의 번호 
                self.balance_tableWidget.setHorizontalHeaderLabels(column_headers)
        else:
            QMessageBox.about(self,"분기","검색할 분기를 입력해 주세요!!")
            self.Quarter_widget.setFocus()
            return

        # 수입예산 가져오기
        row_headers = []
        first_balance = 0
        incomebudgetsum = int(budgetincomesum[0][0])  # [(Decimal('2855000000'),)] 이러한 데이터를 정수형으로 바꾸는 것임
        income_budg_T = format(incomebudgetsum,",")
        self.balance_tableWidget.setItem(0,0,QTableWidgetItem('수입항목총계'))
        row_headers.insert(0, "수입항목총계") # 2+a1,
        if self.balance_tableWidget.item(0,0) is not None:
            self.balance_tableWidget.item(0,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.balance_tableWidget.setItem(0,1,QTableWidgetItem(income_budg_T))
        self.balance_tableWidget.item(0,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        #지출예산 가져오기
        costbudgetsum = int(budgetcostsum[0][0])
        cost_budg_T = format(costbudgetsum,",")
        self.balance_tableWidget.setItem(1,0,QTableWidgetItem('지출항목총계'))
        row_headers.insert(1, "지출항목총계") # 2+a1,
        if self.balance_tableWidget.item(1,0) is not None:
            self.balance_tableWidget.item(1,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.balance_tableWidget.setItem(1,1,QTableWidgetItem(cost_budg_T))
        self.balance_tableWidget.item(1,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    
        # 기초전기이월금액 가져오기
        pastHun = int(past_hun(bogo_year)[0][0])
        pastCost = int(past_cost(bogo_year)[0][0])
      
        first_balance = incomebudgetsum - costbudgetsum
        first_balance_T = format(first_balance,",")
        self.balance_tableWidget.setItem(2,0,QTableWidgetItem('차  액'))  # 차액
        row_headers.insert(2, "차  액") # 2+a1,
        if self.balance_tableWidget.item(2,0) is not None:
            self.balance_tableWidget.item(2,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.balance_tableWidget.setItem(2,1,QTableWidgetItem(first_balance_T))  # 차액
        self.balance_tableWidget.item(2,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        
        start_balance = pastHun - pastCost  # 보고 이전년도의 수입과 지출차액 (전기이월)
        carrid_over = format(start_balance,",")    # 전기이월 표시
        self.balance_tableWidget.setItem(3,0,QTableWidgetItem('전기이월금액'))
        row_headers.insert(3, "전기이월금액") # 2+a1,
        if self.balance_tableWidget.item(3,0) is not None:
            self.balance_tableWidget.item(3,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.balance_tableWidget.setItem(3,1,QTableWidgetItem(carrid_over))
        self.balance_tableWidget.item(3,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        # 예산상의 차기이월금액 구하기
        budg_next_balance_int = incomebudgetsum - costbudgetsum + start_balance
        budg_next_balance = format(budg_next_balance_int,",")
        self.balance_tableWidget.setItem(4,0,QTableWidgetItem('차기이월금액'))
        row_headers.insert(4, "차기이월금액") # 2+a1,
        if self.balance_tableWidget.item(4,0) is not None:
            self.balance_tableWidget.item(4,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.balance_tableWidget.setItem(4,1,QTableWidgetItem(budg_next_balance))
        if self.balance_tableWidget.item(4,1) is not None:
            self.balance_tableWidget.item(4,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        #실적부분 정리
        a1 = 0; a2 = 0 # ; a3 = 0; a4 = 0
        for bun in range(1,bogo_Quarter+1):   # 분기 헌금실적 가져오기
            hun = year_Ge_hun_amount(bogo_year,bun)
            cost = year_cost_amount(bogo_year,bun)
            next_balance = 0; second_balance = 0
            if hun[0][0] != None:
                hun_amo = int(hun[0][0])
                hun_T = format(hun_amo, ",")
                self.balance_tableWidget.setItem(0, bun + 1, QTableWidgetItem(hun_T))
                if self.balance_tableWidget.item(0, bun + 1) != None:
                    self.balance_tableWidget.item(0, bun + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                cost_amo = int(cost[0][0])
                cost_T = format(cost_amo, ",")
                self.balance_tableWidget.setItem(1, bun + 1, QTableWidgetItem(cost_T))
                if self.balance_tableWidget.item(1, bun + 1) != None:
                    self.balance_tableWidget.item(1, bun + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                
                # 실적 차액 구하기
                second_balance = hun_amo - cost_amo
                next_balance += second_balance  # 당기 수입과 지출차액
                second_balance_T = format(second_balance,",")
                self.balance_tableWidget.setItem(2,bun + 1,QTableWidgetItem(second_balance_T))
                self.balance_tableWidget.item(2,bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            
                # 타회계이월부분 행 부분 삽입후 쓰기
                in_ohter = year_Ge_otherhun_amount(bogo_year,bun) #타회계이월 유입
                out_other = year_othercost_amount(bogo_year,bun)   #타회계이월 유출
                if in_ohter[0][0] != None:
                    otherhun_amo = int(in_ohter[0][0])
                    if otherhun_amo != 0:
                        otherhun_T = format(otherhun_amo, ",")
                        next_balance += otherhun_amo
                        if '타회계에서 이월' not in row_headers:
                            a1 = 1
                            self.balance_tableWidget.insertRow(2+a1)
                            row_headers.insert(2+a1,"타회계에서 이월")
                            # self.balance_tableWidget.setVerticalHeaderLabels(row_headers)
                            self.balance_tableWidget.setItem(2 + a1, 0,QTableWidgetItem('타회계에서 이월'))
                            if self.balance_tableWidget.item(2 + a1, 0) is not None:
                                self.balance_tableWidget.item(2 + a1, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
                            self.balance_tableWidget.setItem(2 + a1, bun + 1,QTableWidgetItem(otherhun_T))
                            if self.balance_tableWidget.item(2 + a1, bun + 1) is not None:
                                self.balance_tableWidget.item(2 + a1, bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        else:
                            a1 = 1
                            self.balance_tableWidget.setItem(2 + a1, bun + 1,QTableWidgetItem(otherhun_T))
                            self.balance_tableWidget.item(2 + a1, bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    
                #특별회계로
                if out_other[0][0] != None:
                    othercost_amo = int(out_other[0][0])
                    if othercost_amo != 0:
                        othercost_T = format(othercost_amo, ",")
                        next_balance -= othercost_amo
                        if '타회계로 이월' not in row_headers:
                            a2 = 1
                            self.balance_tableWidget.insertRow(2+a1+a2)
                            row_headers.insert(2+a1+a2,"타회계로 이월")
                            self.balance_tableWidget.setItem(2 + a1 + a2, 0,QTableWidgetItem('타회계로 이월'))
                            if self.balance_tableWidget.item(2 + a1 + a2, 0) is not None:
                                self.balance_tableWidget.item(2 + a1 + a2, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
                            # self.balance_tableWidget.setVerticalHeaderLabels(row_headers)
                            
                            self.balance_tableWidget.setItem(2 + a1 + a2, bun + 1,QTableWidgetItem(othercost_T))
                            if self.balance_tableWidget.item(2 + a1 + a2, bun + 1) is not None:
                                self.balance_tableWidget.item(2 + a1 + a2, bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        else:
                            a2 = 1
                            self.balance_tableWidget.setItem(2 + a1 + a2, bun + 1,QTableWidgetItem(othercost_T))
                            if self.balance_tableWidget.item(2 + a1 + a2, bun + 1) is not None:
                                self.balance_tableWidget.item(2 + a1 + a2 , bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                # 전기이월, 차기이월
                if bun == 1:
                    pre_balance_amount = start_balance
                    next_balance_amount = pre_balance_amount + next_balance
                else:  # 각 분기별 전기이월 과 차분기 이월
                    # cha_bungi = self.balance_tableWidget.item(2+a1+a2+2,bun-1).text()
                    cha_bungi = self.balance_tableWidget.item(2+a1+a2+2,bun).text()
                    pre_balance_amount_s = self.balance_tableWidget.item(2+a1+a2+2, bun).text()
                    pre_balance_amount_int = int(pre_balance_amount_s.replace(",",""))
                    pre_balance_amount = pre_balance_amount_int
                    next_balance_amount = pre_balance_amount_int + next_balance

                pre_balance_amount_T = format(pre_balance_amount,",")
                self.balance_tableWidget.setItem(2+a1+a2+1, bun + 1,QTableWidgetItem(pre_balance_amount_T))
                self.balance_tableWidget.item(2+a1+a2+1, bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                
                next_balance_amount_T = format(next_balance_amount,",")
                self.balance_tableWidget.setItem(2+a1+a2+2, bun + 1,QTableWidgetItem(next_balance_amount_T))
                self.balance_tableWidget.item(2+a1+a2+2, bun + 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                # 차기이월
                next_balance_amount = pre_balance_amount + next_balance
                
                if bun == int(bogo_bungi):  # 마지막에 차기이월, 전기이월 넣기
                    # 년간 누적에서의 전기기월
                    accu_balance_pre = start_balance
                    accu_balance_pre_T = format(accu_balance_pre,",")
                    self.balance_tableWidget.setItem(2+a1+a2+1, bun + 2,QTableWidgetItem(accu_balance_pre_T))
                    self.balance_tableWidget.item(2+a1+a2+1, bun + 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        #년간 누적에서의 차기이월
                    self.balance_tableWidget.setItem(2+a1+a2+2, bun + 2,QTableWidgetItem(next_balance_amount_T))
                    self.balance_tableWidget.item(2+a1+a2+2, bun + 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        row_count = self.balance_tableWidget.rowCount()

        for a in range(row_count - 2):  # 하단에 전기이월과 차기이월이 있으므로 누적을 계산하는데는 제외함
            accu_sum_value_2 = 0; accu_value_2 = 0
            for bun in range(1,int(bogo_bungi)+1):
                try:
                    accu_value_2 = self.balance_tableWidget.item(a, bun + 1).text()
                    accu_sum_value_2 += int(accu_value_2.replace(",",""))
                except:
                    continue
                accu_sum_T = format(accu_sum_value_2,",")
            self.balance_tableWidget.setItem(a, bun + 2, QTableWidgetItem(accu_sum_T))
            if self.balance_tableWidget.item(a, bun + 2) is not None:
                self.balance_tableWidget.item(a, bun + 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.balance_tableWidget.resizeColumnsToContents()

            if self.balance_tableWidget.item(a, 1) != None:  # 집행율 산정을 위한 분모의 숫자 ( 년간 예산액)
                budg_T2 = self.balance_tableWidget.item(a, 1).text()

                budg_value_2 = int(budg_T2.replace(",",""))
            
            if a < 2 :
                rate_fine_2 = (accu_sum_value_2 / budg_value_2) * 100
                rate_T2 = format(rate_fine_2,".2f")
                self.balance_tableWidget.setItem(a, bun + 3, QTableWidgetItem(rate_T2))
                if self.balance_tableWidget.item(a, bun + 3) is not None:
                    self.balance_tableWidget.item(a, bun + 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                accu_sum_value_2 = 0; budg_value_2 = 0
        header_font = QFont()
        header_font.setBold(True)
        self.balance_tableWidget.horizontalHeader().setFont(header_font)

    def print_button_clicked(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

            # 각 라벨의 텍스트와 폰트 설정
            year_int = self.bogo_year_widget.text()
            year_text = self.year_label.text()
            quarter_text = self.Quarter_widget.text()
            title_text = self.title_label.text()
            yoyak = self.balance_label.text()
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)

            x_margin = 50; y_margin = 100
            current_x = x_margin
            current_y = y_margin

            # 페이지 크기 계산
            page_rect = printer.pageRect()
            available_width = page_rect.width() - 2 * x_margin
            available_height = page_rect.height() - current_y - y_margin

            # year_int 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_int, available_width)
            painter.drawText(current_x, current_y, year_int)
            year_int_width = painter.fontMetrics().width(year_int)
            current_x += year_int_width + 10

            # year_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width - current_x)
            painter.drawText(current_x, current_y, year_text)
            year_width = painter.fontMetrics().width(year_text)
            current_x += year_width + 10

            # quarter_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, quarter_text, available_width - current_x)
            painter.drawText(current_x, current_y, quarter_text)
            quarter_width = painter.fontMetrics().width(quarter_text)
            current_x += quarter_width + 20

            # title_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, title_text, available_width - current_x)
            painter.drawText(current_x, current_y, title_text)
            title_width = painter.fontMetrics().width(title_text)
            current_x += title_width + 20

            # 초기 좌표 설정(수입)
            x = x_margin
            y = current_y + 25

            # 각 행과 열의 높이와 너비 계산
            row_height = 35  # 기본 행 높이 40 에서 5를 줄였음
            painter.setFont(font2)
            col_widths = [self.income_tableWidget.columnWidth(col) for col in range(self.income_tableWidget.columnCount())]

            # 테이블 헤더 출력 (비율 조정된 열 너비 사용)
            painter.setFont(font2)
            for col in range(self.income_tableWidget.columnCount()):
                header_text = self.income_tableWidget.horizontalHeaderItem(col).text()
                col_width = int(col_widths[col] * available_width / sum(col_widths))
                self.adjust_font_size(painter, header_text, col_width)
                painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, header_text)
                painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                x += col_width

            y += row_height

            # 테이블 내용 출력
            for row in range(self.income_tableWidget.rowCount()):
                if y + row_height > available_height + y_margin:
                    printer.newPage()
                    y = y_margin + 50

                x = x_margin
                for col in range(self.income_tableWidget.columnCount()):
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                    item = self.income_tableWidget.item(row, col)
                    if item and item.text():
                        cell_text = item.text()
                        self.adjust_font_size(painter, cell_text, col_width)
                        if col == 0 or col == 1:
                            if cell_text == '합   계' or cell_text == '총 합 계':
                                rect = QRect(x, y, col_width, row_height)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 여백 7 픽셀 들여쓰기
                                rect = QRect(x + 7, y, col_width - 7, row_height)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                        else:
                            # 우측 여백 7 픽셀 
                            rect = QRect(x, y, col_width - 7, row_height)
                            if col == -1:
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                align = Qt.AlignRight | Qt.AlignVCenter

                        painter.drawText(rect, align, cell_text)
                        
                        # align = Qt.AlignLeft if col == 0 or col == 1 else (Qt.AlignCenter if col == -1 else Qt.AlignRight)
                        # painter.drawText(QRect(x, y, col_width - 7, row_height), align | Qt.AlignVCenter, cell_text)
                        
                    x += col_width

                y += row_height



            # 초기 좌표 설정(요약)
            # balance_tableWidget 헤더 그리기
            row_height = 40  # 기본 행 높이
            painter.setFont(font2)
            header_height_2 = self.balance_tableWidget.horizontalHeader().height()
            
            y2 = y + 100  # mission_tableWidget 아래에 위치
            x2 = x_margin  # 시작 x 좌표

            bal_widths = [self.balance_tableWidget.columnWidth(col2) for col2 in range(self.balance_tableWidget.columnCount())]

            # 테이블 헤더 출력 (비율 조정된 열 너비 사용)
            for col2 in range(self.balance_tableWidget.columnCount()):
                header_item2 = self.balance_tableWidget.horizontalHeaderItem(col2)  # .text()수평 헤더 가져옴
                bal_width = int(bal_widths[col2] * available_width / sum(bal_widths))
                # col_width2 = self.balance_tableWidget.columnWidth(col2)  # 각 열의 너비를 가져옴
                
                if header_item2:
                    text_rect2 = QRect(x2, y2, bal_width, header_height_2)
                    painter.drawText(text_rect2, Qt.AlignCenter | Qt.AlignVCenter, header_item2.text())
                    painter.drawRect(x2, y2, bal_width, header_height_2)
                x2 += bal_width

            # v_x3 += bal_widths[0]
            y2 += header_height_2  # 헤더 아래부터 데이터 시작
            
            # balance 테이블 내용 출력
            for row3 in range(self.balance_tableWidget.rowCount()):  # 데이터 행 그리기
                x2 = x_margin                
                row_height_2 = self.balance_tableWidget.rowHeight(row3)  # 데이터 행의 높이를 가져옴
                for col3 in range(self.balance_tableWidget.columnCount()):  # 데이터 열 그리기
                    bal_width = int(bal_widths[col3] * available_width / sum(bal_widths))
                    painter.drawRect(x2, y2, bal_width, row_height_2)
                    item3 = self.balance_tableWidget.item(row3, col3)
                    if item3 and item3.text():
                        cell2_text = item3.text()
                        self.adjust_font_size(painter, cell2_text, bal_width)
                        align_2 = Qt.AlignCenter if col3 == 0 else Qt.AlignRight
                        painter.drawText(QRect(x2, y2, bal_width - 7, row_height_2), align_2 | Qt.AlignVCenter, item3.text())

                    x2 += bal_width
                
                y2 += row_height_2

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

    def Quarterly_excel_save(self):  # 홈버튼 

        r1_count = self.income_tableWidget.rowCount()
        c1_count = self.income_tableWidget.columnCount()
        r2_count = self.balance_tableWidget.rowCount()
        c2_count = self.balance_tableWidget.columnCount()
        
        income_columnHeaders = []
        balance_columnHeaders = []
        
        # 수입부분
        # create column header list
        # 열 헤더 가져오기
        income_columnHeaders = []

        for j1 in range(c1_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.income_tableWidget.horizontalHeaderItem(j1)
            if dat1:
                income_columnHeaders.append(
                    self.income_tableWidget.horizontalHeaderItem(j1).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                income_columnHeaders.append('Null')

        # 데이터프레임 생성
        df1 = pd.DataFrame(columns = income_columnHeaders)
        # 수입내역 테이블 데이터로 데이터프레임 채우기
        for row1 in range(r1_count): #self.tbl_result.rowCount()):
            for col1 in range(c1_count): #self.tbl_result.columnCount()):
                try:
                    df1.at[row1, income_columnHeaders[col1]] = self.income_tableWidget.item(row1, col1).text()
                except:
                    continue

        # 요약부분
        # 열 헤더 가져오기
        balance_columnHeaders = []

        for j2 in range(c2_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.balance_tableWidget.horizontalHeaderItem(j2)
            if dat1:
                balance_columnHeaders.append(
                    self.balance_tableWidget.horizontalHeaderItem(j2).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                balance_columnHeaders.append('Null')

        # 데이터프레임 생성
        df2 = pd.DataFrame(columns = balance_columnHeaders)
        # 수입내역 테이블 데이터로 데이터프레임 채우기
        for row2 in range(r2_count): #self.tbl_result.rowCount()):
            for col2 in range(c2_count): #self.tbl_result.columnCount()):
                try:
                    df2.at[row2, balance_columnHeaders[col2]] = self.balance_tableWidget.item(row2, col2).text()
                except:
                    continue

        try :
            with pd.ExcelWriter(saved_file, engine='openpyxl') as writer:
            # 첫 번째 데이터프레임 출력
                df1.to_excel(writer, sheet_name='quarter_income_combined', index=False, startcol=0, startrow=0, na_rep='', inf_rep='')
            
            # 두 번째 데이터프레임 출력 (시작 위치를 6행 더 아래로 이동)
                df2.to_excel(writer, sheet_name='quarter_income_combined', index=True, startcol=0, startrow=len(df1) + 6, na_rep='', inf_rep='') #, header=True)

            subprocess.Popen(["start", "excel.exe", os.path.abspath(saved_file)], shell=True)
            QMessageBox.about(self,'저장',"'일반회계_분기보고_수입및요약.xlsx'파일에 저장되었습니다.!!!")
        except OSError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            QMessageBox.about(self,'파일열기 에러',"'일반회계_분기보고_수입및요약'파일이 열려 있습니다. 파일을 닫고 다시 진행해 주세요. !!!")

    def Quarterly_income_close(self):
        self.Quarter_widget.clear()
        self.close()
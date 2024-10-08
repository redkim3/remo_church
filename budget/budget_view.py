import collections, os
from PyQt5.QtCore import  Qt, QRect # 또는 * 으로 날짜를 불러온다 QDate,
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPainter, QFontMetrics
from PyQt5.QtPrintSupport import QPrintDialog
# from basic.cost_hangmok_select import cost_hang_list, cost_mok_list, cost_semok_list
cur_fold = os.getcwd()
budg_year = None
form_class = uic.loadUiType("./ui/budget_view_form.ui")[0]

class Budget_View(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.row = -1
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.setWindowTitle("수입 지출예산 보기")
        self.budget_year_widget.text()
        budget_view_Button = QPushButton("예산보기")
        budget_view_Button.clicked.connect(self.budget_view)
        budget_view_Button.clicked.connect(self.budget_view_2)

        budget_view_close_Button = QPushButton("종료하기")
        budget_view_close_Button.clicked.connect(self.budget_view_close)
    
    def budget_view(self):
        from budget.budget_call_select import income_budget
        from basic.hun_name_2 import mok_list, hun_hang_values, gubun_values
        budg_year_T = self.budget_year_widget.text()
        if budg_year_T:
            try:
                gubun =gubun_values()
                budg_year = int(budg_year_T)
                hun_list = hun_hang_values(budg_year,gubun[1])
                self.income_budg_hap_widget.clear()
                self.income_budg_tableWidget.clearContents()
                order_amo_hap = 0; order_sum = ""
                
                budget_income = income_budget(budg_year)
                ord_budg_cnt = len(budget_income)

                hun_count = len(hun_list)
                rCount = len(budget_income) + 2
                self.income_budg_tableWidget.setRowCount(rCount)
                row_cnt = 0; hun_amo_hap = 0; hun_sum = ""
                if rCount > 1:
                    for i in range(hun_count):
                        hun_hang = str(hun_list[i][0])  # 항이름
                        or_hun_mok = mok_list(budg_year, hun_hang)  # 헌금 구분에 포함되는 목의 명칭 가져오기 s 
                        or_hun_cnt = len(or_hun_mok) # 헌금 목의 헌금명칭 갯수
                        self.income_budg_tableWidget.setItem(row_cnt,0,QTableWidgetItem(hun_hang))
                        row_cnt += 1
                        for j in range(or_hun_cnt):  # 헌금명칭 개수 만큼 나열하고
                            hun_mok_name = or_hun_mok[j][0] # 개별 헌금 목 출력이름
                            self.income_budg_tableWidget.setItem(row_cnt,1,QTableWidgetItem(hun_mok_name))
                            for j2 in range(ord_budg_cnt):
                                order_budg_mok = str(budget_income[j2][1]) # 헌금명칭(항)
                                if hun_mok_name == order_budg_mok:
                                    order_amo = int(budget_income[j2][2])
                                    int_amo = format(order_amo,",")
                                    order_amo_hap += order_amo
                                    order_sum = format(order_amo_hap,",")
                                    hun_amo_hap += order_amo
                                    hun_sum = format(hun_amo_hap,",")
                                    self.income_budg_tableWidget.setItem(row_cnt, 1,QTableWidgetItem(hun_mok_name))
                                    self.income_budg_tableWidget.setItem(row_cnt, 2,QTableWidgetItem(int_amo))
                                    if self.income_budg_tableWidget.item(row_cnt, 2) != None:
                                        self.income_budg_tableWidget.item(row_cnt, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                            row_cnt += 1
                        self.income_budg_tableWidget.setItem(row_cnt-(or_hun_cnt + 1), 2,QTableWidgetItem(order_sum))
                        if self.income_budg_tableWidget.item(row_cnt - (or_hun_cnt + 1), 2) != None:
                            self.income_budg_tableWidget.item(row_cnt-(or_hun_cnt + 1), 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        order_amo_hap = 0
                    self.income_budg_tableWidget.resizeColumnsToContents()
                self.income_budg_hap_widget.setText(hun_sum)
            except ValueError:
                QMessageBox.about(self, "입력없음","예산년도를 입력해 주세요.")
                self.budget_year_widget.setFocus()
                return
        
    def budget_view_2(self):  #지출예산 가져오기
        from budget.budget_call_select import budget_cost_call
        budg_year_st = self.budget_year_widget.text() #budg_year_st는 예산년도 시작(start)
        if budg_year_st == "" or budg_year_st is None :
            self.budget_year_widget.setFocus()
            return
        budg_year = int(budg_year_st)
        budget_cost = budget_cost_call(budg_year)
        if len(budget_cost):
            self.budget_cost_hang_mok_call(budg_year) # 항목 가져오기
            # try:
            table_row_count = self.cost_budg_tableWidget.rowCount()
            t_hang = None; t_mok = None; t_semok = None
            
            for row in range(table_row_count):
                t_hang_T = self.cost_budg_tableWidget.item(row,0)
                t_mok_T = self.cost_budg_tableWidget.item(row,1)
                t_semok_T = self.cost_budg_tableWidget.item(row,2)
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
                        self.cost_budg_tableWidget.setItem(row, 3,QTableWidgetItem(bug_amount))
                        if self.cost_budg_tableWidget.item(row, 3) != None:
                            self.cost_budg_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.cost_budg_tableWidget.setItem(row, 4,QTableWidgetItem(bug_marks))
            self.cost_budg_tableWidget.resizeColumnsToContents()
            self.re_calculate()
            self.select_delete_rowcount()
    
    def select_delete_rowcount(self):
        # 삭제대상열 선택하고 삭제하기
        del_select_row = self.cost_budg_tableWidget.rowCount()
        # 역순으로 삭제해야 인덱스 문제 방지
        for row in reversed(range(del_select_row)):
            item = self.cost_budg_tableWidget.item(row, 3)
            if item is not None:
                row_value = item.text()
                if row_value == '0' or row_value == None or row_value == 0:
                    self.cost_budg_tableWidget.removeRow(row)
            # else:

    def budget_cost_hang_mok_call(self,budg_year):
        from basic.cost_hangmok_select import cost_budget_hang_list, cost_budget_mok_list, cost_budget_semok_list
        try:
            self.cost_budg_tableWidget.clearContents()
            self.cost_budg_tableWidget.setRowCount(1)
            gubun = "일반회계"
            co_this_hang_list = cost_budget_hang_list(budg_year,gubun)   # 계정 항 가져오기
            co_this_semok_tuple = cost_budget_semok_list(budg_year,'all')
            if co_this_semok_tuple != None:
                co_this_semok_mok_list = [item[0] for item in co_this_semok_tuple]
                co_this_Count = len(co_this_hang_list)
                self.cost_budg_tableWidget.setRowCount(1)
            else:
                co_this_Count = 0

            row = 0
            
            if co_this_Count > 1:
                for j in range(co_this_Count):  # j는 행 c는 열
                    co_this_hang = co_this_hang_list[j][0]
                    co_amp = '0'
                    co_this_mok_list = cost_budget_mok_list(budg_year, co_this_hang)
                    if row != 0:
                        self.cost_budg_tableWidget.insertRow(row)

                    if len(co_this_mok_list) == 0:
                        self.cost_budg_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        self.cost_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                        if self.cost_budg_tableWidget.item(row,3) is not None:
                            self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        row += 1
                    
                    else:
                        self.cost_budg_tableWidget.setItem(row,0,QTableWidgetItem(co_this_hang))
                        self.cost_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                        self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        row += 1
                        for j2 in range(len(co_this_mok_list)):  # j는 행 c는 열
                            co_this_mok = str(co_this_mok_list[j2][0])
                            if row != 0:
                                self.cost_budg_tableWidget.insertRow(row)
                                
                            if co_this_mok in co_this_semok_mok_list:
                                co_this_semok_list = cost_budget_semok_list(budg_year,co_this_mok)
                                self.cost_budg_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                self.cost_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                if self.cost_budg_tableWidget.item(row,3) is not None:
                                    self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                row += 1

                                for j3 in range(len(co_this_semok_list)):  # j는 행 c는 열
                                    co_this_semok = str(co_this_semok_list[j3][0])
                                    if row != 0:
                                        self.cost_budg_tableWidget.insertRow(row)
                                        self.cost_budg_tableWidget.setItem(row,2,QTableWidgetItem(co_this_semok))
                                        self.cost_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                        if self.cost_budg_tableWidget.item(row,3) is not None:
                                            self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                        row += 1
                            else: # if len(co_this_semok_list) == 0:
                                self.cost_budg_tableWidget.setItem(row,1,QTableWidgetItem(co_this_mok))
                                self.cost_budg_tableWidget.setItem(row,3,QTableWidgetItem(co_amp))
                                if self.cost_budg_tableWidget.item(row,3) is not None:
                                    self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                row += 1

                        if self.cost_budg_tableWidget.item(row,3) is not None:
                            self.cost_budg_tableWidget.item(row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        except ValueError:
            QMessageBox.about(self,'ValueError',"예산작성 년도를 입력하세요. !!!")
        except TypeError:
            QMessageBox.about(self,'TypeError',"데이터가 없습니다.")




    def re_calculate(self):
        hap_total = 0
        this_year_count = self.cost_budg_tableWidget.rowCount()
        this_hang_amo_int = 0; this_mok_amo_int =0; this_amo_int = None
        for a in range(this_year_count):
            this_hang_T1 = self.cost_budg_tableWidget.item(a,0)  #a 는 0 부터
            this_hang_T2 = self.cost_budg_tableWidget.item(a+1,0)
            this_semok_T1 = self.cost_budg_tableWidget.item(a,2)
            this_semok_T2 = self.cost_budg_tableWidget.item(a+1,2)
            this_mok_T1 = self.cost_budg_tableWidget.item(a,1)
            this_mok_T2 = self.cost_budg_tableWidget.item(a+1,1)
            if this_hang_T1 != None and this_hang_T2 != None : # 항이 현재항과 아래도 항의 있을때, 목이 없는 경우(현재는 이런 경우 없음)
                this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                this_amo_int = int(this_amo_T.replace(",",''))
                this_amo_f = format(this_amo_int,",")
                hap_total += this_amo_int
                self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            elif this_hang_T1 != None and this_hang_T2 == None : # 현재의 항에는 있고 아래의 항에는 없을때 즉 목에 있다(?)그러므로 목이 있는 항의 시작
                hang_c_adj = 0 ; this_hang_amo_int = 0  # 항의 차감 행의 수(hang_c_adj), 항의 합계(this_hang_amo_int)를 초기화 한다.
            elif this_hang_T1 == None and this_hang_T2 == None :  # 여기는 항의 목이 이어지는 형태이다.
                if this_mok_T1 != None and this_mok_T2 != None:   # 현재와 아래의 목에 값이있다. 목의 갑을 받아 넣는다. 항에 값에 더한다.
                    hang_c_adj += 1
                    this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                elif this_mok_T1 != None and this_mok_T2 == None: # 현재 목의 명칭은 있고 다음 목의 명칭은 없다.  세목이 있거나. 다음 항으로 간다.
                    if this_semok_T1 == None and this_semok_T2 != None: # 아래부터 세목이 있는 경우
                        mok_c_adj = 0
                        hang_c_adj += 1
                    elif this_semok_T1 == None and this_semok_T2 == None:
                        hang_c_adj += 1
                        this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_hang_amo_int += this_amo_int  # this_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        this_hang_amo = format(this_hang_amo_int,",")
                        hap_total += this_amo_int
                        self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))  # 목의 값이다.
                        self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.cost_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))  # 목의 값이다.
                        self.cost_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        hang_c_adj = 0; this_hang_amo_int =0
                    
                elif this_mok_T1 == None and this_mok_T2 == None:  # 현재의 항에도 없고, 다음 항에도 없다
                    if this_semok_T1 != None and this_semok_T2 != None: # 현재와 다음 행에 세목이 있다.
                        mok_c_adj += 1
                        hang_c_adj += 1
                        this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_mok_amo_int += this_amo_int
                        this_hang_amo_int += this_amo_int  # this_hang_amo_int =  목의 합계를 항에 넣을 항의 금액
                        # this_hang_amo = format(this_hang_amo_int,",")
                        hap_total += this_amo_int
                        self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))  # 목의 값이다.
                        self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                elif this_mok_T1 == None and this_mok_T2 != None :
                    if this_semok_T1 != None and this_semok_T2 == None :
                        mok_c_adj += 1
                        hang_c_adj += 1
                        this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                        this_amo_int = int(this_amo_T.replace(",",''))
                        this_amo_f = format(this_amo_int,",")
                        this_mok_amo_int += this_amo_int
                        this_mok_amo = format(this_mok_amo_int,",")
                        this_hang_amo_int += this_amo_int
                        this_hang_amo = format(this_hang_amo_int,",")
                        hap_total += this_amo_int
                        self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                        self.cost_budg_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(this_mok_amo))
                        self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                        self.cost_budg_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                        this_mok_amo_int = 0; mok_c_adj = 0
            
            elif this_hang_T1 == None and this_hang_T2 != None :
                if this_semok_T1 != None and this_semok_T2 == None :
                    mok_c_adj += 1
                    hang_c_adj += 1
                    this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_mok_amo_int += this_amo_int
                    this_mok_amo = format(this_mok_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.cost_budg_tableWidget.setItem(a-mok_c_adj,3,QTableWidgetItem(this_mok_amo))
                    self.cost_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))
                    self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_budg_tableWidget.item(a-mok_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    
                    mok_c_adj = 0; hang_c_adj = 0; this_hang_amo_int =0; this_mok_amo_int = 0
                if this_mok_T1 != None and this_mok_T2 == None :
                    hang_c_adj += 1
                    this_amo_T = self.cost_budg_tableWidget.item(a,3).text()
                    this_amo_int = int(this_amo_T.replace(",",''))
                    this_amo_f = format(this_amo_int,",")
                    this_hang_amo_int += this_amo_int
                    this_hang_amo = format(this_hang_amo_int,",")
                    hap_total += this_amo_int
                    self.cost_budg_tableWidget.setItem(a,3,QTableWidgetItem(this_amo_f))
                    self.cost_budg_tableWidget.setItem(a-hang_c_adj,3,QTableWidgetItem(this_hang_amo))  # 목으로만 분리된 항의 합계
                    self.cost_budg_tableWidget.item(a,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    self.cost_budg_tableWidget.item(a-hang_c_adj,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

                    hang_c_adj = 0; this_hang_amo_int =0
        if this_amo_int != None and this_amo_int != '':
            this_amo_f = format(this_amo_int,",")
        else:
            QMessageBox.about(self,'TypeError',"데이터가 없습니다.")
            self.budget_year_widget.setFocus()
            return
        this_year_hap = format(hap_total,",")
        self.cost_budg_hap_widget.setText(this_year_hap)
        self.cost_budg_tableWidget.resizeColumnsToContents()
        
    def budget_view_close(self):
        global order_amo_hap, income_hap
        order_amo_hap = 0;  income_hap = 0
        self.budget_year_widget.clear()
        self.income_budg_hap_widget.clear()
        self.cost_budg_hap_widget.clear()
        self.income_budg_tableWidget.clearContents()
        self.cost_budg_tableWidget.clearContents()
        self.income_budg_tableWidget.setRowCount(0)
        self.cost_budg_tableWidget.setRowCount(0)
        
        self.close()

    def print_button_clicked(self):
        being1 = self.income_budg_tableWidget.rowCount()
        if not being1 :
            QMessageBox.about(self, "내용없음","출력할 수입예산 내용이 없습니다..")
            self.budget_year_widget.setFocus()
            return
        
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.budget_year_widget.text()
            year_text = self.year_label.text()
            income_title_text = "수입예산 예산"
            
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

            # title_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, income_title_text)
            title_width = painter.fontMetrics().width(income_title_text)
            current_x += title_width + 20  # 다음에 들어갈 내용이 없으므로 사용되지 않음
            
            # 초기 좌표 설정
            x = x_margin
            y = current_y + 20
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 30  # 기본 행 높이
            painter.setFont(font2)
            # 각 열의 열별 넓이의 리스트 만들기
            col_widths = [self.cost_budg_tableWidget.columnWidth(col) for col in range(self.cost_budg_tableWidget.columnCount())]
            # # 아래의 코드를 한줄로 표시한 것이 다
            # col_widths = []
            # for col in range(self.cost_budg_tableWidget.columnCount()):
            #     width = self.cost_budg_tableWidget.columnWidth(col)
            #     col_widths.append(width)
            
             # 테이블 헤더 출력
            for col in range(self.income_budg_tableWidget.columnCount()):
                header_text = self.income_budg_tableWidget.horizontalHeaderItem(col).text()
                col_width = int(col_widths[col] * available_width / sum(col_widths))
                self.adjust_font_size(painter, header_text, col_width)
                painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, self.income_budg_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                x += col_width

            # x = x_margin
            y += row_height
            
            # 테이블 내용 출력
            for row in range(self.income_budg_tableWidget.rowCount()):
                if y + row_height > page_rect.bottom() - y_margin:
                    printer.newPage()
                    y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                x = x_margin

                for col in range(self.income_budg_tableWidget.columnCount()):
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    painter.drawRect(x, y, col_width, row_height)
                    # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    item = self.income_budg_tableWidget.item(row, col)
                    if item and item.text():
                        cell_text = item.text()
                        self.adjust_font_size(painter, cell_text, col_width)
                        if col == 2 :
                            # 우측 여백 5 픽셀 
                            rect = QRect(x, y, col_width - 5, row_height)
                            align = Qt.AlignRight | Qt.AlignVCenter
                        else:
                            # 좌측 여백 5 픽셀 들여쓰기
                            rect = QRect(x + 5, y, col_width, row_height)  # 좌측
                            align = Qt.AlignLeft | Qt.AlignVCenter
                        painter.drawText(rect, align, cell_text)
                    x += col_width
                y += row_height
            painter.end()

        self.print_button_clicked_2()

    def print_button_clicked_2(self):
        being2 = self.cost_budg_tableWidget.rowCount()
        if not being2 or not being2 :
            QMessageBox.about(self, "내용없음","출력할 지출예산 내용이 없습니다..")
            self.budget_year_widget.setFocus()
            return
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.budget_year_widget.text()
            year_text = self.year_label.text()
            cost_title_text = "지출 예산"
            
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

            # title_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, cost_title_text)
            title_width = painter.fontMetrics().width(cost_title_text)
            current_x += title_width + 20  # 다음에 들어갈 내용이 없으므로 사용되지 않음
            
            # 초기 좌표 설정
            x = x_margin
            y = current_y + 20
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 30  # 기본 행 높이
            painter.setFont(font2)
            # 각 열의 열별 넓이의 리스트 만들기
            col_widths = [self.cost_budg_tableWidget.columnWidth(col) for col in range(self.cost_budg_tableWidget.columnCount())]
            # # 아래의 코드를 한줄로 표시한 것이 다
            # col_widths = []
            # for col in range(self.cost_budg_tableWidget.columnCount()):
            #     width = self.cost_budg_tableWidget.columnWidth(col)
            #     col_widths.append(width)
            
             # 테이블 헤더 출력
            for col in range(self.cost_budg_tableWidget.columnCount()):
                header_text = self.cost_budg_tableWidget.horizontalHeaderItem(col).text()
                col_width = int(col_widths[col] * available_width / sum(col_widths))
                self.adjust_font_size(painter, header_text, col_width)
                painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, self.cost_budg_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                x += col_width

            # x = x_margin
            y += row_height
            
            # 테이블 내용 출력
            for row in range(self.cost_budg_tableWidget.rowCount()):
                if y + row_height > page_rect.bottom() - y_margin:
                    printer.newPage()
                    y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                x = x_margin

                for col in range(self.cost_budg_tableWidget.columnCount()):
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    painter.drawRect(x, y, col_width, row_height)
                    # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    item = self.cost_budg_tableWidget.item(row, col)
                    if item and item.text():
                        cell_text = item.text()
                        self.adjust_font_size(painter, cell_text, col_width)
                        if col == 3 :
                            # 우측 여백 5 픽셀 
                            rect = QRect(x, y, col_width - 5, row_height)
                            align = Qt.AlignRight | Qt.AlignVCenter
                        else:
                            # 좌측 여백 5 픽셀 들여쓰기
                            rect = QRect(x + 5, y, col_width, row_height)  # 좌측
                            align = Qt.AlignLeft | Qt.AlignVCenter
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
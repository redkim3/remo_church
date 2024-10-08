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
        from budget.budget_cost_select import past_cost_budget_call
        budg_year_T = self.budget_year_widget.text()
        if budg_year_T:
            try:
                budg_year = int(budg_year_T)
                budget_cost = past_cost_budget_call(budg_year)
                # gubun = '일반회계'
                self.cost_budg_tableWidget.setRowCount(1)
                cost_sum = ""
                #if crCount > 1:
                tree = collections.defaultdict(dict)

                # 결과 데이터를 트리로 변환합니다.
                for item in budget_cost:
                    hang, mok, semok, amount = item
                    if semok:
                        if mok == None:
                            if hang not in tree:
                                tree[hang] = {}
                            if mok not in tree[hang]:
                                tree[hang][mok] = {}
                            tree[hang][mok][semok] = amount
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
                # row_count = self.cost_budg_tableWidget.rowCount()  # 현재 행의 수 가져오기
                row = 0; cost_sum = 0; s = 0; m = 0; mok_sum = 0
                for hang, mok_data in tree.items():
                    hang_sum = 0
                    if row != 0:
                        self.cost_budg_tableWidget.insertRow(row)  # 행 삽입
                    self.cost_budg_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입
                    for mok, semok_data in mok_data.items():
                        if mok:
                            row += 1  # 행 인덱스 증가
                            self.cost_budg_tableWidget.insertRow(row)  # 행 삽입
                            self.cost_budg_tableWidget.setItem(row, 1, QTableWidgetItem(mok))  # 행의 첫 번째 열에 항목 삽입
                            # 행 인덱스 증가;
                            for semok, amount in semok_data.items():
                                if semok != '0':
                                    row += 1 
                                    s += 1; m += 1
                                    self.cost_budg_tableWidget.insertRow(row)  # 행 삽입
                                    amo_txt = format(amount,',')
                                    self.cost_budg_tableWidget.setItem(row, 2, QTableWidgetItem(semok))  # 행의 첫 번째 열에 항목 삽입
                                    self.cost_budg_tableWidget.setItem(row, 3, QTableWidgetItem(amo_txt))  # 행의 두 번째 열에 항목 삽입
                                    if self.cost_budg_tableWidget.item(row, 3) != None:
                                        self.cost_budg_tableWidget.item(row, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    mok_sum += amount  # 목의 합계 갱신
                                    hang_sum += amount
                                    cost_sum += amount
                                    amount = 0
                                
                            mok_sum += amount  # 목의 합계 갱신
                            mok_sum_txt = format(mok_sum,',')
                            self.cost_budg_tableWidget.setItem(row - s, 3, QTableWidgetItem(mok_sum_txt))  # 목의 합계 표시
                            if self.cost_budg_tableWidget.item(row - s, 3) != None:
                                self.cost_budg_tableWidget.item(row - s, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                            #hang_sum += mok_sum  # 행의 합계 갱신
                            hang_sum += amount
                            cost_sum += amount
                            m += 1; s = 0; mok_sum = 0; amount = 0
                        else:
                            #self.cost_budg_tableWidget.insertRow(row)  # 행 삽입
                            self.cost_budg_tableWidget.setItem(row, 0, QTableWidgetItem(hang))  # 행의 첫 번째 열에 항목 삽입
                            # 행 인덱스 증가;
                            for semok, amount in semok_data.items():
                                if semok != '0':
                                    s += 1; m += 1
                                
                            mok_sum += amount  # 목의 합계 갱신
                            mok_sum_txt = format(mok_sum,',')
                            self.cost_budg_tableWidget.setItem(row - s, 3, QTableWidgetItem(mok_sum_txt))  # 목의 합계 표시
                            if self.cost_budg_tableWidget.item(row - s, 3) != None:
                                self.cost_budg_tableWidget.item(row - s, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                            hang_sum += amount
                            cost_sum += amount
                            m += 1; s = 0; mok_sum = 0; amount = 0
                    hang_sum_txt = format(hang_sum,',')
                    self.cost_budg_tableWidget.setItem(row - m, 3, QTableWidgetItem(hang_sum_txt))  # 행의 합계 표시
                    if self.cost_budg_tableWidget.item(row - m, 3) != None:
                        self.cost_budg_tableWidget.item(row - m, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    m = 0; s = 0; row += 1

                    cost_sum_txt = format(cost_sum,',')
                    self.cost_budg_hap_widget.setText(cost_sum_txt)
            except ValueError:
                QMessageBox.about(self, "입력없음","예산년도를 입력해 주세요.")
                self.budget_year_widget.setFocus()
                return
        
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
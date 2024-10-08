import os, subprocess
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt, QRect, QSize
from PyQt5.QtGui import QFont, QIcon, QFontMetrics
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtGui import QPainter
import pandas as pd

cur_fold = os.getcwd()
today = QDate.currentDate()
saved_file = r'./excel_view/특별회계_분기보고.xlsx'
form_secondclass = uic.loadUiType("./ui/Quarter_special_report.ui")[0]

class Special_quarterly_Report(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(Special_quarterly_Report,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("분기 특별회계 재정보고")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        bogo_year = today.year()
        self.bogo_year_widget.setText(str(bogo_year))
        self.bogo_year_widget.setFocus()
    
    def connectFunction(self):
        self.Quarter_view_Button.clicked.connect(self.Quarterly_view)
        self.Quarterly_excel_save_Button.clicked.connect(self.special_Q_excel_save)
        self.Quarterly_income_close_Button.clicked.connect(self.special_Q_income_close)
    
    def Quarterly_view(self):
        global bogo_bungi, bogo_year
        from basic.special_acc_sql import remained_bank_account, special_tree_data_incre, special_tree_data_decre
        from basic.cost_select import cost_hang_values
        
        self.income_tableWidget.clearContents()
        self.income_tableWidget.setColumnCount(4)
        self.out_tableWidget.clearContents()
        self.out_tableWidget.setColumnCount(4)
        column_headers = ['수입내역', '합  계', '비  고']
        self.income_tableWidget.setRowCount(0)
        self.out_tableWidget.setRowCount(0)
        
        bogo_year_T = self.bogo_year_widget.text()
        if bogo_year_T:
            bogo_year = int(bogo_year_T)
            if bogo_year < 1000 or bogo_year > 9999:
                QMessageBox.about(self, '누락', '보고년도는 1000부터 9999 사이의 4자리 수를 입력하세요.')
                self.bogo_year_widget.setFocus()
                return
        
        bogo_bungi_T = self.Quarter_widget.text()
        if bogo_bungi_T:
            bogo_bungi = int(bogo_bungi_T)
            if bogo_bungi < 1 or bogo_bungi > 4:
                QMessageBox.about(self, '누락', '보고 분기는 1부터 4까지의 값을 입력하세요.')
                self.Quarter_widget.setFocus()
                return

        gubun = '특별회계'
        for bun in range(1, bogo_bungi + 1):
            column_headers.insert(bun, str(bun) + '/4분기')
        self.income_tableWidget.setColumnCount(len(column_headers))
        self.income_tableWidget.setHorizontalHeaderLabels(column_headers)

        out_column_headers = ['지출내역', '합  계', '비  고']
        for bun in range(1, bogo_bungi + 1):
            out_column_headers.insert(bun, str(bun) + '/4분기')
        self.out_tableWidget.setColumnCount(len(out_column_headers))
        self.out_tableWidget.setHorizontalHeaderLabels(out_column_headers)
        
        amo_income_int = 0
        amo_out_int = 0
        carryover = remained_bank_account(bogo_year)
        trans_carryover = carryover
        carry_bun = 0
        
        # '전년도 특별회계 예금잔액'을 '전분기 이월잔액'으로 이름 변경하고 첫 번째 행에 추가
        row1 = self.income_tableWidget.rowCount()
        self.income_tableWidget.insertRow(row1)
        self.income_tableWidget.setItem(row1, 0, QTableWidgetItem('전분기 이월잔액'))
        self.income_tableWidget.setItem(row1, 1, QTableWidgetItem(format(carryover, ",")))
        if self.income_tableWidget.item(row1, 1):
            self.income_tableWidget.item(row1, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        income_semoks = {}
        out_semoks = {}
        for bun in range(1, bogo_bungi + 1):
            tree_incre_data = special_tree_data_incre(bogo_year, bun)
            tree_decre_data = special_tree_data_decre(bogo_year, bun)
            inrow_count = self.income_tableWidget.rowCount()
            
            for in_row in range(inrow_count):
                item = self.income_tableWidget.item(in_row, 0)
                if item is not None:
                    semok_r = item.text()
                    income_semoks[in_row] = semok_r
     
            if tree_incre_data is None:
                print(bun, '분기', "No in_data available")
                return
            if tree_decre_data is None:
                print(bun, '분기', "No out_data available")
                return
            
            row1 = self.income_tableWidget.rowCount()

            for o_row, item in enumerate(tree_incre_data):
                semok = item[2]  # 0열 데이터를 semok으로 사용
                amount1 = item[3]  # 3번째 요소를 값으로 사용
                amount_1 = format(amount1, ",")

                # semok이 이미 추가된 경우 해당 행을 가져오고, 추가되지 않은 경우 새로운 행을 추가
                if semok in income_semoks:
                    row1 = income_semoks[semok]
                else:
                    # semok이 처음 추가되는 경우 새로운 행을 추가
                    row1 = self.income_tableWidget.rowCount()
                    self.income_tableWidget.insertRow(row1)
                    self.income_tableWidget.setItem(row1, 0, QTableWidgetItem(semok))
                    income_semoks[semok] = row1

                # 분기별로 열을 추가하면서 데이터를 넣기
                self.income_tableWidget.setItem(row1, bun, QTableWidgetItem(str(amount_1)))
                if self.income_tableWidget.item(row1, bun):
                    self.income_tableWidget.item(row1, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

            # # 디버깅을 위해 각 단계에서의 상태 출력
            outrow_count = self.out_tableWidget.rowCount()
            for out_row in range(outrow_count):
                out_item = self.out_tableWidget.item(out_row, 0)
                if out_item is not None:
                    out_semok = out_item.text()
                    out_semoks[out_row] = out_semok
            
            for o_row2, item2 in enumerate(tree_decre_data):
                semok2 = item2[2]  # 0열 데이터를 semok으로 사용
                amount2 = item2[3]  # 3번째 요소를 값으로 사용
                amount_2 = format(amount2, ",")
               
                if semok2 in out_semoks:
                    row2 = out_semoks[semok2]
                else:
                    # semok2_row_map[semok2] = row2
                    row2 = self.out_tableWidget.rowCount()
                    self.out_tableWidget.insertRow(row2)
                    self.out_tableWidget.setItem(row2, 0, QTableWidgetItem(semok2))
                    out_semoks[semok2] = row2

                self.out_tableWidget.setItem(row2, bun, QTableWidgetItem(amount_2))
                if self.out_tableWidget.item(row2, bun):
                    self.out_tableWidget.item(row2, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                
        bun_sum_income = 0; bun_sum_out = 0; row1 =0 ; row2 = 0
        for bun in range(1, bogo_bungi + 1):
            total_row_income = self.income_tableWidget.rowCount()
            
            for s_row in range(1,total_row_income):
                amo_T1 = self.income_tableWidget.item(s_row, bun)
                if amo_T1 is not None:
                    amo_1 = amo_T1.text()
                    amo_income_int = int(amo_1.replace(",",""))
                else :
                    amo_income_int = 0
                
                bun_sum_income += amo_income_int
            if bun == 1:
                self.income_tableWidget.insertRow(total_row_income)
                self.income_tableWidget.setItem(total_row_income, 0, QTableWidgetItem('분기 합계'))
                self.income_tableWidget.setItem(total_row_income, bun, QTableWidgetItem(format(bun_sum_income, ",")))
                if self.income_tableWidget.item(total_row_income, bun):
                    self.income_tableWidget.item(total_row_income, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            else:
                self.income_tableWidget.setItem(total_row_income - 1, bun, QTableWidgetItem(format(bun_sum_income, ",")))
                if self.income_tableWidget.item(total_row_income - 1, bun):
                    self.income_tableWidget.item(total_row_income - 1, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            
            total_row_out = self.out_tableWidget.rowCount()
            for out_row in range(total_row_out):
                amo_T2 = self.out_tableWidget.item(out_row, bun)
                if amo_T2 is not None:
                    amo_2 = amo_T2.text()
                    amo_out_int = int(amo_2.replace(",",""))
                else:
                    amo_out_int = 0
                bun_sum_out += amo_out_int
            
            if bun == 1:
                self.out_tableWidget.insertRow(total_row_out)
                self.out_tableWidget.setItem(total_row_out, 0, QTableWidgetItem('분기 합계'))
                self.out_tableWidget.setItem(total_row_out, bun, QTableWidgetItem(format(bun_sum_out, ",")))
                if self.out_tableWidget.item(total_row_out, bun):
                    self.out_tableWidget.item(total_row_out, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            else:
                self.out_tableWidget.setItem(total_row_out - 2, bun, QTableWidgetItem(format(bun_sum_out, ",")))
                if self.out_tableWidget.item(total_row_out - 2, bun):
                    self.out_tableWidget.item(total_row_out - 2, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            
            carry_bun = (trans_carryover + bun_sum_income - bun_sum_out)
            if bun == 1 :
                self.out_tableWidget.insertRow(total_row_out + 1)
                self.out_tableWidget.setItem(total_row_out + 1, 0, QTableWidgetItem('당분기 이월잔액'))
                self.out_tableWidget.setItem(total_row_out + 1, bun, QTableWidgetItem(format(carry_bun, ",")))
                self.income_tableWidget.setItem(0, bun + 1, QTableWidgetItem(format(carry_bun, ",")))
                if self.out_tableWidget.item(total_row_out + 1, bun):
                    self.out_tableWidget.item(total_row_out + 1, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                if self.income_tableWidget.item(0, bun + 1):
                    self.income_tableWidget.item(0, bun + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            elif bun == bogo_bungi:
                self.out_tableWidget.setItem(total_row_out - 1, bun, QTableWidgetItem(format(carry_bun, ",")))
                self.income_tableWidget.setItem(0, bun + 1, QTableWidgetItem(format(carryover, ",")))  # carryover 는 전년도 이월금액
                if self.out_tableWidget.item(total_row_out - 1, bun):
                    self.out_tableWidget.item(total_row_out - 1, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                if self.income_tableWidget.item(0, bun + 1):
                    self.income_tableWidget.item(0, bun + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            else:
                self.out_tableWidget.setItem(total_row_out - 1, bun, QTableWidgetItem(format(carry_bun, ",")))
                self.income_tableWidget.setItem(0, bun + 1, QTableWidgetItem(format(carry_bun, ",")))
                if self.out_tableWidget.item(total_row_out - 1, bun):
                    self.out_tableWidget.item(total_row_out - 1, bun).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                if self.income_tableWidget.item(0, bun + 1):
                    self.income_tableWidget.item(0, bun + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    
            amo_income_int = 0; amo_out_int = 0
            bun_sum_income = 0; bun_sum_out = 0
            trans_carryover = carry_bun
        
        # 가로 합계를 계산하여 마지막 열에 설정
        for row in range(self.income_tableWidget.rowCount()):
            row_sum = 0
            if row == 0:
                self.income_tableWidget.setItem(row, bogo_bungi + 1, QTableWidgetItem(format(carryover, ",")))
                if self.income_tableWidget.item(row, bogo_bungi + 1):
                    self.income_tableWidget.item(row, bogo_bungi + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            else:
                for col in range(1, bogo_bungi + 1):
                    item = self.income_tableWidget.item(row, col)
                    if item:
                        row_sum += int(item.text().replace(",", ""))
                self.income_tableWidget.setItem(row, bogo_bungi + 1, QTableWidgetItem(format(row_sum, ",")))
                if self.income_tableWidget.item(row, bogo_bungi + 1):
                    self.income_tableWidget.item(row, bogo_bungi + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

        for row in range(self.out_tableWidget.rowCount() - 1):
            row_sum = 0
            for col in range(1, bogo_bungi + 1):
                item = self.out_tableWidget.item(row, col)
                if item:
                    row_sum += int(item.text().replace(",", ""))
            self.out_tableWidget.setItem(row, bogo_bungi + 1, QTableWidgetItem(format(row_sum, ",")))
            if self.out_tableWidget.item(row, bogo_bungi + 1):
                self.out_tableWidget.item(row, bogo_bungi + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.out_tableWidget.setItem(row + 1, bogo_bungi + 1, QTableWidgetItem(format(carry_bun, ",")))
            if self.out_tableWidget.item(row + 1, bogo_bungi + 1):
                self.out_tableWidget.item(row + 1, bogo_bungi + 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

        for col in range(self.income_tableWidget.columnCount()):
            # width = int(total_width * col_ratios[col])
            width = int(self.income_tableWidget.columnWidth(col)) * 2
            self.income_tableWidget.setColumnWidth(col, width)
        for col in range(self.out_tableWidget.columnCount()):
            # width = int(total_width * col_ratios[col])
            width = int(self.out_tableWidget.columnWidth(col)) * 2
            self.out_tableWidget.setColumnWidth(col, width)

        self.income_tableWidget.resizeColumnsToContents()
        self.out_tableWidget.resizeColumnsToContents()

    def print_button_clicked(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

            # 각 라벨의 텍스트와 폰트 설정
            year_int = self.bogo_year_widget.text()
            year_text = self.year_label.text()
            quarter_int = self.Quarter_widget.text()
            title_text = self.title_label.text()
            asset_sell = self.income_label.text()
            asset_buy = self.balance_label.text()
            font1 = painter.font()
            font_sub = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font_sub.setPointSize(11)
            font2.setPointSize(10)

            x_margin = 50; y_margin = 90
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
            self.adjust_font_size(painter, year_text, available_width)
            painter.drawText(current_x, current_y, year_text)
            year_width = painter.fontMetrics().width(year_text)
            current_x += year_width + 10

            # quarter_int 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, quarter_int, available_width)
            painter.drawText(current_x, current_y, quarter_int)
            quarter_width = painter.fontMetrics().width(quarter_int)
            current_x += quarter_width + 20  #painter.fontMetrics().height() + 20  # 20은 제목과 테이블 간 간격

            # title_text 출력
            painter.setFont(font1)
            self.adjust_font_size(painter, title_text, available_width)
            painter.drawText(current_x, current_y, title_text)
            title_width = painter.fontMetrics().width(title_text)
            
            # asset_sell 출력
            current_x = x_margin
            current_y += 45 # title_width + 10  # 10은 라벨 간 간격

            painter.setFont(font_sub)
            self.adjust_font_size(painter, asset_sell, available_width)
            painter.drawText(current_x, current_y, asset_sell)
            title_width = painter.fontMetrics().width(asset_sell)
            
            # 초기 좌표 설정(수입)
            x = x_margin
            y = current_y + 10
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 35  # 기본 행 높이
            painter.setFont(font2)
            col_widths = [self.income_tableWidget.columnWidth(col) for col in range(self.income_tableWidget.columnCount())]
            
            # 테이블 헤더 출력
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
                        if col == 0 :
                            if cell_text == '분기 합계':
                                rect = QRect(x, y, col_width, row_height)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 여백 7 픽셀 들여쓰기
                                rect = QRect(x + 5, y, col_width, row_height)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                        else:
                            # 우측 여백 7 픽셀 
                            rect = QRect(x, y, col_width - 7, row_height)
                            align = Qt.AlignRight | Qt.AlignVCenter
                        
                        painter.drawText(rect, align, cell_text)

                    x += col_width

                y += row_height

            
            # 초기 좌표 설정(요약)
            # out_tableWidget 헤더 그리기
            row_height = 35  # 기본 행 높이
            painter.setFont(font2)
            header_height_2 = self.out_tableWidget.horizontalHeader().height()
            x2 = x_margin  # 시작 x 좌표
            y2 = y + 40  # mission_tableWidget 아래에 위치

             # asset_sell 출력
            current_x = x_margin
            current_y2 = y2 # title_width + 10  # 10은 라벨 간 간격

            painter.setFont(font_sub)
            self.adjust_font_size(painter, asset_buy, available_width)
            painter.drawText(current_x, current_y2, asset_buy)
            title_width = painter.fontMetrics().width(asset_buy)
            y2 += 10

            bal_widths = [self.out_tableWidget.columnWidth(col2) for col2 in range(self.out_tableWidget.columnCount())]

            # 테이블 헤더 출력 (비율 조정된 열 너비 사용)
            for col2 in range(self.out_tableWidget.columnCount()):
                header_item2 = self.out_tableWidget.horizontalHeaderItem(col2)  # .text()수평 헤더 가져옴
                bal_width = int(bal_widths[col2] * available_width / sum(bal_widths))
                # col_width2 = self.out_tableWidget.columnWidth(col2)  # 각 열의 너비를 가져옴
                if header_item2:
                    text_rect2 = QRect(x2, y2, bal_width, header_height_2)
                    painter.drawText(text_rect2, Qt.AlignCenter | Qt.AlignVCenter, header_item2.text())
                    painter.drawRect(x2, y2, bal_width, header_height_2)
                x2 += bal_width

            # v_x3 += bal_widths[0]
            y2 += header_height_2  # 헤더 아래부터 데이터 시작

            # 테이블 내용 출력
            for row3 in range(self.out_tableWidget.rowCount()):  # +1 제거
                if y2 + row_height > available_height + y_margin:
                    printer.newPage()
                    y2 = y_margin + 50
                x2 = x_margin
                for col3 in range(self.out_tableWidget.columnCount()):
                    col_width3 = int(bal_widths[col3] * available_width / sum(bal_widths))
                    painter.drawRect(x2, y2, col_width3, header_height_2)  # 테두리 그리기
                    item3 = self.out_tableWidget.item(row3, col3)
                    if item3 and item3.text():
                        cell_text3 = item3.text()
                        self.adjust_font_size(painter, cell_text3, col_width)
                        if col3 == 0 :
                            if cell_text3 == '분기 합계':
                                rect2 = QRect(x2, y2, col_width3, header_height_2)  # 좌측
                                align2 = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 여백 7 픽셀 들여쓰기
                                rect2 = QRect(x2 + 5, y2, col_width3, header_height_2)  # 좌측
                                align2 = Qt.AlignLeft | Qt.AlignVCenter
                        else:
                            # 우측 여백 7 픽셀 
                            rect2 = QRect(x2, y2, col_width3 - 7, header_height_2)
                            align2 = Qt.AlignRight | Qt.AlignVCenter
                        
                        painter.drawText(rect2, align2, cell_text3)
                    x2 += col_width3

                y2 += header_height_2
        painter.end()

    def adjust_font_size(self,painter, text, max_width):
        """
        텍스트가 주어진 폭에 맞도록 폰트 크기를 조정합니다.
        """
        font = painter.font()
        font_metrics = QFontMetrics(font) # QFontMetrics는 특정 측정정보를 계산하는데 쓰이는Qt 클래스중 하나
        while font_metrics.boundingRect(text).width() > max_width: # boundingRect는 QFontMetrics 클래스에서 제공하는 메서드 사각형으로 텍스트가 화면에 렌더링될때 차지하는 공간을 나타냄
            font_size = font.pointSize()  # 현재의 폰트 크기를 가져옴
            if font_size <= 10:  # 최소 폰트 크기 제한
                break
            font.setPointSize(font_size - 1) # QFont 객체의 글꼴 크기를 한 포인트 줄이는 코드
            painter.setFont(font)
            font_metrics = QFontMetrics(font)

    def special_Q_excel_save(self):  # 홈버튼

        r1_count = self.income_tableWidget.rowCount()
        c1_count = self.income_tableWidget.columnCount()
        r2_count = self.out_tableWidget.rowCount()
        c2_count = self.out_tableWidget.columnCount()
        
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
            dat1 = self.out_tableWidget.horizontalHeaderItem(j2)
            if dat1:
                balance_columnHeaders.append(
                    self.out_tableWidget.horizontalHeaderItem(j2).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                balance_columnHeaders.append('Null')

        # 데이터프레임 생성
        df2 = pd.DataFrame(columns = balance_columnHeaders)
        # 수입내역 테이블 데이터로 데이터프레임 채우기
        for row2 in range(r2_count): #self.tbl_result.rowCount()):
            for col2 in range(c2_count): #self.tbl_result.columnCount()):
                try:
                    df2.at[row2, balance_columnHeaders[col2]] = self.out_tableWidget.item(row2, col2).text()
                except:
                    continue

        try :
            with pd.ExcelWriter(saved_file, engine='openpyxl') as writer:
            # 첫 번째 데이터프레임 출력
                df1.to_excel(writer, sheet_name='quarter_income_combined', index=False, startcol=0, startrow=0, na_rep='', inf_rep='')
            
            # 두 번째 데이터프레임 출력 (시작 위치를 6행 더 아래로 이동)
                df2.to_excel(writer, sheet_name='quarter_income_combined', index=True, startcol=0, startrow=len(df1) + 6, na_rep='', inf_rep='') #, header=True)

            subprocess.Popen(["start", "excel.exe", os.path.abspath(saved_file)], shell=True)
            QMessageBox.about(self,'저장',"'특별회계_분기보고.xlsx'파일에 저장되었습니다.!!!")
        except OSError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            QMessageBox.about(self,'파일열기 에러',"'특별회계_분기보고'파일이 열려 있습니다. 파일을 닫고 다시 진행해 주세요. !!!")

    def special_Q_income_close(self):
        self.Quarter_widget.clear()
        self.income_tableWidget.setRowCount(0)
        self.income_tableWidget.setColumnCount(4)
        self.out_tableWidget.setRowCount(0)
        self.out_tableWidget.setColumnCount(4)
        self.close()
    
    def closeEvent(self,event):
        self.Quarter_widget.clear()
        self.income_tableWidget.setRowCount(0)
        self.income_tableWidget.setColumnCount(4)
        self.out_tableWidget.setRowCount(0)
        self.out_tableWidget.setColumnCount(4)
        event.accept()
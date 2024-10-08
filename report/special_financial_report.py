import os, subprocess
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt, QRect, QSize
from PyQt5.QtGui import QFont, QIcon, QFontMetrics
from PyQt5.QtWidgets import QTableWidgetItem
from decimal import Decimal
from collections import defaultdict
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtGui import QPainter
import pandas as pd

cur_fold = os.getcwd()
today = QDate.currentDate()
saved_file = r'./excel_view/특별회계_현황보고.xlsx'
form_secondclass = uic.loadUiType("./ui/special_financial_report.ui")[0]

class Special_financial_Report(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(Special_financial_Report,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("분기 특별회계 재정현황보고") # 관리대상 자산 부채 현황
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        bogo_year = today.year()
        self.bogo_year_widget.setText(str(bogo_year))
        self.bogo_year_widget.setFocus()
    
    def connectFunction(self):
        self.Quarter_view_Button.clicked.connect(self.status_view)
        self.Quarterly_excel_save_Button.clicked.connect(self.special_Q_excel_save)
        self.Quarterly_income_close_Button.clicked.connect(self.special_Q_income_close)
    
    def status_view(self):
        global bogo_bungi, bogo_year
        from basic.special_acc_sql import special_tree_financial_data
        from register.bank_account_reg import bank_name_list
                
        self.asset_tableWidget.clearContents()
        self.asset_tableWidget.setColumnCount(4)
        self.liabilities_tableWidget.clearContents()
        self.liabilities_tableWidget.setColumnCount(4)
        column_headers = ['항  목', '세  목', '금  액', '비  고']
        self.asset_tableWidget.setRowCount(0)
        self.liabilities_tableWidget.setRowCount(0)
        
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
        b_name_list = bank_name_list(gubun)
        # print(b_name_list,type(b_name_list))
        
        # 딕셔너리로 변환 
        bank_name_dic = {index: value for index, value in enumerate(b_name_list)} #bank를 딕셔너리로 만들어서 딕셔너리 키값을 행번호로 사용하려고 함.
        self.asset_tableWidget.setColumnCount(len(column_headers))
        self.asset_tableWidget.setHorizontalHeaderLabels(column_headers)
        self.liabilities_tableWidget.setColumnCount(len(column_headers))
        self.liabilities_tableWidget.setHorizontalHeaderLabels(column_headers)
        
        tree_financial_data = special_tree_financial_data(bogo_year, bogo_bungi)
        # print(tree_financial_data)

        # 트리 형태로 변환
        tree_bank_data = self.build_tree_with_bank_adjustments(tree_financial_data)
        tree_balance_data = self.build_tree_with_balance_adjustments(tree_financial_data)
        tree_liab_data = self.build_tree_with_liab_adjustments(tree_financial_data)

        self.populate_bank_table(tree_bank_data)
        self.populate_balance_table(tree_balance_data)
        self.populate_liab_table(tree_liab_data)

        self.asset_tableWidget.resizeColumnsToContents()
        self.liabilities_tableWidget.resizeColumnsToContents()

    # asset_tableWidget에 데이터를 채우는 함수
    def build_tree_with_bank_adjustments(self,data):
        tree = defaultdict(lambda: defaultdict(Decimal))
        char_amount = 0; ga_amount = 0
        for item in data:
            if not isinstance(item, (list, tuple)) or len(item) != 6:
                QMessageBox.critical(None, "데이터 형식 오류", f"데이터 형식이 다릅니다.: {item}")
                continue

            hang, mok, semok, bank, amount, balance = item
        
            mok = "예금잔액"
            if bank != "일반회계에서":
                semok = bank
                if balance == '예금감소':
                    amount = amount * (-1)

                tree[mok][semok] += amount

        return tree

    def build_tree_with_balance_adjustments(self,data):
        tree = defaultdict(lambda: defaultdict(Decimal))
        for item in data:
            if not isinstance(item, (list, tuple)) or len(item) != 6:
                QMessageBox.critical(None, "데이터 형식 오류", f"데이터 형식이 다릅니다.: {item}")
                continue

            hang, mok, semok, bank, amount, balance = item
            if hang != '부채':
                if mok != '보통예금':
                    # print(item)
                    if balance == '예금증가':
                        amount = -amount
                    else:
                        if balance == '예금감소':
                            amount = amount
                
                    tree[mok][semok] += amount

        return tree
    
    def build_tree_with_liab_adjustments(self,data):
        tree = defaultdict(lambda: defaultdict(Decimal))
        for item in data:
            if not isinstance(item, (list, tuple)) or len(item) != 6:
                QMessageBox.critical(None, "데이터 형식 오류", f"데이터 형식이 다릅니다.: {item}")
                continue
            hang, mok, semok, bank, amount, balance = item
            if hang == '부채':
                
                if mok != '보통예금':
                    # print(item)
                    if balance == '예금증가':
                        amount = amount
                    else:
                        if balance == '예금감소':
                            amount = -amount
                
                    tree[mok][semok] += amount

        return tree

    def populate_bank_table(self, tree_bank_data):
        global bank_row
        bank_row = 0
        self.asset_tableWidget.setRowCount(sum(len(semok_dict) for semok_dict in tree_bank_data.values()))

        for mok, semok_dict in tree_bank_data.items():
            for semok, amount in semok_dict.items():
                if amount != 0:
                    self.asset_tableWidget.setItem(bank_row, 0, QTableWidgetItem(mok))
                    self.asset_tableWidget.setItem(bank_row, 1, QTableWidgetItem(semok))
                    self.asset_tableWidget.setItem(bank_row, 2, QTableWidgetItem(format(amount,",")))
                    if self.asset_tableWidget.item(bank_row, 2):
                        self.asset_tableWidget.item(bank_row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    bank_row += 1
                else:
                    self.asset_tableWidget.removeRow(bank_row)

    def populate_balance_table(self, tree_balance_data):
        row = bank_row
        self.asset_tableWidget.setRowCount(sum(len(semok_dict) for semok_dict in tree_balance_data.values()) + bank_row)
        # self.asset_tableWidget.setRowCount(sum((len(semok_dict) + bank_row) for semok_dict in tree_balance_data.values()))

        for mok, semok_dict in tree_balance_data.items():
            for semok, amount in semok_dict.items():
                if amount != 0:
                    self.asset_tableWidget.setItem(row, 0, QTableWidgetItem(mok))
                    self.asset_tableWidget.setItem(row, 1, QTableWidgetItem(semok))
                    self.asset_tableWidget.setItem(row, 2, QTableWidgetItem(format(amount,",")))
                    if self.asset_tableWidget.item(row, 2):
                        self.asset_tableWidget.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    row += 1
                else:
                    self.asset_tableWidget.removeRow(row)

    def populate_liab_table(self, tree_liab_data):
        self.liabilities_tableWidget.setRowCount(sum(len(semok_dict) for semok_dict in tree_liab_data.values()))
        row = 0
        for mok, semok_dict in tree_liab_data.items():
            for semok, amount in semok_dict.items():
                if amount != 0:
                    self.liabilities_tableWidget.setItem(row, 0, QTableWidgetItem(mok))
                    self.liabilities_tableWidget.setItem(row, 1, QTableWidgetItem(semok))
                    self.liabilities_tableWidget.setItem(row, 2, QTableWidgetItem(format(amount,",")))
                    if self.liabilities_tableWidget.item(row, 2):
                        self.liabilities_tableWidget.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    row += 1
                else:
                    self.liabilities_tableWidget.removeRow(row)

    def print_button_clicked(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

            # 각 라벨의 텍스트와 폰트 설정
            year_int = self.bogo_year_widget.text()  # 숫자
            year_text = self.year_label.text()   # 년도
            quarter_text = self.Quarter_widget.text() # 분기 숫자
            title_text = self.title_label.text()  # '분기 특별회계 재정현황'
            managed_asset = self.asset_label.text() # 자산현황
            managed_liability = self.balance_label.text()
            font1 = painter.font()
            font2 = painter.font()
            font_sub = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)
            font_sub.setPointSize(11)

            x_margin = 25; y_margin = 100
            current_x = x_margin
            current_y = y_margin
            
            # year_int 출력
            painter.setFont(font1)
            painter.drawText(current_x, current_y, year_int)
            year_int_width = painter.fontMetrics().width(year_int)
            current_x += year_int_width + 10
            
            # year_text 출력
            painter.setFont(font1)
            painter.drawText(current_x, current_y, year_text)
            year_width = painter.fontMetrics().width(year_text)
            current_x += year_width + 10

            # quarter_text 출력
            painter.drawText(current_x, current_y, quarter_text)
            quarter_width = painter.fontMetrics().width(quarter_text)
            current_x += quarter_width + 20  #painter.fontMetrics().height() + 20  # 20은 제목과 테이블 간 간격
            painter.setFont(font1)

            # title_text 출력
            painter.setFont(font1)
            painter.drawText(current_x, current_y, title_text)
            title_width = painter.fontMetrics().width(title_text)
            # current_x += painter.fontMetrics().height() + 20 # title_width + 10  # 10은 라벨 간 간격

            # managed_asset 출력
            current_x = x_margin
            painter.setFont(font_sub)
            painter.drawText(current_x, current_y + 40, managed_asset)
            title_width = painter.fontMetrics().width(managed_asset)
            # current_x += painter.fontMetrics().height() + 20 # title_width + 10  # 10은 라벨 간 간격
            
            # 페이지 크기 계산
            page_rect = printer.pageRect()
            available_width = page_rect.width() - 2 * x_margin
            available_height = page_rect.height() - current_y - y_margin
            
            # 초기 좌표 설정(수입)
            x = x_margin
            y = current_y + 50
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 35  # 기본 행 높이
            painter.setFont(font2)
            col_widths = [self.asset_tableWidget.columnWidth(col) for col in range(self.asset_tableWidget.columnCount())]
            
            # 테이블 헤더 출력
            col_count = self.asset_tableWidget.columnCount()
            for col in range(col_count):
                painter.drawText(x, y, col_widths[col], row_height, Qt.AlignCenter | Qt.AlignVCenter, self.asset_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x, y, col_widths[col] + 10, row_height)  # 테두리 그리기
                x += col_widths[col] +10
                
            y += row_height
            # x = x_margin
            
            # 테이블 내용 출력
            for row in range(self.asset_tableWidget.rowCount()):
                if y + row_height > available_height + y_margin:  # available_height를 사용하여 페이지 높이 제한
                    printer.newPage()
                    y = y_margin + 50  # 새로운 페이지에서 y 좌표 초기화, 제목 아래 간격 추가

                x = x_margin
                for col in range(self.asset_tableWidget.columnCount()):
                    # col_width = int(col_widths[col] * available_width / sum(col_widths))
                    painter.drawRect(x, y, col_widths[col] + 10, row_height)  # 테두리 그리기
                    item = self.asset_tableWidget.item(row, col)
                    if item and item.text():
                        cell_text = item.text()
                        # self.adjust_font_size(painter, cell_text, col_widths[col])
                        if col == 0 or col == 1:
                            if cell_text == '분기 합계':
                                rect = QRect(x, y, col_widths[col], row_height)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 여백 7 픽셀 들여쓰기
                                rect = QRect(x + 5, y, col_widths[col], row_height)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                        else:
                            # 우측 여백 7 픽셀 
                            rect = QRect(x, y, col_widths[col] - 7, row_height)
                            align = Qt.AlignRight | Qt.AlignVCenter

                        painter.drawText(rect, align, cell_text)

                    x += col_widths[col] + 10
                        
                y += row_height
            
            # 초기 좌표 설정(요약)
            y2 = y + 80
            current_x = x_margin
            painter.setFont(font1)
            painter.drawText(current_x, y2, managed_liability)
            title_width = painter.fontMetrics().width(managed_liability)
            
            # liabilities_tableWidget 헤더 그리기
            row_height = 35  # 기본 행 높이
            painter.setFont(font2)
            header_height_2 = self.liabilities_tableWidget.horizontalHeader().height()
            
            y2 += 10  # mission_tableWidget 아래에 위치
            x2 = x_margin  # 시작 x 좌표
           

            bal_widths = [self.liabilities_tableWidget.columnWidth(col2) for col2 in range(self.liabilities_tableWidget.columnCount())]
            bal_count = self.liabilities_tableWidget.columnCount()
            for col in range(bal_count):
                painter.drawText(x2, y2, bal_widths[col], header_height_2, Qt.AlignCenter | Qt.AlignVCenter, self.liabilities_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x2, y2, bal_widths[col] + 10, header_height_2)  # 테두리 그리기
                x2 += bal_widths[col] +10

            # for col2 in range(self.liabilities_tableWidget.columnCount()):
            #     # col_width2 = self.liabilities_tableWidget.columnWidth(col2)  # 각 열의 너비를 가져옴
            #     header_item2 = self.liabilities_tableWidget.horizontalHeaderItem(col2)  # 수평 헤더 가져옴
            #     if header_item2:
            #         text_rect2 = QRect(x2, y2, bal_widths, header_height_2)
            #         painter.drawText(text_rect2, Qt.AlignCenter | Qt.AlignVCenter, header_item2.text())
            #         painter.drawRect(x2, y2, bal_widths[col] + 10, header_height_2)
            #         x2 += bal_widths[col2] + 10

            # v_x3 += bal_widths[0]
            x2 = x_margin
            y2 += header_height_2  # 헤더 아래부터 데이터 시작
            col_widths3 = [self.liabilities_tableWidget.columnWidth(col2) for col2 in range(self.liabilities_tableWidget.columnCount())]
            for row3 in range(self.liabilities_tableWidget.rowCount()):  # 데이터 행 그리기
                # row_height_2 = self.liabilities_tableWidget.rowHeight(row3)  # 데이터 행의 높이를 가져옴
                for col3 in range(self.liabilities_tableWidget.columnCount()):  # 데이터 열 그리기
                    # col_width3 = self.liabilities_tableWidget.columnWidth(col3)  # 각 열의 너비를 가져옴
                    painter.drawRect(x2, y2, col_widths3[col3] + 10, header_height_2)
                    item3 = self.liabilities_tableWidget.item(row3, col3)
                    if item3 and item3.text():
                        cell_text = item3.text()
                        if col3 == 0 :  # col2가 아닌 col3를 사용해야 함
                            if cell_text == '분기 합계':
                                text_rect3 = QRect(x, y, col_widths3[col3], header_height_2)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            else:
                                # 좌측 맞춤
                                text_rect3 = QRect(x2 + 5, y2, col_widths3[col3], header_height_2)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                            
                            # painter.drawText(text_rect3, Qt.AlignLeft | Qt.AlignVCenter, item3.text())
                        else:
                            # 우측 맞춤 및 우측에서 5픽셀 띄우기
                            text_rect3 = QRect(x2, y2, col_widths3[col3] - 5, header_height_2)
                            align = Qt.AlignRight | Qt.AlignVCenter
                            # painter.drawText(text_rect3, Qt.AlignRight | Qt.AlignVCenter, item3.text())
                        painter.drawText(text_rect3, align, cell_text)
                    
                    x2 += col_widths3[col3] + 10
                
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
            if font_size <= 1:  # 최소 폰트 크기 제한
                break
            font.setPointSize(font_size - 1) # QFont 객체의 글꼴 크기를 한 포인트 줄이는 코드
            painter.setFont(font)
            font_metrics = QFontMetrics(font)

    def special_Q_excel_save(self):  # 홈버튼

        r1_count = self.asset_tableWidget.rowCount()
        c1_count = self.asset_tableWidget.columnCount()
        r2_count = self.liabilities_tableWidget.rowCount()
        c2_count = self.liabilities_tableWidget.columnCount()
        
        income_columnHeaders = []
        balance_columnHeaders = []
        
        # 수입부분
        # create column header list
        # 열 헤더 가져오기
        income_columnHeaders = []

        for j1 in range(c1_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.asset_tableWidget.horizontalHeaderItem(j1)
            if dat1:
                income_columnHeaders.append(
                    self.asset_tableWidget.horizontalHeaderItem(j1).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                income_columnHeaders.append('Null')

        # 데이터프레임 생성
        df1 = pd.DataFrame(columns = income_columnHeaders)
        # 수입내역 테이블 데이터로 데이터프레임 채우기
        for row1 in range(r1_count): #self.tbl_result.rowCount()):
            for col1 in range(c1_count): #self.tbl_result.columnCount()):
                try:
                    df1.at[row1, income_columnHeaders[col1]] = self.asset_tableWidget.item(row1, col1).text()
                except:
                    continue

        # 요약부분
        # 열 헤더 가져오기
        balance_columnHeaders = []

        for j2 in range(c2_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.liabilities_tableWidget.horizontalHeaderItem(j2)
            if dat1:
                balance_columnHeaders.append(
                    self.liabilities_tableWidget.horizontalHeaderItem(j2).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                balance_columnHeaders.append('Null')

        # 데이터프레임 생성
        df2 = pd.DataFrame(columns = balance_columnHeaders)
        # 수입내역 테이블 데이터로 데이터프레임 채우기
        for row2 in range(r2_count): #self.tbl_result.rowCount()):
            for col2 in range(c2_count): #self.tbl_result.columnCount()):
                try:
                    df2.at[row2, balance_columnHeaders[col2]] = self.liabilities_tableWidget.item(row2, col2).text()
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
        self.close()
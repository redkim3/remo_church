import os, subprocess
from PyQt5.QtWidgets import QDialog, QWidget, QTableWidgetItem,QHeaderView, QMessageBox,QHBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QTableWidget, QPushButton, QVBoxLayout
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QDate,Qt, QRect, QSize
import pandas as pd

today = QDate.currentDate()
saved_file = r'./excel_view/선교회계_분기_재정보고.xlsx'
cur_fold = os.getcwd()
form_secondclass = uic.loadUiType("./ui/Q_mission_report.ui")[0]

class Mi_quarterly_Report(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(Mi_quarterly_Report,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("선교회계 분기 재정보고")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        bogoyear = today.year()
        self.bogo_year_widget.setText(str(bogoyear))
        self.bogo_year_widget.setFocus()
        self.Q_view_Button.clicked.connect(self.Quarterly_mission_view)
        self.Q_excel_save_Button.clicked.connect(self.Quarterly_mission_excel_save)
        self.Q_close_Button.clicked.connect(self.Quarterly_mission_close)
         
    def Quarterly_mission_view(self):
        from basic.hun_report_split import past_mission_income, past_mission_cost   # 예산의 내용과 지출비용의 실적 bungi_M_income,
        from basic.hun_report_split import bungi_M_cost, bungi_M_income
        from basic.hun_report_split import bungi_sun_cost, bungi_sun_income
        self.mission_tableWidget.clearContents()
        self.mission_tableWidget.setColumnCount(4)
        bogo_year = int(self.bogo_year_widget.text())
        try:
            bun = int(self.Quarter_widget.text()) # 보고 분기
        except ValueError:
            QMessageBox.about(self,'입력오류',"'분기를 입력해 주세요.!!!")
            self.Quarter_widget.setFocus()
            return
        # self.mission_tableWidget.setColumnCount(4)
        self.mission_tableWidget.setRowCount(9)
        past_M_income = int(past_mission_income(bogo_year))  # 전년도 까지의 선교헌금총액
        past_M_cost = int(past_mission_cost(bogo_year)) # 전년도 까지의 선교지출 총액

        cost_total = 0; row = 0; cost_row = 0; bun_total = 0; bun_sum = 0
        if self.Quarter_widget.text() != '':  # 당분기 이전까지의 내용 즉 전기이월
            Pre_bun_income = bungi_M_income(bogo_year,bun) # 당분기 선교헌금
            Pre_bun_cost = bungi_M_cost(bogo_year,bun)  # 당분기 선교지출
            passed_amount = (past_M_income + Pre_bun_income) - (past_M_cost + Pre_bun_cost)
            bun_sum += passed_amount  # 잔액
            # last_amo  = int(past_M_income-past_M_cost)
            last_a = format(passed_amount,",")
            self.mission_tableWidget.setItem(0,0,QTableWidgetItem('전기이월'))
            self.mission_tableWidget.setItem(0,1,QTableWidgetItem(last_a))
            if self.mission_tableWidget.item(0,1) != None:
                self.mission_tableWidget.item(0,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            
            M_income = bungi_sun_income(bogo_year,bun)
            
            for bun_hun in M_income:
                Mon, hun, amount = bun_hun
                hun_name = str(Mon)+"월"+" "+hun
                amo = amount
                bun_total += amount
                bun_sum += amount
                row += 1
                amo_T = format(amo,",")
                # self.mission_tableWidget.insertRow(row)
                self.mission_tableWidget.setItem(row,0,QTableWidgetItem(hun_name))
                self.mission_tableWidget.setItem(row,1,QTableWidgetItem(amo_T))
                if self.mission_tableWidget.item(row,1) != None:
                    self.mission_tableWidget.item(row,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                amo = 0
                        
            row += 1
            bun_total_T = format(bun_total,",")
            self.mission_tableWidget.setItem(7,0,QTableWidgetItem("분기수입계"))
            self.mission_tableWidget.setItem(7,1,QTableWidgetItem(bun_total_T))
            if self.mission_tableWidget.item(7,1) != None:
                self.mission_tableWidget.item(7,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            row += 1
            bun_sum_T = format(bun_sum,",")
            # self.mission_tableWidget.insertRow(row)
            self.mission_tableWidget.setItem(8,0,QTableWidgetItem("누적합계"))
            self.mission_tableWidget.setItem(8,1,QTableWidgetItem(bun_sum_T))
            if self.mission_tableWidget.item(8,1) != None:
                self.mission_tableWidget.item(8,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            
            bun_suncost = bungi_sun_cost(bogo_year,bun)
            for sun_cost in bun_suncost:
                name, c_amount = sun_cost
                if c_amount != 0:
                    cost_name = name
                    cost_amo = c_amount
                    cost_total += c_amount
                    # cost_sum += c_amount
                    cost_row += 1
                    c_amo_T = format(cost_amo,",")
                    # self.mission_tableWidget.insertRow(row)
                    self.mission_tableWidget.setItem(cost_row,2,QTableWidgetItem(cost_name))
                    self.mission_tableWidget.setItem(cost_row,3,QTableWidgetItem(c_amo_T))
                    if self.mission_tableWidget.item(cost_row,3) != None:
                        self.mission_tableWidget.item(cost_row,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    cost_amo = 0
                        
            cost_row += 1
            cost_total_T = format(cost_total,",")
            self.mission_tableWidget.setItem(7,2,QTableWidgetItem("분기합계"))
            self.mission_tableWidget.setItem(7,3,QTableWidgetItem(cost_total_T))
            if self.mission_tableWidget.item(7,3) != None:
                self.mission_tableWidget.item(7,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            # cost_row += 1
            next_amount = bun_sum - cost_total
            next_amo_T = format(next_amount,",")
            # self.mission_tableWidget.insertRow(row)
            self.mission_tableWidget.setItem(8,2,QTableWidgetItem("차기이월"))
            self.mission_tableWidget.setItem(8,3,QTableWidgetItem(next_amo_T))
            self.next_amount_label.setText(next_amo_T)
            if self.mission_tableWidget.item(8,3) != None:
                self.mission_tableWidget.item(8,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.mission_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #ResizeToContents)
            # cost_total = 0 ; cost_sum = 0
            bun_total = 0 ; bun_sum = 0; cost_total = 0
    
    def print_button_click(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.bogo_year_widget.text()
            year_text = self.year_label.text()
            quarter_text = self.Quarter_widget.text()
            title_text = self.Mission_title_label.text()
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)

            x_margin = 50; y_margin = 100
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
            current_x += painter.fontMetrics().height() + 20 # title_width + 10  # 10은 라벨 간 간격
            painter.setFont(font1)

            # 페이지 크기 계산
            page_rect = printer.pageRect()
            available_width = page_rect.width() - 2 * x_margin
            available_height = page_rect.height() - current_y - y_margin
            
            # 초기 좌표 설정
            x = x_margin
            y = current_y + 25
            
            # 각 행과 열의 높이와 너비 계산
            row_height = 40  # 기본 행 높이
            painter.setFont(font2)
            col_widths = [self.mission_tableWidget.columnWidth(col) for col in range(self.mission_tableWidget.columnCount())]
            
            # 테이블 헤더 출력
            col_count = self.mission_tableWidget.columnCount()
            row_count = self.mission_tableWidget.rowCount()
            for col in range(col_count):
                painter.drawText(x, y, col_widths[col], row_height, Qt.AlignCenter, self.mission_tableWidget.horizontalHeaderItem(col).text())
                painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                x += col_widths[col]
                
            y += row_height
            # x = x_margin
            
            # 테이블 내용 출력
            for row in range(self.mission_tableWidget.rowCount()):
                if y + row_height > available_height + y_margin:  # available_height를 사용하여 페이지 높이 제한
                    printer.newPage()
                    y = y_margin + 50  # 새로운 페이지에서 y 좌표 초기화, 제목 아래 간격 추가

                x = x_margin
                for col in range(self.mission_tableWidget.columnCount()):
                    painter.drawRect(x, y, col_widths[col], row_height)
                    # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    item = self.mission_tableWidget.item(row, col)
                    if item and item.text():
                        if col == 1 or col == 3:
                            # 우측 맞춤 및 우측에서 2픽셀 띄우기
                            text_rect = QRect(x, y, col_widths[col] - 20, row_height)
                            painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, item.text())
                        else:
                            # 중앙 맞춤
                            text_rect = QRect(x + 10, y, col_widths[col], row_height)
                            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, item.text())
                        # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                        x += col_widths[col]
                    else:
                        x += col_widths[col]
                        
                y += row_height

            painter.end()

    def Quarterly_mission_excel_save(self): 

        r1_count = self.mission_tableWidget.rowCount()
        c1_count = self.mission_tableWidget.columnCount()
        # bun_cost_imsi = []; row_append_data = []
       
        cost_columnHeaders = []

        for j1 in range(c1_count):  #self.tbl_result.model().columnCount()):
            dat1 = self.mission_tableWidget.horizontalHeaderItem(j1)
            if dat1:
                cost_columnHeaders.append(dat1.text())
                    #self.mission_tableWidget.horizontalHeaderItem(j1).text())     #tbl_result.horizontalHeaderItem(j).text())
            else:
                cost_columnHeaders.append('')
        df1 = pd.DataFrame(columns = cost_columnHeaders)

        # create dataframe object recordset
        for row1 in range(r1_count): #self.tbl_result.rowCount()):
            for col1 in range(c1_count): #self.tbl_result.columnCount()):
                try:
                    df1.at[row1, cost_columnHeaders[col1]] = self.mission_tableWidget.item(row1, col1).text()
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

            QMessageBox.about(self,'저장',"'선교회계_분기_재정보고.xlsx'파일에 저장되었습니다.!!!")
            subprocess.Popen(["start", "excel.exe", os.path.abspath(saved_file)], shell=True)

        except OSError : #(errno() , strerror[filename[, winerror[,filename2]]]):
            QMessageBox.about(self,'파일열기 에러',"'선교회계_분기_재정보고'파일이 열려 있습니다. 파일을 닫고 다시 진행해 주세요. !!!")
    

    def Quarterly_mission_close(self):
        self.close()
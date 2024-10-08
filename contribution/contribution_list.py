import os
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic # QtCore, QtGui, QtWidgets, 
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPainter

# from datetime import datetime

today = QDate.currentDate()
cur_fold = os.getcwd()

form_class = uic.loadUiType(os.path.join(cur_fold, "ui","contribution_list_form.ui"))[0]

class contributionListView(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.setWindowTitle('기부금영수증 발급 현황')
        issue_year = str(today.year())
        target_year = str(today.year()-1)
        self.issue_year_widget.setText(issue_year)
        self.target_year_widget.setText(target_year)
        self.target_year_widget.setFocus()
        self.target_year_widget.editingFinished.connect(self.serch_view)
        
    def button_collect(self):
        serch_Button = QPushButton("보기")
        serch_Button.clicked.connect(self.serch_view)

        end_close_Button = QPushButton("종료")
        end_close_Button.clicked.connect(self.end_close)

    def serch_view(self):
        from basic.contribution_issue import issued_list_serch
        global serch_year
        # try:
        self.cont_view_tableWidget.clearContents()
        self.issued_amount_widget.clear()
        self.re_issue_count_widget.clear()
        if self.issue_year_widget.text() != "":
            issued_year = int(self.issue_year_widget.text())
            target_year_s = self.target_year_widget.text()
            if target_year_s == "":
                target_year = "모두"
            else:
                target_year = int(target_year_s)
                
            cont_view = issued_list_serch(issued_year,target_year)

            set_row = len(cont_view)
            self.cont_view_tableWidget.setRowCount(set_row)
            cnt1 = 0; cnt2 = 0; hap_total = 0
            for j in range(set_row):  # j는 행 c는 열
                dat = cont_view[j][0]     # 날짜
                vdate = dat.strftime('%Y-%m-%d') #날짜
                sign = str(cont_view[j][1])  #발급기호
                tar_year = str(cont_view[j][2]) #대상년도
                targ_year = tar_year + "년도"
                s_name = str(cont_view[j][3])  # 신청자
                hap_code = str(cont_view[j][4]) # 신청자코드번호
                amo_int = int(cont_view[j][5]) #확인금액
                amo = format(amo_int,",")           #확인금액
                iss_detail = str(cont_view[j][6]) # 발행구분
                if iss_detail == "재발행":
                    cnt2 += 1
                else:
                    hap_total += amo_int
                    cnt1 += 1
                
                self.cont_view_tableWidget.setItem(j,0,QTableWidgetItem(vdate))
                self.cont_view_tableWidget.setItem(j,1,QTableWidgetItem(sign))
                self.cont_view_tableWidget.setItem(j,2,QTableWidgetItem(targ_year))
                self.cont_view_tableWidget.setItem(j,3,QTableWidgetItem(s_name))
                self.cont_view_tableWidget.setItem(j,4,QTableWidgetItem(hap_code))
                self.cont_view_tableWidget.setItem(j,5,QTableWidgetItem(amo))
                self.cont_view_tableWidget.setItem(j,6,QTableWidgetItem(iss_detail))
                self.cont_view_tableWidget.resizeColumnsToContents()
                self.cont_view_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.cont_view_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.cont_view_tableWidget.item(j,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.cont_view_tableWidget.item(j,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.cont_view_tableWidget.item(j,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.cont_view_tableWidget.item(j,5).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.cont_view_tableWidget.item(j,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)

            # 각 열의 폭에 20 픽셀씩 추가
            for col in range(self.cont_view_tableWidget.columnCount()):
                self.cont_view_tableWidget.setColumnWidth(col, self.cont_view_tableWidget.columnWidth(col) + 20)
            hap_total = format(hap_total,",")
            self.issued_amount_widget.setText(hap_total)
            self.first_issue_count_widget.setText(str(cnt1))
            self.re_issue_count_widget.setText(str(cnt2))
        else:
            QMessageBox.about(self,'자료없음','기부금증명서 발급년도를 입력해 주세요.!!!')    
        
        
        # except ValueError:
        #     QMessageBox.about(self,'자료없음','에러확인 요망.!!!')

    def contribution_list_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.issue_year_widget.text()
            year_text = year_int + '년도 발행'
            target_year = self.target_year_widget.text()
            t_year_text = target_year + '년도 기부금영수증 발급 현황'
            amount_text = self.issued_amount_widget.text()
            issued_num = self.first_issue_count_widget.text()
            issued_num_text = '발행 금액 합계   ' + amount_text +'  원 ('+ issued_num + ' 건 )'
            re_issue_num = self.re_issue_count_widget.text()
            re_issue_num_text = '재발행 ' + re_issue_num + '  건  제외'
                        
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(18)
            font2.setPointSize(12)
            # font = painter.font()
            x_margin = 50; y_margin = 100
            current_x = x_margin
            current_y = y_margin
            if year_int != '' and target_year != '':
                # year_text 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, year_text)
                year_int_width = painter.fontMetrics().width(year_text)
                current_x += year_int_width + 10

                # target_year 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, t_year_text)
                hang_width = painter.fontMetrics().width(t_year_text)
                current_x += hang_width + 10

                x2 = x_margin
                y2 = current_y + 60

                # issued_amount 출력
                painter.setFont(font2)
                painter.drawText(x2, y2, issued_num_text)
                issued_width = painter.fontMetrics().width(issued_num_text)
                x2 += issued_width + 30

                # re_issued_num 출력
                painter.setFont(font2)
                painter.drawText(x2, y2, re_issue_num_text)
                issued_width = painter.fontMetrics().width(re_issue_num_text)
                

                # 페이지 크기 계산
                page_rect = printer.pageRect()
                table_width = page_rect.width() - 2 * x_margin  # 페이지의 너비에서 좌우 여백을 뺀 나머지
                column_count = self.cont_view_tableWidget.columnCount()

                # 각 열의 비율을 계산
                col_widths = [self.cont_view_tableWidget.columnWidth(col) for col in range(column_count)]
                total_width = sum(col_widths)
                col_width_ratios = [width / total_width for width in col_widths]
                col_widths = [int(ratio * table_width) for ratio in col_width_ratios]

                # 초기 좌표 설정
                x = x_margin
                y = current_y + 80
                
                # 각 행과 열의 높이와 너비 계산
                row_height = 35  # 기본 행 높이
                painter.setFont(font2)
                col_widths = [self.cont_view_tableWidget.columnWidth(col) for col in range(self.cont_view_tableWidget.columnCount())]
                
                # 테이블 헤더 출력
                for col in range(self.cont_view_tableWidget.columnCount()):
                    painter.drawText(x, y, col_widths[col], row_height, Qt.AlignCenter | Qt.AlignVCenter, self.cont_view_tableWidget.horizontalHeaderItem(col).text())
                    painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                    x += col_widths[col]
                y += row_height
                x = x_margin
                
                # 테이블 내용 출력
                for row in range(self.cont_view_tableWidget.rowCount()):
                    if y + row_height > page_rect.bottom() - y_margin:
                        printer.newPage()
                        y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                    x = x_margin
                    for col in range(column_count):
                        painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                        item = self.cont_view_tableWidget.item(row, col)
                        if item and item.text():
                            text_rect = QRect(x, y, col_widths[col], row_height)
                            if col == 5:
                                # 좌측 맞춤 및 우측에서 여백(10) 띄우기
                                painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, item.text())
                            else:
                                # 중앙 맞춤
                                painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, item.text())

                        x += col_widths[col]
                    y += row_height

                painter.end()
            else:
                QMessageBox.about(self,'내용없음','출력할 사항이 없습니다.')
        # printer = QPrinter(QPrinter.HighResolution)
        # painter = QPainter()
        # if painter.begin(printer):
        #     self.serch_view(printer, painter, self.cont_view_tableWidget, x_margin=20, y_margin=20, font_size=12)
        #     painter.end()

    def end_close(self):
        # self.cont_view_tableWidget.clearContents()
        self.cont_view_tableWidget.setRowCount(0) # clear()
        self.issued_amount_widget.clear()
        self.re_issue_count_widget.clear()
        self.issue_year_widget.clear()
        hap_total = 0
        self.close()



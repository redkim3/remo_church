import pymysql, os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic, QtWidgets # QtCore, QtGui 
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPainter, QFontMetrics
from basic.cost_select import *
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()

from basic.cost_select import cost_hang_values, cost_mok_values, cost_semok_values

form_class = uic.loadUiType(r"./ui/other_income_view.ui")[0]

class Other_income_View(QtWidgets.QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("기타소득 보기")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.load_year_combo()
        self.result_tableWidget.itemChanged.connect(self.on_item_changed)
        self.result_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정

    def load_year_combo(self):
        today = QDate.currentDate()
        view_year = str(today.year())
        combo_year = ["선택"]
        for y in range(1, 6):
            combo_year.append(str(int(view_year) + 1 - y))
        self.year_combo_widget.addItems(combo_year)
        self.year_combo_widget.currentTextChanged.connect(self.gubun_combo)
        self.year_combo_widget.currentTextChanged.connect(self.reset)
        self.reset()
    
    def gubun_combo(self):
        from basic.hun_name_2 import gubun_values
        self.gubun_combo_widget.clear()  # 회계구분 명칭(선교회계,일반회계,특별회계)
        gubun = gubun_values()
        self.gubun_combo_widget.addItems(['선택'] + gubun)
    
    def on_item_changed(self, item):  # 테이블의 숫자값이 변경되고 ' , '  넣어주기
        col = item.column()
        if col == 2:  # 8번째 열
            try:
                value = int(item.text().replace(",", ""))
                item.setText(f"{value:,}")  # 숫자를 쉼표로 포맷팅
            except ValueError:
                QMessageBox.about(None,'입력오류',"올바르지 않은 숫자입니다.")

    def reset(self):
        self.hap_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)

    def serch_close(self):
        self.reset()
        self.close()
    
    def closeEvent(self, event):
        self.reset()
        event.accept()

    def serch_account(self):
        from basic.hun_serch import other_income_view_sql
        hap_total = 0
        self.result_tableWidget.clear()
        serch_year = self.year_combo_widget.currentText()
        gubun = self.gubun_combo_widget.currentText()

        serch_other_income_list = other_income_view_sql(serch_year,gubun)
        self.result_tableWidget.setColumnCount(5)

        self.result_tableWidget.setRowCount(len(serch_other_income_list))
        self.result_tableWidget.setHorizontalHeaderLabels(["일자", "항목", "금액", "비고","id"])
        for j, other_data in enumerate(serch_other_income_list):
            vdate = other_data[0].strftime('%Y-%m-%d')
            hun_mok = other_data[1]
            amo_int_1 = int(other_data[2])
            hap_total += amo_int_1
            amo_1 = format(amo_int_1, ",")
            other_marks = other_data[3]
            if len(other_data) > 4:
                id = str(other_data[4])
            self.result_tableWidget.setItem(j, 0, QTableWidgetItem(vdate))
            self.result_tableWidget.setItem(j, 1, QTableWidgetItem(hun_mok))
            self.result_tableWidget.setItem(j, 2, QTableWidgetItem(amo_1))
            self.result_tableWidget.setItem(j, 3, QTableWidgetItem(other_marks))
            self.result_tableWidget.setItem(j, 4, QTableWidgetItem(id))
            self.result_tableWidget.item(j,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.item(j,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.result_tableWidget.item(j,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.result_tableWidget.item(j,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.result_tableWidget.item(j,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.result_tableWidget.resizeColumnsToContents()
        self.result_tableWidget.setColumnHidden(4, True)
        
        hap_total = format(hap_total, ",")
        self.hap_widget.setText(hap_total)
        
    def edit_other_income(self): #cell_changed
        from modify.other_modify_reg import Other_modify_Register
        from modify.special_balance_modi_reg import Special_modify_register
        gubun = self.gubun_combo_widget.currentText()
        serch_year = int(self.year_combo_widget.currentText())
        v_year = today.year()
        sel_row = self.result_tableWidget.currentRow()
        if v_year == serch_year:
            if sel_row >= 0:
                id_row = 4
                id = self.result_tableWidget.item(sel_row, id_row).text()
            else:
                QMessageBox.information(None, "완료","선택한 행이 없습니다.")
                return
            if gubun != '특별회계':
                self.other_modify_register = Other_modify_Register(str(id))
                self.other_modify_register.exec()
                self.show()
                self.serch_account()
            else:
                self.other_sp_modify_register = Special_modify_register(str(id))
                self.other_sp_modify_register.exec()
                self.show()
                self.serch_account()

        else:
            QMessageBox.information(None, "완료", "금년의 지출내역만 수정할 수 있습니다.")

    def other_income_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정 
            year_int = self.year_combo_widget.currentText()
            year_text = year_int + '년도'
            main_title = self.title_label.text()
            main_title_text = year_text +' ' + main_title
            amount_text = '합계금액  '+ self.hap_widget.text()

            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)
            # font = painter.font()
            x_margin = 40; y_margin = 70
            current_x = x_margin
            current_y = y_margin

            if year_int != '선택':
                # year_text 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, main_title_text)
                year_int_width = painter.fontMetrics().width(main_title_text)
                
                current_y += 60

                # issued_amount 출력
                painter.setFont(font2)
                painter.drawText(current_x, current_y, amount_text)
                issued_width = painter.fontMetrics().width(amount_text)
                # x2 += issued_width + 30

                # 페이지 크기 계산
                page_rect = printer.pageRect()
                available_width = page_rect.width() - 2 * x_margin
                available_height = page_rect.height() - current_y - y_margin
                
                # 초기 좌표 설정
                x = x_margin
                y = current_y + 80
                
                # 각 행과 열의 높이와 너비 계산
                row_height = 35  # 기본 행 높이
                painter.setFont(font2)
                col_widths = [self.result_tableWidget.columnWidth(col) for col in range(self.result_tableWidget.columnCount())]
                
                 # 테이블 헤더 출력
                for col in range(self.result_tableWidget.columnCount()-1):
                    header_text = self.result_tableWidget.horizontalHeaderItem(col).text()
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    self.adjust_font_size(painter, header_text, col_width)
                    painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, self.cost_tableWidget.horizontalHeaderItem(col).text())
                    painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                    x += col_width

                y += row_height
                x = x_margin
                
                # 테이블 내용 출력
                for row in range(self.result_tableWidget.rowCount()):
                    if y + row_height > page_rect.bottom() - y_margin:
                        printer.newPage()
                        y = y_margin  # 새로운 페이지에서 y 좌표 초기화

                    x = x_margin

                    for col in range(self.result_tableWidget.columnCount()):
                        col_width = int(col_widths[col] * available_width / sum(col_widths))
                        painter.drawRect(x, y, col_width, row_height)
                        # painter.drawRect(x, y, col_widths[col], row_height)  # 테두리 그리기
                        item = self.result_tableWidget.item(row, col)
                        if item and item.text():
                            cell_text = item.text()
                            self.adjust_font_size(painter, cell_text, col_width)
                            if col == 0 :
                                rect = QRect(x, y, col_width, row_height)  # 좌측
                                align = Qt.AlignCenter | Qt.AlignVCenter
                            
                            elif col == 2 or col == -1 :
                                # 우측에서 여백(20) 띄우기
                                rect = QRect(x + 3, y, col_width, row_height)  # 좌측
                                align = Qt.AlignLeft | Qt.AlignVCenter
                            
                            else :
                                # 우측에서 여백(20) 띄우기
                                rect = QRect(x, y, col_width - 3, row_height)  # 좌측
                                align = Qt.AlignRight | Qt.AlignVCenter
                        
                            painter.drawText(rect, align, cell_text)
                        x += col_widths[col]
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
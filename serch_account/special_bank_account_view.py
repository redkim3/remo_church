import os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5 import uic, QtWidgets # QtCore, QtGui 
from PyQt5.QtCore import QRect
from PyQt5 import QtGui
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPainter, QFontMetrics
from basic.cost_select import *
import configparser, hashlib

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()

form_class = uic.loadUiType(r"./ui/special_bank_account_form.ui")[0]

class Special_bank_account_view(QtWidgets.QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("특별회계 은행별 검색")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))

        self.load_year_combo()
        self.load_bank_combo()
        self.bank_combo_widget.currentTextChanged.connect(self.special_bank_account_view)
        self.result_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정
        self.hang_combo_items = {}
        self.mok_combo_items = {}
        self.semok_combo_items = {}

    def load_year_combo(self):
        today = QDate.currentDate()
        view_year = str(today.year())
        combo_year = ["선택"]
        for y in range(1, 6):
            combo_year.append(str(int(view_year) + 1 - y))
        self.year_combo_widget.addItems(combo_year)
        self.year_combo_widget.currentTextChanged.connect(self.reset)
        self.reset()
    
    def load_bank_combo(self):
        from basic.special_acc_sql import select_bank
        confirm_data = self.user_confirm()
        special_check = int(confirm_data[3]) # 특별회계
        # ok = self.user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
        self.bank_combo_widget.clear()
        self.result_tableWidget.clearContents()
        self.result_tableWidget.setRowCount(1)
        self.bank_combo_widget.addItems(["선택"] + select_bank("특별회계"))

    def special_bank_account_view(self):
        from basic.special_acc_sql import bank_account_view
        from basic.special_acc_sql import past_bank_account_value

        # 글꼴 설정
        # font = QtGui.QFont()
        # font.setPointSize(12)  # 글자 크기 설정
        # self.result_tableWidget.setFont(font)

        # 헤더 글꼴 설정
        header_font = QtGui.QFont()
        header_font.setPointSize(11) 
        self.result_tableWidget.horizontalHeader().setFont(header_font)

        self.result_tableWidget.clear()
        bank = self.bank_combo_widget.currentText()
        serch_year = self.year_combo_widget.currentText()
        
        serch_result_value = bank_account_view(serch_year, bank)
        past_account_value = past_bank_account_value(serch_year, bank)  # 기초이월

        self.result_tableWidget.setColumnCount(7)
            # self.result_tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
            # self.result_tableWidget.setColumnWidth(5, 1)
        self.result_tableWidget.setRowCount(len(serch_result_value) + 1)
        self.result_tableWidget.setItem(0, 1, QTableWidgetItem("기초이월"))
        self.result_tableWidget.setItem(0, 4, QTableWidgetItem(format(past_account_value,",")))
        if self.result_tableWidget.item(0, 4) is not None:
                self.result_tableWidget.item(0, 4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)

        self.result_tableWidget.setHorizontalHeaderLabels(["일자", "적요", "증가액","감소액", "계좌잔액", "비고","id"])
        for j, value_data in enumerate(serch_result_value):
            vdate = value_data[0].strftime('%Y-%m-%d')
            cost_memo1 = value_data[1]
            balance1 = value_data[2]
            amo = int(value_data[3])
            jan_0 = self.result_tableWidget.item(j, 4)
            if jan_0:
                jan_T = jan_0.text()
                if jan_T != "":
                    jan_float = float(jan_T.replace(",", ""))  # 소수점이 있는 문자열을 실수로 변환
                    jan = int(jan_float)  # 실수를 정수로 변환
                    # jan = int(jan_T.replace(",",""))
            else:
                jan = 0
            marks = value_data[4]
            if len(value_data) > 4:
                id = str(value_data[5])
            
            self.result_tableWidget.setItem(j+1, 0, QTableWidgetItem(vdate))
            self.result_tableWidget.setItem(j+1, 1, QTableWidgetItem(cost_memo1))
            if balance1 ==  "예금증가":
                self.result_tableWidget.setItem(j+1, 2, QTableWidgetItem(format(amo,",")))
                jan = jan + amo
            else:
                self.result_tableWidget.setItem(j+1, 3, QTableWidgetItem(format(amo,",")))
                jan = jan - amo
            self.result_tableWidget.setItem(j+1, 4, QTableWidgetItem(format(jan,",")))
            self.result_tableWidget.setItem(j+1, 5, QTableWidgetItem(marks))
            self.result_tableWidget.setItem(j+1, 6, QTableWidgetItem(id))
            self.result_tableWidget.item(j+1,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.result_tableWidget.item(j+1,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            if self.result_tableWidget.item(j+1,2) is not None:
                self.result_tableWidget.item(j+1,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            if self.result_tableWidget.item(j+1,3) is not None:
                self.result_tableWidget.item(j+1,3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            if self.result_tableWidget.item(j+1,4) is not None:
                self.result_tableWidget.item(j+1,4).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.result_tableWidget.item(j+1,5).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.result_tableWidget.item(j+1,6).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.result_tableWidget.resizeColumnsToContents()
        self.result_tableWidget.setColumnHidden(6, True)

        

    def edit_cost(self): #cell_changed
        from modify.special_balance_modi_reg import Special_modify_register
        bank = self.bank_combo_widget.currentText()
        serch_year = int(self.year_combo_widget.currentText())
        v_year = today.year()
        sel_row = self.result_tableWidget.currentRow()
        if v_year == serch_year:
            if sel_row >= 0:
                id_col = 6
                # 선택한 셀이 존재하는 경우에만 진행
                id = self.result_tableWidget.item(sel_row, id_col).text()
            else:
                QMessageBox.information(None, "완료","선택한 행이 없습니다.")
                return
            self.special_modify_register = Special_modify_register(str(id))
            self.special_modify_register.exec()
            self.show()
            self.special_bank_account_view()
        else:
            QMessageBox.information(None, "완료", "금년의 지출내역만 수정할 수 있습니다.")

    def reset(self):
        self.bank_combo_widget.setCurrentText("선택")
        self.result_tableWidget.setRowCount(0)
        self.result_tableWidget.setRowCount(1)
        # self.gubun_combobox()

    def serch_close(self):
        self.reset()
        self.close()
    
    def closeEvent(self, event):
        self.reset()
        event.accept()

    def user_confirm(self):
        from user.for_user_sql import user_infor_sql
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        user_id = config['user']['user_id']

        user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
        user_name_infor = user_info[0]         # 이름을 가져오고
        user_name_hash = self.user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
        user_name = user_name_infor[0]
        Ge_value = str(user_name_infor[1])       # user_reg_check의 권한을 가져와서
        sun_value = str(user_name_infor[2])       # user_reg_check의 권한을 가져와서
        special_value = str(user_name_infor[3])       # user_reg_check의 권한을 가져와서
        # # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
        # Ge_check = self.user_infor_hash(Ge_value)  # user_reg_check를 hash화 한다.
        # # sun_check = self.user_infor_hash(sun_value)
        config['user'][user_name] = user_name_hash # 해시화된 이름을 저장한다.
        # config['user'][Ge_check] = Ge_check
        # config['user'][sun_check] = sun_check
        
        return user_name_infor  # , sun_check

    def user_infor_hash(self,data):
        # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
        hasher = hashlib.sha256()
        # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
        hasher.update(data.encode('utf-8'))
        # 해시된 결과 반환
        return hasher.hexdigest()
    
    def serch_special_account_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            printer = dialog.printer()
            painter = QPainter(printer)

             # 각 라벨의 텍스트와 폰트 설정
            year_int = self.year_combo_widget.currentText()
            year_text = year_int + '년도'
            bank = self.bank_combo_widget.currentText()
            bank_title = bank + '예금 증감현황'
            
            font1 = painter.font()
            font2 = painter.font()
            font1.setPointSize(12)
            font2.setPointSize(10)
            # font = painter.font()
            x_margin = 25; y_margin = 80
            current_x = x_margin
            current_y = y_margin
            if year_int != '선택' and bank != '선택':
                # year_text 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, year_text)
                year_int_width = painter.fontMetrics().width(year_text)
                current_x += year_int_width + 10

                # bank 출력
                painter.setFont(font1)
                painter.drawText(current_x, current_y, bank_title)
                hang_width = painter.fontMetrics().width(bank_title)
                # current_x += hang_width + 10

                # 페이지 크기 계산
                page_rect = printer.pageRect()
                available_width = page_rect.width() - 2 * x_margin
                available_height = page_rect.height() - current_y - y_margin
                
                # 초기 좌표 설정
                x = x_margin
                y = current_y + 30
                
                # 각 행과 열의 높이와 너비 계산
                row_height = 35  # 기본 행 높이
                painter.setFont(font2)
                col_widths = [self.result_tableWidget.columnWidth(col) for col in range(self.result_tableWidget.columnCount())]
                
                # 테이블 헤더 출력 (비율 조정된 열 너비 사용)
                for col in range(self.result_tableWidget.columnCount() - 1):
                    header_text = self.result_tableWidget.horizontalHeaderItem(col).text()
                    col_width = int(col_widths[col] * available_width / sum(col_widths))
                    self.adjust_font_size(painter, header_text, col_width)
                    painter.drawText(x, y, col_width, row_height, Qt.AlignCenter | Qt.AlignVCenter, header_text)
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
                    for col in range(self.result_tableWidget.columnCount() - 1):
                        col_width = int(col_widths[col] * available_width / sum(col_widths))
                        painter.drawRect(x, y, col_width, row_height)  # 테두리 그리기
                        item = self.result_tableWidget.item(row, col)
                        if item and item.text():
                            cell_text = item.text()
                            self.adjust_font_size(painter, cell_text, col_width)

                            if col == 0:
                                 # 중앙 맞춤
                                text_rect = QRect(x, y, col_width, row_height)
                                painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, item.text())
                            elif col == 2 or col == 3 or col == 4 :
                                # 좌측 맞춤 및 우측에서 여백(10) 띄우기
                                text_rect = QRect(x, y, int(col_width*1.1) - 10, row_height)
                                painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, item.text())
                            else:
                                # 좌측 맞춤
                                text_rect = QRect(x, y, int(col_width*0.9), row_height)
                                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, item.text())
                            
                        x += col_width
                    y += row_height

                painter.end()
            else:
                QMessageBox.about(self,'내용없음','출력할 사항이 없습니다.')
    
    def adjust_font_size(self,painter, text, max_width):
        """
        텍스트가 주어진 폭에 맞도록 폰트 크기를 조정합니다.
        """
        font = painter.font()
        font_metrics = QFontMetrics(font) # QFontMetrics는 특정 측정정보를 계산하는데 쓰이는Qt 클래스중 하나
        min_font_size = 5  # 최소 폰트 크기를 설정합니다.
        while font_metrics.boundingRect(text).width() > max_width: # boundingRect는 QFontMetrics 클래스에서 제공하는 메서드 사각형으로 텍스트가 화면에 렌더링될때 차지하는 공간을 나타냄
            font_size = font.pointSize()  # 현재의 폰트 크기를 가져옴
            if font_size <= min_font_size:  # 최소 폰트 크기에 도달하면 중단if font_size <= 1:  # 최소 폰트 크기 제한
                break
            font.setPointSize(font_size - 1) # QFont 객체의 글꼴 크기를 한 포인트 줄이는 코드
            painter.setFont(font)
            font_metrics = QFontMetrics(font)
import pymysql, configparser, os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())

hun_imsi = []; n = 0

form_class = uic.loadUiType("ui/hun_semok_reg_form.ui")[0]
j = 1
class hun_semokRegister(QDialog, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.hang_comboBox_widget.clear()
        self.registed_semok_tableWidget.setRowCount(0)
        self.new_semok_tableWidget.setRowCount(0)
        self.new_semok_reg_widget.clear()
        self.setWindowTitle('헌금구분 세목 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))

        self.gubun_comboBox_select()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.hun_hang_combobox)
        self.registed_semok_tableWidget.setColumnWidth(0, 150)
        self.new_semok_tableWidget.setRowCount(1)
        self.new_semok_tableWidget.setColumnWidth(0, 150)

    def hun_semok_button(self):
        addsemok_button = QPushButton("신규등록추가")
        addsemok_button.clicked.connect(self.hunsemok_reg_input)
        semok_view_button = QPushButton("다시보기")
        semok_view_button.clicked.connect(self.registed_semok)

        semok_delete_button = QPushButton("선택 행 삭제")
        semok_delete_button.clicked.connect(self.delete_selected_row)
        
        hun_semoksave_button = QPushButton("저장")
        hun_semoksave_button.clicked.connect(self.semokfile_save)
        hun_semokcancel_button = QPushButton("종료(저장취소)")
        hun_semokcancel_button.clicked.connect(self.semokfile_save_cancel)
    
    def gubun_comboBox_select(self):
        from basic.hun_name_2 import gubun_values
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_values())
        

    def hun_hang_combobox(self):  # 구분은 기본으로 기본을 선택하면 항의 콤보박스 활성으로 아래의 대분분은 항에 관한것
        from basic.hun_name_2 import hun_hang_values
        self.hang_comboBox_widget.clear()
        basic_hang = ['선택']
        hun_hang_name_value = []
        self.hang_comboBox_widget.addItems(basic_hang)
        gubun_sel = self.gubun_comboBox_widget.currentText() 
        hun_hang = hun_hang_values(v_year,gubun_sel)
        for h_hang in hun_hang:
            hun_hang_name, id = h_hang                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            hun_hang_name_value.append(hun_hang_name)
        self.hang_comboBox_widget.addItems(hun_hang_name_value)
        self.hang_comboBox_widget.currentTextChanged.connect(self.hun_mok_combobox)

    def hun_mok_combobox(self):  # 구분은 기본으로 기본을 선택하면 항의 콤보박스 활성으로 아래의 대분분은 항에 관한것
        from basic.hun_name_2 import hun_mok_values
        self.mok_comboBox_widget.clear()
        basic_mok = ['선택']
        hun_mok_name_value = []
        self.mok_comboBox_widget.addItems(basic_mok)
        hang_sel = self.hang_comboBox_widget.currentText() 
        hun_mok = hun_mok_values(v_year,hang_sel)
        for h_mok in hun_mok:
            hun_mok_name, id = h_mok                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            hun_mok_name_value.append(hun_mok_name)
        self.mok_comboBox_widget.addItems(hun_mok_name_value)
        self.mok_comboBox_widget.currentTextChanged.connect(self.registed_semok)

    def hunsemok_reg_input(self):
        global j
        gubun = self.gubun_comboBox_widget.currentText()
        hang = self.hang_comboBox_widget.currentText()
        mok = self.mok_comboBox_widget.currentText()
        if gubun != '선택' and hang != '선택' and hang != '' and mok != '선택' and mok != '':
            semok_name = self.new_semok_reg_widget.text()  # 추가 되어야할 세목 
            if semok_name == '':
                QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
            else:
                if j != 1:
                    self.new_semok_tableWidget.insertRow(j-1)
                self.new_semok_tableWidget.setItem((j-1),0,QTableWidgetItem(semok_name))
                self.new_semok_reg_widget.clear()
                self.new_semok_reg_widget.setFocus()
                j += 1
        else:
            QMessageBox.about(self,'입력오류','선택사항을 먼저 선택하세요!!')
            self.new_semok_reg_widget.clear()

    def registed_semok(self):
        from basic.hun_name_2 import hun_semok_values
        hun_mok = self.mok_comboBox_widget.currentText()
        try:
            semok = hun_semok_values(v_year,hun_mok)
            if semok != None:
                set_row = len(semok)
            
                self.registed_semok_tableWidget.setRowCount(set_row)

                for j in range(set_row): #set_row):  # j는
                    registed_data = semok[j][0]
                    id = semok[j][1]
                    self.registed_semok_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
                    self.registed_semok_tableWidget.setItem(j,1,QTableWidgetItem(str(id)))
            self.registed_semok_tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.registed_semok_tableWidget.setColumnHidden(1, True) # 1열을 hidden 즉 숨김으로 함
            
        except pymysql.Error as e: #ValueError:
            QMessageBox.about(self, "입력오류", f"에러 발생: {e}")
            # self.registed_name.setFocus()
            return

    def delete_selected_row(self):
        from acc_menu_sql.hun_menu import hun_semok_selected_row_delete
        global j
        selected_items = self.registed_semok_tableWidget.selectedItems()
        table_name = v_year + '_' + 'hun_semok'
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_semok_tableWidget.row(selected_items[0])
            selected_data = self.registed_semok_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            hun_semok_selected_row_delete(v_year,selected_data)

            # 테이블 위젯에서 선택된 행 삭제
            self.registed_semok_tableWidget.removeRow(row_index)
            self.registed_semok()

    def hunsemok_modify(self):
        from acc_menu_sql.hun_menu import hun_semok_update_row_sql
        sel_row = None
        change_data = []
        
        sel_row = self.registed_semok_tableWidget.currentRow()
        
        # for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
        if self.registed_semok_tableWidget.item(sel_row, 0) != None:
            change_data_0 = self.registed_semok_tableWidget.item(sel_row, 0).text()
            change_data_1 = self.registed_semok_tableWidget.item(sel_row, 1).text()
        else:
            change_data = None
        change_data.append(change_data_0)
        change_data.append(change_data_1)
        
        # 데이터베이스에 연결하여 값을 업데이트
        hun_semok_update_row_sql(v_year,change_data)
        change_data = []
        QMessageBox.about(self,'저장',"헌금 세목명이 변경 되었습니다.!!!")
        self.registed_semok()

    def semok_reset(self):
        global j,hun_imsi
        hun_imsi = []
        self.gubun_comboBox_widget.setCurrentText('선택')
        self.hang_comboBox_widget.clear()
        self.mok_comboBox_widget.clear()
        self.new_semok_tableWidget.setRowCount(0) 
        self.new_semok_tableWidget.setRowCount(1)
        self.registed_semok_tableWidget.setRowCount(0) 
        self.new_semok_reg_widget.clear()
        j=1

    def semokfile_save_cancel(self):
        self.semok_reset()
        self.close()

    def closeEvent(self, event):
        self.semok_reset()
        event.accept()
    
    def semokfile_save(self):
        from acc_menu_sql.hun_menu import current_year_hun_semok_save_sql
        global j, hun_imsi
        rowCount = self.new_semok_tableWidget.rowCount()
        try:
            if self.mok_comboBox_widget.currentText() != '선택':
                for i in range(rowCount):
                    hun_mok = self.mok_comboBox_widget.currentText()
                    try:
                        hun_semok = self.new_semok_tableWidget.item(i, 0).text()
                        hun_imsi.append([hun_mok,hun_semok])
                    except AttributeError as e: # pymysql.Error as e:
                        QMessageBox.critical(self, '에러', f'데이터 저장 중 오류 발생: {e}')
                        
                        self.new_semok_tableWidget.setRowCount(0)
                        self.new_semok_tableWidget.setRowCount(1)
                        self.new_semok_reg_widget.setFocus()
                        return
                    except : 
                        QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")
                        self.new_semok_reg_widget.setFocus()
                        return

                current_year_hun_semok_save_sql(v_year,hun_imsi)
                self.new_semok_tableWidget.setRowCount(0)
                j = 1
                self.new_semok_tableWidget.setRowCount(j)
                hun_semok = []
                self.new_semok_reg_widget.setFocus()

            else:        
                QMessageBox.about(self,'',"회계 구분을 먼저 선택하시고 신규 항을 입력 하세요.!!!")
        except pymysql.Error as error: #.ProgrammingError:
                if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
                    QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
                else:
                    QMessageBox.critical(self, '에러', f'데이터 저장 중 오류 발생: {e}')
        self.registed_semok()
        self.new_semok_tableWidget.setRowCount(0)
        self.new_semok_tableWidget.setRowCount(j)
        self.new_semok_reg_widget.setFocus()

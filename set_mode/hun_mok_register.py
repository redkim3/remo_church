import pymysql, os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())
hun_imsi = []; n = 0

form_class = uic.loadUiType("ui/hun_mok_reg_form.ui")[0]
j = 1
class hun_mokRegister(QDialog, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
    
        self.setWindowTitle('헌금구분 목 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.gubun_comboBox_widget.clear()
        self.hang_comboBox_widget.clear()
        self.new_hun_mok_reg_widget.clear()
        self.new_mok_tableWidget.clearContents()
        self.new_mok_tableWidget.setRowCount(0)
        self.gubun_comboBox_select()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.hun_hang_combobox)
        self.registed_mok_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        self.new_mok_tableWidget.setRowCount(j)
        self.new_mok_tableWidget.setColumnWidth(0, 125)
        self.new_hun_mok_reg_widget.text()
    
    def hun_mok_button(self):
        addmok_button = QPushButton("신규등록추가")
        addmok_button.clicked.connect(self.hunmok_reg_input)
        mok_view_button = QPushButton("다시보기")
        mok_view_button.clicked.connect(self.registed_mok)
        mok_delete_button = QPushButton("선택 행 삭제")
        mok_delete_button.clicked.connect(self.delete_selected_row)

        hun_moksave_button = QPushButton("저장")
        hun_moksave_button.clicked.connect(self.mokfile_save)
        hun_mokcancel_button = QPushButton("종료(저장취소)")
        hun_mokcancel_button.clicked.connect(self.mokfile_save_cancel)
    
    def gubun_comboBox_select(self):
        from basic.hun_name_2 import gubun_values
        self.gubun_comboBox_widget.addItems(['선택'] +gubun_values())

    def registed_mok(self):
        from basic.hun_name_2 import hun_mok_values
        hun_hang = self.hang_comboBox_widget.currentText()
        mok = hun_mok_values(v_year,hun_hang)
        if mok != None:
            set_row = len(mok)
            self.registed_mok_tableWidget.setRowCount(set_row)

            for j in range(set_row): #set_row):  # j는
                registed_data = mok[j][0]
                id = mok[j][1]
                self.registed_mok_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
                self.registed_mok_tableWidget.setItem(j,1,QTableWidgetItem(str(id)))
        self.registed_mok_tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.registed_mok_tableWidget.setColumnHidden(1, True) # 1은 두번째, 0 은 열의 폭을 나타냄

    def hun_hang_combobox(self):
        from basic.hun_name_2 import hun_hang_values
        self.hang_comboBox_widget.clear()
        basic_hang = ['선택']
        hun_hang_name_value = []
        self.hang_comboBox_widget.addItems(basic_hang)
        hang_sel = self.gubun_comboBox_widget.currentText()
        hun_hang = hun_hang_values(v_year,hang_sel)
        for h_hang in hun_hang:
            hun_hang_name, id = h_hang                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            hun_hang_name_value.append(hun_hang_name)
        self.hang_comboBox_widget.addItems(hun_hang_name_value) # 구분아래의 항을 찾기위해 항벨류를 찾는다
        self.hang_comboBox_widget.currentTextChanged.connect(self.registed_mok)

    def hunmok_reg_input(self):
        global j
        hang = self.hang_comboBox_widget.currentText()
        if hang != '선택' and hang != '':
            mok_name = self.new_hun_mok_reg_widget.text()  # 구분
            if mok_name =='':
                QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
            
            else:
                if j != 1:
                    self.new_mok_tableWidget.insertRow(j-1)
                
                self.new_mok_tableWidget.setItem((j-1),0,QTableWidgetItem(mok_name))
                self.new_hun_mok_reg_widget.clear() 
                self.new_hun_mok_reg_widget.setFocus()
                j += 1
        else:
            QMessageBox.about(self,'입력오류','선택사항을 먼저 선택하세요!!')
            self.new_hun_mok_reg_widget.clear()

    def mok_registe_reset(self):
        global j, hun_imsi
        hun_imsi = []
        self.gubun_comboBox_widget.setCurrentText('선택')
        self.hang_comboBox_widget.clear()
        self.registed_mok_tableWidget.setRowCount(0)  # 신규 회계단위 헌금 구분 입력사항 삭제
        self.registed_mok_tableWidget.setRowCount(1)
        self.new_mok_tableWidget.setRowCount(0)
        self.new_mok_tableWidget.setRowCount(1)
        j = 1
    
    def mokfile_save_cancel(self):
        self.mok_registe_reset()
        self.close()

    def closeEvent(self, event):
        self.mok_registe_reset()
        event.accept()

    def delete_selected_row(self):
        from acc_menu_sql.hun_menu import hun_mok_selected_row_delete
        global j
        selected_items = self.registed_mok_tableWidget.selectedItems()
        
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_mok_tableWidget.row(selected_items[0])
            selected_data = self.registed_mok_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            hun_mok_selected_row_delete(v_year,selected_data)
            # 테이블 위젯에서 선택된 행 삭제
            self.registed_mok_tableWidget.removeRow(row_index)
        self.registed_mok()

    def hunmok_modify(self):
        from acc_menu_sql.hun_menu import hun_mok_update_row_sql
        sel_row = None
        change_data = []

        sel_row = self.registed_mok_tableWidget.currentRow()
        # c_count = self.registed_costmok_tableWidget.columnCount()
        # for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
        if self.registed_mok_tableWidget.item(sel_row, 0) != None:
            change_data_0 = self.registed_mok_tableWidget.item(sel_row, 0).text()
            change_data_1 = self.registed_mok_tableWidget.item(sel_row, 1).text()
        else:
            change_data = None
        change_data.append(change_data_0)
        change_data.append(change_data_1)

        # 데이터베이스에 연결하여 값을 업데이트
        hun_mok_update_row_sql(v_year,change_data)
        change_data = []
        QMessageBox.about(self,'저장',"헌금 목 이 변경 되었습니다.!!!")
        self.registed_mok()
                
    def mokfile_save(self):
        from acc_menu_sql.hun_menu import current_year_hun_mok_save_sql
        global j,hun_imsi
        rowCount = self.new_mok_tableWidget.rowCount()
        if self.hang_comboBox_widget.currentText() != '선택':
            for i in range(rowCount):
                gubun = self.gubun_comboBox_widget.currentText()
                hang = self.hang_comboBox_widget.currentText()
                try:
                    mok = self.new_mok_tableWidget.item(i, 0).text()
                    hun_imsi.append([gubun,hang,mok])
                except AttributeError as e: # pymysql.Error as e:
                    QMessageBox.critical(self, '에러', f'데이터 저장 중 오류 발생: {e}')
                    self.new_mok_tableWidget.setRowCount(0)
                    self.new_mok_tableWidget.setRowCount(1)
                    self.new_hun_mok_reg_widget.setFocus()
                    return
            
                except : 
                    QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")
                    self.new_hun_mok_reg_widget.setFocus()
                    return
            current_year_hun_mok_save_sql(v_year,hun_imsi)
            self.new_mok_tableWidget.setRowCount(0)
            self.new_mok_tableWidget.setRowCount(j)
            j = 1
            hun_imsi = []
            self.new_hun_mok_reg_widget.setFocus()

        else:
            QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")
       
        self.new_mok_tableWidget.setRowCount(0)
        self.new_mok_tableWidget.setRowCount(j)
        self.new_hun_mok_reg_widget.setFocus()
        self.registed_mok()

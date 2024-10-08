from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
import pymysql, configparser, os

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())
n = 0

form_class = uic.loadUiType("ui/cost_semok_reg_form.ui")[0]
j = 1
class cost_semokRegister(QDialog, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('지출구분 세목 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.gubun_comboBox_widget.setEnabled(True)
        self.gubun_combo_select()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.costhang_combobox)
        self.costhang_comboBox_widget.currentTextChanged.connect(self.costmok_combobox)
        self.costmok_comboBox_widget.currentTextChanged.connect(self.registed_costsemok)
        self.new_costsemok_widget.editingFinished.connect(self.costsemok_reg_input)
        self.registed_costsemok_tableWidget.setColumnWidth(0, 150)
        self.new_costsemok_tableWidget.setColumnWidth(0, 150)
        self.new_costsemok_tableWidget.setRowCount(1)
    
    def gubun_combo_select(self):
        from basic.hun_name_2 import gubun_values
        gubun_sel = gubun_values()
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_sel)

    def add_co_se_button(self):
        add_costsemok_button = QPushButton("신규등록추가")
        add_costsemok_button.clicked.connect(self.costsemok_reg_input)
        
        costsemok_save = QPushButton("저장")
        costsemok_save.clicked.connect(self.costsemok_save)

        costsemok_save_cancel = QPushButton("종료(저장취소)")
        costsemok_save_cancel.clicked.connect(self.costsemok_save_cancel)

        costsemok_modify = QPushButton("선택행 수정")
        costsemok_modify.clicked.connect(self.costsemok_modify)

    def registed_costsemok(self):
        from basic.cost_select import cost_semok_values
        mok = self.costmok_comboBox_widget.currentText()
        semok = cost_semok_values(v_year,mok)
        if semok != None:
            set_row = len(semok)
            self.registed_costsemok_tableWidget.setRowCount(set_row)

            for j in range(set_row): #set_row):  # j는
                registed_data = semok[j][0]
                id = semok[j][1]
                self.registed_costsemok_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
                self.registed_costsemok_tableWidget.setItem(j,1,QTableWidgetItem(str(id)))
        self.registed_costsemok_tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.registed_costsemok_tableWidget.setColumnHidden(1, True) # 1열을 hidden 즉 숨김으로 함
    
    def costhang_combobox(self):
        from basic.cost_select import cost_hang_values
        self.costhang_comboBox_widget.blockSignals(True)
        self.costhang_comboBox_widget.clear()
        self.registed_costsemok_tableWidget.setRowCount(0)
        self.new_costsemok_tableWidget.clearContents()
        self.new_costsemok_tableWidget.setRowCount(0)
        self.new_costsemok_tableWidget.setRowCount(1)
        cost_hang_name_value = []
        gubun_sel = self.gubun_comboBox_widget.currentText() 
        # gubun_sel = '특별회계'
        cost_hang = cost_hang_values(v_year,gubun_sel)
        for c_hang in cost_hang:
            cost_hang_name, id = c_hang                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            cost_hang_name_value.append(cost_hang_name)
        self.costhang_comboBox_widget.addItems(['선택']+cost_hang_name_value)
        self.costhang_comboBox_widget.blockSignals(False)
        
    def costmok_combobox(self):
        from basic.cost_select import cost_mok_values
        self.costmok_comboBox_widget.blockSignals(True)
        self.costmok_comboBox_widget.clear()
        self.registed_costsemok_tableWidget.setRowCount(0)
        self.new_costsemok_tableWidget.setRowCount(0)  # 신규 회계단위 헌금 구분 입력사항 삭제
        self.new_costsemok_tableWidget.setRowCount(1)
        self.new_costsemok_widget.clear()
        
        cost_mok_name_value = []
        
        hang_sel = self.costhang_comboBox_widget.currentText() 
        cost_mok = cost_mok_values(v_year,hang_sel)
        for c_mok in cost_mok:
            cost_mok_name, id = c_mok                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            cost_mok_name_value.append(cost_mok_name)
        self.costmok_comboBox_widget.addItems(['선택'] + cost_mok_name_value)
        self.costmok_comboBox_widget.blockSignals(False)
    
    def costsemok_reg_input(self):
        global j
        cost_gubun = self.gubun_comboBox_widget.currentText()
        cost_hang = self.costhang_comboBox_widget.currentText()
        cost_mok = self.costmok_comboBox_widget.currentText()
        if cost_gubun != '선택' and cost_hang != '선택' and cost_hang != '' and cost_mok != '선택' and cost_mok != '':
            semok_name = self.new_costsemok_widget.text()  # 추가 되어야할 세목
        
            if semok_name != '':
                if j != 1:
                    self.new_costsemok_tableWidget.insertRow(j-1)
                self.new_costsemok_tableWidget.setItem((j-1),0,QTableWidgetItem(semok_name))
                self.new_costsemok_widget.clear() 
                self.new_costsemok_widget.setFocus()
                j += 1
        else:
            QMessageBox.about(self,'입력오류','선택사항을 먼저 선택하세요!!')
            self.new_costsemok_widget.clear()
    
    def delete_selected_row(self):
        from acc_menu_sql.cost_menu import cost_semok_selected_row_delete
        global j
        #self.registed_hang_tableWidget.clicked.connect(self.handle_table_click)
        selected_items = self.registed_costsemok_tableWidget.selectedItems()
        
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_costsemok_tableWidget.row(selected_items[0])
            if row_index != -1 and self.registed_costsemok_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_costsemok_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            cost_semok_selected_row_delete(v_year,selected_data)
            self.registed_costsemok_tableWidget.removeRow(row_index)
        else:
            QMessageBox.about(self,'저장',"삭제할 세목명을 선택하지 않았습니다.!!!")
            return
        self.registed_costsemok()

    def costsemok_modify(self):
        from acc_menu_sql.cost_menu import cost_semok_update_row_sql
        sel_row = None
        change_data = []
        
        sel_row = self.registed_costsemok_tableWidget.currentRow()
        
        # for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
        if self.registed_costsemok_tableWidget.item(sel_row, 0) != None:
            change_data_0 = self.registed_costsemok_tableWidget.item(sel_row, 0).text()
            change_data_1 = self.registed_costsemok_tableWidget.item(sel_row, 1).text()
        else:
            QMessageBox.about(self,'오류',"수정할 세목을 선택하지 않았습니다.!!!")
            return

        change_data.append(change_data_0)
        change_data.append(change_data_1)
        
        # 데이터베이스에 연결하여 값을 업데이트
        cost_semok_update_row_sql(v_year,change_data)
        change_data = []
        QMessageBox.about(self,'저장',"지출 세목명이 변경 되었습니다.!!!")
        self.registed_costsemok()

    def costsemok_reset(self):
        global j
        self.gubun_comboBox_widget.setCurrentText('선택')
        self.costhang_comboBox_widget.clear()
        self.costmok_comboBox_widget.clear()
        self.registed_costsemok_tableWidget.setRowCount(0)
        self.new_costsemok_tableWidget.setRowCount(0)  # 신규 회계단위 헌금 구분 입력사항 삭제
        self.new_costsemok_tableWidget.setRowCount(1)
        self.new_costsemok_widget.clear() 
        j=1

    def costsemok_save_cancel(self):
        self.costsemok_reset()
        self.close()
        
    def closeEvent(self, event):
        self.costsemok_reset()
        event.accept()
    
    def costsemok_save(self):
        from acc_menu_sql.cost_menu import current_year_cost_semok_save_sql
        global j
        cost_imsi = []
        rowCount = self.new_costsemok_tableWidget.rowCount()
        if self.costmok_comboBox_widget.currentText() != '선택':
            for i in range(rowCount):
                cost_mok = self.costmok_comboBox_widget.currentText()
                try:
                    cost_semok = self.new_costsemok_tableWidget.item(i, 0).text()
                    cost_imsi.append([cost_mok,cost_semok])
                except : 
                    QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")

            current_year_cost_semok_save_sql(v_year,cost_imsi)

            self.new_costsemok_tableWidget.setRowCount(0)
            j = 1
            self.new_costsemok_tableWidget.setRowCount(j)
            
            cost_imsi = []
            self.new_costsemok_widget.setFocus()

        else:        
            QMessageBox.about(self,'',"'지출 항','지출 목'을 먼저 선택하세요.!!!")
        
        self.registed_costsemok()
        self.new_costsemok_tableWidget.setRowCount(0)
        self.new_costsemok_tableWidget.setRowCount(1)
        self.new_costsemok_widget.setFocus()
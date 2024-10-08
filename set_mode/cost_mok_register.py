from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
import pymysql, configparser, os

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())
cost_imsi = []; n = 0

form_class = uic.loadUiType("ui/cost_mok_reg_form.ui")[0]
j = 1
class cost_mokRegister(QDialog, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('지출구분 목 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.end_signal = False
        self.new_costmok_tableWidget.clearContents()
        self.new_costmok_tableWidget.setRowCount(0)
        
        self.gubun_combo_selcet()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.costhang_combobox)
        self.costhang_comboBox_widget.currentTextChanged.connect(self.registed_mok)
        if self.end_signal == False:
            self.new_costmok_widget.editingFinished.connect(self.costmok_reg_input)
        self.registed_costmok_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        self.new_costmok_tableWidget.setRowCount(j)
        self.new_costmok_tableWidget.setColumnWidth(0, 125)
        self.new_costmok_widget.text()

    def gubun_combo_selcet(self):
        from basic.hun_name_2 import gubun_values
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_values())
    
    def add_costmok_button(self):
        add_costmok_button = QPushButton("신규등록추가")
        add_costmok_button.clicked.connect(self.costmok_reg_input)

        cost_mok_view_button = QPushButton("다시보기")
        cost_mok_view_button.clicked.connect(self.registed_mok)
        cost_mok_delete_button = QPushButton("선택 행 삭제")
        cost_mok_delete_button.clicked.connect(self.delete_selected_row)
        cost_mok_modify_button = QPushButton("선택 행 수정")
        cost_mok_modify_button.clicked.connect(self.modify_selected_row)
        
        costmok_save_button = QPushButton("저장")
        costmok_save_button.clicked.connect(self.costmok_save)

        costmok_cancel_button = QPushButton("종료(저장취소)")
        costmok_cancel_button.clicked.connect(self.costmok_save_cancel)

    def registed_mok(self):
        from basic.cost_select import cost_mok_values
        hang = self.costhang_comboBox_widget.currentText()
        costmok = cost_mok_values(v_year,hang)
        if costmok != None:
            set_row = len(costmok)
            self.registed_costmok_tableWidget.setRowCount(set_row)
            for j in range(set_row): #set_row):  # j는
                registed_data = costmok[j][0]
                id = costmok[j][1]
                self.registed_costmok_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
                self.registed_costmok_tableWidget.setItem(j,1,QTableWidgetItem(str(id)))

        self.registed_costmok_tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.registed_costmok_tableWidget.setColumnHidden(1, True) # 1열을 hidden 즉 숨김으로 함
        # self.registed_costmok_tableWidget.setColumnWidth(1, 0) # 1은 두번째, 0 은 열의 폭을 나타냄
    

    def costhang_combobox(self):
        from basic.cost_select import cost_hang_values
        self.costhang_comboBox_widget.clear()
        
        cost_hang_name_value = []
        gubun_sel =  self.gubun_comboBox_widget.currentText() 
        cost_hang = cost_hang_values(v_year,gubun_sel)
        for c_hang in cost_hang:
            cost_hang_name, id = c_hang                       # c_hang을 항 이름과 id로 분리시킨후 항이름을 리스트로 만든다.
            cost_hang_name_value.append(cost_hang_name)
        self.costhang_comboBox_widget.addItems(['선택'] + cost_hang_name_value)
        
    def costmok_reg_input(self):
        global j
        cost_hang = self.costhang_comboBox_widget.currentText()
        if cost_hang != '선택' and cost_hang != '':
            mok_name = self.new_costmok_widget.text()  # 구분
            
            if mok_name !='':
                if j != 1:
                    self.new_costmok_tableWidget.insertRow(j-1)
                self.new_costmok_tableWidget.setItem((j-1),0,QTableWidgetItem(mok_name))
                self.new_costmok_widget.clear() 
                self.new_costmok_widget.setFocus()
                j += 1
        else:
            QMessageBox.about(self,'입력오류','선택사항을 먼저 선택하세요!!')
            self.new_costmok_widget.clear()
            self.new_costmok_widget.setFocus()

    def delete_selected_row(self):
        from acc_menu_sql.cost_menu import cost_mok_selected_row_delete
        global j
        #self.registed_hang_tableWidget.clicked.connect(self.handle_table_click)
        selected_items = self.registed_costmok_tableWidget.selectedItems()

        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_costmok_tableWidget.row(selected_items[0])
            if row_index != -1 and self.registed_costmok_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_costmok_tableWidget.item(row_index, 0).text()
        
        # 데이터베이스 연결
            cost_mok_selected_row_delete(v_year,selected_data)
            self.registed_costmok_tableWidget.removeRow(row_index)
        
        self.registed_mok()
    
    def costmok_modify(self):
        from acc_menu_sql.cost_menu import cost_mok_update_row_sql
        sel_row = None
        change_data = []

        sel_row = self.registed_costmok_tableWidget.currentRow()
        # c_count = self.registed_costmok_tableWidget.columnCount()
        # for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
        if self.registed_costmok_tableWidget.item(sel_row, 0) != None:
            change_data_0 = self.registed_costmok_tableWidget.item(sel_row, 0).text()
            change_data_1 = self.registed_costmok_tableWidget.item(sel_row, 1).text()
        else:
            change_data = None
        change_data.append(change_data_0)
        change_data.append(change_data_1)

        # 데이터베이스에 연결하여 값을 업데이트
        cost_mok_update_row_sql(v_year,change_data)
        change_data = []
        QMessageBox.about(self,'저장',"지출 목 이 변경 되었습니다.!!!")
        self.registed_mok()

    def costmok_reset(self):
        global j, cost_imsi
        cost_imsi = []
        self.gubun_comboBox_widget.setCurrentText('선택')
        self.costhang_comboBox_widget.clear()
        self.registed_costmok_tableWidget.setRowCount(0)
        self.new_costmok_tableWidget.setRowCount(0)  # 신규 회계단위 헌금 구분 입력사항 삭제
        self.new_costmok_tableWidget.setRowCount(1)
        self.new_costmok_widget.clear() 
        j=1

        
        
        

    def costmok_save_cancel(self):
        self.costmok_reset()
        self.end_signal = True
        self.close()
    
    def closeEvent(self, event):
        self.costmok_reset()
        self.end_signal = True
        event.accept()
    
    def costmok_save(self):
        from acc_menu_sql.cost_menu import current_year_cost_mok_save_sql
        global j, cost_imsi
        self.end_signal = True
        
        rowCount = self.new_costmok_tableWidget.rowCount()
        if self.costhang_comboBox_widget.currentText() != '선택':
            for i in range(rowCount):
                cost_hang = self.costhang_comboBox_widget.currentText()
                try:
                    cost_mok = self.new_costmok_tableWidget.item(i, 0).text()
                    cost_imsi.append([cost_hang,cost_mok])
                except : 
                    QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")
            
            current_year_cost_mok_save_sql(v_year,cost_imsi)
            
            self.new_costmok_tableWidget.setRowCount(0)
            j = 1
            self.new_costmok_tableWidget.setRowCount(j)
            cost_imsi = []

            self.new_costmok_widget.setFocus()
            self.registed_mok()

        else:        
            QMessageBox.about(self,'',"'항' 선택을 먼저 하세요.!!!")
        
        self.end_signal = False
        self.new_costmok_tableWidget.setRowCount(0)
        self.new_costmok_tableWidget.setRowCount(1)
        self.new_costmok_widget.setFocus()
        self.registed_mok()


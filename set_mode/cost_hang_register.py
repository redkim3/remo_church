import os, configparser,pymysql
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
v_year = str(today.year())
cost_imsi = []; n = 0

form_class = uic.loadUiType("ui/cost_hang_reg_form.ui")[0]
j = 1
class cost_hangRegister(QDialog, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('지출구분 항 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.new_costhang_tableWidget.clearContents()
        self.new_costhang_tableWidget.setRowCount(0)
        self.gubun_combo_select()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.registed_hang)
        
        self.registed_costhang_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt 
        self.new_costhang_tableWidget.setRowCount(1)
        self.new_costhang_tableWidget.setColumnWidth(0, 125)
    
    def gubun_combo_select(self):
        from basic.hun_name_2 import gubun_values
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_values())
        
    def acc_hang_button(self):
        addcost_hang_button = QPushButton("등록")
        addcost_hang_button.clicked.connect(self.costhang_reg_input)

        cost_hang_view_button = QPushButton("다시보기")
        cost_hang_view_button.clicked.connect(self.registed_hang)
        cost_hang_delete_button = QPushButton("선택 행 삭제")
        cost_hang_delete_button.clicked.connect(self.delete_selected_row)

        cost_hang_save_button = QPushButton("저장")
        cost_hang_save_button.clicked.connect(self.costhang_file_save)
        cancel_button = QPushButton("종료(저장취소)")
        cancel_button.clicked.connect(self.costhang_save_cancel)

    def registed_hang(self):
        from basic.cost_select import cost_hang_values
        gubun =  self.gubun_comboBox_widget.currentText()
        costhang = cost_hang_values(v_year,gubun)
        if costhang != None:
            set_row = len(costhang)
            self.registed_costhang_tableWidget.setRowCount(set_row)

            for j in range(set_row): #set_row):  # j는
                registed_data = costhang[j][0]
                id = costhang[j][1]
                self.registed_costhang_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))
                self.registed_costhang_tableWidget.setItem(j,1,QTableWidgetItem(str(id)))
        self.registed_costhang_tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.registed_costhang_tableWidget.setColumnHidden(1, True) # 1은 두번째, 0 은 열의 폭을 나타냄
    
    def delete_selected_row(self):
        from acc_menu_sql.cost_menu import cost_hang_selected_row_delete
        global j
        #self.registed_hang_tableWidget.clicked.connect(self.handle_table_click)
        selected_items = self.registed_costhang_tableWidget.selectedItems()
       
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_costhang_tableWidget.row(selected_items[0])
            if row_index != -1 and self.registed_costhang_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_costhang_tableWidget.item(row_index, 0).text()
            # 테이블 위젯에서 선택된 행 삭제
            cost_hang_selected_row_delete(v_year,selected_data)
            self.registed_costhang_tableWidget.removeRow(row_index)
            self.registed_hang()

    def costhang_modify(self):
        from acc_menu_sql.cost_menu import cost_hang_update_row_sql
        sel_row = None
        change_data = []
        sel_row = self.registed_costhang_tableWidget.currentRow()

        # for c_cnt in range(c_count): # 1부터 시작하는 것으로 가정합니다. 0은 날짜를 처리하는 부분이므로 수정되지 않습니다.
        if self.registed_costhang_tableWidget.item(sel_row, 0) != None:
            change_data_0 = self.registed_costhang_tableWidget.item(sel_row, 0).text()
            change_data_1 = self.registed_costhang_tableWidget.item(sel_row, 1).text()
        else:
            change_data = None
        change_data.append(change_data_0)
        change_data.append(change_data_1)

        # 데이터베이스에 연결하여 값을 업데이트
        cost_hang_update_row_sql(v_year,change_data)
        change_data = []
        QMessageBox.about(self,'저장',"지출 항 이 변경 되었습니다.!!!")
        self.registed_hang()


    def costhang_reg_input(self):
        global j
        if self.gubun_comboBox_widget.currentText() != '선택':
            costhang_name = self.new_costhang_widget.text()  # 구분
            if costhang_name =='':
                QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
            else:
                if j != 1:
                    self.new_costhang_tableWidget.insertRow(j-1)
                self.new_costhang_tableWidget.setItem((j-1),0,QTableWidgetItem(costhang_name))
                self.new_costhang_widget.clear() 
                self.new_costhang_widget.setFocus()
                j += 1
        else:
            QMessageBox.about(self,'입력오류','선택사항을 먼저 선택하세요!!')
            self.new_costhang_widget.clear()

    def costhang_reset(self):
        self.gubun_comboBox_widget.setCurrentText('선택')
        self.new_costhang_widget.clear() 
        self.new_costhang_tableWidget.setRowCount(0)
        self.new_costhang_tableWidget.setRowCount(1)
        self.registed_costhang_tableWidget.setRowCount(0)
        self.registed_costhang_tableWidget.setRowCount(1)

    def costhang_save_cancel(self):
        self.costhang_reset()
        self.close()
    
    def closeEvent(self, event):
        self.costhang_reset()
        event.accept()

    def costhang_file_save(self):
        from acc_menu_sql.cost_menu import current_year_cost_hang_save_sql
        global j, cost_imsi
        rowCount = self.new_costhang_tableWidget.rowCount()
        try:   
            if self.gubun_comboBox_widget.currentText() != '선택':
                for i in range(rowCount):
                    gubun = self.gubun_comboBox_widget.currentText()
                    try:
                        cost_hang = self.new_costhang_tableWidget.item(i, 0).text()
                        cost_imsi.append([gubun,cost_hang])
                    except : 
                        QMessageBox.about(self,'',"저장할 내용이 없습니다.!!!")

                current_year_cost_hang_save_sql(v_year,cost_imsi)

                self.new_costhang_tableWidget.setRowCount(0)
                self.new_costhang_tableWidget.setRowCount(j)
                self.registed_hang()
                self.new_costhang_widget.setFocus()
                cost_imsi = []; j = 1
                
            else:        
                QMessageBox.about(self,'',"회계 구분을 먼저 선택하시고 신규 항을 입력 하세요.!!!")#     
        except pymysql.Error as e :
            QMessageBox.critical(self, '에러', f'데이터 저장 중 오류 발생: {e}')
            self.new_costhang_tableWidget.setRowCount(0)
            self.new_costhang_tableWidget.setRowCount(1)
            self.new_costhang_widget.setFocus()
        

from PyQt5 import uic 
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import configparser, pymysql, os

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
j = 1; sungdo_imsi = []

form_class = uic.loadUiType("./ui/sungdo_serch.ui")[0]

class Serch_Member(QDialog, form_class) :
    def __init__(self) :
        super(Serch_Member,self).__init__()
        self.setupUi(self)

        self.setWindowTitle("성도 검색")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.code1 = None
        global selector, name_select, sel_row
        selector = 'name'
        self.sungdo_name_widget.text()

        self.name_radio_Button.clicked.connect(self.serch_mode_select1)
        self.hap_code_radio_Button.clicked.connect(self.serch_mode_select2)
        self.code1_radio_Button.clicked.connect(self.serch_mode_select3)
        self.close_pushButton.clicked.connect(self.member_serch_close)
    
    def button_collect(self):
        serch_member_Button = QPushButton("성도검색")
        serch_member_Button.clicked.connect(self.sungdo_view)
        edit_infor_Button = QPushButton("정보수정")
        edit_infor_Button.clicked.connect(self.edit_infor_Button)
        
    def serch_mode_select1(self):
        global sungdo_result, selector
        selector = 'name'
        self.tab_label.setText('성              명')

    def serch_mode_select2(self):
        global sungdo_result, selector
        selector = 'hap_code'
        self.tab_label.setText('합   산   코   드')
    
    def serch_mode_select3(self):
        global sungdo_result, selector
        selector = 'code1'
        self.tab_label.setText('개   별   코   드')

    def serch_data(self):
        from basic.sungdo import sungdo_serch_code
        global target, sungdo_result
        target = self.sungdo_name_widget.text()
        selector = self.check_selection()

        if self.name_radio_Button.isChecked():
            selector = "name"
            sungdo_result = sungdo_serch_code(selector, target)
        elif self.hap_code_radio_Button.isChecked():
            selector = "hap_code"
            sungdo_result = sungdo_serch_code(selector, target)
        elif self.code1_radio_Button.isChecked():
            selector = "code1"
            sungdo_result = sungdo_serch_code(selector, target)
        return sungdo_result
        
    def check_selection(self):
        if self.name_radio_Button.isChecked():
            selector = "name"
        elif self.hap_code_radio_Button.isChecked():
            selector = "hap_code"
        elif self.code1_radio_Button.isChecked():
            selector = "code1"
        return selector
 
    def sungdo_view(self):
        sungdo = self.serch_data()
        count_row = len(sungdo)
        self.regist_sungdo_tableWidget.setRowCount(count_row)
        if count_row > 0:
            for i in range(count_row):
                dat_f = sungdo[i][0]
                if isinstance(dat_f, date):
                    v_dat = dat_f.strftime('%Y-%m-%d')
                else:
                    QMessageBox.about(self,'변환오류', "변환할 수 없는 형태의 값입니다.")
                    # v_dat = datetime.strftime(dat_f,'%Y-%m-%d')
                try:
                    if sungdo:  # sungdo 리스트가 비어있지 않은 경우에만 처리합니다.
                        code1 = str(sungdo[i][1])  # sungdo 리스트의 첫 번째 요소의 두 번째 값
                    else:
                        QMessageBox.about(self,'검색에러',"sungdo 리스트가 비어있습니다.")
                except IndexError:
                    QMessageBox.about(self,'인덱스에러',"인덱스가 범위를 벗어납니다.")
                    
                name_diff = str(sungdo[i][2])
                name = str(sungdo[i][3])
                hap_code = str(sungdo[i][4])
                jikbun = str(sungdo[i][5])
                addr = str(sungdo[i][6])
                marks = str(sungdo[i][7])

                self.regist_sungdo_tableWidget.setItem(i,0,QTableWidgetItem(v_dat))
                self.regist_sungdo_tableWidget.setItem(i,1,QTableWidgetItem(code1))
                self.regist_sungdo_tableWidget.setItem(i,2,QTableWidgetItem(name_diff))
                self.regist_sungdo_tableWidget.setItem(i,3,QTableWidgetItem(name))
                self.regist_sungdo_tableWidget.setItem(i,4,QTableWidgetItem(hap_code))
                if jikbun != None and jikbun != 'None':
                    self.regist_sungdo_tableWidget.setItem(i,5,QTableWidgetItem(jikbun))
                if addr != None and addr != 'None':
                    self.regist_sungdo_tableWidget.setItem(i,6,QTableWidgetItem(addr))
                if marks != None and marks != 'None':
                    self.regist_sungdo_tableWidget.setItem(i,7,QTableWidgetItem(marks))
        else:
            QMessageBox.about(self,"검색","검색된 성도가 없습니다.")

    def edit_information(self): #cell_changed
        sel_row = None
        change_data = []
        sel_row = self.regist_sungdo_tableWidget.currentRow()
               
        c_count = self.regist_sungdo_tableWidget.columnCount()
        for c_cnt in range(c_count):
            if self.regist_sungdo_tableWidget.item(sel_row,c_cnt) != None:
                change_data_0 = self.regist_sungdo_tableWidget.item(sel_row,c_cnt).text()
            else:
                change_data_0 = None

            change_data.append(change_data_0)
        if sel_row != -1:
            code1 = self.regist_sungdo_tableWidget.item(sel_row,1).text()
            change_data.append(code1)

        # 데이터베이스에 연결하여 값을 업데이트
        conn = pymysql.connect(host=host_name,user="root",password="0000",
            db="isbs2024", charset='utf8' )
        cur = conn.cursor()
       
        update_query = f"UPDATE member SET date = %s,code1 = %s,name_diff = %s, name = %s, hap_code = %s,level = %s,addr = %s,marks = %s WHERE code1 = %s"
        cur.execute(update_query, tuple(change_data))
        conn.commit()

        cur.close()
        conn.close()
        QMessageBox.information(None, "완료", "성도 정보가 변경 되었습니다.")

    def member_serch_close(self):
        self.sungdo_name_widget.clear()
        self.regist_sungdo_tableWidget.clearContents()
        self.regist_sungdo_tableWidget.setRowCount(1)
        self.close()

    
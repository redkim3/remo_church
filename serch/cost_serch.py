import os
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from datetime import datetime
from PyQt5 import uic
cur_fold = os.getcwd()
today = QDate.currentDate()
form_secondclass = uic.loadUiType("./ui/cost_serch.ui")[0]

class cost_Serch(QDialog, QWidget, form_secondclass) :
    def __init__(self) :
        super(cost_Serch,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("비용 검색")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.serch_year_widget.setText(str(today.year()))
        self.serch_word_widget.editingFinished.connect(self.cost_reg_serch)
        self.show()        
    
    def button(self):
        self.cost_serch_Button.clicked.connect(self.cost_reg_serch)
        self.reset_Button.clicked.connect(self.serch_reset_Button)
        self.cost_reg_return_Button.clicked.connect(self.cost_reg_return)
        
    def cost_reg_serch(self):
        from basic.cost_split import cost_word_serch
        global v_dat,v_hang,v_mok,v_semok,v_detail,v_amo,v_mar
        self.cost_serch_tableWidget.clearContents()
        self.cost_serch_tableWidget.setRowCount(1)
        word = self.serch_word_widget.text()                
        if word != '':
            try:
                s_year = self.serch_year_widget.text()
                s_year = int(s_year)
                serch_target = cost_word_serch(s_year,word)
                cnt = 0
                for row in serch_target:
                    if cnt != 0:
                        self.cost_serch_tableWidget.insertRow(cnt)
                    s_dat = row[0]
                    v_dat = datetime.strftime(s_dat,'%Y-%m-%d')
                    v_hang = str(row[1])
                    v_mok = str(row[2])
                    v_semok = str(row[3])
                    v_detail = str(row[4])
                    s_amo = int(row[5])
                    v_amo = format(s_amo,",")
                    v_mar = str(row[6])
                   
                    self.cost_serch_tableWidget.setItem(cnt,0,QTableWidgetItem(v_dat)) 
                    self.cost_serch_tableWidget.item(cnt,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                    self.cost_serch_tableWidget.setItem(cnt,1,QTableWidgetItem(v_hang))
                    self.cost_serch_tableWidget.item(cnt,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    if v_mok != None and v_mok != 'None':
                        self.cost_serch_tableWidget.setItem(cnt,2,QTableWidgetItem(v_mok))
                        self.cost_serch_tableWidget.item(cnt,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    if v_semok != None and v_semok != 'None':
                        self.cost_serch_tableWidget.setItem(cnt,3,QTableWidgetItem(v_semok))
                        self.cost_serch_tableWidget.item(cnt,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.cost_serch_tableWidget.setItem(cnt,4,QTableWidgetItem(v_detail))
                    self.cost_serch_tableWidget.item(cnt,4).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.cost_serch_tableWidget.setItem(cnt,5,QTableWidgetItem(v_amo))
                    self.cost_serch_tableWidget.item(cnt,5).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.cost_serch_tableWidget.setItem(cnt,6,QTableWidgetItem(v_mar))
                    self.cost_serch_tableWidget.item(cnt,6).setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.cost_serch_tableWidget.resizeColumnsToContents()
                    cnt += 1

            except ValueError:
                QMessageBox.about(self,'요구사항없음','검색할 사항이 없습니다.!!!')

    def cost_reg_return(self):  # 홈버튼
        self.serch_year_widget.clear()
        self.serch_word_widget.clear()
        self.cost_serch_tableWidget.clearContents()
        self.close()
    
    def serch_reset_Button(self): 
        self.serch_word_widget.clear()
        self.cost_serch_tableWidget.clearContents()
        self.cost_serch_tableWidget.setRowCount(1)
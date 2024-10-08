import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt

cur_fold = os.getcwd()
today = QDate.currentDate()
form_class = uic.loadUiType(r"./ui/hun_detail_view.ui")[0]
Na_code = ''
class hun_detail_view(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("헌금 세부내역 보기")
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        view_year = str(today.year())
        comboyear = [view_year]
        # # 향후에 헌금세부내역을 고치는 방향이 확정되면 그때 수정을 하자
        # self.hun_1_comboBox.setCurrentText('십일조헌금')
        # self.hun_2_comboBox.setCurrentText('감사헌금')
        # self.hun_3_comboBox.setCurrentText('절기헌금')
        # self.hun_4_comboBox.setCurrentText('선교헌금')
        # self.view1_hun_widget.setText('십일조헌금')
        # self.view2_hun_widget.setText('감사헌금')
        # self.view3_hun_widget.setText('절기헌금,지정헌금,주일헌금')
        # self.view4_hun_widget.setText('선교헌금')
        for y in range(4,0,-1):
            comboyear.append(str((int(view_year)-5)+y))
            
        self.combo_year_widget.addItems(comboyear)
        self.registed_name.editingFinished.connect(self.serch_method_combo)
        self.serch_method_combo_widget.currentTextChanged.connect(self.serch_method_select)
    
    def hun_detail_view_button(self):
        hunserch_Button = QPushButton("검색하기")
        hunserch_Button.clicked.connect(self.hun_serch)
        detailclear_Button = QPushButton("내역지우기")
        detailclear_Button.clicked.connect(self.reset_button)
        s_close_Button = QPushButton("종료(닫기)")
        s_close_Button.clicked.connect(self.close_window)
        self.name_code = QDateEdit()

    def input_name(self):
        from basic.member import name_diff_compare
        name_diff = self.registed_name.text()
        name_comp = name_diff_compare(name_diff)
        name_comp = ', '.join(name_comp)
        if name_diff != name_comp:
            QMessageBox.about(self,'입력오류 !!!','등록되지 않은 이름 입니다. 확인하여 주십시오')
        
    def serch_method_combo(self):
        global serch_method, code_no
        self.serch_code_widget.clear()
        self.sum_name_code_widget.clear()
        self.reset_button()
        
        self.sib_tableWidget.setRowCount(1)
        self.gam_tableWidget.setRowCount(1)
        self.jeol_tableWidget.setRowCount(1)
        self.sun_tableWidget.setRowCount(1)

        self.serch_method_combo_widget.clear()  # 헌금 명칭 
        self.serch_method_combo_widget.currentText()
        serch_method = ["선택","합산","개별"]
        self.serch_method_combo_widget.addItems(serch_method)
        self.serch_method_combo_widget.currentText()
        self.serch_method_combo_widget.currentTextChanged.connect(self.serch_method_select)
    
    def serch_method_select(self):
        from basic.member import code1_select, hap_code_select
        
        global id_code, serch_meth
        serch_method = self.serch_method_combo_widget.currentText()
        self.serch_method_combo_widget.currentText()
        name_diff = self.registed_name.text()
        try:
            if serch_method == "개별":
                self.sib_tableWidget.clearContents()
                self.gam_tableWidget.clearContents()
                self.jeol_tableWidget.clearContents()
                self.sun_tableWidget.clearContents()
                self.sib_tableWidget.setColumnCount(2)
                self.gam_tableWidget.setColumnCount(2)
                self.jeol_tableWidget.setColumnCount(3)
                self.sun_tableWidget.setColumnCount(2)
                self.sib_tableWidget.setRowCount(1)
                self.gam_tableWidget.setRowCount(1)
                self.jeol_tableWidget.setRowCount(1)
                self.sun_tableWidget.setRowCount(1)
                self.serch_code_widget.setText(serch_method)
                code = code1_select(name_diff)
                self.sum_name_code_widget.setText(code)
            else:
                if serch_method == "합산":
                    self.sib_tableWidget.clearContents()
                    self.gam_tableWidget.clearContents()
                    self.jeol_tableWidget.clearContents()
                    self.sun_tableWidget.clearContents()
                    self.sib_tableWidget.setColumnCount(3)
                    self.gam_tableWidget.setColumnCount(3)
                    self.jeol_tableWidget.setColumnCount(4)
                    self.sun_tableWidget.setColumnCount(3)
                    self.sib_tableWidget.setRowCount(1)
                    self.gam_tableWidget.setRowCount(1)
                    self.jeol_tableWidget.setRowCount(1)
                    self.sun_tableWidget.setRowCount(1)
                    self.serch_code_widget.setText(serch_method)
                    h_code = hap_code_select(name_diff)
                    self.sum_name_code_widget.setText(h_code)
        except TypeError:
            QMessageBox.about(self, "입력오류","입력이 누락되었습니다. ")
            self.registed_name.setFocus()
        # self.input_name()

    def reset_button(self):
        
        self.hun_total_widget.clear()
        self.sib_total_widget.clear()
        self.gam_total_widget.clear()
        self.jeol_total_widget.clear()
        self.sun_total_widget.clear()
        self.sib_tableWidget.clearContents()
        self.gam_tableWidget.clearContents()
        self.jeol_tableWidget.clearContents()
        self.sun_tableWidget.clearContents()
        self.sib_tableWidget.setRowCount(1)
        self.gam_tableWidget.setRowCount(1)
        self.jeol_tableWidget.setRowCount(1)
        self.sun_tableWidget.setRowCount(1)

    def hun_serch(self):
        from basic.hun_serch import p_hun_list, hap_hun_list
        sip_to = 0; gam_to = 0; jeol_to = 0; sun_to = 0; hun_to = 0
        sip_total = 0; gam_total = 0; jeol_total = 0; sun_total = 0; hun_total = 0
        self.reset_button()
        # 향후에 헌금세부내역을 고치는 방향이 확정되면 그때 수정을 하자
        # hun_sib = self.self.view1_hun_widget.text()
        # hun_gam = self.self.view2_hun_widget.text()
        # hun_jeol = self.self.view3_hun_widget.text()
        # hun_seon = self.self.view4_hun_widget.text()
        id_code = self.sum_name_code_widget.text()
        serch_method = self.serch_method_combo_widget.currentText()  # 개별, 합산
        view_year = int(self.combo_year_widget.currentText())
        
        if serch_method == "개별" :
            p_hun_list_source = p_hun_list(view_year, id_code)

            # 수정 시작
            hun_mok_list = [row[0] for row in p_hun_list_source]
            name_diff_list = [row[2].split(',') if row[2] else [] for row in p_hun_list_source]
            hun_date_list = [row[1] for row in p_hun_list_source]
            amount_list = [row[3] for row in p_hun_list_source]
            hun_hang_list = [row[4] for row in p_hun_list_source]
            # bank_list = [row[5] if len(row) > 5 else None for row in p_hun_list_source]

            # 리스트들을 zip으로 묶어서 정렬
            # sorted_data = sorted(zip(hun_mok_list,name_diff_list, hun_date_list, amount_list, hun_detail_list), key=lambda x: float(x[3]), reverse=True) # , bank_list
            sorted_data = sorted(zip(hun_mok_list, name_diff_list, hun_date_list, amount_list, hun_hang_list), key=lambda x: x[2], reverse=False)
            hun_source = [(item[0], item[1][0] if item[1] and isinstance(item[1], list) else item[1], item[2], item[3] if item[3] != None else None, item[4]) for item in sorted_data]  # , item[5]
            hun_list = []
            for item in hun_source:
                hun_list.append(item)
            
            sip_list = []; gam_list = []; jeolgi_list = []; mission_list = []
            
            for hun_row in hun_list:
                if hun_row[0] == '십일조헌금':
                    sip_list.append((hun_row[0],hun_row[1],hun_row[2],hun_row[3],hun_row[4])) #,hun_row[5]
                elif hun_row[0] == '감사헌금':
                    gam_list.append((hun_row[0],hun_row[1],hun_row[2],hun_row[3],hun_row[4])) #,hun_row[5]
                elif hun_row[4] == '절기헌금' or hun_row[4] == '지정헌금' or hun_row[0] == '주일헌금':
                    jeolgi_list.append((hun_row[0],hun_row[1],hun_row[2],hun_row[3],hun_row[4]))  #,hun_row[5]
                elif hun_row[4] == '선교헌금':
                    mission_list.append((hun_row[0],hun_row[1],hun_row[2],hun_row[3],hun_row[4])) # ,hun_row[5]

            self.sib_tableWidget.setHorizontalHeaderLabels(["일자","금액"])
            self.gam_tableWidget.setHorizontalHeaderLabels(["일자","금액"])
            self.jeol_tableWidget.setHorizontalHeaderLabels(["일자","헌금유형","금액"])
            self.sun_tableWidget.setHorizontalHeaderLabels(["일자","금액"])            
            
            j = 0
            for sip in sip_list:  # j는 행 c는 열  
                dat_1 = sip[2]
                vdate_1 = dat_1.strftime('%Y-%m-%d')
                amo_int_1 = int(sip[3])
                sip_to += amo_int_1
                amo_1 = format(amo_int_1,",")
                sip_total = format(sip_to,",")
                if j != 1:  
                    self.sib_tableWidget.insertRow(j)

                self.sib_tableWidget.setItem(j,0,QTableWidgetItem(vdate_1))
                self.sib_tableWidget.setItem(j,1,QTableWidgetItem(amo_1))
                self.sib_tableWidget.resizeColumnsToContents()
                if self.sib_tableWidget.item(j, 0) != None:
                    self.sib_tableWidget.item(j, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sib_tableWidget.item(j, 1) != None:
                    self.sib_tableWidget.item(j, 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.sib_total_widget.setText(sip_total)
                j += 1
            
            j1 = 0
            for gam in gam_list:  # j는 행 c는 열  
                dat_2 = gam[2]
                vdate_2 = dat_2.strftime('%Y-%m-%d')
                amo_int_2 = int(gam[3])
                gam_to += amo_int_2
                amo_2 = format(amo_int_2,",")
                gam_total = format(gam_to,",")
                if j1 != 1:  
                    self.gam_tableWidget.insertRow(j1)

                self.gam_tableWidget.setItem(j1,0,QTableWidgetItem(vdate_2))
                self.gam_tableWidget.setItem(j1,1,QTableWidgetItem(amo_2))
                self.gam_tableWidget.resizeColumnsToContents()
                if self.gam_tableWidget.item(j1, 0) != None:
                    self.gam_tableWidget.item(j1,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.gam_tableWidget.item(j1, 1) != None:
                    self.gam_tableWidget.item(j1,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.gam_total_widget.setText(gam_total)
                j1 += 1
            j2 = 0
            for jeol in jeolgi_list:  # j는 행 c는 열  
                jeol_name = str(jeol[0])
                dat_3 = jeol[2]
                vdate_3 = dat_3.strftime('%Y-%m-%d')
                amo_int_3 = int(jeol[3])
                jeol_to += amo_int_3
                amo_3 = format(amo_int_3,",")
                jeol_total = format(jeol_to,",")
                if j2 != 1:  
                    self.jeol_tableWidget.insertRow(j2)

                self.jeol_tableWidget.setItem(j2,0,QTableWidgetItem(vdate_3))
                self.jeol_tableWidget.setItem(j2,1,QTableWidgetItem(jeol_name))
                self.jeol_tableWidget.setItem(j2,2,QTableWidgetItem(amo_3))
                self.jeol_tableWidget.resizeColumnsToContents()
                if self.jeol_tableWidget.item(j2, 0) != None:
                    self.jeol_tableWidget.item(j2,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.jeol_tableWidget.item(j2, 1) != None:
                    self.jeol_tableWidget.item(j2,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.jeol_tableWidget.item(j2, 2) != None:
                    self.jeol_tableWidget.item(j2,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.jeol_total_widget.setText(jeol_total)
                j2 += 1
            j3 = 0
            for sun in mission_list:  # j는 행 c는 열  
                
                dat_4 = sun[2]
                vdate_4 = dat_4.strftime('%Y-%m-%d')
                amo_int_4 = int(sun[3])
                sun_to += amo_int_4
                amo_4 = format(amo_int_4,",")
                sun_total = format(sun_to,",")
                if j3 != 1:
                    self.sun_tableWidget.insertRow(j3)

                self.sun_tableWidget.setItem(j3,0,QTableWidgetItem(vdate_4))
                self.sun_tableWidget.setItem(j3,1,QTableWidgetItem(amo_4))
                self.sun_tableWidget.resizeColumnsToContents()
                if self.sun_tableWidget.item(j3, 0) != None:
                    self.sun_tableWidget.item(j3,0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sun_tableWidget.item(j3, 1) != None:
                    self.sun_tableWidget.item(j3,1).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.sun_total_widget.setText(sun_total)
                j3 += 1
            hun_to = sip_to + gam_to + jeol_to + sun_to
            hun_total = format(hun_to,",")
            self.hun_total_widget.setText(hun_total)
           
        elif serch_method == "합산" :
            p_hun_list_source = hap_hun_list(view_year, id_code)

            # 수정 시작
            h_hun_mok_list = [row[0] for row in p_hun_list_source]
            h_name_diff_list = [row[2].split(',') if row[2] else [] for row in p_hun_list_source]
            h_hun_date_list = [row[1] for row in p_hun_list_source]
            h_amount_list = [row[3] for row in p_hun_list_source]
            h_hun_hang_list = [row[4] for row in p_hun_list_source]
            bank_list = [row[5] if len(row) > 5 else None for row in p_hun_list_source]

            # 리스트들을 zip으로 묶어서 정렬
            # sorted_data = sorted(zip(h_hun_mok_list,h_name_diff_list, h_hun_date_list, h_amount_list, h_hun_hang_list), key=lambda x: float(x[3]), reverse=True)  # , bank_list  금액순서로 정렬
            sorted_data = sorted(zip(h_hun_mok_list, h_name_diff_list, h_hun_date_list, h_amount_list, h_hun_hang_list), key=lambda x: x[2], reverse=False)  # 날짜 순서로 정렬
            h_hun_source = [(item[0], item[1][0] if item[1] and isinstance(item[1], list) else item[1], item[2], item[3] if item[3] != None else None, item[4]) for item in sorted_data]
            h_hun_list = []
            for h_item in h_hun_source:
                h_hun_list.append(h_item)
            
            h_sip_list = []; h_gam_list = []; h_jeolgi_list = []; h_mission_list = []
            
            for h_hun_row in h_hun_list:
                if h_hun_row[0] == '십일조헌금':
                    h_sip_list.append((h_hun_row[0],h_hun_row[1],h_hun_row[2],h_hun_row[3],h_hun_row[4]))  #,hun_row[5]
                elif h_hun_row[0] == '감사헌금':
                    h_gam_list.append((h_hun_row[0],h_hun_row[1],h_hun_row[2],h_hun_row[3],h_hun_row[4])) #,hun_row[5]
                elif h_hun_row[4] == '절기헌금' or h_hun_row[4] == '지정헌금' or h_hun_row[0] == '주일헌금':
                    h_jeolgi_list.append((h_hun_row[0],h_hun_row[1],h_hun_row[2],h_hun_row[3],h_hun_row[4]))  # ,hun_row[5]
                elif h_hun_row[4] == '선교헌금':
                    h_mission_list.append((h_hun_row[0],h_hun_row[1],h_hun_row[2],h_hun_row[3],h_hun_row[4]))  # ,hun_row[5]

            self.sib_tableWidget.setHorizontalHeaderLabels(["일자","성명","금액"])
            self.gam_tableWidget.setHorizontalHeaderLabels(["일자","성명","금액"])
            self.jeol_tableWidget.setHorizontalHeaderLabels(["일자","성명","헌금유형","금액"])
            self.sun_tableWidget.setHorizontalHeaderLabels(["일자","성명","금액"])            
            
            j = 0
            for sip in h_sip_list:  # j는 행 c는 열  
                h_dat_1 = sip[2]
                h_vdate_1 = h_dat_1.strftime('%Y-%m-%d')
                h_name1 = sip[1]
                h_amo_int_1 = int(sip[3])
                sip_to += h_amo_int_1
                h_amo_1 = format(h_amo_int_1,",")
                sip_total = format(sip_to,",")
                if j != 1:  
                    self.sib_tableWidget.insertRow(j)

                self.sib_tableWidget.setItem(j, 0, QTableWidgetItem(h_vdate_1))
                self.sib_tableWidget.setItem(j, 1, QTableWidgetItem(h_name1))
                self.sib_tableWidget.setItem(j, 2, QTableWidgetItem(h_amo_1))
                self.sib_tableWidget.resizeColumnsToContents()
                if self.sib_tableWidget.item(j, 0) != None:
                    self.sib_tableWidget.item(j, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sib_tableWidget.item(j, 1) != None:
                    self.sib_tableWidget.item(j, 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sib_tableWidget.item(j, 2) != None:
                    self.sib_tableWidget.item(j, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.sib_total_widget.setText(sip_total)
                j += 1
            
            j1 = 0
            for gam in h_gam_list:  # j는 행 c는 열  
                h_dat_2 = gam[2]
                h_vdate_2 = h_dat_2.strftime('%Y-%m-%d')
                h_name2 = gam[1]
                h_amo_int_2 = int(gam[3])
                gam_to += h_amo_int_2
                h_amo_2 = format(h_amo_int_2,",")
                gam_total = format(gam_to,",")
                if j1 != 1:  
                    self.gam_tableWidget.insertRow(j1)

                self.gam_tableWidget.setItem(j1, 0, QTableWidgetItem(h_vdate_2))
                self.gam_tableWidget.setItem(j1, 1, QTableWidgetItem(h_name2))
                self.gam_tableWidget.setItem(j1, 2, QTableWidgetItem(h_amo_2))
                self.gam_tableWidget.resizeColumnsToContents()
                if self.gam_tableWidget.item(j1, 0) != None:
                    self.gam_tableWidget.item(j1, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.gam_tableWidget.item(j1, 1) != None:
                    self.gam_tableWidget.item(j1, 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.gam_tableWidget.item(j1, 2) != None:
                    self.gam_tableWidget.item(j1, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.gam_total_widget.setText(gam_total)
                j1 += 1
            j2 = 0
            for jeol in h_jeolgi_list:  # j는 행 c는 열  
                
                h_jeol_name = str(jeol[0])
                h_dat_3 = jeol[2]
                h_vdate_3 = h_dat_3.strftime('%Y-%m-%d')
                h_name3 = jeol[1]
                h_amo_int_3 = int(jeol[3])
                jeol_to += h_amo_int_3
                h_amo_3 = format(h_amo_int_3,",")
                jeol_total = format(jeol_to,",")
                if j2 != 1:  
                    self.jeol_tableWidget.insertRow(j2)

                self.jeol_tableWidget.setItem(j2, 0, QTableWidgetItem(h_vdate_3))
                self.jeol_tableWidget.setItem(j2, 1, QTableWidgetItem(h_name3))
                self.jeol_tableWidget.setItem(j2, 2, QTableWidgetItem(h_jeol_name))
                self.jeol_tableWidget.setItem(j2, 3, QTableWidgetItem(h_amo_3))
                self.jeol_tableWidget.resizeColumnsToContents()
                if self.jeol_tableWidget.item(j2, 0) != None:
                    self.jeol_tableWidget.item(j2, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.jeol_tableWidget.item(j2, 1) != None:
                    self.jeol_tableWidget.item(j2, 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.jeol_tableWidget.item(j2, 2) != None:
                    self.jeol_tableWidget.item(j2, 2).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.jeol_tableWidget.item(j2, 3) != None:
                    self.jeol_tableWidget.item(j2, 3).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.jeol_total_widget.setText(jeol_total)
                j2 += 1
            j3 = 0
            for sun in h_mission_list:  # j는 행 c는 열  
                
                h_dat_4 = sun[2]
                h_vdate_4 = h_dat_4.strftime('%Y-%m-%d')
                h_name4 = sun[1]
                h_amo_int_4 = int(sun[3])
                sun_to += h_amo_int_4
                h_amo_4 = format(h_amo_int_4,",")
                sun_total = format(sun_to,",")
                if j3 != 1:  
                    self.sun_tableWidget.insertRow(j3)

                self.sun_tableWidget.setItem(j3, 0, QTableWidgetItem(h_vdate_4))
                self.sun_tableWidget.setItem(j3, 1, QTableWidgetItem(h_name4))
                self.sun_tableWidget.setItem(j3, 2, QTableWidgetItem(h_amo_4))
                self.sun_tableWidget.resizeColumnsToContents()
                if self.sun_tableWidget.item(j3, 0) != None:
                    self.sun_tableWidget.item(j3, 0).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sun_tableWidget.item(j3, 1) != None:
                    self.sun_tableWidget.item(j3, 1).setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                if self.sun_tableWidget.item(j3, 2) != None:
                    self.sun_tableWidget.item(j3,2).setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                self.sun_total_widget.setText(sun_total)
                j3 += 1
           
            hun_to = sip_to + gam_to + jeol_to + sun_to
            hun_total = format(hun_to,",")
            self.hun_total_widget.setText(hun_total)

    def closeEvent(self, event):
        self.registed_name.clear()
        self.serch_method_combo_widget.clear()
        self.serch_code_widget.clear()
        self.sum_name_code_widget.clear()
        self.reset_button()
        event.accept()

    def close_window(self):
        self.registed_name.clear()
        self.serch_method_combo_widget.clear()
        self.serch_code_widget.clear()
        self.sum_name_code_widget.clear()
        self.reset_button()
        self.close()

   
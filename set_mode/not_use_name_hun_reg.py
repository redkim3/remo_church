import os,pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import *
import configparser
from basic.not_use_p_name import not_use_personal_name_hun
# from basic.hun_name_2 import  gubun_mok_values

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()

today = QDate.currentDate()
Y1 = str(today.year())

imsi = []; n = 0

form_class = uic.loadUiType("ui/Not_use_p_name_form.ui")[0]
j = 1
class not_use_name_hunRegister(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('개별이름을 사용하지 않는 헌금목록 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        not_hun_name = not_use_personal_name_hun()
        self.registed_not_use_hun_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        set_row = len(not_hun_name)
        self.registed_not_use_hun_tableWidget.setRowCount(set_row)
        self.hun_gubun_combobox()
        self.gubun_comboBox_widget.currentTextChanged.connect(self.hun_name_combo)
        self.not_use_hun_combo_widget.currentTextChanged.connect(self.not_use_hun_reg_input)

        self.registed_not_use_hun_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #87CEEB; }")  # 선택된 행의 배경색을 빨간색으로 설정
        
        for j in range(set_row): #set_row):  # j는
            registed_data = not_hun_name[j]
            self.registed_not_use_hun_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))

        self.new_not_use_hun_tableWidget.setRowCount(1)
        self.new_not_use_hun_tableWidget.setColumnWidth(0, 125)
        self.not_use_hun_combo_widget.currentText()

    
    def acc_button(self):
        addgubun_button = QPushButton("신규등록 추가")
        addgubun_button.clicked.connect(self.not_use_hun_reg_input)
        
        gubun_view_button = QPushButton("다시보기")
        gubun_view_button.clicked.connect(self.registed_data)
        delete_selected_row_button = QPushButton("선택행삭제")
        delete_selected_row_button.clicked.connect(self.delete_selected_row)

        file_save_button = QPushButton("저장")
        file_save_button.clicked.connect(self.file_save)
        gubuncancel_button = QPushButton("종료(저장취소)")
        gubuncancel_button.clicked.connect(self.file_save_cancel)

    def hun_gubun_combobox(self):  # 헌금명칭을 넣고 나면 진행하는것
        from basic.hun_name_2 import gubun_values
        self.gubun_comboBox_widget.blockSignals(True)
        self.gubun_comboBox_widget.clear()  # 회계구분 명칭(선교회계,일반회계,특별회계)

        gubun_value = gubun_values()
        self.gubun_comboBox_widget.addItems(['선택'] + gubun_value)
        self.gubun_comboBox_widget.blockSignals(False)
    
    def hun_name_combo(self):
        from basic.hun_name_2 import  gubun_mok_values
        self.not_use_hun_combo_widget.blockSignals(True)
        self.not_use_hun_combo_widget.clear()  # 헌금 명칭 콤보
        try:
            gubun = self.gubun_comboBox_widget.currentText()
            self.not_use_hun_combo_widget.addItems(['선택'] + gubun_mok_values(Y1,gubun))  #  콤보 데이터 추가 

        except TypeError:
            pass
            # QMessageBox.about(self, "입력오류","입력내용을 확인 하세요")
        self.not_use_hun_combo_widget.blockSignals(False)

    def registed_data(self):
        not_hun_name = not_use_personal_name_hun()
        self.registed_not_use_hun_tableWidget.setColumnWidth(0, 125) # 컬럼 폭조정 [출처] 파이큐티(PyQt5)의 QTableWidget|작성자 anakt
        set_row = len(not_hun_name)
        self.registed_not_use_hun_tableWidget.setRowCount(set_row)
        for j in range(set_row): #set_row):  # j는
            registed_data = not_hun_name[j]
            self.registed_not_use_hun_tableWidget.setItem(j,0,QTableWidgetItem(registed_data))

    def delete_selected_row(self):
        global j

        selected_items = self.registed_not_use_hun_tableWidget.selectedItems()
        table_name = 'not_use_p_name' 
        if selected_items:
            # 행을 선택하면 여러 열이 선택될 수 있으므로, 여러 선택된 아이템 중에서 첫 번째 아이템의 행 인덱스를 사용합니다.
            row_index = self.registed_not_use_hun_tableWidget.row(selected_items[0])
            
            if row_index != -1 and self.registed_not_use_hun_tableWidget.item(row_index, 0) != None:
                selected_data = self.registed_not_use_hun_tableWidget.item(row_index, 0).text()

            # 데이터베이스 연결
            conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
            cur = conn.cursor()

            try:
                # 데이터 삭제 쿼리 실행
                delete_not_use_name_sql = 'delete from {} where hun_name = %s'.format(table_name)
                cur.execute(delete_not_use_name_sql,(selected_data,))

                # 테이블 위젯에서 선택된 행 삭제
                self.registed_not_use_hun_tableWidget.removeRow(row_index)

                # 변경사항을 데이터베이스에 반영
                conn.commit()
                QMessageBox.about(self, '삭제', '데이터가 성공적으로 삭제되었습니다.')
            except pymysql.Error as e:
                QMessageBox.critical(self, '에러', f'데이터 삭제 중 오류 발생: {e}')
            finally:
                # 데이터베이스 연결 해제
                conn.close()
        
    def not_use_hun_reg_input(self):
        global j
        registed_data =not_use_personal_name_hun()
        hun_name = self.not_use_hun_combo_widget.currentText()
        try:
            if hun_name != '선택':
                if j != 1:
                    self.new_not_use_hun_tableWidget.insertRow(j-1)
                hun_name = self.not_use_hun_combo_widget.currentText()
                if hun_name in registed_data:
                    QMessageBox.about(self,'입력오류','동일한 이름의 헌금이 있습니다.!!!')
                    self.not_use_hun_combo_widget.setCurrentText("선택")
                    self.not_use_hun_combo_widget.setFocus()
                    return
                
                if hun_name =='':
                    QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')
                    if j != 1:
                        j -= 1

                self.new_not_use_hun_tableWidget.setItem((j-1),0,QTableWidgetItem(hun_name))
                # self.not_use_hun_combo_widget.setCurrentText('선택') 
                self.not_use_hun_combo_widget.setFocus()
                j += 1
        
        except ValueError:
            QMessageBox.about(self,'입력오류','신규 등록 내용이 없습니다!!')

    def file_save_cancel(self):
        self.new_not_use_hun_tableWidget.clearContents()
        self.close()
    
    def closeEvent(self, event):
        self.new_not_use_hun_tableWidget.clearContents()
        event.accept()
        
    def file_save(self):
        global j
        rowCount = self.new_not_use_hun_tableWidget.rowCount()
    
        conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
        cur = conn.cursor()

        # 데이터 설정
        imsi=[]
        db_name = 'not_use_p_name' # 테이블 명칭임
        rowCount = self.new_not_use_hun_tableWidget.rowCount()
        #try:
        if rowCount > 0:
            for i in range(rowCount):

                    not_use_hun_name = self.new_not_use_hun_tableWidget.item(i, 0).text()
                    imsi.append([not_use_hun_name])

            for data in imsi:
                not_use_hun_name_sql = "INSERT INTO {} (hun_name) VALUES (%s);".format(db_name)
                cur.execute(not_use_hun_name_sql, (data))  # (data)로 하고 쿼리문에서 hun_name 컬람에만 데이터를 넣도록 넣어준다
            QMessageBox.about(self,'저장',"' 저장되었습니다.!!!")

            conn.commit()
            conn.close()
            # self.new_not_use_hun_tableWidget.clearContents()
            self.new_not_use_hun_tableWidget.setRowCount(0)
            self.new_not_use_hun_tableWidget.setRowCount(1)
            self.not_use_hun_combo_widget.setCurrentText("선택")
            j = 1
            self.registed_data()
            self.not_use_hun_combo_widget.setFocus()
        else:
            QMessageBox.about(self,'저장',"저장할 내용이 없습니다.!!!")
    
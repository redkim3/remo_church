import sys, os, warnings, configparser
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem

from login import LoginDialog
from menu.budget_register_menu import budgetRegister_menu
from menu.hun_cost_menu import hun_cost_menu

from menu.bogoseo_menu import bogoseo_menu
from menu.detail_view_menu import detail_view_menu
from menu.contribution_menu import contribution_menu

from menu.outside_connect_menu import outside_connect_menu 
from basic.bank_account import banklist, cardlist
from menu.setmode_menu import Basic_accounting_menu
from menu.network_mode_menu import NetWork_mode_menu

warnings.filterwarnings("ignore", category=DeprecationWarning)
config = configparser.ConfigParser()
config.read(r'./register/config.ini')
ch_name = config['Church_name']['name']
cur_fold = os.getcwd()

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_dialog = LoginDialog()
        if self.login_dialog.exec_() == QDialog.Accepted:
            self.logged_in_user = self.login_dialog.username_entry.text()  # 사용자명을 가져와서 저장합니다.
            self.initUI()
        else:
            sys.exit() # 프로그램을 종료합니다.  

    def initUI(self):
        pixmap = QPixmap("./img/logo.png")
        # 이미지를 넣을 라벨 생성 
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(250, 300, pixmap.width(), pixmap.height())
        label.setAlignment(Qt.AlignCenter)  # 이미지를 가운데 정렬 
        self.resize(pixmap.width(), pixmap.height())  # 윈도우 크기를 이미지 크기에 맞게 조정

        self.resize(950,600)
        self.setWindowTitle(f'{ch_name} 헌금 및 지출등록 시스템')
        self.setStyleSheet("font-size : 17px ")

        self.setMenuBar(QMenuBar(self))
        self.sub_window = None
        menuBar = self.menuBar() # 
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        budgetRegister_menu(menuBar, self)
        hun_cost_menu(menuBar, self)

        bogoseo_menu(menuBar, self)
        detail_view_menu(menuBar, self)
        contribution_menu(menuBar, self)
        outside_connect_menu(menuBar, self)
        Basic_accounting_menu(menuBar, self)
        NetWork_mode_menu(menuBar, self)
        self.setStyleSheet("font-size : 17px ")

        bankaccount = banklist()
        self.bank_tableWidget = QTableWidget(self)
        self.bank_tableWidget.resize(350,200)
        self.bank_tableWidget.move(70, 60)
        self.bank_tableWidget.setRowCount(len(bankaccount))
        self.bank_tableWidget.setColumnCount(len(bankaccount[0]))
        column_headers = ['은행명', '계좌번호', '사용부서']
        self.bank_tableWidget.setHorizontalHeaderLabels(column_headers)
        self.bank_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 불능 
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked) # 더블클릭으로 수정가능 
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers) #클릭, 더블클릭 으로 수정가능
        self.bank_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bank_tableWidget.setStyleSheet("font-size : 17px ")

        for i, row in enumerate(bankaccount):
            for j, item in enumerate(row):
                self.bank_tableWidget.setItem(i, j, QTableWidgetItem(item))    
        
        cardview = cardlist()
        self.card_tableWidget = QTableWidget(self)
        self.card_tableWidget.resize(360, 200)
        self.card_tableWidget.move(440, 60)
        self.card_tableWidget.setRowCount(len(cardview))
        self.card_tableWidget.setColumnCount(len(cardview[0]))
        column_headers_2 = ['은행명', '카드번호', '사용부서']
        self.card_tableWidget.setHorizontalHeaderLabels(column_headers_2)
        self.bank_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 불능
        self.card_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.card_tableWidget.setStyleSheet("font-size : 17px ")
        
        for i, row in enumerate(cardview):
            for j, item in enumerate(row):
                self.card_tableWidget.setItem(i, j, QTableWidgetItem(item))  
        
        self.show()

    def handle_exception(exc_type, exc_value, exc_traceback):
        from menu.menu_sql import sql_on_close
        # 예외가 발생하면 sql_on_close 호출  
        if issubclass(exc_type, KeyboardInterrupt):
            # 키보드 인터럽트는 무시 
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        sql_on_close()
        print(f"Uncaught exception: {exc_value}", file=sys.stderr)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def closeEvent(self,event):
        from menu.menu_sql import sql_on_close
        sql_on_close()
        event.accept()

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    sys.exit(app.exec_())
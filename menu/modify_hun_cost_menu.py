from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction  #  QMenu, qApp #,  QLabel
from PyQt5.QtGui import QIcon


def Modify_Hun_cost_munu(menu: QMenuBar, window: QMainWindow):
        from modify.hun_modify import Hun_modify
        from modify.cost_modify import Cost_Modify
        # from register.other_reg import OtherIncomeRegister

        window.modify_menu = menu.addMenu('헌금 및 지출 수정')

        action1_1 = QAction("헌금수정", window)
        action1_2 = QAction("지출수정", window)
        #action1_3 = QAction("기타수입 등록", window) 

        window.modify_menu.addAction(action1_1) # ("헌금등록")
        window.modify_menu.addSeparator()
        window.modify_menu.addAction(action1_2)
        # window.modify_menu.addSeparator()
        # window.modify_menu.addAction(action1_3)
        # window.modify_menu.addSeparator()

        window.modify_menu.hun_modify = Hun_modify()
        window.modify_menu.cost_modify = Cost_Modify()
        # window.modify_menu.other_income_register = OtherIncomeRegister()

        action1_1.triggered.connect(window.modify_menu.hun_modify.show)
        action1_2.triggered.connect(window.modify_menu.cost_modify.show)
        # action1_3.triggered.connect(window.modify_menu.other_income_register.show)

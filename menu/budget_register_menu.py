from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction, QMenu, qApp #,  QLabel
from PyQt5.QtGui import QIcon

def budgetRegister_menu(menu: QMenuBar, window: QMainWindow):
        from budget.budget_income_reg import BudgetIncome_Register
        from budget.budget_cost_reg import BudgetCost_Register
        from budget.budget_view import Budget_View

        window.register_menu = menu.addMenu('예산등록')

        action0_1 = QAction("수입예산등록", window)
        action0_2 = QAction("지출예산등록", window)
        action0_3 = QAction("예산보기", window)
                
        window.register_menu.addAction(action0_1) # ("헌금등록")
        window.register_menu.addSeparator()
        window.register_menu.addAction(action0_2)
        window.register_menu.addSeparator()
        window.register_menu.addAction(action0_3)
        window.register_menu.addSeparator()
        

        window.register_menu.budget_income_register = BudgetIncome_Register()
        window.register_menu.budget_cost_register = BudgetCost_Register()
        window.register_menu.budget_view = Budget_View()
        
        action0_1.triggered.connect(window.register_menu.budget_income_register.show)
        action0_2.triggered.connect(window.register_menu.budget_cost_register.show)
        action0_3.triggered.connect(window.register_menu.budget_view.show)
        
        

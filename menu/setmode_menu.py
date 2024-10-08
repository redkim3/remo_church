from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

def Basic_accounting_menu(menu: QMenuBar, window: QMainWindow):
    from set_mode.regist_member import memberRegister
    from serch.serch_member import Serch_Member
    from set_mode.acc_gubun_reg import acc_gubunRegister
    from set_mode.hun_hang_register import hun_hangRegister
    from set_mode.hun_mok_register import hun_mokRegister
    from set_mode.hun_semok_register import hun_semokRegister
    from set_mode.cost_hang_register import cost_hangRegister
    from set_mode.cost_mok_register import cost_mokRegister
    from set_mode.cost_semok_register import cost_semokRegister
    from payed_account.payed_account_register import payed_accountRegister 
    from payed_account.payed_account_view import Payed_AccountView 
    from set_mode.not_use_name_hun_reg import not_use_name_hunRegister
    from register.bank_reg import Bank_Register
    from register.card_reg import Card_Register

    menu_setup = menu.addMenu("회계설정")

    accounting_basic_menu = menu_setup.addMenu("재정 기초등록사항")
    sub_action_acc_gubun = QAction("회계구분 입력", window) 
    accounting_basic_menu.addAction(sub_action_acc_gubun)
    hun_list_menu = accounting_basic_menu.addMenu("헌금목록등록")
    cost_list_menu = accounting_basic_menu.addMenu("지출목록등록")  
    sub_action_payed_account = QAction("지급계좌 입력", window)
    sub_action_payed_account_view = QAction("지급계좌 보기", window)
    accounting_basic_menu.addAction(sub_action_payed_account)
    accounting_basic_menu.addAction(sub_action_payed_account_view)
    sub_action_not_use_name_hun = QAction("성도명 미기입 헌금", window)
    accounting_basic_menu.addAction(sub_action_not_use_name_hun)
    
    action_hun_hang = QAction("헌금 항 입력", window)
    action_hun_mok = QAction("헌금 목 입력", window)
    action_hun_semok = QAction("헌금 세목 입력", window)

    # QAction을 '헌금목록등록' 메뉴에 추가
    hun_list_menu.addAction(action_hun_hang)
    hun_list_menu.addAction(action_hun_mok)
    hun_list_menu.addAction(action_hun_semok)

    menu_setup.acc_gubun_register = acc_gubunRegister()
    menu_setup.hun_hang_register = hun_hangRegister()
    menu_setup.hun_mok_register = hun_mokRegister()
    menu_setup.hun_semok_register = hun_semokRegister()

    action_cost_hang = QAction("지출 항 입력", window)
    action_cost_mok = QAction("지출 목 입력", window)
    action_cost_semok = QAction("지출 세목 입력", window)

    cost_list_menu.addAction(action_cost_hang)
    cost_list_menu.addAction(action_cost_mok)
    cost_list_menu.addAction(action_cost_semok)
    
    menu_setup.cost_hang_register = cost_hangRegister()
    menu_setup.cost_mok_register = cost_mokRegister()
    menu_setup.cost_semok_register = cost_semokRegister()
    menu_setup.payed_account_register = payed_accountRegister()
    menu_setup.payed_account_view = Payed_AccountView()
    menu_setup.sub_action_not_use_name_hun_register = not_use_name_hunRegister()

    sub_action_acc_gubun.triggered.connect(menu_setup.acc_gubun_register.show)
    action_hun_hang.triggered.connect(menu_setup.hun_hang_register.show)
    action_hun_mok.triggered.connect(menu_setup.hun_mok_register.show)
    action_hun_semok.triggered.connect(menu_setup.hun_semok_register.show)

    action_cost_hang.triggered.connect(menu_setup.cost_hang_register.show)
    action_cost_mok.triggered.connect(menu_setup.cost_mok_register.show)
    action_cost_semok.triggered.connect(menu_setup.cost_semok_register.show)
    
    sub_action_payed_account.triggered.connect(menu_setup.payed_account_register.show)
    sub_action_payed_account_view.triggered.connect(menu_setup.payed_account_view.show)
    sub_action_not_use_name_hun.triggered.connect(menu_setup.sub_action_not_use_name_hun_register.show)
    
    batang_basic_menu = menu_setup.addMenu("바탕 자료 수정")

    action_account_modify = QAction("계좌번호 수정", window)  
    action_card_modify = QAction("카드번호 수정", window)

    batang_basic_menu.addAction(action_account_modify)
    batang_basic_menu.addAction(action_card_modify)

    menu_setup.bank_account_register = Bank_Register()
    menu_setup.card_account_register = Card_Register()

    action_account_modify.triggered.connect(menu_setup.bank_account_register.show)
    action_card_modify.triggered.connect(menu_setup.card_account_register.show)

    regist_member = QAction("성도등록", window)

    # menu_setup에 regist_member를 추가합니다.
    menu_setup.addAction(regist_member)
    menu_setup.regist_member =  memberRegister()
    # regist_member이 트리거될 때 실행할 동작을 정의합니다.
    regist_member.triggered.connect(menu_setup.regist_member.show)

    serch_member = QAction("성도검색", window)

    # menu_setup에 regist_member를 추가합니다.
    menu_setup.addAction(serch_member)
    menu_setup.serch_member =  Serch_Member()
    # regist_member이 트리거될 때 실행할 동작을 정의합니다.
    serch_member.triggered.connect(menu_setup.serch_member.show)

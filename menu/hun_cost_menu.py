from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction  #  QMenu, qApp #,  QLabel
from PyQt5.QtGui import QIcon
import configparser, hashlib
# import datetime

def hun_cost_menu(menu: QMenuBar, window: QMainWindow):
     from register.hun_reg_front import HungumRegister
     from register.cost_reg import Cost_register
     from register.other_reg import OtherIncomeRegister
     from modify.hun_modify import Hun_modify
     from modify.cost_modify import Cost_Modify
     from register.special_account_reg import SpecialAccountRegister
     
     confirm_data = user_confirm()
     special_check = confirm_data # 특별회계
     ok = user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다. 

     window.register_menu = menu.addMenu('헌금 및 지출등록')
     action1_1 = QAction("헌금등록", window)
     action1_2 = QAction("지출등록", window)
     action1_3 = QAction("기타소득 등록", window)
     action1_4 = QAction("특별회계 등록", window)
     
     window.register_menu.addAction(action1_1) # ("헌금등록")
     window.register_menu.addSeparator()
     window.register_menu.addAction(action1_2)
     window.register_menu.addSeparator()
     window.register_menu.addAction(action1_3)
     window.register_menu.addSeparator()
     window.register_menu.addSeparator()
     if special_check == ok:
        window.register_menu.addAction(action1_4)
        window.register_menu.addSeparator()
     window.register_menu.addSeparator()
     
     window.register_menu.hun_register = HungumRegister()
     window.register_menu.cost_register = Cost_register()
     window.register_menu.other_income_register = OtherIncomeRegister()
     
     
     action1_1.triggered.connect(window.register_menu.hun_register.show)
     action1_2.triggered.connect(window.register_menu.cost_register.show)
     action1_3.triggered.connect(window.register_menu.other_income_register.show)
     if special_check == ok:
        window.register_menu.special_account_register = SpecialAccountRegister()
        action1_4.triggered.connect(window.register_menu.special_account_register.show)
     
     action1_1 = QAction("헌금수정", window)
     action1_2 = QAction("지출수정", window)
     window.register_menu.addAction(action1_1) # ("헌금등록")
     window.register_menu.addSeparator()
     window.register_menu.addAction(action1_2)
     window.register_menu.hun_modify = Hun_modify()
     window.register_menu.cost_modify = Cost_Modify()
     # window.register_menu.other_income_register = OtherIncomeRegister()
     action1_1.triggered.connect(window.register_menu.hun_modify.show)
     action1_2.triggered.connect(window.register_menu.cost_modify.show)
     # action1_3.triggered.connect(window.register_menu.other_income_modify.show)
     

def user_confirm():
    from user.for_user_sql import user_infor_sql
    config = configparser.ConfigParser()
    config.read(r"./register/config.ini")
    user_id = config['user']['user_id']
    user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
    user_name_infor = user_info[0]        # 이름을 가져오고
    user_name = user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
    special_value = str(user_name_infor[3])       # user_reg_check의 권한을 가져와서
    special_check = user_infor_hash(special_value)
    config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    config['user'][special_check] = special_check
    
    return special_check # Ge_check, sun_check,

def user_infor_hash(data):
    # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
    hasher = hashlib.sha256()
    # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
    hasher.update(data.encode('utf-8'))
    # 해시된 결과 반환
    return hasher.hexdigest()
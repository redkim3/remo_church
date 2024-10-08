import configparser, hashlib
from register.sending_mail_reg import Sending_mail_Reg
from register.regist_email import email_Register
from outside.send_email import Send_Email
from outside.ch2ch import ch2ch_file_Change

from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction #, QMenu, qApp #,  QLabel
# from PyQt5.QtGui import QIcon

def outside_connect_menu(menu: QMenuBar, window: QMainWindow):

    window.outside_connect_menu = menu.addMenu('외부연결')
    confirm_data = confirm()
    user_reg_check = confirm_data

    ok = user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
    if ok == user_reg_check:
        action7_0 = QAction("보내는메일 등록", window)
        window.outside_connect_menu.addAction(action7_0) # ("보내는메일 등록")
        window.outside_connect_menu.addSeparator()
        window.outside_connect_menu.sending_email_register = Sending_mail_Reg()
        action7_0.triggered.connect(window.outside_connect_menu.sending_email_register.show)

    action7_1 = QAction("이메일등록", window)
    window.outside_connect_menu.addAction(action7_1) # ("이메일 등록")
    window.outside_connect_menu.addSeparator()
    window.outside_connect_menu.email_register = email_Register()
    action7_1.triggered.connect(window.outside_connect_menu.email_register.show)

    action7_2 = QAction("이메일 보내기", window)
    window.outside_connect_menu.addAction(action7_2)
    window.outside_connect_menu.addSeparator()
    window.outside_connect_menu.send_email = Send_Email()
    action7_2.triggered.connect(window.outside_connect_menu.send_email.show)

    action7_3 = QAction("교회웹관리", window)
    window.outside_connect_menu.addAction(action7_3)
    window.outside_connect_menu.addSeparator()
    window.outside_connect_menu.ch2ch_connect = ch2ch_file_Change()
    action7_3.triggered.connect(window.outside_connect_menu.ch2ch_connect.show)

def confirm():
    from user.for_user_sql import user_infor_sql
    config = configparser.ConfigParser()
    config.read(r"./register/config.ini")
    user_id = config['user']['user_id']
    user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
    user_name_infor = user_info[0]        # 이름을 가져오고
    user_name = user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
    user_reg = str(user_name_infor[5])       # user_reg_check의 권한을 가져와서
    # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
    user_reg_check = user_infor_hash(user_reg)  # user_reg_check를 hash화 한다.
    
    config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    config['user'][user_reg_check] = user_reg_check
    
    return user_reg_check

def user_infor_hash(data):
    # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
    hasher = hashlib.sha256()
    # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
    hasher.update(data.encode('utf-8'))
    # 해시된 결과 반환
    return hasher.hexdigest()
from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction, qApp
import configparser, hashlib
from PyQt5.QtGui import QIcon


def NetWork_mode_menu(menu: QMenuBar, window: QMainWindow):
    from user.regist_user import userRegister
    from register.server_change import Server_Change
    from register.church_register import Church_Reg
    from menu.connect_close_sql import update_user_connect

    network_menu_setup = menu.addMenu("데이터 연결설정")
    confirm_data = confirm()
    user_reg_check = confirm_data

    ok = user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
    if ok == user_reg_check:
        user_regist= QAction("사용자등록", window)
        network_menu_setup.addAction(user_regist)  # 메뉴에 서버 등록 액션 추가
        network_menu_setup.user_register = userRegister()
        user_regist.triggered.connect(network_menu_setup.user_register.show)  # QAction의 triggered 시그널과 연결

        church_register = QAction("교회등록", window)
        network_menu_setup.addAction(church_register)  # 메뉴에 서버 등록 액션 추가
        network_menu_setup.church_register = Church_Reg()
        church_register.triggered.connect(network_menu_setup.church_register.show)  # QAction의 triggered 시그널과 연결

    # 서버 등록 액션 생성
    server_change = QAction("서버 변경", window)
    network_menu_setup.addAction(server_change)  # 메뉴에 서버 등록 액션 추가
    network_menu_setup.server_change_register = Server_Change()
    server_change.triggered.connect(network_menu_setup.server_change_register.show)  # QAction의 triggered 시그널과 연결

    if ok == user_reg_check:
        Data_backup= QAction("데이터 백업", window)
        Data_backup.triggered.connect(execute_backup)
        network_menu_setup.addAction(Data_backup)  # 메뉴에 서버 등록 액션 추가 
        # network_menu_setup.Data_backup_register = execute_backup
        # Data_backup.triggered.connect(network_menu_setup.Data_backup_register.show)  # QAction의 triggered 시그널과 연결

    # file_exit = menu.addMenu("종료")
    
    exit_action = QAction('종료', window)
    exit_action.triggered.connect(on_close)
    # exit_action.triggered.connect(lambda: (update_user_connect(user_id), qApp.quit()))
    menu.addAction(exit_action)
    # exit_action.triggered.connect(qApp.quit)

def on_close():
    from menu.menu_sql import sql_on_close
    sql_on_close()
    qApp.quit()

def execute_backup():
    from Data_backup.Data_back import backup_database
    backup_database('isbs2024')

def confirm():
    global user_id
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

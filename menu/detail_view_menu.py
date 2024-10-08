import configparser, hashlib
from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction, QMenu, qApp #,  QLabel
from PyQt5.QtGui import QIcon

def detail_view_menu(menu: QMenuBar, window: QMainWindow):
    from serch_account.serch_account import serch_account
    from serch_account.hun_detail_view import hun_detail_view
    from serch_account.other_income_view import Other_income_View
    from serch_account.special_bank_account_view import Special_bank_account_view
    confirm_data = confirm()  # 결과값 hun_detail_check
    detail_check = confirm_data
    ok = user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.
    
    
    window.detail_view_menu = menu.addMenu("세부내역보기")
    action3_1 = QAction("계정별 원장보기", window)   # 2차 메뉴 생성
    window.detail_view_menu.addAction(action3_1) # ("일반재정 주간보고") 2차메뉴와 1차메뉴연결
    window.detail_view_menu.serch_account_window = serch_account() # 실행 연결
    action3_1.triggered.connect(window.detail_view_menu.serch_account_window.show) #트리거 연결
    window.detail_view_menu.addSeparator()

    if confirm_data[4] == str(1): #detail_chec
        action3_2 = QAction("개인별헌금내역", window)
        window.detail_view_menu.addAction(action3_2)  # 메뉴에 서버 등록 액션 추가
        window.detail_view_menu.hun_detail_view_window = hun_detail_view()
        action3_2.triggered.connect(window.detail_view_menu.hun_detail_view_window.show)
        window.detail_view_menu.addSeparator()
    
    action3_3 = QAction("기타소득내역", window)
    window.detail_view_menu.addAction(action3_3)  # 메뉴에 서버 등록 액션 추가
    window.detail_view_menu.other_income_view_window = Other_income_View()
    action3_3.triggered.connect(window.detail_view_menu.other_income_view_window.show)
    window.detail_view_menu.addSeparator()

    if confirm_data[3] == str(1): #detail_chec
        action3_4 = QAction("특별회계 예금 보기", window)
        window.detail_view_menu.addAction(action3_4)  # 메뉴에 서버 등록 액션 추가
        window.detail_view_menu.special_bank_view_window = Special_bank_account_view()
        action3_4.triggered.connect(window.detail_view_menu.special_bank_view_window.show)
        window.detail_view_menu.addSeparator()



def confirm():
    from user.for_user_sql import user_infor_sql
    config = configparser.ConfigParser()
    config.read(r"./register/config.ini")
    user_id = config['user']['user_id']
    user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
    user_name_infor = user_info[0]        # 이름을 가져오고
    user_name = user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
    hun_detail = str(user_name_infor[4])       # user_reg_check의 권한을 가져와서
    # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
    hun_detail_check = user_infor_hash(hun_detail)  # user_reg_check를 hash화 한다.
    
    config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    config['user'][hun_detail_check] = hun_detail_check
    
    return user_name_infor # hun_detail_check

def user_infor_hash(data):
    # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
    hasher = hashlib.sha256()
    # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
    hasher.update(data.encode('utf-8'))
    # 해시된 결과 반환
    return hasher.hexdigest()
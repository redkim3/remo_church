from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction # , QMenu, qApp #,  QLabel
import configparser, hashlib
# from PyQt5.QtGui import QIcon

def bogoseo_menu(menu: QMenuBar, window: QMainWindow):
    from report.Ge_accounting_report import weekly_Ge_report
    from report.Mission_accounting_report import weekly_mission_report
    from report.Acc_start_Quarter_report import Ge_quarterly_Report
    from report.Quarterly_mission_report import Mi_quarterly_Report
    from report.special_report import Special_quarterly_Report
    from report.special_financial_report import Special_financial_Report

    confirm_data = user_confirm()
    Ge_check = confirm_data[0] # 일반회계
    sun_check = confirm_data[1] # 선교회계
    special_check = confirm_data[2] # 선교회계

    ok = user_infor_hash(str(1))  # 1의 해시 값을 받아서 if에서 비교한다.

    window.report_menu = menu.addMenu("보고서")
    if Ge_check == ok:
        action2_1 = QAction("일반재정 주간보고", window)
        window.report_menu.addAction(action2_1) # ("일반재정 주간보고")
        window.report_menu.Ge_accounting_report_window = weekly_Ge_report()
        action2_1.triggered.connect(window.report_menu.Ge_accounting_report_window.show)
        
    if sun_check == ok:
        action2_2 = QAction("선교회계 주간보고", window)
        window.report_menu.addAction(action2_2) # ("선교회계 주간보고")
        window.register_menu.Mission_accounting_report_window = weekly_mission_report()
        action2_2.triggered.connect(window.register_menu.Mission_accounting_report_window.show)

    if Ge_check == ok:
        window.report_menu.addSeparator()
        action2_3 = QAction("일반재정 결산보고", window)
        window.report_menu.addAction(action2_3) # ("일반재정 결산보고")
        window.report_menu.Quaterly_Ge_report_window = Ge_quarterly_Report()
        action2_3.triggered.connect(window.report_menu.Quaterly_Ge_report_window.show)
        
    if sun_check == ok:
        action2_4 = QAction("선교회계 결산보고", window)
        window.report_menu.addAction(action2_4) # ("선교회계 결산보고")
        window.report_menu.Quaterly_Mi_report_window = Mi_quarterly_Report()
        action2_4.triggered.connect(window.report_menu.Quaterly_Mi_report_window.show)
    
    if special_check == ok:
        window.report_menu.addSeparator()
        action2_5 = QAction("특별회계 결산보고", window)
        window.report_menu.addAction(action2_5) # ("선교회계 결산보고")
        window.report_menu.Quaterly_special_report_window = Special_quarterly_Report()
        action2_5.triggered.connect(window.report_menu.Quaterly_special_report_window.show)

    if special_check == ok:
        window.report_menu.addSeparator()
        action2_6 = QAction("특별회계 재정현황", window)
        window.report_menu.addAction(action2_6) # ("선교회계 결산보고")
        window.report_menu.special_financial_report_window = Special_financial_Report()
        action2_6.triggered.connect(window.report_menu.special_financial_report_window.show)

def user_confirm():
    from user.for_user_sql import user_infor_sql
    config = configparser.ConfigParser()
    config.read(r"./register/config.ini")
    user_id = config['user']['user_id']
    user_info = user_infor_sql(user_id)  # user_id로 정보를 가져온다
    user_name_infor = user_info[0]        # 이름을 가져오고
    user_name = user_infor_hash(user_name_infor[0])  # 이름을 해시 한다.
    Ge_value = str(user_name_infor[1])       # user_reg_check의 권한을 가져와서
    sun_value = str(user_name_infor[2])       # user_reg_check의 권한을 가져와서
    special_value = str(user_name_infor[3])       # user_reg_check의 권한을 가져와서
    # user_reg = str(user_info[5])       # user_reg_check의 권한을 가져와서
    Ge_check = user_infor_hash(Ge_value)  # user_reg_check를 hash화 한다.
    sun_check = user_infor_hash(sun_value)
    special_check = user_infor_hash(special_value)
                               
    config['user'][user_name] = user_name # 해시화된 이름을 저장한다.
    config['user'][Ge_check] = Ge_check
    config['user'][sun_check] = sun_check
    config['user'][special_check] = special_check
    
    return Ge_check, sun_check, special_check

def user_infor_hash(data):
    # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
    hasher = hashlib.sha256()
    # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
    hasher.update(data.encode('utf-8'))
    # 해시된 결과 반환
    return hasher.hexdigest()

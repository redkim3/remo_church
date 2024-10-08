import sys
from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction


def basic_register_menu(menu: QMenuBar, window: QMainWindow):
        from set_mode.acc_gubun_reg import acc_gubunRegister
        from set_mode.hun_hang_register import hun_hangRegister
        from set_mode.cost_hang_register import cost_hangRegister
        from set_mode.hun_mok_register import hun_mokRegister
        from set_mode.cost_mok_register import cost_mokRegister
        from set_mode.cost_semok_register import cost_semokRegister
        from set_mode.hun_semok_register import hun_semokRegister

        window.basic_register_menu = menu.addMenu("재정기초 등록사항")  # 상단의 메인메뉴에 기초 등록사항 추가
        action5 = QAction("회계구분 입력", window) # 하위 메뉴 생성
        action5_1 = QAction("헌금 항 입력", window) # 하위 메뉴 생성
        action5_2 = QAction("헌금 목 입력", window)
        action5_3 = QAction("헌금 세목 입력", window)
        action5_11 = QAction("지출 항 입력", window) # 하위 메뉴 생성
        action5_12 = QAction("지출 목 입력", window)
        action5_13 = QAction("지출 세목 입력", window)

        window.basic_register_menu.addAction(action5)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addSeparator()
        window.basic_register_menu.addAction(action5_1)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addAction(action5_2)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addAction(action5_3)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addSeparator()
        window.basic_register_menu.addAction(action5_11)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addAction(action5_12)  # 1차 메뉴와 2차 메뉴 연결
        window.basic_register_menu.addAction(action5_13)  # 1차 메뉴와 2차 메뉴 연결

        window.basic_register_menu.acc_gubun_register = acc_gubunRegister() # 실행 연결
        window.basic_register_menu.hun_hang_register = hun_hangRegister() # 실행 연결
        window.basic_register_menu.hun_mok_register = hun_mokRegister() # 실행 연결
        window.basic_register_menu.hun_semok_register = hun_semokRegister() # 실행 연결
        window.basic_register_menu.cost_hang_register = cost_hangRegister() # 실행 연결
        window.basic_register_menu.cost_mok_register = cost_mokRegister() # 실행 연결
        window.basic_register_menu.cost_semok_register = cost_semokRegister() # 실행 연결

        action5.triggered.connect(window.basic_register_menu.acc_gubun_register.show) #트리거 연결
        action5_1.triggered.connect(window.basic_register_menu.hun_hang_register.show) #트리거 연결
        action5_2.triggered.connect(window.basic_register_menu.hun_mok_register.show) #트리거 연결
        action5_3.triggered.connect(window.basic_register_menu.hun_semok_register.show) #트리거 연결
        action5_11.triggered.connect(window.basic_register_menu.cost_hang_register.show) #트리거 연결
        action5_12.triggered.connect(window.basic_register_menu.cost_mok_register.show) #트리거 연결
        action5_13.triggered.connect(window.basic_register_menu.cost_semok_register.show) #트리거 연결

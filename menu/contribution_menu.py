from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction #, QMenu, qApp #,  QLabel
from PyQt5.QtGui import QIcon

def contribution_menu(menu: QMenuBar, window: QMainWindow):
        from contribution.contribution import contribution_issue_go
        from contribution.contribution_serch import contributionSerch
        from contribution.contribution_list import contributionListView

        window.contribution_menu = menu.addMenu("기부금영수증")
        action4_1 = QAction("기부금영수증발행",window)  # 1차 메뉴 생성
        action4_2 = QAction("기부금발행검색",window)  # 1차 메뉴 생성
        action4_3 = QAction("기부금영수증 발행 리스트",window)  # 1차 메뉴 생성

        window.contribution_menu.addAction(action4_1)  #2차메뉴와 1차 메뉴 연결
        window.contribution_menu.addAction(action4_2)
        window.contribution_menu.addAction(action4_3)
        
        window.contribution_menu.contribution_issue = contribution_issue_go() # 실행 연결
        window.contribution_menu.contribution_Serch = contributionSerch() # 실행 연결
        window.contribution_menu.list_view = contributionListView() # 실행 연결

        action4_1.triggered.connect(window.contribution_menu.contribution_issue.show) #트리거 연결
        action4_2.triggered.connect(window.contribution_menu.contribution_Serch.show) #트리거 연결
        action4_3.triggered.connect(window.contribution_menu.list_view.show) #트리거 연결

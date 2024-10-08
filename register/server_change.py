import os
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import configparser
from PyQt5.QtWidgets import *

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
cur_fold = os.getcwd()

form_class = uic.loadUiType("./ui/server_change.ui")[0]

class Server_Change(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('서버 설정 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        host_name = config['MySQL']['host']
        self.server_name_widget.setText(host_name)

    def Button(self):
        server_save_Button = QPushButton("저장")
        server_save_Button.clicked.connect(self.server_save)

        # 닫기 버튼 연결
        close_Button = QPushButton("종료")
        close_Button.clicked.connect(self.close)

    def server_save(self):
        # 새로운 호스트 이름과 비밀번호를 config 파일에 저장
        new_host = self.server_name_widget.text()

        config['MySQL']['host'] = new_host

        # 설정 파일 저장(register 폴더에 저장됨)
        with open(r"./register/config.ini", 'w') as config_file:
            config.write(config_file)

        # 저장 완료 메시지 표시
        QMessageBox.information(self, "저장 완료", "서버 설정이 저장되었습니다.")
        self.close_exit()

    def close_exit(self):
        self.server_name_widget.clear()
        self.close()
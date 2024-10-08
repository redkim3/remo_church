from PyQt5 import uic
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from configparser import ConfigParser

from PyQt5.QtWidgets import *

config = ConfigParser()
config.read(r"./register/config.ini")
cur_fold = os.getcwd()
# form_class = uic.loadUiType("./ui/sending_mail_reg.ui")[0]
form_class = uic.loadUiType(os.path.join(cur_fold, 'ui', 'sending_mail_reg.ui'))[0]
class Sending_mail_Reg(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('발송메일 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        sending_email = config['e_mail']['sending_email']
        pw = config['e_mail']['my_pw']
        SMTP = config['e_mail']['smtp_server']
        PORT = config['e_mail']['smtp_port']
        
        self.sending_mail_addr_widget.setText(sending_email)
        self.sending_pw_widget.setText(pw)
        self.sending_mail_smtp_widget.setText(SMTP)
        self.sending_port_widget.setText(PORT)
        self.sending_pw_widget.setEchoMode(QtWidgets.QLineEdit.Password)

    def Button(self):
        save_Button = QPushButton("저장")
        save_Button.clicked.connect(self.email_save)

        # 닫기 버튼 연결
        close_Button = QPushButton("종료")
        close_Button.clicked.connect(self.close_exit)

    def email_save(self):
        # 기존 설정 파일 열기
        config = ConfigParser()
        config.read(r"./register/config.ini")

        # 새로운 호스트 이름과 비밀번호를 config 파일에 저장
        new_sending_mail = self.sending_mail_addr_widget.text()
        new_pw = self.sending_pw_widget.text()
        new_smtp = self.sending_mail_smtp_widget.text()
        new_smtp_port = self.sending_port_widget.text()
        
        
        # 기존설정이 있으면 설정 파일에서 이름을 변경
        
        config['e_mail']['sending_email'] = new_sending_mail
        config['e_mail']['my_pw'] = new_pw
        config['e_mail']['smtp_server'] = new_smtp
        config['e_mail']['smtp_port'] = new_smtp_port
        
        
        # 설정 파일 저장
        with open(r"./register/config.ini", 'w') as config_file:
            config.write(config_file)
        # 저장 완료 메시지 표시
        QMessageBox.information(self, "저장 완료", "보내는 메일 등록이 변경 되었습니다.")

    def close_exit(self):
        self.sending_mail_addr_widget.clear()
        self.sending_pw_widget.clear()
        self.close()
import os, hashlib
from PyQt5.QtGui import QIcon, QFont #, QPixmap
from PyQt5.QtWidgets import *

import configparser
import pymysql

cur_fold = os.getcwd()
# Location = os.path.join(cur_fold, "cont_issue") # 챗GPT 수정

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.initUI()
        # self.setStyleSheet("font-size : 20px ")

    def initUI(self):
        font1 = QFont()
        font1.setFamily("Arial")
        font1.setPixelSize(17)  # 픽셀 단위로 크기 지정

        font2 = QFont()
        font2.setFamily("Arial")
        font2.setPixelSize(17)  # 픽셀 단위로 크기 지정

        font3 = QFont()
        font3.setFamily("Arial")
        font3.setPixelSize(10)  # 픽셀 단위로 크기 지정

        self.username_label = QLabel("아이디:")
        self.username_label.setFont(font1)

        self.username_entry = QLineEdit()
        self.username_entry.setFont(font2)

        self.password_label = QLabel("비밀번호:")
        self.password_label.setFont(font1)

        self.password_entry = QLineEdit()
        self.password_entry.setFont(font2)
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("로그인")
        self.login_button.setFont(font2)
        self.login_button.clicked.connect(self.login)
        
        self.server_change_label = QLabel("서버가 변경되었을 경우 서버설정을 변경하세요")
        self.server_change_label.setFont(font3)
        self.server_button = QPushButton("서버설정")
        self.server_button.clicked.connect(self.Server_Change)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)
        # 여기에 빈줄이 생길까?
        layout.addSpacing(20)
        layout.addWidget(self.server_change_label)
        layout.addWidget(self.server_button)

        self.setLayout(layout)

    def Server_Change(self):
        from register.server_change import Server_Change
        # Server_Change()
        dialog = Server_Change()
        dialog.exec_()

    def login(self):
        user_id = self.username_entry.text()
        # password = self.password_entry.text()
        password_raw = self.password_entry.text()
        password = self.hash_password(password_raw)

        # 사용자 정보 확인
        
        if self.authenticate(user_id, password):
            config = configparser.ConfigParser()
            config.read(r"./register/config.ini")
            config['user']['user_id'] = user_id  # 로그인 아이디를 config.ini에 저장
            with open(r"./register/config.ini", 'w') as config_file:
                config.write(config_file)
            self.accept()

        else:
            self.username_entry.clear()
            self.password_entry.clear()
            self.username_entry.setFocus()
        # else:
        #     self.username_entry.setFocus()
        #     return
    
    def hash_password(self,user_password):
        # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
        hasher = hashlib.sha256()
        # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
        hasher.update(user_password.encode('utf-8'))
        # 해시된 결과 반환
        return hasher.hexdigest()

    def authenticate(self, user_id, password):
        config = configparser.ConfigParser()
        config.read(r"./register/config.ini")
        host_name = config['MySQL']['host']
        # LoginDialog.change_authentication_method()
        # try:

        conn=pymysql.connect(host=host_name, user='root',
                        password='0000', db='isbs2024',charset='utf8') # auth_plugin= "mysql_native_password"
        cur = conn.cursor()
        
        # 접속상태 확인 쿼리
        query = """SELECT connect_from FROM user_table WHERE user_id = %s AND user_password = %s"""
        cur.execute(query, (user_id, password))

        # 결과 가져오기
        result = cur.fetchone()  # 접속상태 가져오기
        # 새로운 접속 host_ip 확인
        ip_query = """ select host from information_schema.processlist """
        # 접속상태를 수정하여 저장하기
        ip_connect = """update user_table set connect_from = %s where user_id = %s """

        if result:  # 접속상태라면...
            cur.execute(ip_query)  # 새로운 host_ip 가져오기
            new_host_ip_tuple = cur.fetchone()
            new_host_ip = str(new_host_ip_tuple[0])
            if result[0]:   # ip_addr 은 
                if result[0] == new_host_ip:
                    return True
                else:
                    ip_addr = result[0]
                    reply = QMessageBox.question(
                        self, 
                        'Message', 
                        f"이미 {ip_addr}에 접속자가 있습니다. 이전 접속을 해지 할까요?", 
                        QMessageBox.Yes | QMessageBox.No, 
                        QMessageBox.No
                    )

                    if reply == QMessageBox.Yes:
                        cur.execute("update user_table set connect_from = null where user_id = %s;", user_id)
                        conn.commit()
                        cur.execute(ip_connect,(new_host_ip,user_id),)
                        conn.commit()
                        conn.close()
                        return True
                    else:
                        return False
            else:
                cur.execute(ip_connect,(new_host_ip,user_id),)
                conn.commit()
                conn.close()
                return True  # 인증 성공
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")
            return False  # 인증 실패
        # except pymysql.err.OperationalError:
        #     QMessageBox.about(self,"연결에러","서버설정을 확인 하세요")
        #     connect = "not connect"
        #     return connect

from PyQt5 import uic
import os, shutil
from PyQt5.QtGui import QIcon
from configparser import ConfigParser

from PyQt5.QtWidgets import *

config = ConfigParser()
config.read(r"./register/config.ini")
cur_fold = os.getcwd()
form_class = uic.loadUiType("./ui/church_reg.ui")[0]

class Church_Reg(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('교회 등록')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        Denomination_name = config['Denomination_name']['denomination']
        church_name = config['Church_name']['name']
        church_addr = config['Church_addr']['address']
        church_biz_no = config['biz_no']['biz_No']
        self.denomination_name_widget.setText(Denomination_name)
        self.church_name_widget.setText(church_name)
        self.church_addr_widget.setText(church_addr)
        self.church_biz_widget.setText(church_biz_no)


    def Button(self):
        server_save_Button = QPushButton("저장")
        server_save_Button.clicked.connect(self.church_save)

        # 닫기 버튼 연결
        close_Button = QPushButton("종료")
        close_Button.clicked.connect(self.close_exit)

    def select_logo_file(self):
        default_dir = os.path.join(cur_fold)
        file, _ = QFileDialog.getOpenFileName(self, "파일 선택", default_dir, "png 파일 (*.png)")
        if file:
            # 파일이 선택된 경우 파일 경로를 출력합니다.
            self.selected_logo_file = file
            print(file)
            self.selected_logo_file_label.setText(f'{file}')  # 파일 경로를 QLabel에 표시
        else:
            # 파일이 선택되지 않은 경우 취소되었음을 알립니다.
            QMessageBox.about(self, '취소', '파일 선택이 취소되었습니다.')


    def copyFile(self):
        if self.selected_logo_file:
            # 고정된 경로 설정 (img 폴더 안의 logo.png)
            path_fold = r"./img"
            save_path = os.path.join(cur_fold,'img', 'logo.png')

            os.makedirs(path_fold, exist_ok=True)
            
            # 파일 복사
            shutil.copy(self.selected_logo_file, save_path)
            # self.label.setText(f'파일이 {save_path}에 저장되었습니다.')


    def church_save(self):
        # 기존 설정 파일 열기
        config = ConfigParser()
        config.read(r"./register/config.ini")

        # 새로운 호스트 이름과 비밀번호를 config 파일에 저장 
        new_deno = self.denomination_name_widget.text()
        new_name = self.church_name_widget.text()
        new_addr = self.church_addr_widget.text()
        new_biz_no = self.church_biz_widget.text()
        
        # 기존설정이 있으면 설정 파일에서 이름을 변경
        config['Denomination_name']['name'] = new_deno
        config['Church_name']['name'] = new_name
        config['Church_addr']['address'] = new_addr
        config['biz_no']['biz_No'] = new_biz_no
        
        # 설정 파일 저장
        with open(r"./register/config.ini", 'w') as config_file:
            config.write(config_file)
        
            self.copyFile()
        # 저장 완료 메시지 표시
        QMessageBox.information(self, "저장 완료", "교회 등록이 완료 되었습니다.")

    def close_exit(self):
        self.denomination_name_widget.clear()
        self.church_name_widget.clear()
        self.church_addr_widget.clear()
        self.church_biz_widget.clear()
        self.close()
import os, configparser, pymysql, re
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
email_addr = config['e_mail']['sending_email']
pw = config['e_mail']['my_pw']
SMTP = config['e_mail']['smtp_server'] #= 'smtp.naver.com'
PORT =config['e_mail']['smtp_port']   #     smtp_port = 587

cur_fold = os.getcwd()
email_name_list = []
form_class = uic.loadUiType(os.path.join(cur_fold, 'ui', 'send_email.ui'))[0]
# form_class = uic.loadUiType("./ui/send_email.ui")[0]
class Send_Email(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('이메일 보내기')
        self.setWindowIcon(QIcon(os.path.join(cur_fold, 'img', 'logo.ico')))
        self.email_list_call()
        self.email_line_edit_To.returnPressed.connect(lambda: self.focusNextChild())
        self.email_line_edit_Cc.returnPressed.connect(lambda: self.focusNextChild())
        self.subject_widget.returnPressed.connect(lambda: self.focusNextChild())
        send_email_Button = QPushButton("보내기")
        send_email_Button.clicked.connect(self.email_data_collect)

        file_select_Button = QPushButton("파일선택")
        file_select_Button.clicked.connect(self.open_file_dialog)

        email_close_Button = QPushButton("종료")
        email_close_Button.clicked.connect(self.email_send_close)
        self.attachment_label = QLabel() 

    def email_list_call(self):
        email_list = self.load_email_list_from_mysql()
        for email_info in email_list:
            email_name, email_addr = email_info
            email_name_list.append(f"{email_name} <{email_addr}>")
        # select_1 = ['선택'] # self.receiver_name_combo = QComboBox()
        # self.receiver_name_combo.addItems(select_1)
        self.receiver_name_combo.addItems(['선택'] + email_name_list)
        # self.co_receiver_name_combo.addItems(select_1)
        self.co_receiver_name_combo.addItems(['선택'] + email_name_list)
        self.receiver_name_combo.activated.connect(self.combo_To_select)
        self.co_receiver_name_combo.activated.connect(self.combo_Cc_select)
    
    def open_file_dialog(self):
        default_dir = os.path.join(cur_fold, 'excel_view')
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택", default_dir, "모든 파일 (*.*)")
        if file_path:
            # 파일이 선택된 경우 파일 경로를 출력합니다.
            self.attached_file_listWidget.addItem(file_path)
        else:
            # 파일이 선택되지 않은 경우 취소되었음을 알립니다.
            QMessageBox.about(self, '취소', '파일 선택이 취소되었습니다.')

    def combo_To_select(self):
        selected_email_To = self.receiver_name_combo.currentText()
        if self.email_line_edit_To.text():
            selected_email_To = f"{self.email_line_edit_To.text()},{selected_email_To}"
        
        self.email_line_edit_To.setText(selected_email_To)
        # selected_email_To = selected_email_To.strip(" ","")
    
    def combo_Cc_select(self):
        selected_email_Cc = self.co_receiver_name_combo.currentText()
        if self.email_line_edit_Cc.text():
            selected_email_Cc = f"{self.email_line_edit_Cc.text()},{selected_email_Cc}"
        # 콤보박스에서 선택된 이메일 주소를 라인에디트 위젯에 설정합니다.
       
        self.email_line_edit_Cc.setText(selected_email_Cc)
        # selected_email_Cc = selected_email_Cc.strip(" ","")
        # co_receiver_emails = self.email_line_edit_Cc.text()

    # 이메일 발송 정보
    def email_data_collect(self):
        # try:
        sender_email = email_addr # 'isbs1000@naver.com'
        sender_password = pw
        receiver_emails = self.email_line_edit_To.text()
        co_receiver_emails = self.email_line_edit_Cc.text()

        subject = self.subject_widget.text() #'첨부 파일 테스트'
        body = self.body_contents_widget.toPlainText() #'안녕하세요.  일산백석교회 첨부파일을 보냅니다.' 
        
        # # 첨부파일 경로
        # selected_item = self.attached_file_listWidget.item()
        attachment_paths = []
        for index in range(self.attached_file_listWidget.count()):
            item = self.attached_file_listWidget.item(index)
            attachment_paths.append(item.text())

        # attachment_paths를 사용하여 이메일을 전송합니다.
        self.send_email(sender_email, sender_password, receiver_emails, co_receiver_emails, subject, body, attachment_paths)

    def load_email_list_from_mysql(self):
        # MySQL 연결 및 쿼리 실행
        conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
        cur = conn.cursor()
        
        cur.execute('SELECT email_name, email_addr FROM email_list')
        email_list = cur.fetchall()
        # email_list = [row[0] for row in ]  # 이메일 주소 리스트 추출
        conn.close()
        return email_list

    def send_email(self, sender_email, sender_password, receiver_emails, co_receiver_emails, subject, body, attachment_paths):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        smtp_server = SMTP
        smtp_port = PORT

        # 이메일 구성
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_emails
        msg['Cc'] = co_receiver_emails
        msg['Subject'] = subject

        # 본문 추가
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 첨부 파일 추가
        for attachment_path in attachment_paths:
            attachment = open(attachment_path, 'rb')
            part = MIMEBase('application', 'octet_stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            
            # 파일 이름 추출
            filename = os.path.basename(attachment_path)
            
            # Content-Disposition 헤더에 파일 이름 추가
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            
            msg.attach(part)
            attachment.close()

        try:
            # 이메일 전송
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()

            all_recipients = receiver_emails.split(",") + co_receiver_emails.split(",")

            server.sendmail(sender_email, all_recipients, text)
            server.quit()
            QMessageBox.about(None, '전송', '이메일이 성공적으로 전송되었습니다.!!')

        except Exception as e:
            QMessageBox.critical(None, '실패', '이메일 전송에 실패했습니다.')

   
        self.email_send_close_reset()    
        self.email_send_close()

        # sender_email,sender_password, receiver_emails, co_receiver_emails, subject, body, attachment_path)
        # except Exception as e:
        #     QMessageBox.about(self,'오류',"이메일 전송 중 오류가 발생하였습니다 !!")

    def email_send_close_reset(self):
        self.email_line_edit_To.clear()
        self.email_line_edit_Cc.clear()
        self.subject_widget.clear()
        self.attached_file_listWidget.clear()
        self.body_contents_widget.clear()
    
    def email_send_close(self):
        self.email_send_close_reset()
        self.close()
    
    def closeEvent(self,event):
        self.email_send_close_reset()
        event.accept()
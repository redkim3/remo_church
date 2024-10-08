import pymysql, configparser, os
from PyQt5.QtWidgets import QMessageBox

config = configparser.ConfigParser()
config.read("./register/config.ini")
host_name = config['MySQL']['host']

def load_email_list_from_mysql():
    # MySQL 연결 및 쿼리 실행
    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()
    
    cur.execute('SELECT email_name, email_addr FROM email_list')
    email_list = cur.fetchall()
    # email_list = [row[0] for row in ]  # 이메일 주소 리스트 추출
    conn.close()
    return email_list

def send_email(self, sender_email, sender_password, receiver_emails, Co_receiver_mails, subject, body, attachment_paths):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    smtp_server = 'smtp.naver.com'
    smtp_port = 587

    # 이메일 구성
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_emails #', '.join(receiver_emails)
    msg['Cc'] = Co_receiver_mails #', '.join(Co_receiver_mails)
    msg['Subject'] = subject

    # 본문 추가
    msg.attach(MIMEText(body, 'plain'))  # 'plain'

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
        
    # 이메일 전송
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_emails, text)
        server.quit()
        QMessageBox.about('None','전송','이메일이 성공적으로 전송되었습니다.!!')
        # self.receiver_name_combo.clear()
        # self.co_receiver_name_combo.clear()
        self.email_line_edit_To.clear()
        self.email_line_edit_Cc.clear()
        self.subject_widget.clear() 
        self.attached_file_listWidget.clear()
        self.body_contents_widget.clear()
        self.email_send_close()

    # sender_email,sender_password, receiver_emails, co_receiver_emails, subject, body, attachment_path)
    except Exception as e:
        QMessageBox.about('None','오류',"이메일 전송 중 오류가 발생하였습니다 !!")
import pymysql, configparser
from PyQt5.QtWidgets import QMessageBox
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def update_user_connect(user_id):
    # try:
    conn = pymysql.connect("""
        host= host_name,
        user='root',
        password='0000',
        db='isbs2024',
        charset='utf8'
    """)
    cur = conn.cursor()
    connect_query = "UPDATE user_table SET user_connect = 'N' WHERE user_id = %s"
    cur.execute(connect_query, (user_id))
    conn.commit()
    conn.close()
    # except pymysql.err.OperationalError:
    #     QMessageBox.about(None, "연결에러", "서버설정을 확인 하세요")
    # except Exception as e:
    #     QMessageBox.about(None, "에러", str(e))
        

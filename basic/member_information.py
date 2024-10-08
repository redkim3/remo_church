import pymysql, configparser, os
from PyQt5.QtCore import QDate, Qt # 또는 * 으로 날짜를 불러온다
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()
today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 


def member_code(v_year):
    conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    year_sql = "SELECT count(*) from member where year(date) = %s;"

    with conn.cursor() as cur:
        # Execute query to get the last member code for the given year
        cur.execute(year_sql,(v_year,))
        last_code = cur.fetchone()[0]

    return last_code

def new_member_append(data):
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    member_sql = "INSERT INTO member (date, code1, name_diff, name, hap_code,level,addr,marks) VALUES (%s, %s, %s,%s, %s, %s,%s, %s);"
    
    cur.execute(member_sql, data,)

    conn.commit()
    conn.close()

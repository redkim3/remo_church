import pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

today = QDate.currentDate()
v_year = str(today.year())

def payed_account_values(payed_acc, gubun):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    account_call = []
    payed_acc_name = payed_acc
    
    if payed_acc_name == 'reg':
        account_sql = 'select account_name from payed_account where gubun = %s;'
        cur.execute(account_sql, gubun)
        while(True):
            row = cur.fetchone()
            if row == None : 
                break
            bank_name = row[0]
            
            account_call.append(bank_name)
    elif payed_acc_name == 'view':
        account_sql = 'select account_name, bank_name, account_no, id from payed_account where gubun = %s;'
        cur.execute(account_sql, gubun)
        account_call = cur.fetchall()
    else:
        account_sql = 'select bank_name, account_no from payed_account where account_name = %s and gubun = %s;'
        cur.execute(account_sql, (payed_acc_name, gubun)
    )    
        account_call = cur.fetchall()

    cur.close()
    conn.close()

    return account_call

def payed_account_selected_row_delete(id):
    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()
    
    try:
        # 데이터 삭제 쿼리 실행
        delete_account_sql = 'delete from payed_account where id = %s;'
        cur.execute(delete_account_sql,(id,))

        # 변경사항을 데이터베이스에 반영 
        conn.commit()
        QMessageBox.information(None,"삭제",'데이터가 성공적으로 삭제되었습니다.')
        cur.close()
        conn.close()
    except pymysql.Error as e:
        QMessageBox.critical('에러', f'데이터 삭제 중 오류 발생: {e}')

def update_payed_account_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
            
    update_query = f"UPDATE payed_account SET account_name = %s, bank_name = %s, account_no = %s where id = %s ;"

    # 데이터베이스에 연결하여 값을 업데이트
    cur.execute(update_query, tuple(change_data,))
    conn.commit()
    change_data = []

    cur.close()
    conn.close()
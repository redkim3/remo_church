import configparser,  hashlib
import pymysql
from PyQt5.QtWidgets import QMessageBox
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def card_update_row_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # new_data = change_data[1]
    update_query = """UPDATE card_list SET bank_name = %s, card_number = %s, 
                use_part = %s WHERE card_number = %s;
            """
    
    # 데이터베이스에 연결하여 값을 업데이트 
    cur.execute(update_query, change_data,)
    conn.commit()
    
    cur.close()
    conn.close()

def bank_update_row_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # new_data = change_data[1]
    update_query = """UPDATE bank_acc SET bank_name = %s, bank_account = %s, 
                use_part = %s, gubun = %s, in_use = %s WHERE bank_account = %s;
            """
    
    # 데이터베이스에 연결하여 값을 업데이트 
    cur.execute(update_query, change_data,)
    conn.commit()
    
    cur.close()
    conn.close()

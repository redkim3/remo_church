import pymysql
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def pre_cost_call(Y1,M1,W1,gubun):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    called_precost = []
    
    precost_call_sql = "select cost_hang, cost_mok, cost_semok, cost_Memo, amount, pay_banks, marks from cost_db where year = %s and month = %s and week = %s and gubun = %s"
    cur.execute(precost_call_sql,(Y1, M1, W1,gubun,))
    #while(True):
    rows = cur.fetchall()
    for row in rows:
        # if not row : 
        #     break
        # data1 = row
        processed_row = [value if value != None else '' for value in row]
        called_precost.append(processed_row)

    #called_precost = pd.DataFrame(called_precost, columns=['year','month','week','cost_hang', 'cost_mok', 'cost_semok', 'coxt_memo', 'amount', 'pay_banks', 'cost_marks'])  # 각 열의 이름을 적절하게 지정

    conn.close()
    return called_precost
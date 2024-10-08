import pymysql
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def banklist():
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    bank_call = []
    bank_sql = 'select bank_name, bank_account, use_part, gubun, in_use from bank_acc;'
    cur.execute(bank_sql)
    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        data2 = row[1]
        data3 = row[2]
        data4 = row[3]
        data5 = row[4]
        bank_call.append([data1,data2,data3,data4,data5])
    
    conn.close()
    
    return bank_call


def cardlist():
    conn = pymysql.connect(host= host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    card_call = []
    card_sql = 'select bank_name, card_number, use_part from card_list;'
    cur.execute(card_sql)
    while(True):
        row = cur.fetchone()
        if row == None :
            break
        data1 = row[0]
        data2 = row[1]
        data3 = row[2]
        card_call.append([data1,data2,data3])
    conn.close()
    return card_call

def bank_name_list(gubun):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    bank_name_call = []
    bank_account_sql = """select bank_name from bank_acc 
                    where gubun = %s and in_use = '사용중';"""
    cur.execute(bank_account_sql,gubun)
    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        bank_name_call.append(data1)
    
    conn.close()
    
    return bank_name_call

import pymysql
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
 
def banklist():
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    bank_call = []
    bank_sql = 'select bank_name, bank_account, use_part from bank_acc;'
    cur.execute(bank_sql)
    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        data2 = row[1]
        data3 = row[2]
        bank_call.append([data1,data2,data3])
    
    conn.close()
    
    return bank_call


def cardlist():
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
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

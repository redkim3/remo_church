import pymysql
import pandas as pd
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def sungdodata():
    sungdo_data = pd.read_excel('./DB/sungdo_DB.xlsx',sheet_name="성도_DB", header=2, index_col=None, names=None)
    return sungdo_data

def name_diff_select():
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    name_diff_call = []

    name_diff_sql = 'select name_diff from member'
    cur.execute(name_diff_sql)

    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        
        name_diff_call.append(data1)

    conn.close()

    return name_diff_call

def s_name_select(name_diff):
    sungdo_data = name_diff_select()

    s_name = sungdo_data[(sungdo_data['성명코드'] == name_diff)]['성명'].values
    return s_name

def name_diff_compare(name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    name_diff_call = []

    name_diff_sql = 'select name_diff from member where name_diff = %s ;'
    cur.execute(name_diff_sql,(name_diff,))

    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        name_diff_call.append(data1)

    conn.close()

    return name_diff_call
 

def code1_select(name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    code1_call = []

    try:
        code1_sql = 'select code1 from member where name_diff = %s'
        rows = cur.execute(code1_sql,(name_diff,))

        rows = cur.fetchall()
        for row in rows:
            code1_call = row[0]  # 결과에서 코드값만 추출하여 리스트에 추가

        cur.close()

        return code1_call
    
    except pymysql.Error as e:
        # print("코드 찾기 오류 발생:", e)
        return []

def real_name_select(name_diff):
    sungdo_data = sungdodata()
    r_name = sungdo_data[(sungdo_data['성명코드'] == name_diff)]['성명'].values
    return r_name


def hap_code_select(name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    hap_code_call = []
    try:
        hap_code_sql = 'select hap_code from member where name_diff = %s'
        rows = cur.execute(hap_code_sql,(name_diff,))
       
        rows = cur.fetchall()
        for row in rows:
            hap_code_call = row[0]  # 결과에서 코드값만 추출하여 리스트에 추가
        conn.close()

        return hap_code_call

    except pymysql.Error as e:
        # QMessageBox.about(self,'ValueError',"합산코드 찾기 오류 발생. !!!")
        QMessageBox.about('오류',"합산코드 찾기 오류가 발생되었습니다.!!!")
        # print("합산코드 찾기 오류 발생:", e)
        return []
    
def code1_select_by_hapcode(hap_code):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    code1_call = []
    try:
        code1_sql = 'select code1 from member where hap_code = %s'
        rows = cur.execute(code1_sql,(hap_code,))

        rows = cur.fetchall()
        for row in rows:
            code1_call.append(row[0])  # 결과에서 코드값만 추출하여 리스트에 추가
            
    except pymysql.Error as e:
        # print("코드 찾기 오류 발생:", e)
        QMessageBox.about('오류',"코드 찾기 오류가 발생되었습니다.!!!")
        return []

    return code1_call

def sungdo_serch_name(name):
    sungdo_data = sungdodata()
    sungdoserch = sungdo_data[(sungdo_data.성명.str.contains(name))]
    return sungdoserch

def sungdo_count(Y1):
    sungdo_data = sungdodata()
    sungdocount = sungdo_data[(sungdo_data.합산코드 >= Y1) & (sungdo_data.합산코드 < 'ㄱ' )][['성명코드']].values
    
    lastcount = len(sungdocount)
#    lastcount = len(sungdocount)
    return lastcount


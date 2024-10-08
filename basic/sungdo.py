import os, pymysql
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

cur_fold = os.getcwd()


def name_code_select():
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    name_code_select_sql = "select name_diff from member"
    cur.execute(name_code_select_sql)
    name_diff = cur.fetchall()

    return name_diff

def s_name_select(name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    code_name_call = []
    code_name_sql = "select hap_code, name from member where name_diff = %s"
    cur.execute(code_name_sql,(name_diff,))
    code_name = cur.fetchall()
    for row in code_name:
        if not row : 
            break
        processed_row = [value if value != None else '' for value in row]
    code_name_call.append(processed_row)

    return code_name_call
    # sungdo_data = sungdodata()
    # #sungdo_data = pd.read_excel(cur_fold + '/DB/백석교회.xlsm',sheet_name="성도_DB", header=2, index_col=None, names=None)
    # code_name = sungdo_data[(sungdo_data['성명코드'] == name_code)][['합산코드','성명']]
    # #s_name = sungdo_data[(sungdo_data['성명코드'] == name_code)]['성명'].values


def sungdoname_serch(code1,name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    sungdoserch_sql = "select * from member where year = %s and hap_code = %s ;"
    cur.execute(sungdoserch_sql, (code1, name_diff,))
    sungdoserch = cur.fetchall()

    return sungdoserch

def sungdo_serch_code(selector, value):
    conn = pymysql.connect(host = host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()
        

    if selector == 'hap_code':
        search_value = value
        sungdoserch_sql = "SELECT date, code1, name_diff, name, hap_code, level, addr, marks FROM member WHERE hap_code = %s;"
    elif selector == 'code1':
        search_value = value
        sungdoserch_sql = "SELECT date, code1, name_diff, name, hap_code, level, addr, marks FROM member WHERE code1 = %s;"
    else:
        search_value = '%' + value + '%'
        sungdoserch_sql = "SELECT date, code1, name_diff, name, hap_code, level, addr, marks FROM member WHERE name_diff LIKE CONCAT(%s);"
    
    cur.execute(sungdoserch_sql, (search_value,))
                    
    sungdoserch = cur.fetchall()

    return sungdoserch
#     sungdo_data = sungdodata()
#     sungdoserch = sungdo_data[(sungdo_data.합산코드 == namecode)] #tablewidget에 넣을때는 values 또는 tolist()는 하지 않는다 
#     return sungdoserch

def sungdo_serch_name(code1,name_diff):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    sungdoserch_sql = "select * from member where code1 = %s and name_diff like '%s%' ;"
    cur.execute(sungdoserch_sql, (code1, name_diff,))
    sungdoserch = cur.fetchall()

    return sungdoserch
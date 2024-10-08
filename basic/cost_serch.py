import pymysql
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def serch_hang(start_date, end_date, gubun, hang):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    if gubun != "특별회계":
        ser_semok_sql ="""
                        select date, cost_mok, cost_semok, cost_memo, amount, pay_banks, marks, id from cost_db 
                        where date >= %s and date <= %s and cost_hang = %s order by date;
                    """ 
    else:
        ser_semok_sql ="""
                        select date, cost_hang, cost_mok, cost_semok, cost_memo, amount, bank_account, marks, id, balance from balance_db 
                        where date >= %s and date <= %s and cost_hang = %s order by date;
                    """ 
    cur.execute(ser_semok_sql,(start_date, end_date, hang,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_mok(start_date, end_date, gubun, hang, mok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    if gubun != "특별회계":
        ser_semok_sql ="""
                        select date, cost_semok, cost_memo, amount, pay_banks, marks, id from cost_db 
                        where date >= %s and date <= %s and cost_hang = %s and cost_mok = %s order by date;
                    """
    else:
        ser_semok_sql ="""
                        select date, cost_hang, cost_semok, cost_memo, amount, bank_account, marks, id, balance from balance_db 
                        where date >= %s and date <= %s and cost_hang = %s and cost_mok = %s order by date;
                    """
    cur.execute(ser_semok_sql,(start_date, end_date, hang, mok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_semok(start_date, end_date, gubun, hang,mok,semok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    if gubun != "특별회계":
        ser_semok_sql ="""
                        select date, cost_memo, amount, pay_banks, marks, id from cost_db 
                        where date >= %s and date <= %s and cost_hang = %s and cost_mok = %s and cost_semok = %s order by date;
                    """
    else:
        ser_semok_sql ="""
                        select date, cost_hang, cost_memo, amount, bank_account, marks, id, balance from balance_db 
                        where date >= %s and date <= %s and cost_hang = %s and cost_mok = %s and cost_semok = %s order by date;
                    """
    cur.execute(ser_semok_sql,(start_date, end_date, hang,mok,semok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def week_cost_serch(Y1, M1, W1, gubun): # 헌금 명칭(hun_mok)별 리스트
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    # 합코드에 포함된 개별코드 가져오기
    cost_week_list = []
    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    
    cost_week_list_sql = """
        SELECT date, cost_hang, cost_mok, cost_semok, cost_memo, amount, pay_banks, marks, id
        FROM cost_db WHERE year = %s AND month = %s AND week = %s AND gubun = %s
        ORDER BY id; 
    """
    cur.execute(cost_week_list_sql, (Y1, M1, W1, gubun,))
    cost_week_list_data = cur.fetchall()
    cost_week_list.extend(cost_week_list_data)  # 모든 행을 리스트에 추가
    

    return cost_week_list

# 검색일 이전의 잔액 찾기
def serch_hang_pre_year(start_date, hang):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_hang_sql_s ="""
                    select date, cost_hang, cost_mok, cost_semok, cost_memo, amount, bank_account, marks, id, balance from balance_db 
                    where date < %s and cost_hang = %s order by date;
                """ 
    cur.execute(ser_hang_sql_s,(start_date, hang,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_mok_pre_year(start_date, hang, mok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_mok_sql_s ="""
                    select date, cost_hang, cost_mok, cost_semok, cost_memo, amount, bank_account, marks, id, balance from balance_db 
                    where date < %s and cost_hang = %s and cost_mok = %s order by date;
                """
    cur.execute(ser_mok_sql_s,(start_date, hang, mok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_semok_pre_year(start_date, hang, mok, semok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_semok_sql_s ="""
                    select date, cost_hang, cost_semok, amount, bank_account, marks, id, balance from balance_db 
                    where date < %s and cost_hang = %s and cost_mok = %s and cost_semok = %s order by date;
                """
    cur.execute(ser_semok_sql_s,(start_date, hang, mok, semok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_hang_pre_date(start_date, year, hang):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_hang_sql_s ="""
                    select date, cost_mok, cost_semok, cost_memo, amount, pay_banks, marks, id from cost_db 
                    where date < %s and year = %s and cost_hang = %s order by date;
                """ 
    cur.execute(ser_hang_sql_s,(start_date, year, hang,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_mok_pre_date(start_date, year, hang, mok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_mok_sql_s ="""
                    select date, cost_semok, cost_memo, amount, pay_banks, marks, id from cost_db 
                    where date < %s and year = %s and cost_hang = %s and cost_mok = %s order by date;
                """
    cur.execute(ser_mok_sql_s,(start_date, year, hang, mok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_semok_pre_date(start_date, year, hang, mok, semok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    
    ser_semok_sql_s ="""
                    select date, cost_memo, amount, pay_banks, marks, id from cost_db 
                    where date < %s and year = %s and cost_hang = %s and cost_mok = %s and cost_semok = %s order by date;
                """
    cur.execute(ser_semok_sql_s,(start_date, year, hang, mok, semok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list
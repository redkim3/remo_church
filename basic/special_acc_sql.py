import pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

today = QDate.currentDate()
v_year = str(today.year())

def remained_bank_account(bogo_year): # 기초예금잔액
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    increament_sql = """select sum(amount) from balance_db where balance = '예금증가' and year < %s;"""

    cur.execute(increament_sql, bogo_year)
    increment_sum_tu = cur.fetchone()  # fetchone() 메소드를 호출하여 결과를 변수에 할당 
    increment_sum = increment_sum_tu[0]
    if increment_sum:
        pass
    else:
        increment_sum = 0


    decreament_sql = """select sum(amount) from balance_db where balance = '예금감소' and year < %s;"""

    cur.execute(decreament_sql, bogo_year)
    decrement_sum_tu = cur.fetchone()  # fetchone() 메소드를 호출하여 결과를 변수에 할당
    decrement_sum =decrement_sum_tu[0]

    if decrement_sum:
        pass
    else:
        decrement_sum = 0
    
    result = increment_sum - decrement_sum
    
    return result

def special_tree_data_incre(year, bun):
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    tree_sql = """
                select cost_hang, cost_mok, cost_semok, sum(amount) from balance_db where year = %s 
                and month >= ((%s * 3) - 2) and month <= (%s * 3) and balance = '예금증가'
                GROUP BY cost_hang, cost_mok, cost_semok;
            """
    cur.execute(tree_sql,(year,bun,bun))

    data = cur.fetchall()
    # print(data)
    return data

def special_tree_data_decre(year, bun):
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    tree_sql = """
                select cost_hang, cost_mok, cost_semok, sum(amount) from balance_db where year = %s 
                and month >= ((%s * 3) - 2) and month <= (%s * 3) and balance = '예금감소'
                GROUP BY cost_hang, cost_mok, cost_semok;
            """
    cur.execute(tree_sql,(year,bun,bun))

    data = cur.fetchall()

    # print(data)
    return data

def special_tree_financial_data(year, bun):
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    tree_sql = """
                select cost_hang, cost_mok, cost_semok, bank_account, sum(amount), balance from balance_db where year < %s 
                or (year = %s and month <= (%s * 3))
                GROUP BY cost_hang, cost_mok, cost_semok, bank_account, balance;
            """
    cur.execute(tree_sql,(year,year,bun))

    data = cur.fetchall()
    # print(data)
    return data

def past_bank_account_value(serch_year,bank):
    import decimal
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    ser_bank_plus_sql ="""
                    select sum(amount) from balance_db 
                    where year < %s and bank_account = %s and balance = '예금증가';
                """
    cur.execute(ser_bank_plus_sql,(serch_year,bank,))

    past_plus_value = cur.fetchone()
    
    ser_bank_minus_sql ="""
                    select sum(amount) from balance_db 
                    where year < %s and bank_account = %s and balance = '예금감소';
                """
    cur.execute(ser_bank_plus_sql, (serch_year, bank,))
    past_plus_value = cur.fetchone()
    
    cur.execute(ser_bank_minus_sql, (serch_year, bank,))
    past_minus_value = cur.fetchone()

    cur.close()
    conn.close()
    
    # None 값을 0으로 대체
    past_plus_value = past_plus_value[0] if past_plus_value[0] is not None else decimal.Decimal('0.00')
    past_minus_value = past_minus_value[0] if past_minus_value[0] is not None else decimal.Decimal('0.00')
    
    past_bank_balance_value = past_plus_value - past_minus_value
    
    return past_bank_balance_value


def select_bank(gubun):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    selected_bank = []

    select_bank_spl = """
                    select bank_name from bank_acc where gubun = %s;
                """
    cur.execute(select_bank_spl, gubun)
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row[0]
        selected_bank.append(data)

    cur.close()
    conn.close()

    return selected_bank

def bank_account_view(serch_year,bank):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    ser_semok_sql ="""
                    select date, cost_memo, balance, amount, marks, id from balance_db 
                    where year = %s and bank_account = %s order by date;
                """
    cur.execute(ser_semok_sql,(serch_year,bank,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_hang(serch_year,hang):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    ser_semok_sql ="""
                    select date, cost_mok, cost_semok, cost_memo, bank_account, amount, balance, marks, id from balance_db 
                    where year = %s and cost_hang = %s order by date;
                """ 
    cur.execute(ser_semok_sql,(serch_year,hang,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_mok(serch_year,hang,mok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    ser_semok_sql ="""
                    select date, cost_semok, cost_memo, bank_account, amount, balance, marks, id from balance_db 
                    where year = %s and cost_hang = %s and cost_mok = %s order by date;
                """
    cur.execute(ser_semok_sql,(serch_year,hang,mok,))
    
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        data = row
        select_cost_list.append(data)
    
    cur.close()
    
    return select_cost_list

def serch_semok(serch_year,hang,mok,semok):
    conn = pymysql.connect(host= host_name, user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    select_cost_list = []
    ser_semok_sql ="""
                    select date, cost_memo, balance, amount, bank_account, marks, id from balance_db 
                    where year = %s and cost_hang = %s and cost_mok = %s and cost_semok = %s order by date;
                """
    cur.execute(ser_semok_sql,(serch_year,hang,mok,semok,))
    
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
        SELECT date, cost_hang, cost_mok, cost_semok, cost_memo, bank_account, amount, balance, marks, id
        FROM cost_db WHERE year = %s AND month = %s AND week = %s AND gubun = %s
        ORDER BY id; 
    """
    cur.execute(cost_week_list_sql, (Y1, M1, W1, gubun,))
    cost_week_list_data = cur.fetchall()
    cost_week_list.extend(cost_week_list_data)  # 모든 행을 리스트에 추가
    

    return cost_week_list
import pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

today = QDate.currentDate()
v_year = str(today.year())

def income_budget(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'hun_budget'
    
    hun_budget_sql = "SELECT hun_budget_hang, hun_budget_mok, hun_budget_amount FROM {} where budget_year = %s;".format(table_name)
    cur.execute(hun_budget_sql, (Y1,))

    hun_budget = cur.fetchall()
    
    conn.close()
    return hun_budget

def income_budget_sum(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'hun_budget'
    
    hun_budget_sql = "SELECT SUM(hun_budget_amount) FROM {} where budget_year = %s;".format(table_name)
    cur.execute(hun_budget_sql, (Y1,))

    hun_budget = cur.fetchall()
        
    conn.close()
    return hun_budget


def cost_budget(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_budget'
    
    cost_budget_sql = "SELECT cost_budget_mok, cost_budget_amount FROM {} where budget_year = %s;".format(table_name)
    cur.execute(cost_budget_sql, (Y1,))

    cost_budget = cur.fetchall()
    
    conn.close()

    return cost_budget

def cost_budget_sum (Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_budget'
    
    cost_budget_sql = "SELECT SUM(cost_budget_amount) FROM {} where budget_year = %s;".format(table_name)
    cur.execute(cost_budget_sql, (Y1,))

    cost_budget = cur.fetchall()
    
    conn.close()

    return cost_budget

def income_order_budget(Y1,hun_hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    income_order_budget_sql = """ select hun_budget_mok, hun_budget_amount from hun_budget where budget_year = %s and hun_budget_hang = %s; """
    cur.execute(income_order_budget_sql,(Y1,hun_hang,))

    income_order_budget = cur.fetchall()
    
    conn.close()

    return income_order_budget

def income_jeol_budget(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    income_jeol_budget_sql = """ select hun_budget_mok, hun_budget_amount from hun_budget where budget_year = %s and hun_budget_hang = '절기헌금'; """
    cur.execute(income_jeol_budget_sql,(Y1,))

    income_jeol_budget = cur.fetchall()
    
    conn.close()

    return income_jeol_budget

def budget_mok_list(v_year, hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    try:
        current_year = today.year()
        table_name = str(v_year) + '_' + 'hun_mok'

            # 테이블 존재 여부 확인
        cur.execute(f"select table_name from information_schema.tables where table_schema = 'isbs2024' and table_name = '{table_name}'; ")
        table_exists = cur.fetchone()

        if table_exists:
        
            hun_mok_sql = 'SELECT hun_mok FROM {} where hun_hang = %s;'.format(table_name)
            cur.execute(hun_mok_sql,(hang,))

            mok_list = cur.fetchall()
            
            conn.close()

            return mok_list
        else:
            # if v_year == current_year + 1:
            previous_year_table = str(current_year - 1) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(v_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도 
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
            cur.execute(create_table_query)

            hun_mok_sql = 'SELECT hun_mok FROM {} where hun_hang = %s;'.format(table_name)
            cur.execute(hun_mok_sql,(hang,))

            mok_list = cur.fetchall()
            
            conn.close()

            return mok_list

    except pymysql.Error as error: #.ProgrammingError:

        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            create_table_query
            QMessageBox.information("예산 '헌금 목'이 없습니다.")

def hun_budget_call(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    hun_budget_call_sql = """ select hun_budget_hang, hun_budget_mok, hun_budget_amount, id from hun_budget where budget_year = %s; """
    cur.execute(hun_budget_call_sql,(Y1,))

    hun_budget = cur.fetchall()

    conn.close()

    return hun_budget

def cost_budget_call(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    cost_budget_call_sql = """ select cost_budget_hang, cost_budget_mok, cost_budget_semok, cost_budget_amount, id from cost_budget where budget_year = %s; """
    cur.execute(cost_budget_call_sql,(Y1,))

    cost_budget = cur.fetchall()

    conn.close()

    return cost_budget

def budget_income_save(received_data):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    data_type = received_data[0][-1]
    if data_type == "new":
        input_data = received_data[0][:6]
    else:
        input_data = received_data[0][:4]

    if data_type != "new" :  #새로운 데이터 아님

        income_budget_update_sql = """
                    update hun_budget set hun_budget_amount = %s, hun_budget_marks = %s, user = %s 
                    where id = %s;
                """
        cur.execute(income_budget_update_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
        conn.commit()
        conn.close()
    
    else:
        new_income_budget_sql = """
                    insert into hun_budget (budget_year, hun_budget_hang, hun_budget_mok, hun_budget_amount,hun_budget_marks,user)
                    values (%s, %s, %s, %s, %s, %s);
                """
        cur.execute(new_income_budget_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
        conn.commit()
        conn.close()

def delete_hun_budget(year):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    hun_delete_sql = """ 
            delete from hun_budget where budget_year = %s;
        """
    cur.execute(hun_delete_sql, year)
    conn.commit()

def budget_hun_call(year):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    confirm_sql = """ 
            select hun_budget_hang, hun_budget_mok, hun_budget_amount, hun_budget_marks, id from hun_budget where budget_year = %s;
        """
    cur.execute(confirm_sql, year)
    conn.commit()

    hun_budget_confirm = cur.fetchall()
    
    return hun_budget_confirm

def budget_cost_call(year):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    cost_confirm_sql = """ 
            select cost_budget_hang, cost_budget_mok, cost_budget_semok, cost_budget_amount, cost_budget_marks, id from cost_budget where budget_year = %s;
        """
    cur.execute(cost_confirm_sql, year)
    conn.commit()

    cost_budget_confirm = cur.fetchall()
    
    return cost_budget_confirm

def delete_cost_budget(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    delete_cost_sql = """
                delete from cost_budget where budget_year = %s;"
            """
    
    cur.execute(delete_cost_sql, (Y1,))

    conn.commit()

    conn.close()
    cur.close()

def budget_cost_save(received_data):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    data_type = received_data[0][-1]
    if data_type == "new":
        input_data = received_data[0][:7]
    else:
        input_data = received_data[0][:4]

    if data_type == "modi" :  #새로운 데이터 아님,  기존 데이터 수정

        cost_budget_update_sql = """
                    update cost_budget set cost_budget_amount = %s, cost_budget_marks = %s, user = %s 
                    where id = %s;
                """
        cur.execute(cost_budget_update_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
        conn.commit()
        conn.close()
    
    elif data_type == 'new':  # 신규 데이터 입력
        new_cost_budget_sql = """insert into cost_budget (budget_year,cost_budget_hang, cost_budget_mok, cost_budget_semok,
                            cost_budget_amount, cost_budget_marks, user) values(%s, %s, %s, %s, %s, %s, %s)
                        """    
        cur.execute(new_cost_budget_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
        conn.commit()
        conn.close()
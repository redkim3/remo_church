import pymysql
from PyQt5.QtWidgets import QMessageBox
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def cost_budget_call(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name_1 = str(Y1) + '_' + 'cost_hang'
    table_name_2 = 'cost_budget'
    try:
        cost_hang = f"select id, cost_hang from {table_name_1} order by id asc;"
        cur.execute(cost_hang)
    except pymysql.err.ProgrammingError:
        QMessageBox.about(None, '누락', '해당년도 cost_hang 이 없습니다.')
        return

    cost_hang_tuple = cur.fetchall()
    # desireed_order_column_list = ', '.join([item[0] for item in order_hang_tuple])  #  튜플을 str 문자열로 변경하는 것
    desireed_cost_column_list = [item[1] for item in cost_hang_tuple]  # tuple을 리스트로 변경하는 것

    cost_column = ', '.join([f'"{col}"' for col in desireed_cost_column_list])  #  이 부분은 정렬에 관한 부분으로 # ORDER BY {order_column};을 마지각에 삭제함 이유는 정렬을 앞에 있는 것으로 

    cost_budget_sql = f"""
                    SELECT 
                        cost_budget_hang,
                        cost_budget_mok,
                        CASE
                            WHEN cost_budget_semok IS NOT NULL THEN cost_budget_semok
                            ELSE 0  -- 또는 다른 대체값 사용 가능
                        END AS cost_budget_semok,
                        SUM(cost_budget_amount) AS total_amount,
                        cost_budget_marks, 
                        id
                    FROM {table_name_2} WHERE budget_year = %s 
                    GROUP BY cost_budget_hang, cost_budget_mok, cost_budget_semok, cost_budget_marks, id
                    ORDER BY {cost_column} asc
                """

    cur.execute(cost_budget_sql, (Y1,))    
    
    cost_budget_origin = cur.fetchall()
    

    conn.close()

    return cost_budget_origin

# def cost_budget_call(Y1):
#     conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
#     cur = conn.cursor()
    
#     table_name_1 = str(Y1) + '_' + 'cost_hang'
#     table_name_2 = 'cost_budget'
#     try:
#         order_hang = f"select cost_hang from {table_name_1} order by id asc;"
#         cur.execute(order_hang)
#     except pymysql.err.ProgrammingError:
#         QMessageBox.about(None, '누락', '해당년도 cost_hang 이 없습니다..')
#         return

#     cost_hang_tuple = cur.fetchall()
#     # desireed_order_column_list = ', '.join([item[0] for item in order_hang_tuple])  #  튜플을 str 문자열로 변경하는 것
#     desireed_cost_column_list = [item[0] for item in cost_hang_tuple]  # tuple을 리스트로 변경하는 것

#     cost_column = ', '.join([f'"{col}"' for col in desireed_cost_column_list])

#     cost_budget_call_sql = f"""
#                     SELECT 
#                         cost_budget_hang,
#                         cost_budget_mok,
#                         cost_budget_semok,
#                         cost_budget_amount,
#                         cost_budget_marks,
#                         id
#                     FROM {table_name_2} WHERE budget_year = %s
#                     GROUP BY cost_budget_hang, cost_budget_mok, cost_budget_semok,cost_budget_marks,id
#                     ORDER BY {cost_column};
#                 """

#     cur.execute(cost_budget_call_sql, (Y1,))    
    
#     cost_budget_origin = cur.fetchall()

#     conn.close()

#     return cost_budget_origin

def result_serch_hang_list(Y1,gubun):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_db'
    
    cost_budget_sql = "SELECT DISTINCT cost_hang FROM {} where year = %s and gubun = %s;".format(table_name)
    cur.execute(cost_budget_sql, (Y1,gubun,))

    cost_budget_origin = cur.fetchall()
    
    cost_hang_list = [item[0] for item in cost_budget_origin]  

    conn.close()

    return cost_hang_list

def result_serch_mok_list(Y1,hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_db'
    
    cost_mok_sql = "SELECT DISTINCT cost_mok FROM {} where year = %s and cost_hang = %s;".format(table_name)
    cur.execute(cost_mok_sql, (Y1,hang))

    cost_mok_origin = cur.fetchall()
    
    result_cost_mok_list = [item[0] for item in cost_mok_origin]  
    conn.close()

    
    return result_cost_mok_list

def result_serch_semok_list(Y1,mok):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_db'
    
    cost_semok_sql = "SELECT DISTINCT cost_semok FROM {} where year = %s and cost_mok = %s;".format(table_name)
    cur.execute(cost_semok_sql, (Y1,mok,))

    cost_semok_origin = cur.fetchall()
    
    result_cost_semok_list = [item[0] for item in cost_semok_origin]  
    conn.close()

    
    return result_cost_semok_list


def serch_budget_hang_list(Y1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = str(Y1) +'_' + 'cost_hang'
    
    cost_budget_sql = "SELECT id, cost_hang FROM {} order by id asc;".format(table_name) # 내림차순 정리는 desc
    # cost_budget_sql = "SELECT DISTINCT cost_budget_hang, id FROM {} where budget_year = %s order by id;".format(table_name) 중복을 피하면서 '항' 가져외기  선서는 가나다 순임
    cur.execute(cost_budget_sql)
    # cur.execute(cost_budget_sql, (Y1,))  중복방지 항 가져오기로 할때 
    cost_budget_origin = cur.fetchall()
    
    cost_hang_list = [item[1] for item in cost_budget_origin]  

    conn.close()


    return cost_hang_list
    

def serch_mok_list(Y1,hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_budget'
    # 중복 값을 제거 하는 코드입니다. DISTINCT
    cost_budget_sql = "SELECT DISTINCT cost_budget_mok FROM {} where budget_year = %s and cost_budget_hang = %s;".format(table_name)
    cur.execute(cost_budget_sql, (Y1,hang))

    cost_budget_origin = cur.fetchall()
    
    cost_mok_list = [item[0] for item in cost_budget_origin]  
    conn.close()

    
    return cost_mok_list

def serch_semok_list(Y1,mok):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name = 'cost_budget'
    
    cost_budget_sql = "SELECT DISTINCT cost_budget_semok FROM {} where budget_year = %s and cost_budget_mok = %s;".format(table_name)
    cur.execute(cost_budget_sql, (Y1,mok,))

    cost_budget_origin = cur.fetchall()
    
    cost_semok_list = [item[0] for item in cost_budget_origin]  
    conn.close()

    return cost_semok_list



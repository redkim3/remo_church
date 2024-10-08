import pymysql 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
today = QDate.currentDate()

def cost_hang_list(budg_year,gubun):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    table_name = str(budg_year) + '_' + 'cost_hang'
    cost_hang_call = []
    
    cost_hang_sql = 'SELECT cost_hang FROM {} where gubun = %s;'.format(table_name)
    cur.execute(cost_hang_sql,(gubun,))

    hang_list = cur.fetchall()

    conn.close()
    
    return hang_list

def cost_mok_list(budg_year,hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    table_name = str(budg_year) + '_' + 'cost_mok'
    cost_mok_call = []

    cost_mok_sql = 'SELECT cost_mok FROM {} where cost_hang = %s;'.format(table_name)
    cur.execute(cost_mok_sql,(hang,))

    mok_list = cur.fetchall() 

    conn.close()
    
    return mok_list

def cost_semok_list(budg_year, mok):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    table_name = str(budg_year) + '_' + 'cost_semok'
    cost_semok_call = []
    
    if mok == 'all':
        cost_semok_sql = 'SELECT cost_mok FROM {};'.format(table_name)
        cur.execute(cost_semok_sql)
    else:
        cost_semok_sql = 'SELECT cost_semok FROM {} where cost_mok = %s;'.format(table_name)
        cur.execute(cost_semok_sql,(mok,))
    semok_list = cur.fetchall()

    conn.close()
    
    return semok_list

# 없으면 만들어라 (예산에서 사용) 

def cost_budget_hang_list(budg_year,gubun):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    try:
        table_name = str(budg_year) + '_' + 'cost_hang'
        # 테이블 존재 여부 확인
        table_name_query = """
                select table_name from information_schema.tables 
                where table_schema = %s and table_name = %s ;
                """
        cur.execute(table_name_query,('isbs2024',table_name))
        table_exists = cur.fetchone()

        if table_exists:
            hang_list = []
            
            cost_hang_sql = 'SELECT cost_hang FROM {} where gubun = %s;'.format(table_name)
            cur.execute(cost_hang_sql,(gubun,))

            hang_list = cur.fetchall()

            conn.close()
            return hang_list
        else:
            previous_year_table = str(budg_year - 1) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(budg_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"

            cur.execute(create_table_query)
            conn.close()
            QMessageBox.information(None,"error","지출 '항' 데이터가 없습니다. 재정기초등록에서 등록해주세요")

    except pymysql.Error as error : 
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)

def cost_budget_mok_list(budg_year,hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    table_name = str(budg_year) + '_' + 'cost_mok'
    
    table_name_query = """
                select table_name from information_schema.tables 
                where table_schema = %s and table_name = %s ;
                """
    cur.execute(table_name_query,('isbs2024',table_name))
    
    table_exists = cur.fetchone()
    
    try:
        if table_exists:
            cost_mok_sql = 'SELECT cost_mok FROM {} where cost_hang = %s;'.format(table_name)
            cur.execute(cost_mok_sql,hang)

            mok_list = cur.fetchall()

            conn.close()
            
            return mok_list

        else:
            previous_year_table = str(budg_year - 1) + '_' + 'cost_mok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(budg_year) + '_' + 'cost_mok' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
            cur.execute(create_table_query)

            conn.close()
            QMessageBox.information(None,"error","지출 '목' 데이터가 없습니다. 재정기초등록에서 등록해주세요")

    except pymysql.Error as error :
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)

def cost_budget_semok_list(budg_year, mok):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    try:
        table_name = str(budg_year) + '_' + 'cost_semok'
        
        table_name_query = """
                select table_name from information_schema.tables 
                where table_schema = %s and table_name = %s ;
                """
        cur.execute(table_name_query,('isbs2024',table_name))

        table_exists = cur.fetchone()
        
        if table_exists:
            if mok == 'all':
                cost_semok_sql = 'SELECT cost_mok FROM {};'.format(table_name)
                cur.execute(cost_semok_sql)
            else:
                cost_semok_sql = 'SELECT cost_semok FROM {} where cost_mok = %s;'.format(table_name)
                cur.execute(cost_semok_sql, mok)
        
            semok_list = cur.fetchall()
            conn.close()    
            return semok_list
        
        else:
            previous_year_table = str(budg_year - 1) + '_' + 'cost_semok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(budg_year) + '_' + 'cost_semok' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"

            cur.execute(create_table_query)
            conn.close()

            QMessageBox.information(None,"error","지출 '세목' 데이터가 없습니다. 재정기초등록에서 등록해주세요")
    
    
    except pymysql.Error as error : 
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        


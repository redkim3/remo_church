import pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

today = QDate.currentDate()
v_year = str(today.year())

def cost_hang_values(v_year,gubun):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # try:
    current_year = today.year()
    
    check_table_query = f"SHOW TABLES LIKE '{str(v_year) + '_' + 'cost_hang'}';"
    cur.execute(check_table_query)

    # 존재하는 테이블을 확인하고 그에 따라서 처리
    if cur.fetchone():  # 테이블이 존재하는 경우
        # 테이블 이름 설정
        table_name = str(v_year) + '_' + 'cost_hang'
    else:

        if v_year == current_year + 1:
            previous_year_table = str(current_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(v_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
            cur.execute(create_table_query)
        else:
            table_name = str(v_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            if table_name != None:
                table_name = str(current_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도

    cost_hang_call = []
    cost_hang_sql = 'SELECT cost_hang, id FROM {} where gubun = %s'.format(table_name)
    cur.execute(cost_hang_sql,(gubun,))
    row = cur.fetchall()
                
    conn.commit()
    conn.close()
    return row
    
    # except pymysql.Error as e:
    #     QMessageBox.information("'지출 항'이 없습니다.")

def cost_mok_values(v_year,cost_hang):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    v_year = int(v_year)
    table_name = str(v_year) + '_' + 'cost_mok' # budg_year 가 내년이면 전년은 당해년도

    # try:
    cur.execute("""
                SELECT table_name 
                FROM information_schema.tables
                WHERE table_schema = 'isbs2024' AND table_name = %s;
            """, (table_name,))
    
    table_exists = cur.fetchone()

    if table_exists:
        cost_mok_call = []
        
        cost_mok_sql = 'SELECT cost_mok, id FROM {} where cost_hang = %s'.format(table_name)
        cur.execute(cost_mok_sql,(cost_hang,))
        cost_mok_call = cur.fetchall()
        
        conn.commit()
        conn.close()

        return cost_mok_call

    else:
        previous_year_table = str(v_year - 1) + '_' + 'cost_mok' # budg_year 가 내년이면 전년은 당해년도
        # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
        cur.execute(create_table_query)

    # except pymysql.Error as e:
    #     QMessageBox.information("'지출 목'이 없습니다.")

def cost_semok_values(v_year,cost_mok):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록 
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    v_year = int(v_year)
    # db_name = [isbs2024]
    # try:
    current_year = today.year()
    table_name = str(v_year) + '_' + 'cost_semok'
    cur.execute("""
                select table_name from information_schema.tables
                where table_schema = 'isbs2024' and table_name = %s;
            """, (table_name,))

    # 존재하는 테이블을 확인하고 그에 따라서 처리
    table_exists = cur.fetchone()  # 테이블이 존재하는 경우
    if table_exists:
        cost_semok_sql = 'SELECT cost_semok, id FROM {} where cost_mok = %s'.format(table_name)
        cur.execute(cost_semok_sql,(cost_mok,))
        cost_semok_call = cur.fetchall()
        
        conn.commit()
        conn.close()
    else:
        previous_year_table = str(v_year - 1) + '_' + 'cost_semok' # budg_year 가 내년이면 전년은 당해년도
        table_name = str(v_year) + '_' + 'cost_semok' # budg_year 가 내년이면 전년은 당해년도
        # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
        cur.execute(create_table_query)
        
    # while(True):
    #     row = cur.fetchone()
    #     if row == None : 
    #         break
    #     data1 = row[0]
    #     cost_semok_call.append(data1)

        conn.commit()
        conn.close()

    return cost_semok_call
    
    # except pymysql.Error as e:
    #     QMessageBox.about(None,'오류',"'지출 세목'이 없습니다.")
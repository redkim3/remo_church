from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
import pymysql, configparser, os
from basic.hun_name_2 import gubun_values

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
today = QDate.currentDate()

cost_imsi = []; n = 0

def hun_semok_selected_row_delete(v_year,selected_data):
    table_name = v_year + '_' + 'hun_semok'

    # 데이터베이스 연결
    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()

    try:
        # 데이터 삭제 쿼리 실행
        delete_semok_sql = 'delete from {} where hun_semok = %s'.format(table_name)
        cur.execute(delete_semok_sql,(selected_data,))

        # 변경사항을 데이터베이스에 반영
        conn.commit()
        QMessageBox.about(None,'삭제', '데이터가 성공적으로 삭제되었습니다.')
    except pymysql.Error as e:
        QMessageBox.critical(None,'에러', f'데이터 삭제 중 오류 발생: {e}')
    finally:

        # 데이터베이스 연결 해제
        cur.close()
        conn.close()

def hun_semok_update_row_sql(v_year,change_data):
    table_name = v_year + '_' + 'hun_semok'
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # new_data = change_data[1]
    update_query = "UPDATE {} SET hun_semok = %s WHERE id = %s;".format(table_name)
    
    # 데이터베이스에 연결하여 값을 업데이트 
    cur.execute(update_query, change_data,)
    conn.commit()
    
    cur.close()
    conn.close()

def hun_mok_selected_row_delete(v_year,selected_data):
    table_name = v_year + '_' + 'hun_mok'

    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()

    try:
        # 데이터 삭제 쿼리 실행
        delete_mok_sql = 'delete from {} where hun_mok = %s'.format(table_name)
        cur.execute(delete_mok_sql,(selected_data,))

        # 변경사항을 데이터베이스에 반영
        conn.commit()
        QMessageBox.about(None, '삭제', '데이터가 성공적으로 삭제되었습니다.')
    except pymysql.Error as e:
        QMessageBox.critical(None, '에러', f'데이터 삭제 중 오류 발생: {e}')
    finally:

        # 데이터베이스 연결 해제
        conn.close()

def hun_mok_update_row_sql(v_year,change_data):
    table_name = v_year + '_' + 'hun_mok'
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # new_data = change_data[1]
    update_query = "UPDATE {} SET hun_mok = %s WHERE id = %s;".format(table_name)

    
    # 데이터베이스에 연결하여 값을 업데이트 
    cur.execute(update_query, change_data,)
    conn.commit()
    
    cur.close()
    conn.close()

def hun_hang_selected_row_delete(v_year,selected_data):
    table_name = v_year + '_' + 'hun_hang'
            # 데이터베이스 연결
    conn = pymysql.connect(host=host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()

    try:
        # 데이터 삭제 쿼리 실행
        delete_hang_sql = 'delete from {} where hun_hang = %s'.format(table_name)
        cur.execute(delete_hang_sql,(selected_data,))

        # 변경사항을 데이터베이스에 반영
        conn.commit()
        QMessageBox.about(None, '삭제', '데이터가 성공적으로 삭제되었습니다.')
    except pymysql.Error.DataError:
        QMessageBox.critical(None, '에러', '데이터의 길이가 너무 깁니다. 길이를 줄여 주세요')
    except pymysql.Error as e:
        QMessageBox.critical(None, '에러', f'데이터 삭제 중 오류 발생: {e}')
    finally:
        # 데이터베이스 연결 해제
        cur.close()
        conn.close()
    
def hun_hang_update_row_sql(v_year,change_data):
    table_name = v_year + '_' + 'hun_hang'
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
    try:
        # new_data = change_data[1]
        update_query = "UPDATE {} SET hun_hang = %s WHERE id = %s;".format(table_name)

        # 데이터베이스에 연결하여 값을 업데이트 
        cur.execute(update_query, change_data,)
        conn.commit()
        
        cur.close()
        conn.close()
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.critical(None, '에러', f'데이터 삭제 중 오류 발생: {error}')

def current_year_hun_hang_save_sql(v_year,hun_imsi):
    current_year = today.year()
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    check_table_query = f"SHOW TABLES LIKE '{v_year + '_' + 'hun_hang'}';"
    cur.execute(check_table_query)
    
    # 존재하는 테이블을 확인하고 그에 따라서 처리
    if cur.fetchone():  # 테이블이 존재하는 경우
        # 테이블 이름 설정
        table_name = v_year + '_' + 'hun_hang'
    else:
        if int(v_year) == current_year + 1:
            # previous_year_table = str(current_year) + '_' + 'cost_hang' # budg_year 가 내년이면 전년은 당해년도
            table_name = v_year + '_' + 'hun_hang' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id int AI PK, gubun VARCHAR(6) not null, cost_hang VARCHAR(12) not null);"
            cur.execute(create_table_query)
        else:
            table_name = str(current_year) + '_' + 'hun_hang' # budg_year 가 내년이면 전년은 당해년도
    
    try:
        for data in hun_imsi:
            gubun, hun_hang = data
            hun_hang_sql = "INSERT INTO {} (hun_gubun, hun_hang) VALUES (%s, %s);".format(table_name)
            cur.execute(hun_hang_sql, (gubun,hun_hang))

        QMessageBox.about(None,'저장',"'지출 항 이 저장되었습니다.!!!")
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.critical(None, '에러', f'데이터 삭제 중 오류 발생: {error}')
        
    conn.commit()
    conn.close()

def current_year_hun_mok_save_sql(v_year,hun_imsi):
    current_year = today.year()
    
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    current_year = today.year()
    check_table_query = f"SHOW TABLES LIKE '{v_year + '_' + 'hun_mok'}';"
    cur.execute(check_table_query)

    try:
        # 존재하는 테이블을 확인하고 그에 따라서 처리
        if cur.fetchone():  # 테이블이 존재하는 경우
            # 테이블 이름 설정
            table_name = v_year + '_' + 'hun_mok'
        else:
            if int(v_year) == current_year + 1:
                previous_year_table = str(current_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
                table_name = v_year + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
                # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id int AI PK, gubun VARCHAR(5) not null, cost_hang VARCHAR(12) not null, cost_mok VARCHAR(12) not null));"
                cur.execute(create_table_query)
            else:
                table_name = str(current_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
                
        for data in hun_imsi:
            gubun, hun_hang, hun_mok = data
            hun_mok_sql = "INSERT INTO {} (gubun, hun_hang, hun_mok) VALUES (%s, %s, %s);".format(table_name)
            cur.execute(hun_mok_sql, (gubun, hun_hang, hun_mok))
        
        QMessageBox.about(None,'저장',"'데이터가 저장되었습니다.!!!")
        
        conn.commit()
        conn.close()
    
    except pymysql.Error as error :
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.critical(None, '에러', f'데이터 삭제 중 오류 발생: {error}')

def current_year_hun_semok_save_sql(v_year,hun_imsi):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    current_year = today.year()
    check_table_query = f"SHOW TABLES LIKE '{v_year + '_' + 'hun_semok'}';"
    cur.execute(check_table_query)

    try:
        # 존재하는 테이블을 확인하고 그에 따라서 처리
        if cur.fetchone():  # 테이블이 존재하는 경우
            # 테이블 이름 설정
            table_name = v_year + '_' + 'hun_semok'
        else:
            if int(v_year) == current_year + 1:
                previous_year_table = str(current_year) + '_' + 'hun_semok' # budg_year 가 내년이면 전년은 당해년도
                table_name = v_year + '_' + 'hun_semok' # budg_year 가 내년이면 전년은 당해년도
                # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id int AI PK, cost_mok VARCHAR(12) not null, cost_semok VARCHAR(12) not null);"
                cur.execute(create_table_query)
            else:
                table_name = str(current_year) + '_' + 'hun_semok' # budg_year 가 내년이면 전년은 당해년도

        for data in hun_imsi:
            hun_mok, hun_semok = data
            hun_semok_sql = "INSERT INTO {} (hun_mok, hun_semok) VALUES (%s, %s);".format(table_name)
            cur.execute(hun_semok_sql, (hun_mok, hun_semok))
        QMessageBox.about(None,'저장',"'저장되었습니다.!!!")
        
        conn.commit()
        conn.close()

    except pymysql.Error as error :
            QMessageBox.critical(None, '에러', f'데이터 저장 중 오류 발생: {error}')

            
        
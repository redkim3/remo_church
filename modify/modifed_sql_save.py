import pymysql,  configparser
from PyQt5.QtWidgets import *
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def update_hun_db_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
            
    update_query = f"UPDATE hun_db SET date = %s, code1 = %s, name_diff = %s, amount = %s, bank = %s, marks = %s, user_name = %s WHERE id = %s"

    # 데이터베이스에 연결하여 값을 업데이트
    cur.execute(update_query, tuple(change_data,))
    conn.commit()
    change_data = []

    cur.close()
    conn.close()


def delete_row_from_database(id):
    # MySQL 데이터베이스와 연결하는 코드
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    delete_query = "DELETE FROM hun_db WHERE id = %s"
    cur.execute(delete_query, (id,))  # 예를 들어, id가 1부터 시작하는 경우
    conn.commit()

    # 연결 해제
    cur.close()
    conn.close()

# 선택행 수정()
def update_cost_db_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
            
    update_query = f"UPDATE cost_db SET date = %s, cost_memo = %s, amount = %s, pay_banks = %s, marks = %s, user_name = %s WHERE id = %s"

    # 데이터베이스에 연결하여 값을 업데이트
    cur.execute(update_query, change_data,)
    conn.commit()

    cur.close()
    conn.close()
    QMessageBox.information(None, "완료", "지출내역 정보가 변경 되었습니다.")


def cost_delete_row_from_database(id):
    # MySQL 데이터베이스와 연결하는 코드
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    delete_query = "DELETE FROM cost_db WHERE id = %s"
    cur.execute(delete_query, (id,))  # 예를 들어, id가 1부터 시작하는 경우
    conn.commit()

    # 연결 해제
    cur.close()
    conn.close()

def selected_row_data_call(id):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    selected_id_call_query = "SELECT * FROM cost_db WHERE id = %s"
    cur.execute(selected_id_call_query, (id,))  # 예를 들어, id가 1부터 시작하는 경우
    
    data = cur.fetchall()
    
    # 연결 해제
    cur.close()
    conn.close()

    return data

def cost_db_row_modify(data):
    # MySQL 데이터베이스와 연결하는 코드
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 데이터 설정
    cost_save_sql = "UPDATE cost_db set date = %s, year = %s, month = %s, week = %s, gubun = %s, cost_hang = %s, cost_mok = %s, cost_semok = %s," \
        "cost_memo = %s, amount = %s, pay_banks = %s, marks = %s, user_name = %s where id = %s;"
    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    
    cur.execute(cost_save_sql, data)
    conn.commit()

    conn.close()
    QMessageBox.about(None,'',"저장이 완료되었습니다.!!!")
    record = 'saved'
    
    return record

def special_selected_row_data_call(id):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    selected_id_call_query = "SELECT * FROM balance_db WHERE id = %s"
    cur.execute(selected_id_call_query, (id,))  # 예를 들어, id가 1부터 시작하는 경우
    
    data = cur.fetchall()
    
    # 연결 해제
    cur.close()
    conn.close()

    return data

def balance_db_row_modify(data):
    # MySQL 데이터베이스와 연결하는 코드
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 데이터 설정 
    cost_save_sql = "UPDATE balance_db set date = %s, year = %s, month = %s, week = %s, gubun = %s,cost_hang = %s, cost_mok = %s, cost_semok = %s," \
        "cost_memo = %s, bank_account = %s, amount = %s, balance = %s, marks = %s, user_name = %s where id = %s;"
    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    
    cur.execute(cost_save_sql, data)
    conn.commit()

    conn.close()
    QMessageBox.about(None,'',"저장이 완료되었습니다.!!!")
    record = 'saved'
    
    return record
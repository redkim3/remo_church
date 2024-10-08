import pymysql,  configparser
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

def update_hun_db_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
            
    
    hun_update_query = "UPDATE hun_db SET date = %s, year = %s, month = %s, week = %s, code1 = %s, name_diff = %s, gubun = %s,"\
             "hun_hang = %s, hun_mok = %s, amount = %s, hun_detail = %s, Bank = %s, marks = %s, user_name = %s WHERE id = %s;"

    # 데이터베이스에 연결하여 값을 업데이트
    cur.execute(hun_update_query, change_data,)
    conn.commit()

    cur.close()
    conn.close()


def hun_delete_row_from_database(id):
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

def selected_row_data_call(id):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행 
    selected_id_call_query = "SELECT * FROM hun_db WHERE id = %s"
    cur.execute(selected_id_call_query, (id,))  # 예를 들어, id가 1부터 시작하는 경우
    
    data = cur.fetchall()
    
    # 연결 해제
    cur.close()
    conn.close()

    return data

def other_income_edit(extracted_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()
    
    update_query = f"UPDATE hun_db SET date = %s, hun_mok = %s, amount = %s, marks = %s WHERE id = %s"
    cur.execute(update_query, tuple(extracted_data))
    conn.commit()

    cur.close()
    conn.close()
    
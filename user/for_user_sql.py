import configparser,  hashlib
import pymysql
from PyQt5.QtWidgets import QMessageBox
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

# MySQL 연결 설정 

def add_user_sql(data):
    conn = pymysql.connect(host=host_name, user = 'root', password= '0000', db = 'isbs2024', charset = 'utf8')
    cur = conn.cursor()
    data = data[0]
    
    try:
        add_user_query = f"""INSERT INTO user_table (user_id, reg_date, registed_id, user_name, 
                        user_password, Ge_check,sun_check,special_check,hun_detail_check, user_reg_check)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
        
        cur.execute(add_user_query,data)
        conn.commit()
        
        # # 데이터베이스 접근 사용자 추가(이것은 만들지 말자)
        # new_user_id = data[0]
        # new_password = data[4]
        # creat_user_query = f"""CREATE USER '{new_user_id}'@'{host_name}' IDENTIFIED BY '{new_password}';"""
        # cur.execute(creat_user_query)

        #  # 사용자에게 데이터베이스 액세스 권한 부여
        # grant_privileges_query = f"""GRANT ALL PRIVILEGES ON isbs2024.* TO '{new_user_id}'@'{host_name}';"""

        # cur.execute(grant_privileges_query)

        # QMessageBox.information(None, "사용자", "'{new_user_id}'에게 데이터베이스 액세스 권한을 부여 했습니다.")

        # conn.commit()
  
        data = []
        cur.close()
        conn.close()
        QMessageBox.information(None, "성공", "사용자가 성공적으로 추가되었습니다.")
        record = 'record'

    except pymysql.err.IntegrityError:
        QMessageBox.warning(None, "에러", "중복된 사용자 아이디입니다.")
        record = 'exist'
    return record

    # except Exception as e:
    #     QMessageBox.critical(None, "에러", f"오류 발생: {str(e)}")

def hash_password(user_password):
    # 사용할 해시 알고리즘 선택 (여기서는 SHA256 사용)
    hasher = hashlib.sha256()
    # 비밀번호를 바이트 문자열로 변환하여 해시 함수에 업데이트
    hasher.update(user_password.encode('utf-8'))
    # 해시된 결과 반환
    return hasher.hexdigest()
    

def update_row_sql(change_data):
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # new_password = change_data[3]
    # user_id = change_data[8] # regist_user.py에서 user_id를 넣었음
    update_query = """UPDATE user_table SET reg_date = %s, user_name = %s, 
                user_password = %s, Ge_check = %s,sun_check = %s,special_check = %s,
                hun_detail_check = %s, user_reg_check = %s WHERE user_id = %s;
            """
    
    # 데이터베이스에 연결하여 값을 업데이트 
    cur.execute(update_query, change_data,)
    conn.commit()
    
    # update_query =f""" ALTER USER '{user_id}'@'{host_name}' IDENTIFIED BY '{new_password}';"""

    # cur.execute(update_query)
    # conn.commit()
    # change_data = []

    cur.close()
    conn.close()


def delete_row_from_database(user_id):
    # MySQL 데이터베이스와 연결하는 코드
    conn = pymysql.connect(host=host_name,user="root",password="0000", db="isbs2024", charset='utf8' )
    cur = conn.cursor()

    # 테이블에서 해당하는 행을 삭제하는 SQL 쿼리 실행
    delete_query = """DELETE FROM user_table WHERE user_id = %s"""
    cur.execute(delete_query, (user_id,))  # 예를 들어, id가 1부터 시작하는 경우 
    conn.commit()

    # delete_user_query = f"""DROP USER '{user_id}'@'{host_name}';"""
    # cur.execute("DROP USER '{user_id}'@'{host_name}';")
    
    # conn.commit()

    # 연결 해제
    cur.close()
    conn.close()

def user_view_sql():
    conn = pymysql.connect(host=host_name, user = 'root', password= '0000', db = 'isbs2024', charset = 'utf8')
    cur = conn.cursor()
    user_data = []
    user_view_query = f"""select user_id, reg_date, user_name, user_password, 
                    Ge_check,sun_check,special_check,hun_detail_check, user_reg_check,
                    connect_from
                    from user_table """
    
    cur.execute(user_view_query)
    user_data = cur.fetchall()
    
    cur.close()
    conn.close()
    return user_data

def user_infor_sql(user_id):
    conn = pymysql.connect(host=host_name, user = 'root', password= '0000', db = 'isbs2024', charset = 'utf8')
    cur = conn.cursor()
    user_data = []
    user_view_query = f"""select user_name, Ge_check,sun_check,special_check,hun_detail_check, user_reg_check
                    from user_table where user_id = %s ;"""
    
    cur.execute(user_view_query,(user_id,))
    user_data = cur.fetchall()
    
    cur.close()
    conn.close()
    return user_data
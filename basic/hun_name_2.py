import pymysql
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

today = QDate.currentDate()
v_year = str(today.year())

def gubun_values_check(ge_check):
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    gubun_call = []
    if ge_check == 1 :
        gubun_sql = 'select * from gubun;'

        cur.execute(gubun_sql)
        while(True):
            row = cur.fetchone()
            if row == None : 
                break
            data1 = row[1]
            
            gubun_call.append(data1)
    
        conn.close()
    else:
        gubun_call.append('선교회계')

    return gubun_call

def gubun_values():
    conn = pymysql.connect(host=host_name ,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    gubun_call = []
    
    gubun_sql = """select * from gubun;"""

    cur.execute(gubun_sql)
    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[1]
        
        gubun_call.append(data1)

    conn.close()

    return gubun_call

def gubun_mok_values(v_year, gubun):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록 
    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()

    try: 
        
        current_year = today.year()
        table_name = str(v_year) + '_' + 'hun_mok'
        if table_name:
            gubun_mok_call = []
            if gubun == '일반회계':
                # hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang != '선교헌금' and hun_hang != '특별회계'
                #                  and hun_hang != '기타소득' ;""".format(table_name)
                hun_mok_sql = """SELECT hun_mok FROM {} where gubun = '일반회계' and hun_hang != '기타소득';""".format(table_name)
                cur.execute(hun_mok_sql)
            elif gubun == '선교회계':
                hun_mok_sql = """SELECT hun_mok FROM {} where gubun = '선교회계' 
                                and hun_mok != '타회계이월' and hun_mok != '이자소득_선교';""".format(table_name)  # 
                cur.execute(hun_mok_sql)
            elif gubun == '특별회계':
                QMessageBox.about(None,"특별회계","'특별회계의 입력은 기타소득에서 입력하세요.")
                # hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang = '특별회계';""".format(table_name)  # and hun_mok = '선교헌금' and hun_mok = '구역헌금'
                # cur.execute(hun_mok_sql)
                gubun_mok_call = []
                return gubun_mok_call
            # else:
            #     raise Exception('현재는 일반회계와 선교회계만을 대상으로 합니다.') 

            while(True):
                row = cur.fetchone()
                if row == None : 
                    break
                data1 = row[0]
                gubun_mok_call.append(data1)
        else:
            v_year == current_year
            previous_year_table = str(current_year - 1) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(v_year) + '_' + 'hun_mok' # 테이블이 없으면 전녀도 테이블을 모두 복사 
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM {previous_year_table}"
            cur.execute(create_table_query)

            gubun_mok_call = []
            if gubun == '일반회계':
                hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang != '선교헌금' and hun_hang != '특별회계' and hun_hang != '기타소득';""".format(table_name)
                cur.execute(hun_mok_sql)
            elif gubun == '선교회계':
                hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang = '선교헌금' and hun_mok = '선교헌금' or hun_mok = '구역헌금';""".format(table_name)  # 
                cur.execute(hun_mok_sql)
            elif gubun == '특별회계':
                QMessageBox.about(None,"특별회계","'특별회계의 입력은 기타소득에서 입력하세요.")
                # hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang = '특별회계';""".format(table_name)  # and hun_mok = '선교헌금' and hun_mok = '구역헌금'
                # cur.execute(hun_mok_sql)
                gubun_mok_call = []
                return gubun_mok_call
            # else:
            #     raise Exception('현재는 일반회계와 선교회계만을 대상으로 합니다.') 

            while(True):
                row = cur.fetchone()
                if row == None : 
                    break
                data1 = row[0]
                gubun_mok_call.append(data1)

    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.information("예산 '헌금 목'이 없습니다.")

    finally:
        conn.close()
        
    return gubun_mok_call

def mok_hang_values(v_year,hun_mok,gubun): # 헌금입력에서 목을 가지고 항을 찾을때
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    try:
        current_year = today.year()
        table_name = str(v_year) + '_' + 'hun_mok'
        
        if v_year == current_year + 1:
            previous_year_table = str(current_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(v_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"""
            cur.execute(create_table_query)
   
        hun_hang_call = []
    
        hun_hang_sql = """SELECT hun_hang FROM {} where hun_mok = %s and gubun = %s """.format(table_name)
        cur.execute(hun_hang_sql,(hun_mok,gubun))
        while(True):
            row = cur.fetchone()
            if row == None : 
                break
            data1 = row[0]
            hun_hang_call.append(data1)
        
        conn.commit()
        conn.close()

        return hun_hang_call
    
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.information("예산 '헌금 항'이 없습니다.")

    
def hun_hang_values(v_year,gubun_code):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # try:
    current_year = today.year()
    table_name = str(v_year) + '_' + 'hun_hang'
    table_name = f"{v_year}_hun_hang"

    # 테이블 존재 여부 확인
    cur.execute(f"select table_name from information_schema.tables where table_schema = 'isbs2024' and table_name = '{table_name}'; ")
    table_exists = cur.fetchone()
    
    if table_exists:
        hun_hang_call = []
    
        hun_hang_sql = 'SELECT hun_hang, id FROM {} where hun_gubun = %s'.format(table_name)
        cur.execute(hun_hang_sql,(gubun_code,))

        hun_hang_call = cur.fetchall()
        
        conn.commit()
        conn.close()

        return hun_hang_call
    else:
        v_year = current_year
        table_name = str(v_year) + '_' + 'hun_hang' # budg_year 가 내년이면 전년은 당해년도
        # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
        create_table_query = f"""
                        CREATE TABLE IF NOT EXISTS `{table_name}` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `hun_gubun` VARCHAR(6) NOT NULL,
                            `hun_hang` VARCHAR(8) NOT NULL,
                            PRIMARY KEY (`id`)
                        );
                        """
        cur.execute(create_table_query)

        hun_hang_call = []
    
        hun_hang_sql = 'SELECT hun_hang, id FROM {} where hun_gubun = %s'.format(table_name)
        cur.execute(hun_hang_sql,(gubun_code,))

        hun_hang_call = cur.fetchall()
        
        
        conn.commit()
        conn.close()

        return hun_hang_call

def hun_mok_values(v_year,hang):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록 
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    try: 
        table_name = str(v_year) + '_' + 'hun_mok'

            # 테이블 존재 여부 확인
        cur.execute(f"select table_name from information_schema.tables where table_schema = 'isbs2024' and table_name = '{table_name}'; ")
        table_exists = cur.fetchone()
    
        if table_exists:
        
            hun_mok_call = []
            
            hun_mok_sql = "SELECT hun_mok, id FROM {} where hun_hang = %s;".format(table_name)
            cur.execute(hun_mok_sql, (hang,))
            hun_mok_call = cur.fetchall()
            # while(True):
            #     row = cur.fetchone()
            #     if row == None : 
            #         break
            #     data1 = row[0]
                
            #     hun_mok_call.append(data1)
            
            conn.close()

            return hun_mok_call
        else:
            table_name = str(v_year) + '_' + 'hun_mok' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
    
            create_table_query = f"""
                            CREATE TABLE IF NOT EXISTS `{table_name}` (
                                `id` INT NOT NULL AUTO_INCREMENT,
                                `hun_hang` VARCHAR(8) NOT NULL,
                                `hun_mok` VARCHAR(12) NOT NULL,
                                PRIMARY KEY (`id`)
                            );
                            """
            cur.execute(create_table_query)

            hun_hang_call = []
        
            hun_hang_sql = 'SELECT hun_mok, id FROM {} where hun_hang = %s'.format(table_name)
            cur.execute(hun_hang_sql,(hang,))

            hun_hang_call = cur.fetchall()

            conn.commit()
            conn.close()

            return hun_hang_call
    
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.information("예산 '헌금 목'이 없습니다.")

def hun_semok_values(v_year,hun_mok):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    v_year = int(v_year)

    try: 
        table_name = str(v_year) + '_' + 'hun_semok'
        cur.execute("""
                select table_name from information_schema.tables
                where table_schema = 'isbs2024' and table_name = %s;
            """, (table_name))

        # 존재하는 테이블을 확인하고 그에 따라서 처리 
        table_exists = cur.fetchone()  # 테이블이 존재하는 경우
        if table_exists:
            hun_semok_call = []
            if hun_mok == '전체':
                hun_semok_sql = 'SELECT hun_semok FROM {}'.format(table_name)
                cur.execute(hun_semok_sql)
            else:
                hun_semok_sql = 'SELECT hun_semok, id FROM {} where hun_mok = %s'.format(table_name)
                cur.execute(hun_semok_sql,(hun_mok,))
            
            hun_semok_call = cur.fetchall()
            conn.commit()
            conn.close()

        else:
            previous_year_table = str(v_year - 1) + '_' + 'hun_semok' # budg_year 가 내년이면 전년은 당해년도
            table_name = str(v_year) + '_' + 'hun_semok' # budg_year 가 내년이면 전년은 당해년도
            # 전년도 테이블의 구조를 복제하여 새로운 테이블 생성
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {previous_year_table}"
            cur.execute(create_table_query)
            
            hun_semok_call = []
            if hun_mok == '전체':
                hun_semok_sql = 'SELECT hun_semok FROM {}'.format(table_name)
                cur.execute(hun_semok_sql)
            else:
                hun_semok_sql = 'SELECT hun_semok, id FROM {} where hun_mok = %s'.format(table_name)
                cur.execute(hun_semok_sql,(hun_mok,))
            
            hun_semok_call = cur.fetchall()
            conn.commit()
            conn.close()
        
        return hun_semok_call
    
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
            # 여기에 에러 처리 로직을 추가하세요


def other_hun_mok_values(Y1, gubun):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    # try:
    table_name = str(Y1) + '_' + 'hun_mok'
    other_hun_mok_call = []
    other_hun_mok_sql = ''  # 변수 미리 선언 및 초기화

    if gubun == '일반회계':
        other_hun_mok_sql = "SELECT hun_mok FROM {} WHERE gubun = '일반회계' and hun_hang = '기타소득';".format(table_name)
    elif gubun == '선교회계':
        other_hun_mok_sql = "SELECT hun_mok FROM {} WHERE gubun = '선교회계' and hun_hang = '선교헌금' AND hun_mok != '선교헌금' AND hun_mok != '구역헌금';".format(table_name)
    else:
        if gubun == '특별회계':
            other_hun_mok_sql = """SELECT hun_mok FROM {} where gubun = '특별회계';""".format(table_name)  # and hun_mok = '선교헌금' and hun_mok = '구역헌금'
            # QMessageBox.about(None,"특별회계","'특별회계의 입력은 기타소득에서 입력하세요.")
    cur.execute(other_hun_mok_sql)
    rows = cur.fetchall()
    if rows:
        other_hun_mok_call = [row[0] for row in rows]

    cur.close()
    conn.close()
    
    return other_hun_mok_call

def other_hun_mokhang_values(v_year,hun_mok):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    table_name = str(v_year) + '_' + 'hun_mok'
    hun_mokhang_call = []

    hun_mokhang_sql = 'SELECT hun_hang FROM {} where hun_mok = %s'.format(table_name)
    cur.execute(hun_mokhang_sql,(hun_mok,))

    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        
        hun_mokhang_call.append(data1)
    
    conn.close()

    return hun_mokhang_call

def cost_hang_values(v_year,gubun):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    table_name = v_year + '_' + 'cost_hang'
    cost_hang_call = []

    try:
        cost_hang_sql = 'SELECT cost_hang FROM {} where gubun = %s'.format(table_name)
        cur.execute(cost_hang_sql,(gubun,))
        while(True):
            row = cur.fetchone()
            if row == None : 
                break
            data1 = row[0]
            cost_hang_call.append(data1)
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


    return cost_hang_call

def cost_mok_values(v_year,cost_hang):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    table_name = str(v_year) + '_' + 'cost_mok'
    cost_mok_call = []
    if cost_hang == '전체':
        cost_mok_sql = 'SELECT cost_mok FROM {}'.format(table_name)    
        cur.execute(cost_mok_sql)
    else:
        cost_mok_sql = 'SELECT cost_mok FROM {} where cost_hang = %s'.format(table_name)
        cur.execute(cost_mok_sql,(cost_hang,))

    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        
        cost_mok_call.append(data1)
    
    conn.close()

    return cost_mok_call

def cost_semok_values(v_year,cost_mok):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록 
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    table_name = v_year + '_' + 'cost_semok'
    cost_semok_call = []
    if cost_mok == '전체':
        cost_semok_sql = 'SELECT cost_semok FROM {}'.format(table_name)
        cur.execute(cost_semok_sql)
    else:
        cost_semok_sql = 'SELECT cost_semok FROM {} where cost_mok = %s'.format(table_name)
        cur.execute(cost_semok_sql,(cost_mok,))

    while(True):
        row = cur.fetchone()
        if row == None : 
            break
        data1 = row[0]
        
        cost_semok_call.append(data1)
    
    conn.close()

    return cost_semok_call

def mok_list(v_year, hang):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    try:
        table_name = str(v_year) + '_' + 'hun_mok'
            
        hun_mok_sql = 'SELECT hun_mok FROM {} where hun_hang = %s;'.format(table_name)
        cur.execute(hun_mok_sql,(hang,))

        mok_list = cur.fetchall()

        conn.close()
    except pymysql.err.ProgrammingError:
        mok_list = []

    return mok_list

def other_gubun_mok_values(v_year, gubun):  # 헌금 등록할때 헌금항 과 회계구분을 안보여도 진행하도록 
    conn = pymysql.connect(host= host_name, user='root', password='0000', db='isbs2024', charset='utf8')
    cur = conn.cursor()

    try: 
        
        current_year = today.year()
        table_name = str(v_year) + '_' + 'hun_mok'
        if table_name:
            gubun_mok_call = []
            if gubun == '일반회계':
                # hun_mok_sql = """SELECT hun_mok FROM {} where hun_hang != '선교헌금' and hun_hang != '특별회계'
                #                  and hun_hang != '기타소득' ;""".format(table_name)
                hun_mok_sql = """SELECT hun_mok FROM {} where gubun = '일반회계';""".format(table_name)
                cur.execute(hun_mok_sql)
            elif gubun == '선교회계':
                hun_mok_sql = """SELECT hun_mok FROM {} where gubun = '선교회계';""".format(table_name)  # 
                cur.execute(hun_mok_sql)
            else: 
                QMessageBox.information(None,"정보","특별회계는 선택 할 수 없습니다.")
                return None

            while(True):
                row = cur.fetchone()
                if row == None : 
                    break
                data1 = row[0]
                gubun_mok_call.append(data1)
        
    except pymysql.Error as error: #.ProgrammingError:
        if error.args[0] == 1406:  # MySQL 에러 코드 1406: 열에 너무 많은 데이터가 들어감
            QMessageBox.information("MySQL 데이터가 너무 깁니다:", error)
        else:
            QMessageBox.information("예산 '헌금 목'이 없습니다.")

    finally:
        conn.close()
        
    return gubun_mok_call


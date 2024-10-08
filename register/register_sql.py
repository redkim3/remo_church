import pymysql, os
import configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
cur_fold = os.getcwd()

def hun_register(data):
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # 데이터 설정
    hun_save_sql = """INSERT INTO hun_db (date, year, month, week, code1, name_diff, gubun, hun_hang, hun_mok,
            amount, hun_detail, Bank, marks, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    cur.execute(hun_save_sql, data)
                    
    conn.commit()
    conn.close()
    cur.close()

def cost_register(data):
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    # 데이터 설정
    cost_save_sql = "INSERT INTO cost_db (date, year, month, week, gubun,cost_hang, cost_mok, cost_semok," \
        "cost_memo, amount, pay_banks, marks, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    cur.execute(cost_save_sql, data)

    conn.commit()
    conn.close()

def other_register(data2):
    conn = pymysql.connect(host = host_name, user='root', password='0000', db='isbs2024',charset='utf8')
    cur = conn.cursor()
    # 데이터 설정 
    other_save_sql = """INSERT INTO hun_db (date, year, month, week, code1, name_diff, gubun, 
                        hun_hang, hun_mok, amount, hun_detail, Bank, marks, user_name) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
    cur.execute(other_save_sql, data2)
                
    conn.commit()
    conn.close()

def contribution_reg(data):
    conn = pymysql.connect(host = host_name, user='root', password='0000', db = 'isbs2024',charset ='utf8')
    cur = conn.cursor()

    contribution_list_save_sql = """
            insert into contribution_list (issued_date, issued_sign, target_year, hap_code, name_diff, id_no, addr, type_acc,
            type_code, gubun, startdate, enddate, jujeong_ratio, amount, issued_type, issue_church, biz_no, church_address) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
    
    cur.execute(contribution_list_save_sql,data)

    conn.commit()
    conn.close()

def contribution_re_reg(data_tu):
    conn = pymysql.connect(host = host_name, user='root', password='0000', db = 'isbs2024',charset ='utf8')
    cur = conn.cursor()
    
    contribution_list_save_sql = """
        INSERT INTO contribution_list (issued_date, issued_sign, target_year, hap_code, name_diff, id_no, addr, type_acc,
        type_code, gubun, startdate, enddate, jujeong_ratio, amount, issued_type, issue_church, biz_no, church_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # 쿼리 실행 
    cur.execute(contribution_list_save_sql, data_tu[0])

    conn.commit()
    conn.close()

def asset_control_register(data):
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    # 데이터 설정
    cost_save_sql = "INSERT INTO balance_db (date, year, month, week, gubun, cost_hang, cost_mok, cost_semok," \
        "cost_memo, bank_account, amount, balance, marks, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    cur.execute(cost_save_sql, data)

    conn.commit()
    conn.close()
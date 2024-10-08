import pymysql, decimal
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def p_hun_list(Y1, p_code): # 헌금 명칭(hun_mok)별 리스트

    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    P_hun_name_sql = """
        SELECT hun_mok, date, name_diff, CAST(amount AS SIGNED) AS amount, hun_hang
        FROM hun_db WHERE year = %s AND code1 = %s; 
    """

    cur.execute(P_hun_name_sql, (Y1, p_code,))

    hun_list = cur.fetchall()

    cur.close()

    return hun_list

def hap_hun_list(Y1, hap_code): # 헌금 명칭(hun_mok)별 리스트
    from basic.member import code1_select_by_hapcode
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    hap_hun = []
    # 합코드에 포함된 개별코드 가져오기
    codes = code1_select_by_hapcode(hap_code)
    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    for code1 in codes:
        P_hun_name_sql = """
            SELECT hun_mok, date, name_diff, CAST(amount AS SIGNED) AS amount, hun_hang
            FROM hun_db WHERE year = %s AND code1 = %s ORDER BY date;; 
        """
        cur.execute(P_hun_name_sql, (Y1, code1,))
        rows = cur.fetchall()
        hap_hun.extend(rows)  # 모든 행을 리스트에 추가

    return hap_hun

def week_hun_list(Y1, M1, W1, gubun, mok): # 헌금 명칭(hun_mok)별 리스트
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    # 합코드에 포함된 개별코드 가져오기
    hun_week_list = []
    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    
    hun_week_list_sql = """
        SELECT date, code1, name_diff, amount, bank, marks, id
        FROM hun_db WHERE year = %s AND month = %s AND week = %s AND gubun = %s AND hun_mok = %s
        ORDER BY amount DESC; 
    """
    cur.execute(hun_week_list_sql, (Y1, M1, W1, gubun, mok,))
    hun_week_list_data = cur.fetchall()
    hun_week_list.extend(hun_week_list_data)  # 모든 행을 리스트에 추가
    

    return hun_week_list

def other_income_view_sql(Y1, gubun): # 헌금 명칭(hun_mok)별 리스트
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    # 합코드에 포함된 개별코드 가져오기
    other_income_list_view = []
    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    if gubun == '일반회계':
        other_income_list_sql = """
            SELECT date, hun_mok, amount, marks, id
            FROM hun_db WHERE year = %s AND gubun = %s AND hun_hang = "기타소득";
        """
    elif gubun == '선교회계':
        other_income_list_sql = """
            SELECT date, hun_mok, amount, marks, id
            FROM hun_db WHERE year = %s AND gubun = %s AND hun_hang = "선교헌금" and (hun_mok = '타회계이월' or hun_mok = '이자소득_선교');
        """
    else: # 특별회계 이면
        other_income_list_sql = """
            SELECT date, cost_semok, amount, marks, id
            FROM balance_db WHERE year = %s AND gubun = %s AND cost_semok = "타회계이월";
        """
    cur.execute(other_income_list_sql, (Y1,gubun))
    other_income_data = cur.fetchall()
    other_income_list_view.extend(other_income_data)  # 모든 행을 리스트에 추가 
    

    return other_income_list_view


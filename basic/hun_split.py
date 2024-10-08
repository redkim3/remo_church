import pymysql, decimal
from PyQt5.QtCore import QDate
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
today = QDate.currentDate()
c_year = str(today.year())

def today_income_report(Y1,M1,W1) : # 각 회계주체별 당일 입금 총액(각 헌금별 금액을 group by 를 사용하여 구했다)
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name_1 = str(c_year) + '_' + 'hun_mok'
    order_mok = f"select id, hun_mok from {table_name_1} order by id asc;"
    cur.execute(order_mok)
    
    order_hang_tuple = cur.fetchall()
    desireed_order_column_list = [item[1] for item in order_hang_tuple]  # tuple을 리스트로 변경하는 것
    #order_column = ', '.join([f'"{col}"' for col in desireed_order_column_list])

    group_sum_sql = f"""
        SELECT hun_mok, SUM(amount) AS 합계금액, hun_hang
        FROM hun_db WHERE year = %s AND month = %s AND week = %s AND gubun != '선교회계'
        GROUP BY hun_mok, hun_hang
        ORDER BY FIND_IN_SET(hun_mok, %s);
    """
                            #  ORDER BY sum(amount) DESC 
    cur.execute(group_sum_sql, (Y1, M1, W1, ','.join(desireed_order_column_list)))
    result_tuple = cur.fetchall()

    result = [(row[0], int(row[1]), row[2]) for row in result_tuple]
   
    cur.close()
    conn.close()
    return result


def today_total_income(Y1,M1,W1) : # 각 회계주체별 당일 입금 총액(각 헌금별 금액을 group by 를 사용하여 구했다)
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    table_name_1 = str(Y1) + '_' + 'hun_mok'
    order_mok = f"select id, hun_mok from {table_name_1} order by id asc;"
    cur.execute(order_mok)

    order_hang_tuple = cur.fetchall()
    desireed_order_column_list = [item[1] for item in order_hang_tuple]  # tuple을 리스트로 변경하는 것
    #order_column = ', '.join([f'"{col}"' for col in desireed_order_column_list])

    group_sum_sql = f"""
        SELECT hun_mok, SUM(amount) AS 합계금액, hun_hang, marks
        FROM hun_db WHERE year = %s AND month = %s AND week = %s AND gubun != '선교회계'
        GROUP BY hun_mok, hun_hang, marks
        ORDER BY FIND_IN_SET(hun_mok, %s);
    """
                            #  ORDER BY sum(amount) DESC 
    cur.execute(group_sum_sql, (Y1, M1, W1, ','.join(desireed_order_column_list)))
    result_tuple = cur.fetchall()

    result = [(row[0], int(row[1]), row[2], row[3]) for row in result_tuple]
   
    cur.close()
    conn.close()
    return result


def today_hun_list(Y1, M1, W1): # 헌금 명칭(hun_mok)별 리스트

    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    hun_name_sql = """
        SELECT hun_mok, hun_hang, name_diff, CAST(amount AS SIGNED) AS amount, hun_detail, bank, marks
        FROM hun_db WHERE year = %s AND month = %s AND week = %s; 
    """

    cur.execute(hun_name_sql, (Y1, M1, W1))

    hun_list = cur.fetchall()

    cur.close()

    return hun_list

def bank_income_call(Y1,M1,W1):  # 헌금유형별 통장예입 금액
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    group_sum_sql = """SELECT hun_mok, SUM(amount) as 금액합계
        FROM hun_db WHERE year = %s AND month = %s AND week = %s and bank = '통장예입' GROUP BY hun_mok; """
    cur.execute(group_sum_sql,(Y1,M1,W1,))  # 현금으로 입금된 각 목록별 금액 (이부분은 수정함 and gubun != '선교회계')
    #      SUM(CASE WHEN bank == NULL OR bank != '통장예입' THEN amount ELSE 0 END) AS amount_without_bank   현금수입은 제외함 
    group_sum = cur.fetchall()

    # conn.commit()
    cur.close()

    return group_sum



def past_income_sum(Y1,M1,W1):  # 과거(기준일 이전)  - 총 합계금액 - 기준일의 금액 = 과거 금액
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    Ge_income_year_sql = "select sum(amount) from hun_db where gubun = '일반회계' and year < %s ;"
    Ge_income_month_sql = "select sum(amount) from hun_db where gubun = '일반회계' and year = %s and month < %s ;"
    Ge_income_week_sql = "select sum(amount) from hun_db where gubun = '일반회계' and year = %s and month = %s and week < %s ;"

    cur.execute(Ge_income_year_sql, (Y1,))
    Ge_income_year_value = cur.fetchall()
    Ge_income_year_value_result = Ge_income_year_value[0][0] if Ge_income_year_value and Ge_income_year_value[0][0] != None else decimal.Decimal('0')
    Ge_year_income = int(Ge_income_year_value_result)

    cur.execute(Ge_income_month_sql, (Y1, M1,))
    Ge_income_month_value = cur.fetchall()
    Ge_income_month_value_result = Ge_income_month_value[0][0] if Ge_income_month_value and Ge_income_month_value[0][0] != None else decimal.Decimal('0')
    Ge_month_income = int(Ge_income_month_value_result)

    cur.execute(Ge_income_week_sql, (Y1, M1, W1,))
    Ge_income_week_value = cur.fetchall()
    Ge_income_week_value_result = Ge_income_week_value[0][0] if Ge_income_week_value and Ge_income_week_value[0][0] != None else decimal.Decimal('0')
    Ge_week_income = int(Ge_income_week_value_result)

    past_Ge_income_value = Ge_year_income + Ge_month_income + Ge_week_income  # 누적금액 - 기준일 금액  = 기준일 이전의 금액

    cur.close()

    return past_Ge_income_value

def today_sun_income_list(Y1, M1, W1): # 헌금 명칭(hun_mok)별 리스트 

    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다. 
    hun_name_sql = """
        SELECT hun_mok, hun_hang, name_diff, CAST(amount AS SIGNED) AS amount, bank, marks
        FROM hun_db WHERE year = %s AND month = %s AND week = %s AND gubun = '선교회계'; 
    """

    cur.execute(hun_name_sql, (Y1, M1, W1))

    sun_list = cur.fetchall()

    cur.close()

    return sun_list


def past_sun_income(Y1,M1,W1):  # 과거(기준일 이전의 선교헌금)  - 총 합계금액 - 기준일의 금액 = 과거 금액
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    sun_income_year_sql = "select sum(amount) from hun_db where gubun = '선교회계' and year < %s "
    sun_income_month_sql = "select sum(amount) from hun_db where gubun = '선교회계' and year = %s and month < %s "
    sun_income_week_sql = "select sum(amount) from hun_db where gubun = '선교회계' and year = %s and month = %s and week < %s "

    cur.execute(sun_income_year_sql, (Y1,))
    sun_income_year_value = cur.fetchall()
    sun_income_year_value_result = sun_income_year_value[0][0] if sun_income_year_value and sun_income_year_value[0][0] != None else decimal.Decimal('0')
    sun_year_income = int(sun_income_year_value_result)

    cur.execute(sun_income_month_sql, (Y1, M1,))
    sun_income_month_value = cur.fetchall()
    sun_income_month_value_result = sun_income_month_value[0][0] if sun_income_month_value and sun_income_month_value[0][0] != None else decimal.Decimal('0')
    sun_month_income = int(sun_income_month_value_result)

    cur.execute(sun_income_week_sql, (Y1, M1, W1,))
    sun_income_week_value = cur.fetchall()
    sun_income_week_value_result = sun_income_week_value[0][0] if sun_income_week_value and sun_income_week_value[0][0] != None else decimal.Decimal('0')
    sun_week_income = int(sun_income_week_value_result)

    past_sun_income_value = sun_year_income + sun_month_income + sun_week_income  # 누적금액 - 기준일 금액  = 기준일 이전의 금액

    cur.close()

    return past_sun_income_value

def contribution_amount(Y1,hap_code):
    from basic.member import code1_select_by_hapcode
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    
    hap_hun = 0
    codes = code1_select_by_hapcode(hap_code)
    # hun_mok에 데이터가 있으면 name_diff로 의 금액을 합산하여 리스트 하는 것이다.
    for code1 in codes:
        P_hun_name_sql = """
            SELECT sum(amount) FROM hun_db WHERE year = %s AND code1 = %s ; 
        """
        cur.execute(P_hun_name_sql, (Y1, code1,))
        hun_amount = cur.fetchone()
    
        if hun_amount[0] == None:
            hap_hun += 0
        else:
            hap_hun += int(hun_amount[0])

    return hap_hun
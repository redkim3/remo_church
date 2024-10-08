import pymysql,decimal
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def today_cost_list(Y1,M1,W1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    today_cost_sql = """
            select cost_memo, amount, marks, pay_banks from cost_db 
            where year = %s and month = %s and week = %s and gubun = '일반회계';
            """
    
    cur.execute(today_cost_sql,(Y1,M1,W1))
    today_cost = cur.fetchall()

    cur.close()
    
    return today_cost

def past_cost_by_year_week(Y1,M1,W1): #  by year  ,    based on year
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    cost_year_sql = "select sum(amount) from cost_db where gubun = '일반회계' and year < %s ;"
    
    cur.execute(cost_year_sql, (Y1,))
    cost_year_value = cur.fetchall()
    cost_year_value_result = cost_year_value[0][0] if cost_year_value and cost_year_value[0][0] != None else decimal.Decimal('0')
    cost_year = int(cost_year_value_result)
    
    Ge_month_sql = "select sum(amount) from cost_db where gubun = '일반회계' and year = %s and month < %s ;"
    
    cur.execute(Ge_month_sql, (Y1, M1,))
    cost_month_value = cur.fetchall()
    cost_month_value_result = cost_month_value[0][0] if cost_month_value and cost_month_value[0][0] != None else decimal.Decimal('0')
    cost_month = int(cost_month_value_result)

    Ge_week_sql = "select sum(amount) from cost_db where gubun = '일반회계' and year = %s and month = %s and week < %s ;"

    cur.execute(Ge_week_sql, (Y1, M1, W1,))
    cost_week_value = cur.fetchall()
    cost_week_value_result = cost_week_value[0][0] if cost_week_value and cost_week_value[0][0] != None else decimal.Decimal('0')
    cost_week = int(cost_week_value_result)
    
    past_cost_amount = cost_year + cost_month + cost_week  # 누적금액 - 기준일 금액  = 기준일 이전의 금액
  
    cur.close()

    return past_cost_amount

def today_mission_cost_list(Y1,M1,W1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    today_sun_cost_sql = """
            select cost_memo, amount, marks, cost_mok from cost_db 
            where year = %s and month = %s and week = %s and gubun = '선교회계';
            """

    cur.execute(today_sun_cost_sql,(Y1,M1,W1,))
    today_sun_cost_list = cur.fetchall()

    cur.close()
        
    return today_sun_cost_list

def past_mission_cost(Y1,M1,W1):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    sun_cost_year_sql = "select sum(amount) from cost_db where gubun = '선교회계' and year < %s ;"
    sun_cost_month_sql = "select sum(amount) from cost_db where gubun = '선교회계' and year = %s and month < %s;"
    sun_cost_week_sql = "select sum(amount) from cost_db where gubun = '선교회계' and year = %s and month = %s and week < %s ;"

    cur.execute(sun_cost_year_sql, (Y1,))
    sun_cost_year_value = cur.fetchall()
    sun_cost_year_value_result = sun_cost_year_value[0][0] if sun_cost_year_value and sun_cost_year_value[0][0] != None else decimal.Decimal('0')
    sun_cost_year = int(sun_cost_year_value_result)

    cur.execute(sun_cost_month_sql, (Y1, M1,))
    sun_cost_month_value = cur.fetchall()
    sun_cost_month_value_result = sun_cost_month_value[0][0] if sun_cost_month_value and sun_cost_month_value[0][0] != None else decimal.Decimal('0')
    sun_cost_month = int(sun_cost_month_value_result)

    cur.execute(sun_cost_week_sql, (Y1, M1, W1,))
    sun_cost_week_value = cur.fetchall()
    sun_cost_week_value_result = sun_cost_week_value[0][0] if sun_cost_week_value and sun_cost_week_value[0][0] != None else decimal.Decimal('0')
    sun_cost_week = int(sun_cost_week_value_result)
    
    sun_past_cost_amount = sun_cost_year + sun_cost_month + sun_cost_week  # 누적금액 - 기준일 금액  = 기준일 이전의 금액
  
    cur.close()

    return sun_past_cost_amount

def cost_word_serch(Y1,word):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    cost_call_sql = """
            Select date, cost_hang, cost_mok, cost_semok, cost_memo, amount, marks from cost_db WHERE (cost_memo LIKE %s or marks like %s) and year = %s;
    """
    like_pattern = f"%{word}%"
    cur.execute(cost_call_sql, (like_pattern, like_pattern,Y1,))

    cost_word = cur.fetchall()

    cur.close()

    return cost_word
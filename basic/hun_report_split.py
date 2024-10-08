import configparser
from PyQt5.QtWidgets import QMessageBox
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']
from datetime import datetime

def past_hun(Y1): # 이전 년도 헌금 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_Ge_hungum_sql = """
                    SELECT SUM(amount) FROM hun_db WHERE year < %s and gubun = "일반회계"
                 """
    cur.execute(past_year_Ge_hungum_sql,(Y1,))
    past_year_Ge_hungum = cur.fetchall()

    cur.close()
    conn.close()
        
    return past_year_Ge_hungum

def past_cost(Y1): # 이전 년도 지출액 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_Ge_hungum_sql = """
                    SELECT SUM(amount) FROM cost_db WHERE year < %s and gubun = "일반회계"
                 """
    cur.execute(past_year_Ge_hungum_sql,(Y1,))
    past_year_Ge_hungum = cur.fetchall()

    cur.close()
    conn.close()
        
    return past_year_Ge_hungum

def year_Ge_hun_amount(Y1,bun): # 당해년도 헌금 월별 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    year_Ge_hungum_sql = """
                    SELECT SUM(amount) FROM hun_db 
                    WHERE year = %s  and month >= ((%s * 3)-2) and month <= (%s * 3) 
                    and hun_hang != "선교헌금" and hun_mok != "타회계이월";
                 """
    cur.execute(year_Ge_hungum_sql,(Y1,bun,bun,))
    year_Ge_hungum = cur.fetchall()

    cur.close()
    conn.close()
        
    return year_Ge_hungum

def year_cost_amount(Y1,bun): # 당해년도 헌금 월별 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    year_Ge_cost_sql = """
                    SELECT SUM(amount) FROM cost_db 
                    WHERE year = %s and month >= ((%s * 3)-2) and month <= (%s * 3)
                    and cost_hang != "선교회계" and cost_hang != "타회계이월";
                 """
    cur.execute(year_Ge_cost_sql,(Y1,bun,bun,))
    year_Ge_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return year_Ge_cost

def year_Ge_otherhun_amount(Y1,bun): # 당해년도 헌금 월별 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    year_Ge_hungum_sql = """
                    SELECT SUM(amount) FROM hun_db 
                    WHERE year = %s  and month >= ((%s * 3)-2) and month <= (%s * 3) and hun_mok = "타회계이월";
                 """
    cur.execute(year_Ge_hungum_sql,(Y1,bun,bun,))
    year_Ge_hungum = cur.fetchall()

    cur.close()
    conn.close()
        
    return year_Ge_hungum

def year_othercost_amount(Y1,bun): # 당해년도 지출에서 타회계이월 금액
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    year_Ge_cost_sql = """
                    SELECT SUM(amount) FROM cost_db 
                    WHERE Year = %s and Month >= ((%s * 3)-2) and Month <= (%s * 3)
                    and cost_hang = '타회계이월';
                 """
    cur.execute(year_Ge_cost_sql,(Y1,bun,bun,))
    year_Ge_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return year_Ge_cost

def year_Ge_hun_bun_hang_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_hungum_sql = """
                    SELECT hun_hang, SUM(amount) AS total_amount FROM hun_db
                    WHERE year = %s AND month >= ((%s * 3)-2) and month <= (%s * 3) 
                    and hun_hang != "절기헌금" and hun_hang != "예배" and hun_hang != "선교헌금" and hun_mok != '타회계이월' GROUP BY hun_hang;
                """
    cur.execute(Ge_year_hungum_sql,(Y1,bun,bun,))  
    Ge_year_hungum = cur.fetchall()         # 는 튜플의 형태로 ('감사헌금', 1, Decimal('2095000')), ('신년감사헌금', 1, Decimal('2490000')), ('십일조헌금', 1, Decimal('13894000')),의 형태임
    cur.close()
    conn.close()
        
    return Ge_year_hungum

def year_Ge_hun_bun_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_hungum_sql = """
                    SELECT hun_hang, hun_mok, SUM(amount) AS total_amount FROM hun_db
                    WHERE Year = %s and month >= ((%s * 3)-2) and month <= (%s * 3)  AND hun_hang != "선교헌금" 
                    GROUP BY hun_mok, hun_hang;
                """
    cur.execute(Ge_year_hungum_sql,(Y1,bun,bun))  
    Ge_year_hungum = cur.fetchall()         # 는 튜플의 형태로 ('감사헌금', 1, Decimal('2095000')), ('신년감사헌금', 1, Decimal('2490000')), ('십일조헌금', 1, Decimal('13894000')),의 형태임
    cur.close()
    conn.close()
        
    return Ge_year_hungum


def year_Ge_cost_bun_hang_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_cost_sql = """
                    SELECT cost_hang,SUM(amount) AS total_amount FROM cost_db
                    WHERE year = %s AND month >= (%s * 3)-2 and month <= %s * 3 
                    and hun_hang != "선교회계" GROUP BY cost_hang;
                """
    cur.execute(Ge_year_cost_sql,(Y1,bun,bun,))
    Ge_year_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return Ge_year_cost

def year_Ge_cost_bun_mok_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_cost_sql = """
                    SELECT cost_mok,SUM(amount) AS total_amount FROM cost_db
                    WHERE year = %s AND month >= (%s * 3)-2 AND month <= %s * 3 and cost_hang != "선교회계"
                    GROUP BY cost_mok;
                """
    cur.execute(Ge_year_cost_sql,(Y1,bun,bun,))
    Ge_year_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return Ge_year_cost

def year_Ge_cost_bun_semok_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_cost_sql = """
                    SELECT cost_semok,SUM(amount) AS total_amount FROM cost_db
                    WHERE year = %s AND month >= (%s * 3)-2 AND month <= %s * 3 and cost_hang != "선교회계"
                    GROUP BY cost_semok;
                """
    cur.execute(Ge_year_cost_sql,(Y1,bun,bun,))
    Ge_year_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return Ge_year_cost



def year_Ge_cost_month_amount(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_cost_sql = """
                    SELECT month, SUM(amount) AS total_amount FROM cost_db
                    WHERE year = %s AND month <= %s * 3 and cost_hang != "선교헌금"
                    GROUP BY month, cost_hang
                    ORDER BY month;
                """
    cur.execute(Ge_year_cost_sql,(Y1,bun))
    Ge_year_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return Ge_year_cost

def year_Ge_hun_hang_mok(Y1,bun):  # 분기 헌금 항, 목 별 금액 추출 
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_hungum_sql = """
                    SELECT hun_mok, month, SUM(amount) AS total_amount, hun_hang
                    FROM hun_db
                    WHERE year = %s AND month <= %s * 3 and hun_hang != "선교헌금"
                    GROUP BY hun_mok, month, hun_hang
                    ORDER BY hun_mok, month;
                """
    cur.execute(Ge_year_hungum_sql,(Y1,bun))
    Ge_year_hungum_list = cur.fetchall()

    cur.close()
    conn.close()
        
    return Ge_year_hungum_list

def bungi_cost_hang_mok(Y1,bun):
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    Ge_year_cost_hang_mok_sql = """
                    SELECT cost_mok, month, SUM(amount) AS total_amount, cost_hang
                    FROM cost_db
                    WHERE year = %s AND month <= %s * 3
                    GROUP BY cost_mok, month, cost_hang
                    ORDER BY cost_mok, month;
                """
    cur.execute(Ge_year_cost_hang_mok_sql,(Y1,bun))
    result = cur.fetchall()

    cur.close()

    return result

def bungi_Ge_M_cost(Y1,bun):  # 입력월 기준
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    table_name_1 = str(Y1) + '_' + 'cost_hang'
    table_name_2 = 'cost_db'

    order_hang = f"select cost_hang from {table_name_1} order by id asc;"
    cur.execute(order_hang)
    
    order_hang_tuple = cur.fetchall()
    desireed_order_column_list = [item[0] for item in order_hang_tuple]  # tuple을 리스트로 변경하는 것

    order_column = ', '.join([f'"{col}"' for col in desireed_order_column_list])


    Ge_year_cost_hang_mok_sql = f"""
                    SELECT  cost_hang,cost_mok,cost_semok,SUM(amount) AS total_amount
                    FROM {table_name_2}
                    WHERE year = %s AND month >= (%s * 3) -2 AND month <= %s * 3 AND cost_hang != '선교회계'
                    GROUP BY cost_hang, cost_mok, cost_semok
                    ORDER BY {order_column};
                """
    
    cur.execute(Ge_year_cost_hang_mok_sql,(Y1,bun,bun))
    result = cur.fetchall()

    cur.close()

    return result

def bungi_Ge_D_cost(Y1,bun):  # 입력 일자 기준
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    table_name_1 = str(Y1) + '_' + 'cost_hang'
    table_name_2 = 'cost_db'
    try :
        order_hang = f"select cost_hang from {table_name_1} order by id asc;"
        cur.execute(order_hang)
    except pymysql.err.ProgrammingError:
        QMessageBox.about(None, '누락', '해당년도 cost_hang 이 없습니다..')
        result = "없음"
        return result

    
    order_hang_tuple = cur.fetchall()
    desireed_order_column_list = [item[0] for item in order_hang_tuple]  # tuple을 리스트로 변경하는 것

    order_column = ', '.join([f'"{col}"' for col in desireed_order_column_list])

    # Ge_year_cost_hang_mok_sql = f"""
    #                 SELECT  cost_hang,cost_mok,cost_semok,SUM(amount) AS total_amount
    #                 FROM {table_name_2}
    #                 where Year(date) = %s and QUARTER(date) = %s
    #                 AND cost_hang != '선교회계'
    #                 GROUP BY cost_hang, cost_mok, cost_semok
    #                 ORDER BY {order_column};
    #             """
    
    # cur.execute(Ge_year_cost_hang_mok_sql,(Y1,bun))

    Ge_year_cost_hang_mok_sql = f"""
                    SELECT  cost_hang,cost_mok,cost_semok,SUM(amount) AS total_amount
                    FROM {table_name_2}
                    where year = %s and month >= (%s * 3) -2 AND month <= %s * 3
                    AND cost_hang != '선교회계'
                    GROUP BY cost_hang, cost_mok, cost_semok
                    ORDER BY {order_column};
                """
    
    cur.execute(Ge_year_cost_hang_mok_sql,(Y1,bun,bun))

    result = cur.fetchall()

    cur.close()

    return result


def past_mission_income(Y1): # 이전 년도 헌금 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_sun_hungum_sql = """
                    SELECT SUM(amount) FROM hun_db WHERE year < %s and hun_hang = "선교헌금"
                 """
    cur.execute(past_year_sun_hungum_sql,(Y1,))
    past_year_sun_hungum = cur.fetchall()
    result = int(past_year_sun_hungum[0][0])

    cur.close()
    conn.close()
        
    return result

def past_mission_cost(Y1): # 이전 년도 지출액 합계(금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_sun_cost_sql = """
                    SELECT SUM(amount) FROM cost_db WHERE year < %s and cost_hang = "선교회계"
                 """
    cur.execute(past_year_sun_cost_sql,(Y1,))
    past_year_sun_cost = cur.fetchall()
    result = int(past_year_sun_cost[0][0])

    cur.close()
    conn.close()
        
    return result


def bungi_sun_income(Y1,bun): # 분기, hun_mok, 금액
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    bungi_sun_income_sql = """
                    SELECT month, hun_mok, SUM(amount) FROM hun_db WHERE year = %s 
                    and month >= ((%s * 3) -2) AND month <= (%s * 3)
                    and hun_hang = "선교헌금"
                    Group by month, hun_mok
                 """
    cur.execute(bungi_sun_income_sql,(Y1,bun,bun))
    bungi_sun_income = cur.fetchall()

    cur.close()
    conn.close()
        
    return bungi_sun_income

def bungi_M_income(Y1,bun): # 당해년도의 전분기 까지의 선교헌금 합계액 (금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_sun_cost_sql = """
                    SELECT SUM(amount) FROM hun_db WHERE year = %s 
                    and month <= ((%s-1) * 3)
                    and hun_hang = "선교헌금"
                 """
    cur.execute(past_year_sun_cost_sql,(Y1,bun,))
    past_year_sun_cost = cur.fetchall()
    if past_year_sun_cost and past_year_sun_cost[0][0] != None:
        result = int(past_year_sun_cost[0][0])
    else:
        result = 0
        # result = int(past_year_sun_cost[0][0])

    cur.close()
    conn.close()
        
    return result

def bungi_sun_cost(Y1,bun): # 분기헌금 월별 cost_mok ,금액 )
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    bungi_sun_cost_sql = """
                    SELECT cost_mok, SUM(amount) FROM cost_db WHERE year = %s 
                    and month >= ((%s * 3) -2) AND month <= (%s * 3)
                    and cost_hang = "선교회계"
                    Group by cost_mok
                 """
    cur.execute(bungi_sun_cost_sql,(Y1,bun,bun))
    bungi_sun_cost = cur.fetchall()

    cur.close()
    conn.close()
        
    return bungi_sun_cost

def bungi_M_cost(Y1,bun): # 당해년도의 전분기 까지의 선교헌금 합계액 (금액만 나옴)
    import pymysql
    conn=pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur=conn.cursor()

    past_year_sun_cost_sql = """
                    SELECT SUM(amount) FROM cost_db WHERE year = %s
                    and month <= ((%s-1) * 3) and cost_hang = "선교회계"
                 """
    cur.execute(past_year_sun_cost_sql,(Y1, bun,))
    past_year_sun_cost = cur.fetchall()
    if past_year_sun_cost and past_year_sun_cost[0][0] != None:
        result = int(past_year_sun_cost[0][0])
    else:
        result = 0


    cur.close()
    conn.close()
        
    return result

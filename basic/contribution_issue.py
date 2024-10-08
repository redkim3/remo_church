import pymysql
import configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def issued_count(Y1):
    conn = pymysql.connect(host= host_name, user='root', password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    issued_count_sql = "select * from contribution_list where  YEAR(issued_date) = %s and issued_type != '재발행' "
    cur.execute(issued_count_sql, (Y1,))

    issued_count = cur.fetchall()
    row_count = 0
    for row in issued_count:
        row_count += 1

    new_count = row_count + 1

    cur.close()
    conn.close()

    return new_count

def issued_amount_hap(Y1,hap_code):
    
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()
    issued_amount = 0
    named_amount_sql = "select sum(amount) from contribution_list where target_year = %s and hap_code = %s "
    cur.execute(named_amount_sql, (Y1, hap_code,))
    named_amount = cur.fetchall()
    if named_amount[0][0] == None:
        named_amount = 0
    else:
        issued_amount = int(named_amount[0][0])
    
    return issued_amount

def issued_status_serch(Y1,hap_code):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    issue_detail_sql = """
                select issued_date, issued_sign,name_diff, amount, issued_type 
                from contribution_list where target_year = %s and hap_code = %s
            """
                    # ['발급일','발급기호','신청자','확인금액','재발행(최초발행)'] 

    cur.execute(issue_detail_sql, (Y1, hap_code,))
    issue_detail = cur.fetchall()

    return issue_detail

def issued_list_serch(issued_year, target_year):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    issue_list_sql = """
                select issued_date, issued_sign, target_year, name_diff, hap_code, amount, issued_type 
                from contribution_list where YEAR(issued_date) = %s and target_year = %s;
            """
                    # ['발급일','발급기호','신청자','합산코드','확인금액','재발행']

    cur.execute(issue_list_sql, (issued_year, target_year,))
    issue_list = cur.fetchall()

    return issue_list

def re_issued_list_serch(sign):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    re_issue_sql = """
                select issued_date, issued_sign,name_diff, id_no, addr, type_acc, type_code,
                gubun, startdate, enddate,jujeong_ratio, amount, issue_church, biz_no, church_address 
                from contribution_list where issued_sign = %s
            """
            #['발급일','발급기호','신청자','주민번호','주소','유형','유형코드','구분','시작일','종료일'
            # ,'확인금액','발행인','사업자번호','교회주소']
    cur.execute(re_issue_sql, (sign,))
    re_issue = cur.fetchall()
    
    return re_issue


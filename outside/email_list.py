import pymysql, configparser

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']


def email_list_view():
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    email_list_sql = """
                    select email_name, email_addr from email_list
                """ 
    cur.execute(email_list_sql)
    result = cur.fetchall()

    cur.close()
    conn.close()
    return result

def email_regist(email_imsi):
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    email_list_sql = "INSERT INTO {}(email_name, email_addr) values (%s,%s)".format('email_list')

    cur.execute(email_list_sql, email_imsi)
    
    conn.commit()
    conn.close()

def modify_email(change_data):
    conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    email_list_sql = """
                    UPDATE email_list SET email_addr = %s WHERE email_name = %s ;
                """ 
    cur.execute(email_list_sql,change_data,)
    conn.commit()
    # result = cur.fetchall()

    cur.close()
    conn.close()


def remome_email(delete_email):
    import pymysql
    conn = pymysql.connect(host= host_name,user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    email_list_delete_sql = "DELETE FROM {} WHERE email_name = %s AND email_addr = %s".format('email_list')        

    
    cur.execute(email_list_delete_sql, delete_email)
    conn.commit()
    
    cur.close()
    conn.close()

    return
    
import pymysql, configparser
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def not_use_personal_name_hun():
    conn = pymysql.connect(host=host_name, user = 'root', db = 'isbs2024', password='0000', charset='utf8')
    cur = conn.cursor()
    not_use_hun_name = []
    cur.execute("select hun_name from not_use_p_name ")
    
    hun_name_data = cur.fetchall()

    for item in hun_name_data:
        not_use_hun_name.extend(item)
    
    conn.close()

    return not_use_hun_name

def not_use_personal_name_hun_add(add_not_use_hun_name): 
    conn = pymysql.connect(host=host_name, user = 'root', db = 'isbs2024', password='0000', charset='utf8')
    cur = conn.cursor()

    cur.execute("update not_use_p_name set hun_name = %s ", add_not_use_hun_name)
    
    conn.commit()

    conn.close()

    return 


import pymysql, configparser

def sql_on_close():
    config = configparser.ConfigParser()
    config.read(r'./register/config.ini')
    host_name = config['MySQL']['host']
    user = config['user']['user_id']
    conn = pymysql.connect(host=host_name, user='root', password='0000', database='isbs2024', charset = 'utf8')
    cur = conn.cursor()
    close_query = "update user_table set connect_from = Null WHERE user_id = %s;"
    cur.execute(close_query, user,)
    conn.commit()
    conn.close()

    config['user']['user_id'] = ""
    with open(r"./register/config.ini", 'w') as config_file:
        config.write(config_file)
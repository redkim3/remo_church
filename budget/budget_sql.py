import pymysql
from PyQt5.QtWidgets import QMessageBox

def budget_income_save(input_data):
    conn = pymysql.connect(host='localhost',user='root',password='0000',db='isbs2024',charset='utf8')
    cur = conn.cursor()

    order_income_budget_sql = """
                insert into hun_budget (budget_year, hun_budget_hang, hun_budget_mok, hun_budget_amount,hun_budget_marks,user)
                values (%s, %s, %s, %s, %s, %s);
            """
    cur.executemany(order_income_budget_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
    conn.commit()

    jeol_income_budget_sql = """
                insert into hun_budget (budget_year, hun_budget_hang, hun_budget_mok, hun_budget_amount, hun_budget_marks, user)
                values (%s, %s, %s, %s, %s, %s);
            """
    cur.executemany(jeol_income_budget_sql, input_data) #execute(income_budget_sql,(hun_order_imsi))
    conn.commit()

    conn.close()
    
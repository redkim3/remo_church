import pymysql, subprocess, os
import numpy as np
from PyQt5.QtWidgets import QDialog, QPushButton #*
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from datetime import datetime

import configparser
import pandas as pd

today = QDate.currentDate()
s_today = today.toString(Qt.ISODate) 
cur_fold = os.getcwd()
config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

form_class = uic.loadUiType("./ui/ch2ch_file_change.ui")[0]
class ch2ch_file_Change(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ch2ch.or.kr 용 파일 변환')
        self.setWindowIcon(QIcon(os.path.join(cur_fold,'img','logo.ico')))
        self.end_dateEdit.setDate(today)
        six_days_ago = today.addDays(-6)
        self.start_dateEdit.setDate(six_days_ago)
        start_Button = QPushButton("변환시작")
        start_Button.clicked.connect(self.change_start)
        
        close_Button = QPushButton("닫기")
        close_Button.clicked.connect(self.close)
    
    def change_start(self):
        dat_01 = self.start_dateEdit.text()
        dat_02 = self.end_dateEdit.text()
        dat1 = datetime.strptime(dat_01,'%Y-%m-%d')
        dat2 = datetime.strptime(dat_02,'%Y-%m-%d')
        
        # MySQL 데이터베이스 연결
        conn = pymysql.connect(host=host_name,user='root',password='0000',db='isbs2024',charset='utf8')
        cur = conn.cursor()
        
        # MySQL 쿼리 실행하여 데이터 가져오기
        hun_query = """
                SELECT hun_hang as 항, hun_mok as 목, LEFT(name_diff, 3) AS 이름,
                SUBSTRING(name_diff, 4) AS 배우자이름, amount as 금액, date as 날짜, marks as 메모 from hun_db
                WHERE date >= %s AND date <= %s and hun_hang != '선교헌금';
            """
        cost_query = """SELECT cost_hang as 항, cost_mok as 목, cost_semok as 세목, amount as 금액, date as 날짜, 
                        concat(COALESCE(marks, ''), ' ', COALESCE(cost_memo, '')) AS 메모 FROM cost_db
                        WHERE date >= %s AND date <= %s AND cost_hang != '선교회계';
                    """
        
        sun_hun_query = """
                SELECT hun_hang as 항, hun_mok as 목, LEFT(name_diff, 3) AS 이름,
                SUBSTRING(name_diff, 4) AS 배우자이름, amount as 금액, date as 날짜, marks as 메모 from hun_db
                WHERE date >= %s AND date <= %s and hun_hang = '선교헌금';
            """
        sun_cost_query = """SELECT cost_mok as 항, cost_semok as 목, amount as 금액, date as 날짜, cost_memo as 메모 FROM cost_db
                        WHERE date >= %s AND date <= %s AND cost_hang = '선교회계';
                    """

        cur.execute(hun_query, (dat1, dat2,))
        df1 = pd.DataFrame(cur.fetchall(), columns=['항', '목', '이름', '배우자이름', '금액', '날짜','메모'])
        # df1 = pd.DataFrame(cur.fetchall(), columns=['hun_hang', 'hun_mok', 'name_diff1', 'name_diff2', 'amount', 'date', 'memo'])
        df1.insert(loc=2, column='세목', value='') # 컬럼 끼워넣기 'Column3'
        df1.insert(loc=3, column='세세목', value='')  # 컬럼 끼워넣기 'Column4'

        cur.execute(cost_query, (dat1, dat2,))
        df2 = pd.DataFrame(cur.fetchall(), columns=['항', '목', '세목','금액', '날짜', '메모'])
        # df2 = pd.DataFrame(cur.fetchall(), columns=['cost_hang', 'cost_mok', 'cost_semok','amount', 'date', 'memo_marks'])
        df2.insert(loc=3, column='세세목', value='') # 컬럼 끼워넣기 'Column4'
        
       # '세목'이 NaN 또는 빈 문자열인 경우에 '목' 값을 넣습니다.
        df2['세목'] = df2['세목'].replace('', np.nan)  # 빈 문자열을 NaN으로 변환
        df2['세목'] = df2['세목'].fillna(df2['목'])    # NaN 값을 '목' 값으로 채움
     
        # df2.loc[df2['cost_semok'].isnull(), 'cost_semok'] = df2['cost_mok']

        cur.execute(sun_hun_query, (dat1, dat2,))
        df3 = pd.DataFrame(cur.fetchall(), columns=['항', '목', '이름', '배우자이름', '금액', '날짜','메모'])
        # df3 = pd.DataFrame(cur.fetchall(), columns=['hun_hang', 'hun_mok', 'name_diff1', 'name_diff2', 'amount', 'date'])
        df3.insert(loc=2, column='세목', value='') # 컬럼 끼워넣기  'Column3'
        df3.insert(loc=3, column='세세목', value='')  # 컬럼 끼워넣기 'Column4'

        cur.execute(sun_cost_query, (dat1, dat2,))
        df4 = pd.DataFrame(cur.fetchall(), columns=['항', '목', '금액', '날짜', '메모'])
        # df4 = pd.DataFrame(cur.fetchall(), columns=['cost_hang', 'cost_mok', 'cost_semok','amount', 'date', 'cost_memo', 'marks'])
        df4.insert(loc=2, column='세목', value='') # 컬럼 끼워넣기 Column4
        df4.insert(loc=3, column='세세목', value='')  # 컬럼 끼워넣기 'Column4'


        # 데이터프레임을 엑셀 파일에 시트로 저장
        output_file = './excel_view/교회앱업로드파일.xlsx'

        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 첫 번째 시트에 데이터를 추가합니다.
                df1.to_excel(writer, index=False, sheet_name='일반회계수입')

                # 두 번째 시트에 데이터를 추가합니다.
                df2.to_excel(writer, index=False, sheet_name='일반회계지출')

                # 세 번째 시트에 데이터를 추가합니다.
                df3.to_excel(writer, index=False, sheet_name='선교회계수입')

                # 네 번째 시트에 데이터를 추가합니다.
                df4.to_excel(writer, index=False, sheet_name='선교지출')

                QMessageBox.about(self, "완료", "데이터 저장이 완료되었습니다.")
                subprocess.Popen(["start", "excel.exe", os.path.abspath("./excel_view/교회앱업로드파일.xlsx")], shell=True)

        
        except PermissionError: #[Errno 13] Permission denied:
            QMessageBox.about(self,'파일open',"파일이 열려있습니다.")

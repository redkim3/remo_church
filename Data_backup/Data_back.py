import os, datetime, configparser
import pymysql
from PyQt5.QtWidgets import QMessageBox

config = configparser.ConfigParser()
config.read(r"./register/config.ini")
host_name = config['MySQL']['host']

def backup_database(database):
    # 현재 날짜 및 시간을 기준으로 백업 파일 이름 생성
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_filename = f'{database}_{current_datetime}.sql'

    # MySQL 데이터베이스에 연결
    conn = pymysql.connect(host=host_name, user='root', password='0000', database=database)
    cur = conn.cursor()

    # 백업 쿼리 실행
    backup_query = f'SHOW CREATE DATABASE {database};'
    cur.execute(backup_query)
    create_database_query = cur.fetchone()[1]

    try:
        with open(os.path.join('DB/backup', backup_filename), 'w', encoding='utf-8') as f:
        
            f.write(f'{create_database_query};\n\n')

            tables_query = 'SHOW TABLES;'
            cur.execute(tables_query)
            tables = cur.fetchall()

            for table in tables:
                table_name = table[0]
                
                # 테이블의 구조를 백업 파일에 쓰는 부분
                table_structure_query = f'SHOW CREATE TABLE {table_name};'
                cur.execute(table_structure_query)
                table_structure = cur.fetchone()[1]
                f.write(f'\n\n-- Table structure for table `{table_name}`\n')
                f.write(f'{table_structure};\n')

                # 테이블의 데이터를 백업 파일에 쓰는 부분
                table_backup_query = f'SELECT * FROM {table_name};'
                cur.execute(table_backup_query)
                table_data = cur.fetchall()
                if table_data:
                    f.write(f'\n-- Dumping data for table `{table_name}`\n')
                    for row in table_data:
                        # DATE 또는 DATETIME 값을 문자열로 변환하여 백업 파일에 쓰기
                        row_str = [str(value) if isinstance(value, (datetime.date, datetime.datetime)) and value is not None else 'NULL' if value is None else value for value in row]
                        f.write(f'INSERT INTO `{table_name}` VALUES {tuple(row_str)};\n')
       
        # 백업 완료 메시지
        QMessageBox.about(None,'백업완료',"데이터베이스 백업이 완료되었습니다.")
    except FileNotFoundError:  #[Errno 2] No such file or directory:
            QMessageBox.about(None,'폴더없음',"'backup' 폴더가 없습니다. DB폴더에 backup 폴더를 만들어 주세요.")        

    # msg_box = QMessageBox()
    # msg_box.setWindowTitle("백업 완료")
    # msg_box.setText("데이터베이스 백업이 완료되었습니다.")
        
    
    
    
    
    
    
    
    
    
    
    # backup_query = f'SHOW CREATE DATABASE {database};'
    # cur.execute(backup_query)
    # create_database_query = cur.fetchone()[1]

    # with open(os.path.join('DB/backup', backup_filename), 'w', encoding='utf-8') as f:
    #     f.write(f'{create_database_query};\n\n')

    #     tables_query = 'SHOW TABLES;'
    #     cur.execute(tables_query)
    #     tables = cur.fetchall()

    #     for table in tables:
    #         table_name = table[0]
    #         table_backup_query = f'SELECT * FROM {table_name};'
    #         cur.execute(table_backup_query)
    #         table_data = cur.fetchall()

    #         f.write(f'\n\n-- Table structure for table `{table_name}`\n')
    #         f.write(f'DROP TABLE IF EXISTS `{table_name}`;\n')
    #         f.write(f'{create_database_query};\n')

    #         f.write(f'\n-- Dumping data for table `{table_name}`\n')
    #         for row in table_data:
    #             f.write(f'INSERT INTO `{table_name}` VALUES {row};\n')
    #         msg_box = QMessageBox()
    #         msg_box.setWindowTitle("백업 완료")
    #         msg_box.setText("데이터베이스 백업이 완료되었습니다.")

    # 연결 및 커서 닫기
    cur.close()
    conn.close()
if __name__ == '__main__':
    host_name = host_name
    database_name = 'isbs2024'
    backup_database(database_name, host_name)
import os
import sqlite3
db_path = "./MicroMsg.db"


class dbMsg():
    """ 数据库操作 """
    def __init__(self):
        self.DB = None
        self.cursor = None
        self.init_database()
        self.init_table()

    def init_database(self):
        # 初始化数据库
        # if os.path.exists(db_path):
        self.DB = sqlite3.connect(db_path)
        # 创建游标
        self.cursor = self.DB.cursor()

    def init_table(self):
        # 建表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                datetime VARCHAR,
                contents VARCHAR
            )
        ''')

    def insert_data(self, date, contents):
        date = date.toPyDate().strftime('%Y-%m-%d')
        self.cursor.execute(f"INSERT INTO notes (datetime, contents) VALUES ('{date}', '{contents}')")
        # 提交更改
        self.DB.commit()

    def update_date(self, date, contents):
        date = date.toPyDate().strftime('%Y-%m-%d')

        self.cursor.execute(f"UPDATE notes SET contents = '{contents}' WHERE datetime = '{date}'")
        results = self.cursor.fetchall()
        print(results)
        self.DB.commit()


    def delete_data(self, date):
        date = date.toPyDate().strftime('%Y-%m-%d')

        self.cursor.execute(f"DELETE FROM notes WHERE datetime = '{date}'")

        self.DB.commit()

    def get_data(self, date):
        date = date.toPyDate().strftime('%Y-%m-%d')
        self.cursor.execute(f"SELECT contents from notes where datetime = '{date}'")
        results = self.cursor.fetchall()
        return results
        # self.DB.commit()

    def getDate(self, date):
        date = date.toPyDate().strftime('%Y-%m-%d')

        self.cursor.execute(f"SELECT * from notes where datetime = '{date}'")
        results = self.cursor.fetchall()
        print(results)
        return results

    def __del__(self):
        # 对象销毁时执行
        self.cursor.close()
        self.DB.close()


import os
import sys 
import requests
import traceback

import pymysql
from pymysql.cursors import DictCursor

if os.path.abspath(os.curdir) in sys.path: sys.path.append(os.path.abspath(os.curdir))

from config import MYSQL_HOST, MYSQL_DB, MYSQL_PASSWORD, MYSQL_USER



my_ip = requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '')
host = '127.0.0.1' if my_ip == MYSQL_HOST else MYSQL_HOST
conn = pymysql.connect(
    host=host,
    port=3306,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    charset='utf8mb4',
    cursorclass=DictCursor
)
def query(query):
    # time_start = time.time()
    with conn.cursor() as cursor:
        try: cursor.execute(query)
        except pymysql.err.OperationalError: 
            conn.ping()
            cursor.execute(query)
        conn.commit()
        # print("query:", 1000*(time.time() - time_start), "ms", query)
        return cursor.fetchall()
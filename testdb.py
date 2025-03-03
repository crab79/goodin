import mysql.connector

# 資料庫配置
DB_CONFIG = {
    'host': '140.127.220.85',
    'user': 'nukim',
    'password': 'nukim',
    'database': 'goodin'
}

try:
    # 嘗試連線
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        print("成功連接到遠端資料庫！")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("資料庫中的表格：", tables)
    conn.close()
except mysql.connector.Error as err:
    print(f"連線失敗：{err}")

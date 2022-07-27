import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "mysql_db",
    "charset": "utf8"
}

def uptords(text,file):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            print("--新增--")
            #指令
            sql = "INSERT INTO message (message, photo) VALUES (%s, %s);"
            new_data = (text, file)
            cursor.execute(sql, new_data)
            conn.commit()
            return {"ok": True}
    finally:
            cursor.close()
            conn.close()
            print("資料庫連線已關閉")

def loadtords():
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            print("--讀取--")
            cursor.execute("select * from message;")
            records = cursor.fetchall()
            myrdsdata = []
            for i in range(len(records)):
                myrdsdata.append({
                    "text":records[i][1],
                    "image":records[i][2].decode() if records[i][2] else ''
                })
            return myrdsdata
    finally:
            cursor.close()
            conn.close()
            print("資料庫連線已關閉")
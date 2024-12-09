import os
import psycopg2

def fetch_patent_data(): #データベースからデータを取得
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT registration_number, invention_title, right_person_name FROM patents_info")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    print(data)

    return data

fetch_patent_data()
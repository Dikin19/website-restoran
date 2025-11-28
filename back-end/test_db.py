import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def test_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Database CONNECTED")
        conn.close()

    except Exception as e:
        print("Database FAILED!")
        print("Error:", e)

if __name__ == "__main__":
    test_db()

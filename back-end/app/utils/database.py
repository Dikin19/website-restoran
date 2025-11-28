import mysql.connector

def get_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   
            database="restorandb"
        )
        print("✅ Terhubung ke database MySQL!")
        return db
    except mysql.connector.Error as err:
        print("❌ Gagal koneksi:", err)
        return None

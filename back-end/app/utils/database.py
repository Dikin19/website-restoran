import mysql.connector

def get_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   
            database="restorandb"
        )
        print("Terhubung ke database MySQL!")
        return db
    except mysql.connector.Error as err:
        print("❌ Gagal koneksi:", err)
        return None

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    
    db = get_db()
    if not db:
        return None
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone() if fetch_one else cursor.fetchall()
        else:
            db.commit()
            result = cursor.lastrowid
        
        cursor.close()
        db.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        if db:
            db.close()
        return None

def get_db_connection():
    
    return get_db()

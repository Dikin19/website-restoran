import bcrypt
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_admin():
    
    print("=" * 50)
    print("CREATE ADMIN BARU - Website Restoran")
    print("=" * 50)
    
    username = input("\nUsername: ")
    password = input("Password: ")
    nama_lengkap = input("Nama Lengkap: ")
    
    # Validasi input
    if not username or not password or not nama_lengkap:
        print("❌ Semua field harus diisi!")
        return
    
    if len(password) < 6:
        print("❌ Password minimal 6 karakter!")
        return
    
    hashed_password = hash_password(password)
    
    # Koneksi ke database
    try:
        db = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'restorandb'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = db.cursor()
        
        cursor.execute("SELECT id FROM admins WHERE username = %s", (username,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"Username '{username}' sudah digunakan!")
            cursor.close()
            db.close()
            return
        
        # Insert admin baru
        query = """
            INSERT INTO admins (username, password, nama_lengkap)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password, nama_lengkap))
        db.commit()
        
        admin_id = cursor.lastrowid
        
        cursor.close()
        db.close()
        
        print("\n" + "=" * 50)
        print("Admin berhasil dibuat!")
        print("=" * 50)
        print(f"ID: {admin_id}")
        print(f"Username: {username}")
        print(f"Nama: {nama_lengkap}")
        print(f"Password: {password} (sudah di-hash)")
        print("\nSilakan login di aplikasi dengan username dan password di atas.")
        
    except pymysql.Error as e:
        print(f"Error database: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
        create_admin()
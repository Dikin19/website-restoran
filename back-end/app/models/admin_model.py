from app.utils.database import execute_query
from app.utils.helpers import hash_password, verify_password

class Admin:
    
    @staticmethod
    def find_by_username(username):
        """Cari admin berdasarkan username"""
        query = "SELECT * FROM admins WHERE username = %s"
        return execute_query(query, (username,), fetch_one=True)
    
    @staticmethod
    def verify_login(username, password):
        """Verifikasi login admin"""
        admin = Admin.find_by_username(username)
        
        if admin and verify_password(password, admin['password']):
            admin.pop('password', None)
            return admin
        
        return None
    
    @staticmethod
    def create(username, password):
        """Buat admin baru"""
        hashed_password = hash_password(password)
        query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
        return execute_query(query, (username, hashed_password))
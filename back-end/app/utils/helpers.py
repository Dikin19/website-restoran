import bcrypt
import os
from werkzeug.utils import secure_filename
import uuid

def hash_password(password):
    """Hash password menggunakan bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verifikasi password dengan hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_required_fields(data, required_fields):
    """Validasi field yang wajib diisi"""
    if not data:
        return False, required_fields
    
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return False, missing_fields
    
    return True, []

def save_image(file, upload_folder='uploads'):
    """Simpan gambar dan return nama file"""
    if not file:
        return None
    
    # Buat folder jika belum ada
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(upload_folder, unique_filename)
    
    file.save(filepath)
    return unique_filename

def delete_image(filename, upload_folder='uploads'):
    """Hapus gambar dari folder uploads"""
    if not filename:
        return False
    
    filepath = os.path.join(upload_folder, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False

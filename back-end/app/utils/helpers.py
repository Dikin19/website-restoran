import bcrypt

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

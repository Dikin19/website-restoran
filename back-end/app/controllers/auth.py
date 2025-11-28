from flask import jsonify
from app.models.admin import Admin
from app.utils.helpers import validate_required_fields

class AuthController:
    
    @staticmethod
    def login(data):
        
        is_valid, missing = validate_required_fields(data, ['username', 'password'])
        
        if not is_valid:
            return jsonify({
                'success': False,
                'message': f'Field wajib kosong: {", ".join(missing)}',
                'data': None
            }), 400
        

        admin = Admin.verify_login(data['username'], data['password'])
        
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Username atau password salah',
                'data': None
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Login berhasil',
            'data': {
                'admin': admin
            }
        }), 200

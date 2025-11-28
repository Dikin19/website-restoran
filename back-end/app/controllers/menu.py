from flask import jsonify, current_app
from app.models.menu import Menu
from app.utils.helpers import validate_required_fields, save_image, delete_image

class MenuController:
    
    @staticmethod
    def get_all_menus(page=1, limit=10, kategori=None, search=None):
        
        try:
            result = Menu.get_all(page, limit, kategori, search)
            
            return jsonify({
                'success': True,
                'message': 'Data menu berhasil diambil',
                'data': result['data'],
                'pagination': result['pagination']
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
    
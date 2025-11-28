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
    
    @staticmethod
    def get_menu_by_id(menu_id):
        
        try:
            menu = Menu.get_by_id(menu_id)
            
            if not menu:
                return jsonify({
                    'success': False,
                    'message': 'Menu tidak ditemukan',
                    'data': None
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Detail menu berhasil diambil',
                'data': menu
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def create_menu(data, file=None):
        
        try:
            
            required = ['nama', 'harga', 'kategori']
            is_valid, missing = validate_required_fields(data, required)
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': f'Field wajib kosong: {", ".join(missing)}',
                    'data': None
                }), 400
            
            
            try:
                harga = float(data['harga'])
                if harga <= 0:
                    raise ValueError()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Harga harus angka positif',
                    'data': None
                }), 400
            
            
            filename = None
            if file:
                filename = save_image(file, current_app.config['UPLOAD_FOLDER'])
                if not filename:
                    return jsonify({
                        'success': False,
                        'message': 'Gagal upload gambar. Format harus jpg/png/gif',
                        'data': None
                    }), 400
            
            
            data['gambar'] = filename
            menu_id = Menu.create(data)
            
            return jsonify({
                'success': True,
                'message': 'Menu berhasil ditambahkan',
                'data': {
                    'id': menu_id,
                    'gambar': filename
                }
            }), 201
            
        except Exception as e:
            
            if filename:
                delete_image(filename, current_app.config['UPLOAD_FOLDER'])
            
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
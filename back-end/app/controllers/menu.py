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

    @staticmethod
    def update_menu(menu_id, data, file=None):
        
        try:
            
            existing_menu = Menu.get_by_id(menu_id)
            if not existing_menu:
                return jsonify({
                    'success': False,
                    'message': 'Menu tidak ditemukan',
                    'data': None
                }), 404
            
            
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
            
            
            old_image = existing_menu['gambar']
            new_filename = old_image
            
            if file:
                
                new_filename = save_image(file, current_app.config['UPLOAD_FOLDER'])
                if new_filename:
                    # Hapus gambar lama
                    if old_image:
                        delete_image(old_image, current_app.config['UPLOAD_FOLDER'])
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Gagal upload gambar baru',
                        'data': None
                    }), 400
            
            # Update ke database
            data['gambar'] = new_filename
            Menu.update(menu_id, data)
            
            return jsonify({
                'success': True,
                'message': 'Menu berhasil diupdate',
                'data': {
                    'id': menu_id,
                    'gambar': new_filename
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def delete_menu(menu_id):
        try:
            # Cek apakah menu ada
            menu = Menu.get_by_id(menu_id)
            if not menu:
                return jsonify({
                    'success': False,
                    'message': 'Menu tidak ditemukan',
                    'data': None
                }), 404
            
            # Hapus gambar jika ada
            if menu['gambar']:
                delete_image(menu['gambar'], current_app.config['UPLOAD_FOLDER'])
            
            # Hapus dari database
            Menu.delete(menu_id)
            
            return jsonify({
                'success': True,
                'message': 'Menu berhasil dihapus',
                'data': None
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def toggle_tersedia(menu_id):
        
        try:
            
            menu = Menu.get_by_id(menu_id)
            if not menu:
                return jsonify({
                    'success': False,
                    'message': 'Menu tidak ditemukan',
                    'data': None
                }), 404
            
            
            Menu.toggle_tersedia(menu_id)
            
            
            new_status = not menu.get('tersedia', True)
            
            return jsonify({
                'success': True,
                'message': f'Menu berhasil diubah menjadi {"tersedia" if new_status else "tidak tersedia"}',
                'data': {
                    'id': menu_id,
                    'tersedia': new_status
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
    
    @staticmethod
    def get_menu_by_kategori(kategori):
        """Get menu berdasarkan kategori yang tersedia"""
        try:
            menus = Menu.get_by_kategori(kategori)
            
            return jsonify({
                'success': True,
                'message': f'Data menu kategori {kategori} berhasil diambil',
                'data': menus or [],
                'total': len(menus) if menus else 0
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
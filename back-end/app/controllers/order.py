from flask import jsonify
from app.models.order import Order
from app.utils.helpers import validate_required_fields

class OrderController:
    @staticmethod
    def get_all_orders(page=1, limit=10, status=None):
        
        try:
            result = Order.get_all(page, limit, status)
            
            return jsonify({
                'success': True,
                'message': 'Data pesanan berhasil diambil',
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
    def get_order_by_id(order_id):

        try:
            order = Order.get_by_id(order_id)
            
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Pesanan tidak ditemukan',
                    'data': None
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Detail pesanan berhasil diambil',
                'data': order
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
    
    @staticmethod
    def create_order(data):
        
        try:
            
            required = ['nama_customer', 'items']
            is_valid, missing = validate_required_fields(data, required)
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': f'Field wajib kosong: {", ".join(missing)}',
                    'data': None
                }), 400
            
            
            items = data['items']
            
            if not isinstance(items, list) or len(items) == 0:
                return jsonify({
                    'success': False,
                    'message': 'Pesanan harus memiliki minimal 1 item',
                    'data': None
                }), 400
            
         
            for idx, item in enumerate(items):
                if 'menu_id' not in item or 'jumlah' not in item:
                    return jsonify({
                        'success': False,
                        'message': f'Item #{idx+1}: menu_id dan jumlah wajib diisi',
                        'data': None
                    }), 400
                
                try:
                    jumlah = int(item['jumlah'])
                    if jumlah <= 0:
                        raise ValueError()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': f'Item #{idx+1}: jumlah harus angka positif',
                        'data': None
                    }), 400
            
            
            order_data = {
                'nama_customer': data['nama_customer'],
                'catatan': data.get('catatan', '')
            }
            
            order_id = Order.create(order_data, items)
            
            
            new_order = Order.get_by_id(order_id)
            
            return jsonify({
                'success': True,
                'message': 'Pesanan berhasil dibuat',
                'data': new_order
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def update_status(order_id, data):
      
        try:
           
            order = Order.get_by_id(order_id)
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Pesanan tidak ditemukan',
                    'data': None
                }), 404
            
           
            if 'status' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Field status wajib diisi',
                    'data': None
                }), 400
            
            new_status = data['status']
            if new_status not in ['pending', 'selesai']:
                return jsonify({
                    'success': False,
                    'message': 'Status harus "pending" atau "selesai"',
                    'data': None
                }), 400
            
          
            Order.update_status(order_id, new_status)
            
            return jsonify({
                'success': True,
                'message': f'Status pesanan diubah menjadi {new_status}',
                'data': {
                    'id': order_id,
                    'status': new_status
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def delete_order(order_id):
        try:
            
            order = Order.get_by_id(order_id)
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Pesanan tidak ditemukan',
                    'data': None
                }), 404
            
           
            Order.delete(order_id)
            
            return jsonify({
                'success': True,
                'message': 'Pesanan berhasil dihapus',
                'data': None
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500

    @staticmethod
    def get_statistics():
        
        try:
            stats = Order.get_statistics()
            
            return jsonify({
                'success': True,
                'message': 'Statistik berhasil diambil',
                'data': stats
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'data': None
            }), 500
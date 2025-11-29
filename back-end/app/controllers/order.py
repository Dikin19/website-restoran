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
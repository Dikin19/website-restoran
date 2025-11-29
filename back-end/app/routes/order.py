from flask import Blueprint, request
from app.controllers.order import OrderController

bp = Blueprint('order', __name__, url_prefix='/api/orders')

@bp.route('', methods=['GET'])
def get_all_orders():
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    status = request.args.get('status', None)
    
    return OrderController.get_all_orders(page, limit, status)

@bp.route('/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    
    return OrderController.get_order_by_id(order_id)

@bp.route('', methods=['POST'])
def create_order():
    """
    Endpoint: POST /api/orders
    
    Request Body (JSON):
    {
        "nama_customer": "Budi Santoso",
        "catatan": "Pedas sedang",
        "items": [
            {
                "menu_id": 1,
                "jumlah": 2
            },
            {
                "menu_id": 5,
                "jumlah": 1
            }
        ]
    }
    
    Response (201):
    {
        "success": true,
        "message": "Pesanan berhasil dibuat",
        "data": {
            "id": 1,
            "nama_customer": "Budi Santoso",
            "total_harga": 60000,
            "status": "pending",
            "items": [...]
        }
    }
    
    Penjelasan:
    - Endpoint ini membuat pesanan baru dengan items-nya
    - Harga dihitung otomatis dari menu yang dipilih
    - Total harga otomatis dijumlahkan
    """
    data = request.get_json()
    return OrderController.create_order(data)
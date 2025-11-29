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
    
    data = request.get_json()
    return OrderController.create_order(data)

@bp.route('/<int:order_id>/status', methods=['PATCH'])
def update_status(order_id):
    
    data = request.get_json()
    return OrderController.update_status(order_id, data)

@bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    
    return OrderController.delete_order(order_id)

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    
    return OrderController.get_statistics()
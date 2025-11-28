from flask import Blueprint, request
from app.controllers.menu import MenuController

bp = Blueprint('menu', __name__, url_prefix='/api/menu')

@bp.route('', methods=['GET'])
def get_all_menus():
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    kategori = request.args.get('kategori', None)
    search = request.args.get('search', None)
    
    return MenuController.get_all_menus(page, limit, kategori, search)


@bp.route('/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    
    return MenuController.get_menu_by_id(menu_id)
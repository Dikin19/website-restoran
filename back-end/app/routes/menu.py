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
  
@bp.route('', methods=['POST'])
def create_menu():
    """Create new menu with multipart/form-data support"""
    data = {
        'nama': request.form.get('nama'),
        'deskripsi': request.form.get('deskripsi', ''),
        'harga': request.form.get('harga'),
        'kategori': request.form.get('kategori')
    }
    file = request.files.get('gambar')
    return MenuController.create_menu(data, file)

@bp.route('/update/<int:menu_id>', methods=['POST'])
def update_menu(menu_id):
    """Update menu via POST with FormData support"""
    # Parse form data
    data = {
        'nama': request.form.get('nama'),
        'deskripsi': request.form.get('deskripsi', ''),
        'harga': request.form.get('harga'),
        'kategori': request.form.get('kategori')
    }
    
    # Debug logging
    print(f"Update Menu {menu_id}")
    print(f"Form data: {dict(request.form)}")
    print(f"Files: {list(request.files.keys())}")
    
    file = request.files.get('gambar')
    
    return MenuController.update_menu(menu_id, data, file)

@bp.route('/<int:menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    
    return MenuController.delete_menu(menu_id)

@bp.route('/<int:menu_id>/toggle', methods=['PATCH'])
def toggle_tersedia(menu_id):
    return MenuController.toggle_tersedia(menu_id)

@bp.route('/kategori/<string:kategori>', methods=['GET'])
def get_by_kategori(kategori):
    return MenuController.get_menu_by_kategori(kategori)

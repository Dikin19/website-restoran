from flask import Blueprint, jsonify
from app.utils.database import get_db

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"])
def get_menu():
    """API untuk mendapatkan semua data menu dari database"""
    db = get_db()
    
    if db is None:
        return jsonify({
            "error": "Tidak dapat terhubung ke database",
            "message": "Pastikan MySQL sudah berjalan dan database 'restorandb' sudah dibuat"
        }), 500
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menus ORDER BY kategori, nama")
        data = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Gagal mengambil data menu",
            "message": str(e)
        }), 500

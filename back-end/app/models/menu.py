from app.utils.database import execute_query, get_db_connection
import pymysql

class Menu:

    @staticmethod
    def get_all(page=1, limit=10, kategori=None, search=None):
        
        offset = (page - 1) * limit
        
        where_clauses = []
        params = []
        
        if kategori:
            where_clauses.append("kategori = %s")
            params.append(kategori)
        
        if search:
            where_clauses.append("nama LIKE %s")
            params.append(f"%{search}%")
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        # Ubah dari 'menu' menjadi 'menus'
        query = f"""
            SELECT * FROM menus 
            WHERE {where_sql}
            ORDER BY id DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        menus = execute_query(query, tuple(params), fetch_all=True)
        
        count_query = f"SELECT COUNT(*) as total FROM menus WHERE {where_sql}"
        count_params = params[:-2]  # Hapus limit dan offset
        count_result = execute_query(count_query, tuple(count_params), fetch_one=True)
        
        # Handle jika query gagal
        total = count_result['total'] if count_result else 0
        
        return {
            'data': menus or [],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit if total > 0 else 0
            }
        }
    
    @staticmethod
    def get_by_id(menu_id):
        query = "SELECT * FROM menus WHERE id = %s"
        return execute_query(query, (menu_id,), fetch_one=True)

    @staticmethod
    def create(data):
        query = """
            INSERT INTO menus (nama, deskripsi, harga, kategori, gambar) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['nama'],
            data.get('deskripsi', ''),
            data['harga'],
            data['kategori'],
            data.get('gambar', None)
        )
        return execute_query(query, params)

    @staticmethod
    def update(menu_id, data):
        query = """
            UPDATE menus 
            SET nama = %s, deskripsi = %s, harga = %s, kategori = %s, gambar = %s
            WHERE id = %s
        """
        params = (
            data['nama'],
            data.get('deskripsi', ''),
            data['harga'],
            data['kategori'],
            data.get('gambar'),
            menu_id
        )
        return execute_query(query, params)
    
    @staticmethod
    def delete(menu_id):
        query = "DELETE FROM menus WHERE id = %s"
        return execute_query(query, (menu_id,))

    @staticmethod
    def toggle_tersedia(menu_id):
        query = "UPDATE menus SET tersedia = NOT tersedia WHERE id = %s"
        return execute_query(query, (menu_id,))
    
    @staticmethod
    def get_by_kategori(kategori):
        query = "SELECT * FROM menus WHERE kategori = %s AND tersedia = TRUE ORDER BY nama"
        return execute_query(query, (kategori,), fetch_all=True)

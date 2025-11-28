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
    
   
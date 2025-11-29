from app.utils.database import execute_query, get_db_connection
import pymysql

class Order:

    @staticmethod
    def get_all(page=1, limit=10, status=None):
        
        offset = (page - 1) * limit
        
       
        where_sql = "WHERE status = %s" if status else "WHERE 1=1"
        params = [status] if status else []
        
        query = f"""
            SELECT * FROM orders 
            {where_sql}
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        orders = execute_query(query, tuple(params), fetch_all=True)
        
        count_query = f"SELECT COUNT(*) as total FROM orders {where_sql}"
        count_params = params[:-2] if status else []
        total = execute_query(count_query, tuple(count_params), fetch_one=True)['total']
        
        return {
            'data': orders or [],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit
            }
        }
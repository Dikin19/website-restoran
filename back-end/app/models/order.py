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

    @staticmethod
    def get_by_id(order_id):
        
        query = "SELECT * FROM orders WHERE id = %s"
        order = execute_query(query, (order_id,), fetch_one=True)
        
        if not order:
            return None
        
        items_query = """
            SELECT oi.*, m.gambar as menu_gambar
            FROM order_items oi
            LEFT JOIN menus m ON oi.menu_id = m.id
            WHERE oi.order_id = %s
        """
        items = execute_query(items_query, (order_id,), fetch_all=True)
        
        order['items'] = items or []
        return order

    @staticmethod
    def create(order_data, items_data):
        
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            order_query = """
                INSERT INTO orders (nama_customer, catatan, total_harga, status) 
                VALUES (%s, %s, 0, 'pending')
            """
            cursor.execute(order_query, (
                order_data['nama_customer'],
                order_data.get('catatan', '')
            ))
            order_id = cursor.lastrowid
            

            total_harga = 0
            
            for item in items_data:
                
                menu_query = "SELECT id, nama, harga FROM menus WHERE id = %s"
                cursor.execute(menu_query, (item['menu_id'],))
                menu = cursor.fetchone()
                
                if not menu:
                    raise Exception(f"Menu ID {item['menu_id']} tidak ditemukan")
                
                menu_id = menu[0]
                menu_nama = menu[1]
                menu_harga = menu[2]
                
                jumlah = item['jumlah']
                subtotal = menu_harga * jumlah
                total_harga += subtotal
                
                item_query = """
                    INSERT INTO order_items 
                    (order_id, menu_id, nama_menu, harga_satuan, jumlah, subtotal) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(item_query, (
                    order_id,
                    menu_id,
                    menu_nama,
                    menu_harga,
                    jumlah,
                    subtotal
                ))
            
            update_query = "UPDATE orders SET total_harga = %s WHERE id = %s"
            cursor.execute(update_query, (total_harga, order_id))
            
            connection.commit()
            return order_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error membuat pesanan: {e}")
            raise
        finally:
            if connection:
                connection.close()

    
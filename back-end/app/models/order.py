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

    @staticmethod
    def create(order_data, items_data):
        """
        Buat pesanan baru dengan items-nya
        
        Args:
            order_data (dict): {
                'nama_customer': str,
                'catatan': str (opsional)
            }
            items_data (list): [{
                'menu_id': int,
                'jumlah': int
            }, ...]
        
        Return:
            int: ID order yang baru dibuat
        
        Penjelasan:
        - Pakai transaction untuk memastikan data konsisten
        - Jika ada error, rollback semua perubahan
        - Step: 1) Insert order, 2) Insert items, 3) Update total harga
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Step 1: Insert ke tabel orders
            order_query = """
                INSERT INTO orders (nama_customer, catatan, total_harga, status) 
                VALUES (%s, %s, 0, 'pending')
            """
            cursor.execute(order_query, (
                order_data['nama_customer'],
                order_data.get('catatan', '')
            ))
            order_id = cursor.lastrowid
            
            # Step 2: Insert ke tabel order_items
            total_harga = 0
            
            for item in items_data:
                # Ambil data menu untuk harga dan nama
                menu_query = "SELECT id, nama, harga FROM menu WHERE id = %s"
                cursor.execute(menu_query, (item['menu_id'],))
                menu = cursor.fetchone()
                
                if not menu:
                    raise Exception(f"Menu ID {item['menu_id']} tidak ditemukan")
                
                jumlah = item['jumlah']
                subtotal = menu['harga'] * jumlah
                total_harga += subtotal
                
                # Insert order item
                item_query = """
                    INSERT INTO order_items 
                    (order_id, menu_id, jumlah, harga, subtotal) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(item_query, (
                    order_id,
                    menu['id'],
                    jumlah,
                    menu['harga'],
                    subtotal
                ))
            
            # Step 3: Update total harga di tabel orders
            update_query = "UPDATE orders SET total_harga = %s WHERE id = %s"
            cursor.execute(update_query, (total_harga, order_id))
            
            # Commit semua perubahan
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
    
    @staticmethod
    def update_status(order_id, status):
        
        query = "UPDATE orders SET status = %s WHERE id = %s"
        return execute_query(query, (status, order_id), commit=True)

    @staticmethod
    def delete(order_id):
        
        query = "DELETE FROM orders WHERE id = %s"
        return execute_query(query, (order_id,), commit=True)

    @staticmethod
    def get_statistics():
        
        stats = {
            'total_pesanan': 0,
            'pesanan_pending': 0,
            'pesanan_selesai': 0,
            'total_pendapatan': 0
        }
        
        # Total semua pesanan
        query1 = "SELECT COUNT(*) as total FROM orders"
        result1 = execute_query(query1, fetch_one=True)
        stats['total_pesanan'] = result1['total']
        
        # Pesanan pending
        query2 = "SELECT COUNT(*) as total FROM orders WHERE status = 'pending'"
        result2 = execute_query(query2, fetch_one=True)
        stats['pesanan_pending'] = result2['total']
        
        # Pesanan selesai
        query3 = "SELECT COUNT(*) as total FROM orders WHERE status = 'selesai'"
        result3 = execute_query(query3, fetch_one=True)
        stats['pesanan_selesai'] = result3['total']
        
        # Total pendapatan (hanya dari pesanan selesai)
        query4 = "SELECT SUM(total_harga) as total FROM orders WHERE status = 'selesai'"
        result4 = execute_query(query4, fetch_one=True)
        stats['total_pendapatan'] = float(result4['total']) if result4['total'] else 0
        
        return stats
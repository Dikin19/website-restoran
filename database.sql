
CREATE DATABASE IF NOT EXISTS restorandb 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE restorandb;

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    deskripsi TEXT, 
    harga DECIMAL(10, 2) NOT NULL,
    kategori ENUM('Makanan', 'Minuman', 'Dessert', 'Snack') NOT NULL,
    gambar VARCHAR(255) NULL,  -- path file gambar (opsional)
    tersedia BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_customer VARCHAR(100) NOT NULL,
    total_harga DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status ENUM('pending', 'selesai') NOT NULL DEFAULT 'pending',
    catatan TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_id INT NOT NULL,
    nama_menu VARCHAR(100) NOT NULL,  -- simpan nama menu saat order dibuat
    harga_satuan DECIMAL(10, 2) NOT NULL,
    jumlah INT NOT NULL DEFAULT 1,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO admins (username, password, nama_lengkap) VALUES 
('admin', 'admin123', 'Administrator Restoran'),
('kasir', 'kasir123', 'Kasir Restoran');


INSERT INTO menus (nama, deskripsi, harga, kategori, tersedia) VALUES 


('Nasi Goreng Spesial', 'Nasi goreng dengan telur, ayam, dan sayuran segar', 25000, 'Makanan', TRUE),
('Mie Ayam Bakso', 'Mie ayam dengan bakso sapi dan pangsit goreng', 20000, 'Makanan', TRUE),
('Soto Ayam', 'Soto ayam kuah kuning dengan lontong dan telur', 18000, 'Makanan', TRUE),
('Ayam Penyet', 'Ayam goreng penyet dengan sambal terasi pedas', 22000, 'Makanan', TRUE),
('Gado-Gado', 'Sayuran segar dengan bumbu kacang khas Indonesia', 15000, 'Makanan', TRUE),
('Rawon', 'Sup daging sapi hitam khas Jawa Timur', 30000, 'Makanan', TRUE),
('Bakso Sapi', 'Bakso sapi kenyal dengan kuah gurih', 18000, 'Makanan', TRUE),
('Nasi Kuning', 'Nasi kuning dengan ayam dan sambal goreng', 20000, 'Makanan', TRUE),
('Rendang', 'Daging sapi empuk dimasak bumbu rempah', 35000, 'Makanan', TRUE),
('Sate Ayam', 'Sate ayam dengan bumbu kacang dan lontong', 27000, 'Makanan', TRUE),


('Es Teh Manis', 'Teh manis dingin segar', 5000, 'Minuman', TRUE),
('Es Jeruk', 'Jus jeruk segar dengan es batu', 8000, 'Minuman', TRUE),
('Kopi Hitam', 'Kopi hitam panas tanpa gula', 10000, 'Minuman', TRUE),
('Jus Alpukat', 'Jus alpukat segar dengan coklat', 12000, 'Minuman', TRUE),
('Es Campur', 'Es campur dengan berbagai topping', 15000, 'Minuman', TRUE),
('Jus Mangga', 'Jus mangga segar manis alami', 10000, 'Minuman', TRUE),
('Milkshake Coklat', 'Milkshake coklat creamy dan lembut', 15000, 'Minuman', TRUE),
('Teh Tarik', 'Teh tarik khas Malaysia', 12000, 'Minuman', TRUE),
('Lemon Tea', 'Teh lemon segar dingin', 7000, 'Minuman', TRUE),
('Kopi Susu Gula Aren', 'Kopi susu creamy dengan gula aren asli', 18000, 'Minuman', TRUE),


('Pisang Goreng', 'Pisang goreng renyah dengan madu', 10000, 'Dessert', TRUE),
('Es Krim Vanilla', 'Es krim vanilla dengan topping coklat', 12000, 'Dessert', TRUE),
('Klepon', 'Klepon isi gula merah dengan kelapa', 8000, 'Dessert', TRUE),
('Pudding Coklat', 'Pudding coklat lembut dengan saus vanilla', 9000, 'Dessert', TRUE),
('Bolu Kukus', 'Bolu kukus lembut berbagai rasa', 7000, 'Dessert', TRUE),
('Kue Lumpur', 'Kue lumpur kentang manis dan lembut', 6000, 'Dessert', TRUE),
('Cheesecake Mini', 'Cheesecake mini dengan topping stroberi', 15000, 'Dessert', TRUE),
('Es Buah', 'Buah segar dengan sirup dan susu', 12000, 'Dessert', TRUE),
('Brownies', 'Brownies coklat fudgy', 14000, 'Dessert', TRUE),
('Martabak Mini', 'Martabak manis mini topping coklat/keju', 13000, 'Dessert', TRUE),


('Kentang Goreng', 'Kentang goreng crispy dengan saus sambal', 12000, 'Snack', TRUE),
('Risoles', 'Risoles isi daging dan sayuran', 10000, 'Snack', TRUE),
('Tahu Crispy', 'Tahu krispi dengan bumbu pedas gurih', 8000, 'Snack', TRUE),
('Tempe Mendoan', 'Tempe mendoan hangat dengan sambal kecap', 6000, 'Snack', TRUE),
('Dimsum Ayam', 'Dimsum ayam kukus lembut', 15000, 'Snack', TRUE),
('Onion Ring', 'Bawang goreng tepung renyah', 10000, 'Snack', TRUE),
('Sosis Bakar', 'Sosis bakar dengan saus BBQ', 12000, 'Snack', TRUE),
('Singkong Thailand', 'Singkong lembut dengan saus santan', 9000, 'Snack', TRUE),
('Popcorn Chicken', 'Ayam kecil goreng crispy', 15000, 'Snack', TRUE),
('Pangsit Goreng', 'Pangsit goreng garing dengan sambal', 7000, 'Snack', TRUE);


INSERT INTO orders (nama_customer, total_harga, status, catatan) VALUES 
('Budi Santoso', 45000, 'pending', 'Tidak pakai cabe'),
('Siti Aminah', 33000, 'selesai', NULL),
('Agus Wijaya', 50000, 'pending', 'Pesan untuk dine-in meja 5');

-- Data Order Items untuk Order 1 (Budi Santoso)
INSERT INTO order_items (order_id, menu_id, nama_menu, harga_satuan, jumlah, subtotal) VALUES 
(1, 1, 'Nasi Goreng Spesial', 25000, 1, 25000),
(1, 1, 'Nasi Goreng Spesial', 25000, 1, 25000),
(1, 7, 'Es Jeruk', 8000, 2, 16000);

-- Update total harga order 1
UPDATE orders SET total_harga = (SELECT SUM(subtotal) FROM order_items WHERE order_id = 1) WHERE id = 1;


INSERT INTO order_items (order_id, menu_id, nama_menu, harga_satuan, jumlah, subtotal) VALUES 
(2, 3, 'Soto Ayam', 18000, 1, 18000),
(2, 6, 'Es Teh Manis', 5000, 3, 15000);


UPDATE orders SET total_harga = (SELECT SUM(subtotal) FROM order_items WHERE order_id = 2) WHERE id = 2;


INSERT INTO order_items (order_id, menu_id, nama_menu, harga_satuan, jumlah, subtotal) VALUES 
(3, 4, 'Ayam Penyet', 22000, 2, 44000),
(3, 6, 'Es Teh Manis', 5000, 1, 5000);


UPDATE orders SET total_harga = (SELECT SUM(subtotal) FROM order_items WHERE order_id = 3) WHERE id = 3;

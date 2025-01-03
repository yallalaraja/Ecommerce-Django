-- truncate table store_promotion cascade;

	INSERT INTO store_promotion (id, description, discount)
	VALUES
(1, 'New Year Sale', 0.10),
(2, 'Summer Discount', 0.15),
(3, 'Winter Clearance', 0.20),
(4, 'Black Friday Sale', 0.25),
(5, 'Cyber Monday Offer', 0.30),
(6, 'Holiday Special', 0.35),
(7, 'Spring Savings', 0.12),
(8, 'End of Season Sale', 0.18),
(9, 'Christmas Discount', 0.40),
(10, 'Valentines Day Promo', 0.22);

INSERT INTO store_product (id, title, slug, description, price, inventory, last_update,collection_id)
VALUES
(1, 'Laptop', 'laptop', 'A powerful gaming laptop', 1500.00, 50, CURRENT_TIMESTAMP,1),
(2, 'Smartphone', 'smartphone', 'The latest smartphone model', 799.99, 200, CURRENT_TIMESTAMP,2),
(3, 'Headphones', 'headphones', 'Noise-canceling over-ear headphones', 199.99, 150, CURRENT_TIMESTAMP,6),
(4, 'Smartwatch', 'smartwatch', 'A sleek smartwatch with fitness tracking', 249.99, 120, CURRENT_TIMESTAMP,3),
(5, 'Tablet', 'tablet', 'A versatile tablet with a high-resolution screen', 499.99, 80, CURRENT_TIMESTAMP,1),
(6, 'Wireless Mouse', 'wireless-mouse', 'Ergonomic wireless mouse for smooth navigation', 29.99, 500, CURRENT_TIMESTAMP,10),
(7, 'Bluetooth Speaker', 'bluetooth-speaker', 'Portable Bluetooth speaker with deep bass', 89.99, 300, CURRENT_TIMESTAMP,6),
(8, 'Monitor', 'monitor', '24-inch Full HD monitor with vibrant colors', 149.99, 100, CURRENT_TIMESTAMP,8),
(9, 'Keyboard', 'keyboard', 'Mechanical keyboard with RGB lighting', 129.99, 250, CURRENT_TIMESTAMP,8),
(10, 'External SSD', 'external-ssd', 'Fast and reliable external storage device', 99.99, 180, CURRENT_TIMESTAMP,9);

INSERT INTO store_collection (id, title, product_id, feature_product_id)
VALUES
(1, 'Electronics', 1, 2),
(2, 'Mobiles', 2, 1),
(3, 'Accessories', 3, 4),
(4, 'Wearables', 4, 5),
(5, 'Laptops', 1, 3),
(6, 'Audio', 6, 7),
(7, 'Home Entertainment', 7, 2),
(8, 'Computer Peripherals', 8, 9),
(9, 'Storage Devices', 10, 1),
(10, 'Gaming Gear', 1, 3);

INSERT INTO store_customers (id, first_name, last_name, email, phone, birth_date, membership)
VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '1234567890', '1990-01-01', 'B'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '0987654321', '1995-05-05', 'G'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', '1122334455', '1987-03-15', 'S'),
(4, 'Bob', 'Williams', 'bob.williams@example.com', '2233445566', '1992-07-20', 'B'),
(5, 'Charlie', 'Brown', 'charlie.brown@example.com', '3344556677', '1990-11-25', 'G'),
(6, 'David', 'Davis', 'david.davis@example.com', '4455667788', '1983-09-10', 'S'),
(7, 'Eve', 'Miller', 'eve.miller@example.com', '5566778899', '1997-12-02', 'B'),
(8, 'Frank', 'Wilson', 'frank.wilson@example.com', '6677889900', '1985-04-18', 'G'),
(9, 'Grace', 'Moore', 'grace.moore@example.com', '7788990011', '1993-02-14', 'S'),
(10, 'Hannah', 'Taylor', 'hannah.taylor@example.com', '8899001122', '1991-06-30', 'B');

INSERT INTO store_address (id, street, city, zip_addr, customer_id)
VALUES
(1, '123 Main Street', 'New York', '10001', 1),
(2, '456 Elm Street', 'San Francisco', '94101', 2),
(3, '789 Oak Avenue', 'Los Angeles', '90001', 3),
(4, '101 Pine Road', 'Chicago', '60601', 4),
(5, '202 Maple Lane', 'Houston', '77001', 5),
(6, '303 Birch Boulevard', 'Phoenix', '85001', 6),
(7, '404 Cedar Street', 'Dallas', '75201', 7),
(8, '505 Walnut Drive', 'Miami', '33101', 8),
(9, '606 Cherry Court', 'Seattle', '98101', 9),
(10, '707 Ash Crescent', 'Boston', '02101', 10);

INSERT INTO store_order (id, placed_at, payment_status)
VALUES
(1, CURRENT_TIMESTAMP, 'P'),
(2, CURRENT_TIMESTAMP, 'C'),
(3, CURRENT_TIMESTAMP, 'P'),
(4, CURRENT_TIMESTAMP, 'C'),
(5, CURRENT_TIMESTAMP, 'P'),
(6, CURRENT_TIMESTAMP, 'C'),
(7, CURRENT_TIMESTAMP, 'P'),
(8, CURRENT_TIMESTAMP, 'C'),
(9, CURRENT_TIMESTAMP, 'P'),
(10, CURRENT_TIMESTAMP, 'C');

INSERT INTO store_orderitem (id, order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 2, 1500.00),
(2, 2, 2, 1, 799.99),
(3, 3, 3, 3, 199.99),
(4, 4, 4, 2, 249.99),
(5, 5, 5, 1, 499.99),
(6, 6, 6, 4, 29.99),
(7, 7, 7, 2, 89.99),
(8, 8, 8, 1, 149.99),
(9, 9, 9, 3, 129.99),
(10, 10, 10, 5, 99.99);

INSERT INTO store_cart (id, created_at, order_item_id)
VALUES
(1, CURRENT_TIMESTAMP, 1),
(2, CURRENT_TIMESTAMP, 2),
(3, CURRENT_TIMESTAMP, 3),
(4, CURRENT_TIMESTAMP, 4),
(5, CURRENT_TIMESTAMP, 5),
(6, CURRENT_TIMESTAMP, 6),
(7, CURRENT_TIMESTAMP, 7),
(8, CURRENT_TIMESTAMP, 8),
(9, CURRENT_TIMESTAMP, 9),
(10, CURRENT_TIMESTAMP, 10);

INSERT INTO store_cartitem (id, order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 1, 1500.00),
(2, 2, 2, 1, 799.99),
(3, 3, 3, 2, 199.99),
(4, 4, 4, 1, 249.99),
(5, 5, 5, 3, 499.99),
(6, 6, 6, 1, 29.99),
(7, 7, 7, 2, 89.99),
(8, 8, 8, 4, 149.99),
(9, 9, 9, 1, 129.99),
(10, 10, 10, 5, 99.99);






-- ============================================================
-- SmartCafe - Cafeteria Management System
-- Database Schema
-- Authors: Muhammad Usman (24P-0665), Fida Hussain (24P-0676)
-- ============================================================

-- TABLES

CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS Staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT
);

CREATE TABLE IF NOT EXISTS Menu_Item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    staff_id INTEGER,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE IF NOT EXISTS Order_Details (
    order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES Menu_Item(item_id)
);

CREATE TABLE IF NOT EXISTS Bill (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE,
    total_amount REAL NOT NULL,
    payment_method TEXT,
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL,
    unit TEXT,
    threshold INTEGER DEFAULT 5
);

-- ============================================================
-- TRIGGER: Auto-update inventory after each order detail insert
-- ============================================================

CREATE TRIGGER IF NOT EXISTS update_inventory_after_order
AFTER INSERT ON Order_Details
BEGIN
    UPDATE Inventory
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE item_name = (
        SELECT name FROM Menu_Item WHERE item_id = NEW.item_id
    );
END;

-- ============================================================
-- VIEWS
-- ============================================================

-- View: Full order history with customer and staff names
CREATE VIEW IF NOT EXISTS Order_History AS
SELECT
    o.order_id,
    c.name AS customer_name,
    c.phone,
    s.name AS staff_name,
    s.role,
    o.order_date,
    o.total_amount,
    o.status
FROM Orders o
LEFT JOIN Customer c ON o.customer_id = c.customer_id
LEFT JOIN Staff s ON o.staff_id = s.staff_id;

-- View: Sales summary per menu item
CREATE VIEW IF NOT EXISTS Sales_Summary AS
SELECT
    m.name AS item_name,
    m.category,
    SUM(od.quantity) AS total_sold,
    SUM(od.price * od.quantity) AS total_revenue
FROM Order_Details od
JOIN Menu_Item m ON od.item_id = m.item_id
GROUP BY m.item_id;

-- View: Low stock alert
CREATE VIEW IF NOT EXISTS Low_Stock_Alert AS
SELECT
    inventory_id,
    item_name,
    stock_quantity,
    unit,
    threshold
FROM Inventory
WHERE stock_quantity <= threshold;

-- ============================================================
-- SAMPLE DATA
-- ============================================================

INSERT OR IGNORE INTO Staff (name, role) VALUES
    ('Ali Hassan', 'Manager'),
    ('Sara Khan', 'Cashier'),
    ('Bilal Ahmed', 'Chef');

INSERT OR IGNORE INTO Menu_Item (name, price, category) VALUES
    ('Chicken Biryani', 250.0, 'Main Course'),
    ('Beef Burger', 180.0, 'Fast Food'),
    ('Green Tea', 50.0, 'Beverages'),
    ('Samosa', 30.0, 'Snacks'),
    ('Daal Chawal', 150.0, 'Main Course'),
    ('Cold Coffee', 120.0, 'Beverages'),
    ('Spring Rolls', 80.0, 'Snacks'),
    ('Fruit Chaat', 90.0, 'Snacks');

INSERT OR IGNORE INTO Inventory (item_name, stock_quantity, unit, threshold) VALUES
    ('Chicken Biryani', 50, 'plates', 5),
    ('Beef Burger', 40, 'pieces', 5),
    ('Green Tea', 100, 'cups', 10),
    ('Samosa', 80, 'pieces', 10),
    ('Daal Chawal', 60, 'plates', 5),
    ('Cold Coffee', 70, 'cups', 10),
    ('Spring Rolls', 60, 'pieces', 8),
    ('Fruit Chaat', 45, 'plates', 5);

# ============================================================
# SmartCafe - Cafeteria Management System
# Main Flask Application (Backend)
# Authors: Muhammad Usman (24P-0665), Fida Hussain (24P-0676)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'smartcafe_secret_key_2024'

DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'smartcafe.db')

# ============================================================
# DATABASE HELPER FUNCTIONS
# ============================================================

def get_db():
    """Open a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So rows behave like dictionaries
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    return conn

def init_db():
    """Initialize the database using schema.sql."""
    conn = get_db()
    with open(os.path.join(os.path.dirname(__file__), 'database', 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# ============================================================
# HOME / DASHBOARD
# ============================================================

@app.route('/')
def index():
    """Dashboard showing key stats."""
    conn = get_db()

    total_orders = conn.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]
    total_revenue = conn.execute("SELECT IFNULL(SUM(total_amount),0) FROM Bill").fetchone()[0]
    total_menu_items = conn.execute("SELECT COUNT(*) FROM Menu_Item").fetchone()[0]
    low_stock_count = conn.execute("SELECT COUNT(*) FROM Low_Stock_Alert").fetchone()[0]
    recent_orders = conn.execute("SELECT * FROM Order_History ORDER BY order_date DESC LIMIT 5").fetchall()

    conn.close()
    return render_template('index.html',
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           total_menu_items=total_menu_items,
                           low_stock_count=low_stock_count,
                           recent_orders=recent_orders)

# ============================================================
# MENU MANAGEMENT
# ============================================================

@app.route('/menu')
def menu():
    conn = get_db()
    items = conn.execute("SELECT * FROM Menu_Item ORDER BY category, name").fetchall()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        name = request.form['name'].strip()
        price = float(request.form['price'])
        category = request.form['category'].strip()

        conn = get_db()
        # Use prepared statement (parameterized query) to prevent SQL Injection
        conn.execute(
            "INSERT INTO Menu_Item (name, price, category) VALUES (?, ?, ?)",
            (name, price, category)
        )
        conn.commit()
        conn.close()
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('menu'))
    return render_template('add_menu_item.html')

@app.route('/menu/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_menu_item(item_id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name'].strip()
        price = float(request.form['price'])
        category = request.form['category'].strip()

        conn.execute(
            "UPDATE Menu_Item SET name=?, price=?, category=? WHERE item_id=?",
            (name, price, category, item_id)
        )
        conn.commit()
        conn.close()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('menu'))

    item = conn.execute("SELECT * FROM Menu_Item WHERE item_id=?", (item_id,)).fetchone()
    conn.close()
    return render_template('edit_menu_item.html', item=item)

@app.route('/menu/delete/<int:item_id>', methods=['POST'])
def delete_menu_item(item_id):
    conn = get_db()
    conn.execute("DELETE FROM Menu_Item WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()
    flash('Menu item deleted.', 'info')
    return redirect(url_for('menu'))

# ============================================================
# CUSTOMER MANAGEMENT
# ============================================================

@app.route('/customers')
def customers():
    conn = get_db()
    customers = conn.execute("SELECT * FROM Customer ORDER BY customer_id DESC").fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name'].strip()
        phone = request.form['phone'].strip()
        conn = get_db()
        conn.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html')

# ============================================================
# ORDER MANAGEMENT
# ============================================================

@app.route('/orders')
def orders():
    conn = get_db()
    all_orders = conn.execute("SELECT * FROM Order_History ORDER BY order_date DESC").fetchall()
    conn.close()
    return render_template('orders.html', orders=all_orders)

@app.route('/orders/new', methods=['GET', 'POST'])
def new_order():
    conn = get_db()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        staff_id = request.form['staff_id']
        item_ids = request.form.getlist('item_id[]')
        quantities = request.form.getlist('quantity[]')
        payment_method = request.form['payment_method']

        if not item_ids:
            flash('Please add at least one item to the order.', 'danger')
            return redirect(url_for('new_order'))

        # Calculate total
        total = 0.0
        order_items = []
        for item_id, qty in zip(item_ids, quantities):
            item = conn.execute("SELECT * FROM Menu_Item WHERE item_id=?", (item_id,)).fetchone()
            if item and int(qty) > 0:
                subtotal = item['price'] * int(qty)
                total += subtotal
                order_items.append((int(item_id), int(qty), item['price']))

        # Insert order (using transaction)
        try:
            cur = conn.execute(
                "INSERT INTO Orders (customer_id, staff_id, total_amount, status) VALUES (?, ?, ?, 'Completed')",
                (customer_id, staff_id, total)
            )
            order_id = cur.lastrowid

            # Insert order details (trigger fires here automatically)
            for item_id, qty, price in order_items:
                conn.execute(
                    "INSERT INTO Order_Details (order_id, item_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (order_id, item_id, qty, price)
                )

            # Generate bill
            conn.execute(
                "INSERT INTO Bill (order_id, total_amount, payment_method) VALUES (?, ?, ?)",
                (order_id, total, payment_method)
            )

            conn.commit()
            flash(f'Order #{order_id} placed successfully! Total: Rs. {total:.2f}', 'success')
            return redirect(url_for('view_bill', order_id=order_id))

        except Exception as e:
            conn.rollback()
            flash(f'Error placing order: {str(e)}', 'danger')
            return redirect(url_for('new_order'))

    customers = conn.execute("SELECT * FROM Customer").fetchall()
    staff = conn.execute("SELECT * FROM Staff").fetchall()
    menu_items = conn.execute("SELECT * FROM Menu_Item ORDER BY category").fetchall()
    conn.close()
    return render_template('new_order.html', customers=customers, staff=staff, menu_items=menu_items)

# ============================================================
# BILLING
# ============================================================

@app.route('/bill/<int:order_id>')
def view_bill(order_id):
    conn = get_db()
    bill = conn.execute("""
        SELECT b.*, o.order_date, o.status,
               c.name AS customer_name, c.phone,
               s.name AS staff_name
        FROM Bill b
        JOIN Orders o ON b.order_id = o.order_id
        LEFT JOIN Customer c ON o.customer_id = c.customer_id
        LEFT JOIN Staff s ON o.staff_id = s.staff_id
        WHERE b.order_id = ?
    """, (order_id,)).fetchone()

    items = conn.execute("""
        SELECT m.name, od.quantity, od.price, (od.quantity * od.price) AS subtotal
        FROM Order_Details od
        JOIN Menu_Item m ON od.item_id = m.item_id
        WHERE od.order_id = ?
    """, (order_id,)).fetchall()

    conn.close()
    return render_template('bill.html', bill=bill, items=items)

# ============================================================
# INVENTORY MANAGEMENT
# ============================================================

@app.route('/inventory')
def inventory():
    conn = get_db()
    items = conn.execute("SELECT * FROM Inventory ORDER BY item_name").fetchall()
    low_stock = conn.execute("SELECT * FROM Low_Stock_Alert").fetchall()
    conn.close()
    return render_template('inventory.html', items=items, low_stock=low_stock)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        item_name = request.form['item_name'].strip()
        stock_quantity = int(request.form['stock_quantity'])
        unit = request.form['unit'].strip()
        threshold = int(request.form['threshold'])

        conn = get_db()
        conn.execute(
            "INSERT INTO Inventory (item_name, stock_quantity, unit, threshold) VALUES (?, ?, ?, ?)",
            (item_name, stock_quantity, unit, threshold)
        )
        conn.commit()
        conn.close()
        flash('Inventory item added!', 'success')
        return redirect(url_for('inventory'))
    return render_template('add_inventory.html')

@app.route('/inventory/restock/<int:inventory_id>', methods=['POST'])
def restock(inventory_id):
    qty = int(request.form['qty'])
    conn = get_db()
    conn.execute(
        "UPDATE Inventory SET stock_quantity = stock_quantity + ? WHERE inventory_id = ?",
        (qty, inventory_id)
    )
    conn.commit()
    conn.close()
    flash('Stock updated!', 'success')
    return redirect(url_for('inventory'))

# ============================================================
# STAFF MANAGEMENT
# ============================================================

@app.route('/staff')
def staff():
    conn = get_db()
    staff_list = conn.execute("SELECT * FROM Staff").fetchall()
    conn.close()
    return render_template('staff.html', staff=staff_list)

@app.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        name = request.form['name'].strip()
        role = request.form['role'].strip()
        conn = get_db()
        conn.execute("INSERT INTO Staff (name, role) VALUES (?, ?)", (name, role))
        conn.commit()
        conn.close()
        flash('Staff member added!', 'success')
        return redirect(url_for('staff'))
    return render_template('add_staff.html')

# ============================================================
# REPORTS / SALES SUMMARY
# ============================================================

@app.route('/reports')
def reports():
    conn = get_db()
    sales = conn.execute("SELECT * FROM Sales_Summary ORDER BY total_revenue DESC").fetchall()
    order_history = conn.execute("SELECT * FROM Order_History ORDER BY order_date DESC LIMIT 20").fetchall()
    conn.close()
    return render_template('reports.html', sales=sales, order_history=order_history)

# ============================================================
# API ENDPOINT (JSON) - for dynamic order form
# ============================================================

@app.route('/api/menu_items')
def api_menu_items():
    conn = get_db()
    items = conn.execute("SELECT item_id, name, price, category FROM Menu_Item").fetchall()
    conn.close()
    return jsonify([dict(i) for i in items])

# ============================================================
# RUN APP
# ============================================================

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print("Database initialized successfully.")
    app.run(debug=True)

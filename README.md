# SmartCafe Cafeteria Management System

## Project Overview
SmartCafe is a web-based cafeteria management system developed for the Database Systems Lab project. The system helps automate cafeteria operations such as order management, billing, customer handling, inventory tracking, and report generation.

The project is developed using Flask and SQLite with a simple and user-friendly interface.

---

## Objectives
The main objective of this project is to reduce manual work in cafeteria management by providing a digital system for handling daily operations efficiently.

---

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python Flask

### Database
- SQLite

---

## Main Features

- Customer Management
- Staff Management
- Menu Management
- Order Processing
- Billing System
- Inventory Management
- Sales Reports
- Low Stock Alerts

---

## Database Concepts Used

The project implements important database concepts including:

- Primary Keys
- Foreign Keys
- Relationships
- SQL Queries
- Views
- Triggers

---

## Important Functionalities

### Order Management
Customers can place orders and the system stores all order details in the database.

### Billing System
Bills are generated automatically with total amount calculation.

### Inventory Tracking
Inventory stock updates automatically whenever an order is placed.

### Reports
Admin can view sales reports and low stock alerts.

---

## Trigger Used

### update_inventory_after_order
This trigger automatically decreases inventory stock after a new order is inserted into the database.

---

## Views Used

### Sales_Summary
Displays total sales and revenue information.

### Low_Stock_Alert
Displays items with low inventory stock.

### Order_History
Displays complete order details with customer and staff information.

---

## How to Run
1. Install Flask (pip install flask)
2. Run:
   python app.py
3. Open:
   http://127.0.0.1:5000
   ## Project Structure

```text
SmartCafe/
│
├── app.py
├── templates/
├── static/
├── database/
├── README.md

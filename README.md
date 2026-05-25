# SmartCafe Cafeteria Management System

## Group Information

### Group Number
11

### Group Members
- Muhammad Usman (24P-0665)
- Fida Hussain (24P-0676)
- Muhammad Ahmed (22P-9069)
---

## Project Title
# SmartCafe Cafeteria Management System

---

## Project Overview
SmartCafe is a web-based cafeteria management system developed for the Database Systems Lab project. The system helps automate cafeteria operations such as:

- Order Management
- Billing System
- Customer Handling
- Inventory Tracking
- Report Generation

The project is developed using Flask and SQLite with a simple and user-friendly interface.

---

## GitHub Repository URL
https://github.com/fam-usman/SmartCafe-Cafeteria-Management-System

---

## Objectives
The main objective of this project is to reduce manual work in cafeteria management by providing a digital system for handling daily cafeteria operations efficiently and accurately.

---

# Technologies Used

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python Flask

## Database
- SQLite

## Development Tools
- VS Code

---

# Main Features

- Customer Management
- Cashier Management
- Menu Management
- Order Placement and Bill Generation
- Automatic Inventory Update
- Stock Alert for Low Inventory Items
- Sales Summary and Reports
- Order History Tracking

---

# CRUD Operations Implemented

The project implements all four CRUD operations:

## Create
- Add new customers
- Add menu items
- Create orders

## Read
- View customers
- View menu items
- View sales reports
- View order history

## Update
- Update customer information
- Update menu items
- Update inventory stock

## Delete
- Delete menu items
- Remove customer records
- Delete unnecessary records

---

# Database Concepts Used

The project implements important database concepts including:

- Primary Keys
- Foreign Keys
- Relationships
- SQL Queries
- Views
- Triggers
- Normalization

---

# Important Functionalities

## Order Management
Customers can place orders and all order details are stored in the database.

## Billing System
Bills are generated automatically with total price calculation.

## Inventory Tracking
Inventory stock updates automatically whenever an order is placed.

## Sales Reports
Admin can view sales summaries and order reports.

## Low Stock Alert
The system displays alerts for items with low inventory stock.

---

# Trigger Used

## update_inventory_after_order
This trigger automatically decreases inventory stock whenever a new order is inserted into the database.

---

# Views Used

## Sales_Summary
Displays total sales and revenue information.

## Low_Stock_Alert
Displays items with low inventory stock.

## Order_History
Displays complete order details with customer and staff information.

---

# SQL Injection Understanding

## What is SQL Injection?
SQL Injection is a security attack in which a user inserts malicious SQL queries into input fields to access or damage the database.

## How to Prevent SQL Injection?
- Use parameterized queries
- Validate user inputs
- Avoid direct SQL query concatenation
- Use secure database handling methods

## Is Our Application Secure?
Yes, our application uses Flask with SQLite queries in a controlled manner and avoids unsafe query handling to reduce SQL Injection risks.

---

# Project Structure

```text
SmartCafe/
│
├── app.py
├── templates/
├── static/
├── database/
├── README.md

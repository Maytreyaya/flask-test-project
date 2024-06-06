-- Create database
CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

-- Create table: roles
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) UNIQUE,
    description VARCHAR(255)
);

-- Insert sample data into roles table
INSERT INTO roles (name, description) VALUES
('admin', 'Administrator'),
('user', 'Regular User');

-- Create table: users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    active BOOLEAN,
    confirmed_at DATETIME,
    fs_uniquifier VARCHAR(255) UNIQUE NOT NULL
);

-- Create table: roles_users (many-to-many relationship between users and roles)
CREATE TABLE IF NOT EXISTS roles_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Create table: products
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    color VARCHAR(30),
    weight FLOAT,
    price FLOAT
);

-- Create table: addresses
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(80),
    city VARCHAR(80),
    street VARCHAR(120)
);

-- Create table: orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address_id INT,
    status VARCHAR(20),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

-- Create table: order_items
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data into products table
INSERT INTO products (name, color, weight, price) VALUES
('Product A', 'Red', 1.5, 19.99),
('Product B', 'Blue', 2.0, 29.99),
('Product C', 'Green', 1.8, 39.99);

-- Insert sample data into addresses table
INSERT INTO addresses (country, city, street) VALUES
('USA', 'New York', '123 Main St'),
('UK', 'London', '456 Elm St');

-- Insert sample data into orders table
INSERT INTO orders (address_id, status) VALUES
(1, 'Pending'),
(2, 'Shipped');

-- Insert sample data into order_items table
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 2),
(2, 3, 1);
-- Drop tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS fraud_flagged;

-- Create products table
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2)
);

-- Create customers table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    signup_date DATE,
    billing_address TEXT,
    shipping_address TEXT,
    customer_type VARCHAR(20)
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    product_id VARCHAR(20) REFERENCES products(product_id),
    order_date DATE,
    order_time TIME,
    amount DECIMAL(10, 2),
    quantity INTEGER,
    payment_method VARCHAR(50),
    shipping_address TEXT,
    billing_address TEXT,
    acquisition_channel VARCHAR(50),
    is_fraud BOOLEAN,
    chargeback_date DATE,
    device_type VARCHAR(20),
    ip_address VARCHAR(50)
);

-- Create the analytical table
CREATE TABLE fraud_flagged (
    -- Original Transaction Data
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    order_date DATE,
    order_time TIME,
    amount DECIMAL(10, 2),
    quantity INTEGER,
    payment_method VARCHAR(50),
    shipping_address TEXT,
    billing_address TEXT,
    acquisition_channel VARCHAR(50),
    is_fraud BOOLEAN,            
    chargeback_date DATE,
    device_type VARCHAR(20),
    ip_address VARCHAR(50),

    -- Engineered Features (from 01_data_cleaning.ipynb)
    is_weekend INTEGER,
    is_high_value INTEGER,
    signup_date DATE,
    days_since_signup INTEGER,
    is_new_customer INTEGER,
    shipping_billing_mismatch INTEGER,

    -- Machine Learning Predictions (from 03_fraud_detection_model.ipynb)
    fraud_prediction INTEGER,
    fraud_probability DECIMAL(5, 4)
);

-- Create Indexes for fast analysis
CREATE INDEX idx_ff_date ON fraud_flagged(order_date);
CREATE INDEX idx_ff_prediction ON fraud_flagged(fraud_prediction);
CREATE INDEX idx_ff_isfraud ON fraud_flagged(is_fraud);

-- Create indexes
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(order_date);
CREATE INDEX idx_transactions_fraud ON transactions(is_fraud);
CREATE INDEX idx_customers_email ON customers(email);
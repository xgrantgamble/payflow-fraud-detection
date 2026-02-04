import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Setting random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

print("Starting data generation...")

print("Generating products...")

products = []
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']

for i in range(1, 501):
    category = random.choice(categories)
    price = round(random.uniform(10, 500), 2)
    cost = round(price * random.uniform(0.4, 0.7), 2)
    
    products.append({
        'product_id': f'PROD{i:04d}',
        'product_name': fake.catch_phrase(),
        'category': category,
        'price': price,
        'cost': cost
    })

products_df = pd.DataFrame(products)
print(f"Generated {len(products_df)} products")


print("Generating customers...")

customers = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 9, 30)

for i in range(1, 10001):
    signup_date = fake.date_between(start_date=start_date, end_date=end_date)
    
    # Introducing some duplicates (2%)
    if i > 1 and random.random() < 0.02:
        # Duplicate email from previous customer
        email = customers[-1]['email']
    else:
        email = fake.email()
    
    customers.append({
        'customer_id': f'CUST{i:05d}',
        'customer_name': fake.name(),
        'email': email,
        'phone': fake.phone_number(),
        'signup_date': signup_date,
        'billing_address': fake.address().replace('\n', ', '),
        'shipping_address': fake.address().replace('\n', ', '),
        'customer_type': 'new' if signup_date >= datetime(2024, 9, 1).date() else 'returning'
    })

customers_df = pd.DataFrame(customers)
print(f"Generated {len(customers_df)} customers")


print("Generating transactions...")

transactions = []
transaction_id = 1

# Date ranges for Q4 2024
oct_start = datetime(2024, 10, 1)
oct_end = datetime(2024, 10, 31)
nov_start = datetime(2024, 11, 1)
nov_end = datetime(2024, 11, 30)
dec_start = datetime(2024, 12, 1)
dec_end = datetime(2024, 12, 31)

# Revenue targets
oct_revenue = 1_850_000
nov_revenue = 2_100_000
dec_revenue = 2_450_000

black_friday = datetime(2024, 11, 29)
cyber_monday = datetime(2024, 12, 2)

channels = ['Paid Search', 'Organic', 'Social', 'Email']
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay']
device_types = ['Desktop', 'Mobile', 'Tablet']

def generate_transactions_for_month(start_date, end_date, target_revenue, month_name):
    global transaction_id
    month_transactions = []
    current_revenue = 0
    days_in_month = (end_date - start_date).days + 1
    
    # Calculating daily target (with spikes for special days)
    daily_target = target_revenue / days_in_month
    
    for single_date in pd.date_range(start_date, end_date):
        if single_date.date() == black_friday.date():
            multiplier = 3.0  # Black Friday spike
        elif single_date.date() == cyber_monday.date():
            multiplier = 2.5  # Cyber Monday spike
        elif single_date.weekday() in [5, 6]:  # Weekend
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        day_target = daily_target * multiplier
        day_revenue = 0
        
        # Generating transactions until daily target hit
        while day_revenue < day_target:
            customer = customers_df.sample(1).iloc[0]
            product = products_df.sample(1).iloc[0]
            
            # Determine if customer is "new" (signed up within 30 days)
            days_since_signup = (single_date.date() - customer['signup_date']).days
            is_new_customer = days_since_signup < 30
            
            # Transaction amount
            quantity = random.randint(1, 3)
            amount = round(product['price'] * quantity, 2)
            
            # Determine fraud based on risk factors
            is_weekend = single_date.weekday() in [5, 6]
            is_high_value = amount > 500
            
            # Base fraud rate: 2.1%
            fraud_probability = 0.021
            
            if is_high_value:
                fraud_probability = 0.051  # 5.1% for high value
            elif amount < 100:
                fraud_probability = 0.008  
            
            if is_weekend:
                fraud_probability *= 3.2  # 3.2x higher on weekends
            
            if is_new_customer:
                fraud_probability *= 1.5  # 1.5x higher for new customers
            
            is_fraud = random.random() < fraud_probability
            
            # Shipping/billing mismatches (risk factor)
            if random.random() < 0.15:
                shipping_address = fake.address().replace('\n', ', ')
            else:
                shipping_address = customer['shipping_address']
            
            # Generating order times
            hour = int(np.random.normal(14, 4))  # Peak around 2 PM
            hour = max(0, min(23, hour))
            minute = random.randint(0, 59)
            order_time = f"{hour:02d}:{minute:02d}:00"
            
            # Missing data (5% missing order_time, 3% missing shipping_address)
            if random.random() < 0.05:
                order_time = None
            if random.random() < 0.03:
                shipping_address = None
            
            # Channel-specific fraud rates
            channel = random.choice(channels)
            if channel == 'Email':
                fraud_probability *= 0.43  # Email has 0.9% fraud (lower)
            elif channel == 'Paid Search':
                fraud_probability *= 1.52  # Paid Search has 3.2% fraud (higher)
            
            # Chargeback date (30-60 days after fraud)
            chargeback_date = None
            if is_fraud and random.random() < 0.9:  # 90% of fraud results in chargeback
                chargeback_days = random.randint(30, 60)
                chargeback_date = single_date + timedelta(days=chargeback_days)
            
            transaction = {
                'transaction_id': f'TXN{transaction_id:06d}',
                'customer_id': customer['customer_id'],
                'product_id': product['product_id'],
                'order_date': single_date.date(),
                'order_time': order_time,
                'amount': amount,
                'quantity': quantity,
                'payment_method': random.choice(payment_methods),
                'shipping_address': shipping_address,
                'billing_address': customer['billing_address'],
                'acquisition_channel': channel,
                'is_fraud': is_fraud,
                'chargeback_date': chargeback_date.date() if chargeback_date else None,
                'device_type': random.choice(device_types),
                'ip_address': fake.ipv4()
            }
            
            month_transactions.append(transaction)
            day_revenue += amount
            transaction_id += 1
        
        current_revenue += day_revenue
    
    print(f"{month_name}: Generated {len(month_transactions)} transactions, Revenue: ${current_revenue:,.2f}")
    return month_transactions

# Generating transactions for each month
all_transactions = []
all_transactions.extend(generate_transactions_for_month(oct_start, oct_end, oct_revenue, "October"))
all_transactions.extend(generate_transactions_for_month(nov_start, nov_end, nov_revenue, "November"))
all_transactions.extend(generate_transactions_for_month(dec_start, dec_end, dec_revenue, "December"))

transactions_df = pd.DataFrame(all_transactions)

# Add data quality issues - some amounts as strings with $
mask = transactions_df.sample(frac=0.02).index
transactions_df.loc[mask, 'amount'] = transactions_df.loc[mask, 'amount'].apply(lambda x: f"${x}")

print(f"Total transactions generated: {len(transactions_df)}")
print(f"Total fraud transactions: {transactions_df['is_fraud'].sum()} ({transactions_df['is_fraud'].mean()*100:.2f}%)")


print("\nSaving files...")

products_df.to_csv('data/raw/products_raw.csv', index=False)
print("Saved products_raw.csv")

customers_df.to_csv('data/raw/customers_raw.csv', index=False)
print("Saved customers_raw.csv")

transactions_df.to_csv('data/raw/transactions_raw.csv', index=False)
print("Saved transactions_raw.csv")

print("\n" + "="*50)
print("DATA GENERATION COMPLETE")
print("="*50)
print(f"\nSummary:")
print(f"  Products: {len(products_df)}")
print(f"  Customers: {len(customers_df)}")
print(f"  Transactions: {len(transactions_df)}")
print(f"  Fraud Rate: {transactions_df['is_fraud'].mean()*100:.2f}%")
print(f"  Total Revenue: ${transactions_df[transactions_df['amount'].apply(lambda x: isinstance(x, (int, float)))]['amount'].sum():,.2f}")
import pandas as pd

df = pd.read_csv('data/processed/fraud_flagged.csv')

# Defining columns for db load
expected_columns = [
    'transaction_id', 
    'customer_id', 
    'product_id', 
    'order_date', 
    'order_time', 
    'amount', 
    'quantity', 
    'payment_method', 
    'shipping_address', 
    'billing_address', 
    'acquisition_channel', 
    'is_fraud', 
    'chargeback_date', 
    'device_type', 
    'ip_address', 
    'fraud_prediction', 
    'fraud_probability'
]

# (This drops 'Unnamed: 0' or any extra columns causing the error)
df_clean = df[expected_columns].copy()

df_clean.to_csv('data/processed/fraud_flagged_clean.csv', index=False, header=False)

print("Clean CSV created: data/processed/fraud_flagged_clean.csv")
print(f"Columns: {len(df_clean.columns)}")
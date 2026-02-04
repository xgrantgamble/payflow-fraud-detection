import pandas as pd

df = pd.read_csv('data/raw/transactions_raw.csv')

# Removing $ from amount column
df['amount'] = df['amount'].astype(str).str.replace('$', '').astype(float)

df.to_csv('data/raw/transactions_raw.csv', index=False)

print("Cleaned transaction amounts")
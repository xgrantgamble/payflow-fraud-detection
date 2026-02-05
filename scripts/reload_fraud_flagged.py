import pandas as pd
from sqlalchemy import create_engine, text  # ← Added 'text' import
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
fraud_flagged_csv = PROJECT_ROOT / 'data' / 'processed' / 'fraud_flagged.csv'

print("="*70)
print("RELOADING POSTGRESQL fraud_flagged TABLE")
print("="*70)

# Check if file exists
print(f"\n1. Checking file: {fraud_flagged_csv}")
if not fraud_flagged_csv.exists():
    print("    ERROR: fraud_flagged.csv not found!")
    print(f"   Expected location: {fraud_flagged_csv}")
    print("   Run 03_fraud_detection_model.ipynb first to create it!")
    exit(1)

# Load CSV
df = pd.read_csv(fraud_flagged_csv)
print(f"   Found file with {len(df):,} rows and {len(df.columns)} columns")

# Check for ML predictions
if 'fraud_prediction' in df.columns and 'fraud_probability' in df.columns:
    print(f"   Has ML predictions")
    predictions = df['fraud_prediction'].sum()
    print(f"   {predictions:,} transactions flagged as fraud")
else:
    print(f"   Missing ML predictions - run 03_fraud_detection_model.ipynb first!")
    exit(1)

# Connect to PostgreSQL
print(f"\n2. Connecting to PostgreSQL...")
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', '5432')

if not DB_PASSWORD:
    print("   ERROR: DB_PASSWORD not set in .env file")
    exit(1)

DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@localhost:{DB_PORT}/payflow_commerce"

try:
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))  
    print(f"   Connected to database")
except Exception as e:
    print(f"   Connection failed: {e}")
    exit(1)

# Check current state
current_count = pd.read_sql(text("SELECT COUNT(*) as count FROM fraud_flagged"), engine)  
print(f"   Current rows in fraud_flagged: {current_count['count'][0]:,}")

# Clear and reload
print(f"\n3. Clearing old data...")
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE fraud_flagged;"))  
    conn.commit()
print(f"   Table truncated")

print(f"\n4. Loading {len(df):,} rows...")
df.to_sql('fraud_flagged', engine, if_exists='append', index=False)
print(f"   Data loaded")

# Verify
verify_count = pd.read_sql(text("SELECT COUNT(*) as count FROM fraud_flagged"), engine)  
print(f"\n5. Verification:")
print(f"   Rows in CSV: {len(df):,}")
print(f"   Rows in DB:  {verify_count['count'][0]:,}")

if verify_count['count'][0] == len(df):
    print(f"\n{'='*70}")
    print(f"SUCCESS! fraud_flagged table reloaded successfully")
    print(f"{'='*70}")
    
    # Show sample query
    print(f"\nSample data:")
    sample = pd.read_sql(text("SELECT * FROM fraud_flagged LIMIT 3"), engine)  
    print(sample[['transaction_id', 'amount', 'is_fraud', 'fraud_prediction', 'fraud_probability']].to_string())
else:
    print(f"\nWARNING: Row count mismatch!")
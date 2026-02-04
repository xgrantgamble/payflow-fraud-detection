"""
Automated database setup script for PayFlow Commerce
This script creates the database schema and loads all data automatically

Run this script from the project root directory:
    python setup_database.py
"""
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get project paths
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
POSTGRES_DIR = PROJECT_ROOT / 'postgres'

# Database configuration from .env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'payflow_commerce')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Create database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_sql_file(engine, sql_file):
    """Execute SQL commands from a file"""
    print(f"\n📄 Executing {sql_file.name}...")
    
    with open(sql_file, 'r') as f:
        sql_commands = f.read()
    
    # Split on semicolons to execute each command separately
    commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
    
    with engine.connect() as conn:
        for i, command in enumerate(commands, 1):
            try:
                conn.execute(text(command))
                conn.commit()
                print(f"   ✅ Command {i} executed successfully")
            except Exception as e:
                print(f"   ⚠️  Command {i} error: {e}")
                continue

def load_csv_to_table(engine, csv_path, table_name):
    """Load CSV file into PostgreSQL table"""
    print(f"\n📊 Loading {csv_path.name} into {table_name}...")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        print(f"   Found {len(df)} rows, {len(df.columns)} columns")
        
        # Load to database
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"   ✅ Successfully loaded {len(df)} rows into {table_name}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error loading {table_name}: {e}")
        return False

def verify_data(engine):
    """Verify data was loaded correctly"""
    print("\n🔍 Verifying data...")
    
    verification_queries = [
        ("products", "SELECT COUNT(*) as count FROM products"),
        ("customers", "SELECT COUNT(*) as count FROM customers"),
        ("transactions", "SELECT COUNT(*) as count FROM transactions")
    ]
    
    with engine.connect() as conn:
        for table, query in verification_queries:
            try:
                result = conn.execute(text(query)).fetchone()
                count = result[0]
                print(f"   {table}: {count:,} rows")
            except Exception as e:
                print(f"   ❌ {table}: Error - {e}")

def main():
    """Main setup function"""
    print("="*60)
    print("PayFlow Commerce - Automated Database Setup")
    print("="*60)
    
    # Verify environment
    print("\n🔍 Checking environment...")
    print(f"   Project root: {PROJECT_ROOT}")
    print(f"   Data directory: {RAW_DATA_DIR}")
    print(f"   Database: {DB_NAME}")
    print(f"   Host: {DB_HOST}:{DB_PORT}")
    
    if not DB_PASSWORD:
        print("\n❌ ERROR: DB_PASSWORD not set in .env file")
        print("\n💡 Make sure you have a .env file with:")
        print("   DB_PASSWORD=your_password")
        return
    
    # Step 1: Connect to database
    print("\n🔌 Connecting to PostgreSQL...")
    try:
        engine = create_engine(DATABASE_URL)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("   ✅ Connection successful")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n💡 Make sure:")
        print("   1. PostgreSQL is running")
        print("   2. .env file has correct credentials")
        print(f"   3. Database '{DB_NAME}' exists")
        print("\nTo create the database, run:")
        print(f"   psql -U {DB_USER} -c 'CREATE DATABASE {DB_NAME};'")
        return
    
    # Step 2: Run schema SQL
    print("\n" + "="*60)
    print("Creating Database Schema")
    print("="*60)
    
    schema_file = POSTGRES_DIR / 'payflow_commerce.sql'
    if schema_file.exists():
        run_sql_file(engine, schema_file)
    else:
        print(f"\n⚠️  Schema file not found: {schema_file}")
        print("   Skipping schema creation")
        print("   Looking for file at:", schema_file.absolute())
    
    # Step 3: Load raw data
    print("\n" + "="*60)
    print("Loading Raw Data")
    print("="*60)
    
    data_files = [
        ('products_raw.csv', 'products'),
        ('customers_raw.csv', 'customers'),
        ('transactions_raw.csv', 'transactions')
    ]
    
    success_count = 0
    for csv_file, table_name in data_files:
        csv_path = RAW_DATA_DIR / csv_file
        if csv_path.exists():
            if load_csv_to_table(engine, csv_path, table_name):
                success_count += 1
        else:
            print(f"\n⚠️  File not found: {csv_path}")
            print(f"   Expected location: {csv_path.absolute()}")
    
    # Step 4: Verify
    print("\n" + "="*60)
    print("Verification")
    print("="*60)
    verify_data(engine)
    
    # Summary
    print("\n" + "="*60)
    print("Setup Complete")
    print("="*60)
    print(f"✅ {success_count}/{len(data_files)} tables loaded successfully")
    
    if success_count == len(data_files):
        print("\n🎉 Database setup successful!")
        print("\n💡 Next steps:")
        print("   1. Run the Jupyter notebooks:")
        print("      - notebooks/01_data_cleaning.ipynb")
        print("      - notebooks/02_exploratory_analysis.ipynb")
        print("      - notebooks/03_fraud_detection_model.ipynb")
    else:
        print("\n⚠️  Some files were not loaded. Please check the errors above.")
        print("\n💡 Make sure your data/raw/ directory contains:")
        for csv_file, _ in data_files:
            print(f"   - {csv_file}")

if __name__ == "__main__":
    main()
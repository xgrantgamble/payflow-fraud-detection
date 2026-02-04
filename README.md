# End-to-End Financial Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![PowerBI](https://img.shields.io/badge/Power_BI-Desktop-yellow)
![Status](https://img.shields.io/badge/Status-Complete-green)

## Project Overview & Business Problem

**PayFlow Commerce**, a high-volume payment processor, experienced a critical surge in chargebacks during Q4 2024. The operational team was overwhelmed by false positives, while actual fraud was undetected.

**The Goal:** Analyze **14,000+ transaction records** to identify the root cause of the fraud spike and build a Machine Learning solution to mitigate risk without impacting revenue.

---

## Key Findings

1.  **Risk Exposure:** The platform's fraud rate hit **7.03%** (Industry benchmark: <1%), exposing the business to **$496k** in potential losses.
2.  **Weekend Trend:** Fraud patterns revealed a massive spike on Saturdays and Sundays (**13.79% fraud rate**) compared to weekdays (3.99%), exploiting reduced staff coverage.
3.  **Model Impact:** The XGBoost model achieved **89% accuracy** and is projected to save **$51k per quarter** by auto-flagging high-probability fraud >$300.

---

## Visual Analysis

### Executive Dashboard

![Executive Dashboard](execSum.png)
_Figure 1: Executive KPI Dashboard tracking $7.06M in revenue and the fraud spike._

### Risk Analysis

![Fraud Analysis](fraudRisk.png)
_Figure 2: Analysis identifying the 13.8% weekend fraud spike._

---

## Tech Stack

- **Python:** Pandas (ETL), NumPy, Scikit-Learn (ML), XGBoost
- **SQL (PostgreSQL):** Case statements, aggregations, data storage
- **Power BI:** Data modeling (DAX), interactive dashboard
- **Excel:** Financial modeling (3-Statement model, Variance Analysis)

## Project Structure

```text
├── data/                   # Raw and processed datasets
├── excel/                  # Financial models (Income Statement, Variance Analysis)
├── output/                 # Model artifacts (.pkl) and visual assets
├── Payflow/                # Screenshots for documentation
├── postgres/               # SQL schema and analytical queries
├── scripts/                # Python source code
│   ├── fix_transactions.py # ETL Pipeline
│   ├── notebooks/          # Jupyter notebooks for training and EDA
└── README.md               # Project documentation
```

## Data Source Disclosure
This project uses synthetic transaction data designed to simulate realistic e-commerce fraud patterns, seasonal trends, and data quality issues commonly found in production systems.

Data was generated using Python (Faker, NumPy) to ensure:

Realistic fraud patterns: Weekend spikes, high-value transaction risk, and category-specific targeting.

Seasonal trends: Modeled Q4 holiday surge and Black Friday volume spikes.

Data quality challenges: Intentionally introduced nulls, duplicates, and formatting inconsistencies to test ETL robustness.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/payflow-fraud-detection.git
cd payflow-fraud-detection
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your PostgreSQL credentials
# Update DB_PASSWORD with your actual password
```

### 5. Create PostgreSQL database (if not exists)
```bash
psql -U postgres -c 'CREATE DATABASE payflow_commerce;'
```

### 6. Run automated database setup
```bash
python setup_database.py
```

Expected output:
```
============================================================
PayFlow Commerce - Automated Database Setup
============================================================

🔍 Checking environment...
   Project root: /path/to/payflow-fraud-detection
   Database: payflow_commerce
   Host: localhost:5432

🔌 Connecting to PostgreSQL...
   ✅ Connection successful

📄 Executing payflow_commerce.sql...
   ✅ Command 1 executed successfully
   ✅ Command 2 executed successfully
   ...

📊 Loading products_raw.csv into products...
   Found 500 rows, 5 columns
   ✅ Successfully loaded 500 rows into products

📊 Loading customers_raw.csv into customers...
   Found 10000 rows, 8 columns
   ✅ Successfully loaded 10000 rows into customers

📊 Loading transactions_raw.csv into transactions...
   Found 14082 rows, 15 columns
   ✅ Successfully loaded 14082 rows into transactions

🔍 Verifying data...
   products: 500 rows
   customers: 10,000 rows
   transactions: 14,082 rows

---

Grant Gamble  

Role: Data Analyst / Financial Analyst  

LinkedIn: [xgrantgamble](linkedin.com/in/xgrantgamble)  
X: [xgrantgamble](x.com/xgrantgamble)  
Email: grantgamble1122@gmail.com  
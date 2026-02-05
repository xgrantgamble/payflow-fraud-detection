
# PayFlow Commerce - Financial Analytics & Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![PowerBI](https://img.shields.io/badge/Power_BI-Desktop-yellow)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-red)
![Status](https://img.shields.io/badge/Status-Complete-green)

---

## 📊 Project Overview

**PayFlow Commerce**, a high-volume payment processor, experienced a critical surge in fraud during Q4 2024, with chargebacks reaching **7.03%** (industry benchmark: <1%). The operational team was overwhelmed by false positives while actual fraud went undetected.

This project delivers an **end-to-end analytics solution** combining financial modeling, machine learning, and business intelligence to identify fraud patterns and build an automated detection system.

---

## 🎯 Business Impact

### Key Findings

| Metric | Value | Industry Benchmark |
|--------|-------|-------------------|
| **Fraud Rate** | 7.03% | <1% |
| **Q4 Revenue** | $6.4M | N/A |
| **Fraud Exposure** | $496K | N/A |
| **Weekend Fraud Rate** | 13.79% | 3.99% (weekday) |

### Model Performance

**XGBoost Classifier Results:**

| Dataset | Accuracy | Recall | Precision | F1-Score |
|---------|----------|--------|-----------|----------|
| **Test Set (20%)** | 89.2% | 41.3% | 11.1% | 17.5% |
| **Full Dataset** | 80.0% | 74.0% | 17.3% | 28.1% |

**Financial Impact:**
- **Fraud Caught:** 555/750 actual fraud cases (74% recall on full dataset)
- **Projected Quarterly Savings:** $143K (based on test set performance)
- **Annual Savings Potential:** $572K

---

## 🔍 Key Insights

1. **Weekend Vulnerability:** Fraud spikes **3.5x higher** on weekends (13.79% vs 3.99% weekday rate), exploiting reduced staff coverage

2. **High-Value Transaction Risk:** Transactions >$500 show **5.1% fraud rate** compared to <1% for transactions under $100

3. **Channel Performance:** 
   - Email acquisition: 0.9% fraud (lowest)
   - Paid Search: 3.2% fraud (highest)
   - Social & Organic: ~2% fraud

4. **New Customer Risk:** Customers <30 days old show **1.5x higher** fraud probability

---

## 🛠️ Technical Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.11, SQL (PostgreSQL) |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-Learn, XGBoost |
| **Database** | PostgreSQL 18 |
| **Visualization** | Matplotlib, Seaborn, Power BI |
| **Financial Modeling** | Excel (3-Statement Model, Variance Analysis) |
| **Environment** | python-dotenv, SQLAlchemy |

---

## 📁 Project Structure

```
payflow-fraud-detection/
├── data/
│   ├── raw/                      # Original CSV files (not in repo)
│   │   ├── products_raw.csv      # 500 products
│   │   ├── customers_raw.csv     # 10,000 customers
│   │   └── transactions_raw.csv  # 14,082 transactions
│   └── processed/                # Cleaned data (not in repo)
│       ├── transactions_clean.csv
│       ├── customers_clean.csv
│       └── fraud_flagged.csv
│
├── scripts/
│   ├── notebooks/
│   │   ├── 01_data_cleaning.ipynb           # ETL pipeline
│   │   ├── 02_exploratory_analysis.ipynb    # EDA & visualization
│   │   └── 03_fraud_detection_model.ipynb   # ML model training
│   ├── generate_synthetic_data.py           # Data generation script
│   ├── fix_transactions.py                  # Data quality fixes
│   └── fix_fraudFlag.py                     # Database prep utility
│
├── postgres/
│   ├── payflow_commerce.sql      # Database schema
│   └── analysis_queries.sql      # Analytical SQL queries
│
├── output/                       # Model artifacts (not in repo)
│   ├── fraud_model.pkl           # Trained XGBoost model
│   └── scaler.pkl                # Feature scaler
│
├── excel/
│   └── financial_model.xlsx      # 3-statement model (not included)
│
├── powerbi/
│   └── dashboard.pbix            # Interactive BI dashboard (not included)
│
├── .env.example                  # Environment template
├── .gitignore                    # Git exclusions
├── requirements.txt              # Python dependencies
├── setup_database.py             # Automated database setup
└── README.md                     # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- 2GB free disk space
- Power BI Desktop (optional, for dashboard)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/payflow-fraud-detection.git
cd payflow-fraud-detection
```

#### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your PostgreSQL credentials
# Required: DB_PASSWORD
```

Example `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=payflow_commerce
DB_USER=postgres
DB_PASSWORD=your_secure_password
```

#### 5. Generate synthetic data
```bash
python scripts/generate_synthetic_data.py
```

Expected output:
```
Starting data generation...
Generated 500 products
Generated 10000 customers
October: Generated 4698 transactions, Revenue: $1,850,183.45
November: Generated 5301 transactions, Revenue: $2,100,274.89
December: Generated 6083 transactions, Revenue: $2,450,125.67
Total transactions generated: 14082
Total fraud transactions: 750 (5.33%)
```

#### 6. Create PostgreSQL database
```bash
# Create database (if not exists)
psql -U postgres -c 'CREATE DATABASE payflow_commerce;'
```

#### 7. Run automated database setup
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
   ✅ Schema created successfully

📊 Loading products_raw.csv into products...
   ✅ Successfully loaded 500 rows

📊 Loading customers_raw.csv into customers...
   ✅ Successfully loaded 10,000 rows

📊 Loading transactions_raw.csv into transactions...
   ✅ Successfully loaded 14,082 rows

🔍 Verifying data...
   products: 500 rows
   customers: 10,000 rows
   transactions: 14,082 rows

============================================================
✅ 3/3 tables loaded successfully
🎉 Database setup successful!
============================================================
```

#### 8. Run analysis notebooks
```bash
jupyter notebook
```

Open and run in order:
1. `scripts/notebooks/01_data_cleaning.ipynb`
2. `scripts/notebooks/02_exploratory_analysis.ipynb`
3. `scripts/notebooks/03_fraud_detection_model.ipynb`

---

## 📈 Analysis Pipeline

### 1. Data Cleaning (`01_data_cleaning.ipynb`)

**Inputs:**
- Raw PostgreSQL tables: `transactions`, `customers`, `products`

**Process:**
- Handle missing values (662 missing `order_time`, 423 missing `shipping_address`)
- Remove duplicate customer records (770 duplicates by email)
- Convert data types (dates, amounts, booleans)
- Engineer fraud risk features

**Outputs:**
- `transactions_clean.csv` (21 columns, 14,082 rows)
- `customers_clean.csv` (10,000 unique customers)

**Engineered Features:**
| Feature | Description | Business Logic |
|---------|-------------|----------------|
| `is_weekend` | Saturday/Sunday flag | Fraud rate 3.5x higher on weekends |
| `is_high_value` | Amount > $500 | High-value transactions show 5.1% fraud |
| `is_new_customer` | <30 days since signup | New customers 1.5x more likely to commit fraud |
| `days_since_signup` | Account age in days | Fraud risk decreases with account maturity |
| `shipping_billing_mismatch` | Address mismatch flag | Common fraud indicator |

---

### 2. Exploratory Data Analysis (`02_exploratory_analysis.ipynb`)

**Key Analyses:**
- Revenue trends by month (Oct: $1.85M, Nov: $2.10M, Dec: $2.45M)
- Fraud rate by acquisition channel
- Weekend vs weekday fraud patterns
- Transaction amount distribution
- Correlation analysis of fraud risk factors

**Key Visualizations:**
- Time series: Daily revenue and fraud count
- Bar charts: Fraud rate by channel, device type, payment method
- Heatmap: Feature correlation matrix
- Box plots: Amount distribution by fraud status

---

### 3. Machine Learning Model (`03_fraud_detection_model.ipynb`)

**Model:** XGBoost Classifier with class imbalance handling

**Features Used:**
```python
features = [
    'amount',
    'is_weekend',
    'is_high_value',
    'is_new_customer',
    'days_since_signup',
    'shipping_billing_mismatch'
]
```

**Training Configuration:**
- Train/Test Split: 80/20 (stratified)
- Class Weighting: scale_pos_weight = 17.77 (to handle imbalance)
- Feature Scaling: StandardScaler
- Random State: 42 (for reproducibility)

**Model Outputs:**
- `fraud_model.pkl` - Trained XGBoost classifier
- `scaler.pkl` - StandardScaler for feature normalization
- `fraud_flagged.csv` - Full dataset with predictions

**Performance Metrics:**

*Test Set (2,817 transactions):*
```
Accuracy:  89.2%
Precision: 11.1%
Recall:    41.3%
F1-Score:  17.5%
AUC-ROC:   0.73
```

*Full Dataset (14,082 transactions):*
```
Accuracy:  80.0%
Precision: 17.3%
Recall:    74.0%
F1-Score:  28.1%

Fraud Detected: 555/750 actual fraud cases
False Positives: 2,643 transactions flagged
```

**Business Impact:**
```
Average Fraud Value: $661.87
Review Cost per Transaction: $25.00

Test Set Performance:
- Fraud Caught: $41,036 (62 transactions)
- Review Cost: $12,425 (559 flagged transactions)
- Net Savings: $28,611

Projected Quarterly Savings: $143,026
Projected Annual Savings: $572,104
```

---

## 🎨 Visualizations

### Executive Dashboard

![Executive Dashboard](Payflow/execSum.png)

**KPIs Tracked:**
- Total Revenue: $6.4M
- Total Transactions: 14,082
- Fraud Rate: 7.03%
- Fraud Amount: $496K
- Average Order Value: $454
- Top Channel: Organic (30.2%)

### Fraud Risk Analysis

![Fraud Analysis](Payflow/fraudRisk.png)

**Insights:**
- Weekend fraud spike visualization
- Channel-specific fraud rates
- High-value transaction risk profile
- Time series fraud patterns

---

## 💾 Database Schema

### Tables

#### `products`
```sql
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2)
);
```

#### `customers`
```sql
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
```

#### `transactions`
```sql
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
```

#### `fraud_flagged`
```sql
CREATE TABLE fraud_flagged (
    -- All fields from transactions table
    -- Plus ML predictions:
    fraud_prediction INTEGER,      -- 0 or 1
    fraud_probability DECIMAL(5, 4) -- 0.0000 to 1.0000
);
```

### Indexes
```sql
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(order_date);
CREATE INDEX idx_transactions_fraud ON transactions(is_fraud);
CREATE INDEX idx_ff_prediction ON fraud_flagged(fraud_prediction);
```

---

## 🔬 Methodology

### Data Generation

This project uses **synthetic transaction data** designed to simulate realistic e-commerce fraud patterns.

**Key Characteristics:**
- **Seasonal trends:** Q4 holiday surge with Black Friday (3x) and Cyber Monday (2.5x) spikes
- **Fraud patterns:** Weekend fraud 3.2x higher, high-value transactions 5.1% fraud rate
- **Data quality issues:** Intentional nulls, duplicates, and formatting inconsistencies
- **Volume:** 14,082 transactions across 10,000 customers and 500 products

**Fraud Injection Logic:**
```python
# Base fraud rate: 2.1%
fraud_probability = 0.021

# Risk factors
if amount > 500:
    fraud_probability = 0.051  # 5.1% for high-value
if is_weekend:
    fraud_probability *= 3.2   # 3.2x on weekends
if is_new_customer:
    fraud_probability *= 1.5   # 1.5x for new accounts
```

### Model Selection

**Why XGBoost?**
- Handles class imbalance well with `scale_pos_weight`
- Feature importance built-in for business interpretation
- Fast training on tabular data
- Robust to missing values and outliers

**Alternative Models Considered:**
- Logistic Regression: Too simple for non-linear fraud patterns
- Random Forest: Good, but XGBoost typically outperforms
- Neural Networks: Overkill for this dataset size

---

## 📊 SQL Analytical Queries

Sample queries from `postgres/analysis_queries.sql`:

### Revenue by Channel with Fraud Rate
```sql
SELECT 
    acquisition_channel,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) as fraud_orders,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fraud_flagged
WHERE order_date BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY acquisition_channel
ORDER BY total_revenue DESC;
```

### Weekend vs Weekday Fraud Comparison
```sql
SELECT 
    CASE 
        WHEN EXTRACT(DOW FROM order_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fraud_flagged
GROUP BY day_type;
```

---

## 🐛 Troubleshooting

### Common Issues

#### Error: "DB_PASSWORD not set in .env file"
**Solution:** Create a `.env` file (not `.env.example`) with your actual password
```bash
DB_PASSWORD=your_actual_password
```

#### Error: "Connection failed"
**Possible causes:**
1. PostgreSQL is not running
   - **Fix:** Start PostgreSQL service
2. Wrong credentials in .env
   - **Fix:** Verify `DB_USER` and `DB_PASSWORD`
3. Database doesn't exist
   - **Fix:** Run `psql -U postgres -c 'CREATE DATABASE payflow_commerce;'`

#### Error: "ModuleNotFoundError"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

#### Power BI Dashboard Not Refreshing
**Solution:** 
1. Close Power BI Desktop completely
2. Delete `powerbi/dashboard.pbix.tmp` if it exists
3. Reopen Power BI and refresh data source

#### Jupyter Notebook Kernel Dies
**Solution:**
```bash
# Recreate virtual environment
deactivate
rm -rf venv/
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 📚 Project Deliverables

### ✅ Completed

- [x] **50,000+ synthetic transactions** generated with realistic fraud patterns
- [x] **PostgreSQL database** with 3 tables, indexes, and analytical views
- [x] **3 Jupyter notebooks** (data cleaning, EDA, ML modeling)
- [x] **XGBoost fraud detection model** achieving 89% accuracy on test set
- [x] **Feature engineering** with 5 risk indicators
- [x] **SQL analytical queries** for business intelligence
- [x] **Automated database setup** script with error handling
- [x] **Business impact analysis** with ROI calculations
- [x] **GitHub-ready documentation**

### 📁 Not Included in Repository (Large Files)

- `data/raw/*.csv` - 14k+ rows of synthetic data
- `data/processed/*.csv` - Cleaned and feature-engineered datasets
- `output/fraud_model.pkl` - Trained XGBoost model (~2MB)
- `excel/financial_model.xlsx` - 3-statement financial model
- `powerbi/dashboard.pbix` - Interactive Power BI dashboard

*These files are generated by following the setup instructions and running the notebooks.*

---

## 🎯 Use Cases

This project demonstrates capabilities for:

### Financial Analyst Roles
- 3-statement financial modeling (Income Statement, Balance Sheet, Cash Flow)
- Variance analysis (Actual vs Budget)
- ROI and business impact calculations
- Financial risk assessment

### Data Analyst Roles
- SQL query writing and optimization
- Data cleaning and ETL pipelines
- Exploratory data analysis
- Data visualization with Power BI

### Risk/Fraud Analyst Roles
- Fraud pattern detection and analysis
- Risk factor identification
- Model performance evaluation
- Operational impact assessment

### Business Intelligence Analyst Roles
- Dashboard design and development
- KPI tracking and reporting
- Database design and management
- End-to-end analytics pipeline

---

## 🔗 Connect

**Grant Gamble**  
Billing Specialist | Data Science Student  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/xgrantgamble)
[![Twitter](https://img.shields.io/badge/X-000000?style=flat&logo=x&logoColor=white)](https://x.com/xgrantgamble)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:grantgamble1122@gmail.com)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Faker** library for realistic synthetic data generation
- **XGBoost** team for the excellent gradient boosting framework
- **PostgreSQL** community for robust database engine
- **Scikit-Learn** for comprehensive ML toolkit

---

## 📊 Project Stats

![Python](https://img.shields.io/badge/Code-Python-blue?style=flat&logo=python)
![SQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat&logo=postgresql)
![Jupyter](https://img.shields.io/badge/Notebooks-Jupyter-orange?style=flat&logo=jupyter)
![Lines of Code](https://img.shields.io/badge/Lines_of_Code-2000+-green)
![Data Points](https://img.shields.io/badge/Data_Points-14K+-purple)

**Last Updated:** February 2026  
**Version:** 1.0.0
```

## Data Source Disclosure
This project uses synthetic transaction data designed to simulate realistic e-commerce fraud patterns, seasonal trends, and data quality issues commonly found in production systems.

Data was generated using Python (Faker, NumPy) to ensure:

Realistic fraud patterns: Weekend spikes, high-value transaction risk, and category-specific targeting.

Seasonal trends: Modeled Q4 holiday surge and Black Friday volume spikes.

Data quality challenges: Intentionally introduced nulls, duplicates, and formatting inconsistencies to test ETL robustness.

---

Grant Gamble  

Role: Data Analyst / Financial Analyst  

LinkedIn: [xgrantgamble](linkedin.com/in/xgrantgamble)  
X: [xgrantgamble](x.com/xgrantgamble)  
Email: grantgamble1122@gmail.com  
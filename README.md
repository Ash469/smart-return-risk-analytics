# Smart Return Risk Analytics System

**Advanced E-Commerce Return Prediction & Fraud Detection Platform**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

##  Project Overview

An end-to-end intelligent system that predicts product return probability, identifies fraudulent return behavior, and optimizes refund workflows for e-commerce platforms.

**Key Capabilities:**
-  Return probability prediction
-  Anomaly detection for fraud patterns
-  Customer risk segmentation
-  Explainable AI with SHAP values
-  Interactive risk analytics dashboard

---

##  Architecture

```
CSV Data → SQLite → Feature Engineering → ML Models → Risk Scoring → Dashboard
```

---

##  Project Structure

```
smart-return-risk-analytics/
├── data/                  # All datasets
├── sql/                   # SQL analytics layer
├── notebooks/             # Jupyter notebooks
├── src/                   # Python modules
├── dashboard/             # Streamlit app
├── models/                # Trained models
└── outputs/               # Results & visualizations
```

---

##  Quick Start

### 1. Clone Repository
```bash
git clone 
cd smart-return-risk-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python src/db_setup.py
```

### 4. Run Analysis
```bash
jupyter notebook notebooks/01_initial_data_exploration.ipynb
```

### 5. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

---

##  Dataset

**Source:** Brazilian E-Commerce Public Dataset by Olist  
**Link:** [Kaggle - Olist Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Dataset Includes:**
- 100k+ orders from 2016-2018
- Customer demographics
- Product categories
- Review scores
- Delivery information

**Note:** Return flags are synthetically engineered using domain research and industry benchmarks.

---

##  Tech Stack

**Data Processing:** Pandas, NumPy, SQLite  
**Machine Learning:** Scikit-learn, XGBoost, LightGBM  
**Imbalance Handling:** SMOTE, Class Weights  
**Explainability:** SHAP  
**Visualization:** Matplotlib, Seaborn, Plotly  
**Dashboard:** Streamlit  
**Version Control:** Git

---

##  Key Features

### SQL Analytics Layer
- Customer behavior aggregations
- Product return propensity analysis
- Temporal pattern detection
- Risk segmentation

### Machine Learning Pipeline
- Binary classification (Return / No Return)
- Customer risk scoring (0-100)
- Anomaly detection for fraud
- Model explainability with SHAP

### Business Intelligence
- Cost-savings simulation
- Precision-recall optimization
- Operational recommendations

---

##  Learning Outcomes

This project demonstrates:

✅ Real-world problem-solving  
✅ SQL-first analytics approach  
✅ Feature engineering creativity  
✅ Handling imbalanced datasets  
✅ Model explainability  
✅ Business metrics focus  
✅ End-to-end ML pipeline  

---

##  Project Workflow

1. **Data Acquisition** → Download Olist dataset
2. **SQL Setup** → Load CSVs into SQLite
3. **Feature Engineering** → SQL + Python features
4. **Return Simulation** → Engineer target variable
5. **Model Training** → Train multiple classifiers
6. **Evaluation** → Business + technical metrics
7. **Dashboard** → Interactive risk analytics

---

##  Results

*(To be filled after completion)*

- **Model Performance:** ROC-AUC, Precision, Recall
- **Business Impact:** Estimated cost savings
- **Risk Detection:** Fraud interception rate

---

##  Author

**Ayush Shandilya**  
Data Science Enthusiast | ML Engineer  
[ashshandilya4@gmail.com](mailto:ashshandilya4@gmail.com)  
[LinkedIn](https://www.linkedin.com/in/ayush-ranjan-9928192a9) | [GitHub](https://github.com/ash469)

---



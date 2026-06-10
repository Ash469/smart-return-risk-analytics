# Python Feature Engineering


This document outlines the exact transformations applied to the SQL outputs before they are passed into ML pipelines.

## 1. Data Merging & Grouping

The notebook begins by loading the three primary outputs from the SQL pipeline:
- `order_features_with_returns.csv`
- `customer_features.csv`
- `product_features.csv`

**Category Risk Aggregation:** 
To prevent the model from overfitting on sparse product IDs, the notebook aggregates product-level metrics up to the `product_category_name` level. It calculates mean complaint rates and dissatisfaction rates for each category, which are then merged back into the main dataset.

## 2. Temporal Engineering

Machine Learning models cannot natively process string timestamps like `2017-10-02 10:56:33`. 
The `order_purchase_timestamp` is converted into cyclic integers to capture seasonal and weekly trends:
- `purchase_month` (1-12)
- `purchase_day_of_week` (0-6)

## 3. Data Leakage Prevention & Dimensionality Reduction

To ensure the models learn generalized patterns rather than cheating by memorizing identifiers or proxy variables, several columns are explicitly dropped:

**Identifiers (Overfitting Risk):**
- `order_id`, `customer_unique_id`, `product_id`

**Raw Timestamps:**
- `order_purchase_timestamp`, `last_order_date`, `first_order_date`

**Leakage Flags:**
- `return_probability_score` (The exact continuous probability used to generate the labels. Including this would yield 100% fake accuracy).
- `is_unhappy_customer`, `frequent_late_deliveries` (Redundant binary flags that cause multicollinearity).

## 4. Categorical Encoding

This is the most critical step in establishing our Model Performance Ladder.

- **Ordinal Variables:** `price_segment` ('low', 'medium', 'high') is mapped cleanly to `0, 1, 2` because it has a strict mathematical order.
- **High-Cardinality Strings:** `product_category`, `customer_state`, and `customer_city` are transformed using Pandas' `.cat.codes()`. 

**Why `.cat.codes()`?**
By mapping states like 'SP' to `25` and 'RJ' to `15`, we represent them as single, arbitrary integer columns rather than One-Hot Encoded matrices. 
- **Logistic Regression** treats these integers as continuous numbers, attempting to draw a straight line through arbitrarily sorted categories. It completely fails to extract the underlying state/category risk.
- **Tree-Based Models (XGBoost, Random Forest)** simply use these integers as branching thresholds (e.g., `if state_code < 16`), effortlessly isolating the high-risk categories we injected during the SQL simulation phase.

## 5. Interaction Feature Injection

Finally, two mathematical interaction features are manually injected to help linear models marginally improve their  compounding risks:
- `delay_freight_cross` = `delivery_delay_days * freight_ratio`
- `review_delay_cross` = `review_score * delivery_delay_days`

The final processed data is saved as `ml_ready_dataset.csv` in the `data/final/` directory.

# The Model Performance Ladder

This directory contains the machine learning pipelines used to predict e-commerce return risks. Our strategy focuses on a progressive "Ladder" approach, where we start with a simple, interpretable linear model and incrementally step up to complex ensembles, analyzing the mathematical flaws and victories at every stage.

## The Progression

We evaluated our models primarily on **ROC-AUC** and **Recall** at specific business thresholds

| Model | ROC-AUC | Key Business Takeaway |
| :--- | :--- | :--- |
| **1. Logistic Regression** | `0.8968` | Strong baseline, but mathematically blind to our label-encoded categorical risks. |
| **2. Decision Tree (Optimized)** | `0.9109` | Successfully extracted hidden geographical and category risks, but highly unstable. |
| **3. Random Forest** | `0.9141` | Solved tree instability via bagging, but suffered from poor probability calibration. |
| **4. XGBoost (The Champion)** | `0.9179` | Perfect probability calibration. Caught 89% of returns at an aggressive 35% cutoff. |

---

##  Model Breakdowns & Insights

### 1. Logistic Regression (`01_logistic_regression.ipynb`)
- **The Baseline:** Provided a fast, explainable baseline achieving nearly 90% ROC-AUC.
- **The Flaw (Categoricals):** We deliberately label-encoded categorical variables (like `customer_state` and `product_category`) into arbitrary integers. Logistic Regression applied linear weights to these arbitrary numbers (assuming state `25` is inherently "higher" than state `15`), rendering it completely blind to the geographical risks we engineered.
- **The Flaw (Multicollinearity):** It was confused by highly correlated features (like `review_score` and `avg_review_score`), forcing it to arbitrarily flip signs and making the coefficients unstable.

### 2. Decision Tree (`02_decision_tree.ipynb`)
- **The Overfitting Trap:** Our unconstrained tree grew to 61 levels deep and achieved 99.96% training accuracy, memorizing individual noise. Constraining `max_depth` to 8 and `min_samples_leaf` to 50 fixed this.
- **The Categorical Victory:** The Decision Tree effortlessly branched on specific integer codes, elevating `customer_state` to the 3rd most important feature in the entire dataset. It captured the exact risk signals that Logistic Regression missed.

### 3. Random Forest (`03_random_forest.ipynb`)
- **Fixing the Staircase:** A single tree draws rigid, harsh threshold steps. By averaging 150 different trees, Random Forest smoothed out the probability curve and vastly improved Testing Accuracy.
- **The Calibration Flaw:** Because we used `class_weight='balanced'` to punish minority class mistakes, the Random Forest aggressively over-predicted risk. A probability calibration curve proved that when the model outputted a "90% risk", the actual real-world risk was often much lower. 

### 4. XGBoost (`04_xgboost.ipynb`)
- **The Final Boss:** XGBoost trains *sequentially* using Gradient Descent, optimizing a logistical loss function. This allowed it to draw beautiful, perfectly calibrated probability curves that Random Forest couldn't achieve.
- **Bayesian Optimization:** Using Optuna, we discovered that XGBoost only needed incredibly shallow trees (`max_depth: 3`) because it relies on hundreds of smart, small corrections rather than deep logic.
- **Business Application:** We shifted the classification threshold from the default 50% down to a highly aggressive **35%**. Because the financial cost of a missed return is so high, this aggressive threshold allowed XGBoost to intercept a staggering **89%** of all real-world returns.

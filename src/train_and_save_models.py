import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline as ImbPipeline

def train_and_save():
    print("Loading data...")
    # 1. Load Data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'final', 'ml_ready_dataset.csv')
    df = pd.read_csv(data_path)
    
    # Target and Features
    y = df['is_returned']
    X = df.select_dtypes(exclude=['object', 'string']).drop(columns=['is_returned'], errors='ignore')
    
    # Save the feature columns so the dashboard knows the exact order
    feature_cols = X.columns.tolist()
    
    print("Calculating feature medians...")
    # Save medians for the dashboard baseline
    medians = X.median().to_dict()
    joblib.dump(medians, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'feature_medians.pkl'))
    joblib.dump(feature_cols, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'feature_columns.pkl'))
    
    print("Training Logistic Regression...")
    # LR needs scaling. We'll use a pipeline.
    lr_model = ImbPipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(C=1.0, penalty='l2', class_weight='balanced', random_state=42, max_iter=1000))
    ])
    lr_model.fit(X, y)
    joblib.dump(lr_model, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'lr_model.pkl'))
    
    print("Training Decision Tree...")
    dt_model = DecisionTreeClassifier(class_weight='balanced', max_depth=8, min_samples_leaf=50, min_samples_split=20, random_state=42)
    dt_model.fit(X, y)
    joblib.dump(dt_model, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'dt_model.pkl'))
    
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(class_weight='balanced', max_depth=10, min_samples_split=50, n_estimators=150, random_state=42, n_jobs=-1)
    rf_model.fit(X, y)
    joblib.dump(rf_model, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'rf_model.pkl'))
    
    print("Training XGBoost...")
    scale_pos_weight = (y == 0).sum() / (y == 1).sum()
    xgb_model = xgb.XGBClassifier(
        max_depth=3, 
        learning_rate=0.119, 
        subsample=0.973, 
        colsample_bytree=0.793, 
        n_estimators=139, 
        scale_pos_weight=scale_pos_weight,
        eval_metric='auc',
        random_state=42
    )
    xgb_model.fit(X, y)
    joblib.dump(xgb_model, os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'models', 'xgb_model.pkl'))
    
    print("All models successfully trained and exported to dashboard/models/ directory!")

if __name__ == "__main__":
    train_and_save()

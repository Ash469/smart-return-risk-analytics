import streamlit as st
import pandas as pd
import joblib
import os

@st.cache_resource
def load_assets():
    base_dir = os.path.join(os.path.dirname(__file__), 'models')
    models = {
        "Logistic Regression": joblib.load(os.path.join(base_dir, "lr_model.pkl")),
        "Decision Tree": joblib.load(os.path.join(base_dir, "dt_model.pkl")),
        "Random Forest": joblib.load(os.path.join(base_dir, "rf_model.pkl")),
        "XGBoost": joblib.load(os.path.join(base_dir, "xgb_model.pkl")),
    }
    medians = joblib.load(os.path.join(base_dir, "feature_medians.pkl"))
    cols = joblib.load(os.path.join(base_dir, "feature_columns.pkl"))
    
    # Load dataset for historical analytics
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'final', 'ml_ready_dataset.csv')
    df = pd.read_csv(data_path)
    
    return models, medians, cols, df

# Mappings
STATE_MAP = {f"State Name {i}": i for i in range(27)}
CITY_MAP = {f"City Name {i}": i for i in range(4085)}

def get_risk(models_dict, model_name, input_data):
    m = models_dict[model_name]
    return m.predict_proba(input_data)[0][1]

def build_customer_df(medians, feature_cols, review_score, delivery_delay_days, freight_ratio, state_name, city_name, advanced_overrides=None):
    data = medians.copy()
    data['review_score'] = review_score
    data['avg_review_score'] = review_score
    data['delivery_delay_days'] = delivery_delay_days
    data['is_late_delivery'] = 1 if delivery_delay_days > 0 else 0
    data['freight_ratio'] = freight_ratio
    data['customer_state'] = STATE_MAP.get(state_name, 25)
    data['customer_city'] = CITY_MAP.get(city_name, 1000)
    
    if advanced_overrides:
        for k, v in advanced_overrides.items():
            data[k] = v
            
    return pd.DataFrame([data])[feature_cols]

def sidebar_settings(models):
    st.sidebar.header("Global Settings")
    selected_model_name = st.sidebar.selectbox("Select AI Model", list(models.keys()), index=3)
    
    risk_threshold = st.sidebar.slider(
        "Interception Threshold (%)", 
        min_value=1, max_value=99, value=35, 
        help="If predicted risk exceeds this %, flag as RETURN."
    ) / 100.0
    return selected_model_name, risk_threshold

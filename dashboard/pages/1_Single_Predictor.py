import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import shap
import sys
import os

# Add the dashboard directory to the path so we can import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import load_assets, STATE_MAP, CITY_MAP, get_risk, build_customer_df, sidebar_settings

st.set_page_config(page_title="Single Predictor", layout="wide")

models, medians, feature_cols, _ = load_assets()
selected_model_name, risk_threshold = sidebar_settings(models)
selected_model = models[selected_model_name]

st.title("Single Order Predictor & Explainer")
st.markdown("Evaluate a single customer's return risk in real-time.")

col_input, col_results = st.columns([1, 2])

with col_input:
    st.subheader("Customer Scenario")
    review_score = st.slider("Review Score", 1.0, 5.0, 3.0, step=1.0)
    delivery_delay_days = st.number_input("Delivery Delay (Days)", min_value=-15, max_value=30, value=0)
    freight_ratio = st.slider("Freight to Value Ratio", 0.0, 1.0, 0.15, step=0.01)
    selected_state = st.selectbox("Customer State", list(STATE_MAP.keys()), index=25)
    selected_city = st.selectbox("Customer City", list(CITY_MAP.keys()), index=1000)
    
    advanced_inputs = {}
    with st.expander("Advanced / All Features"):
        st.markdown("Override background features:")
        for col in feature_cols:
            if col in ['review_score', 'delivery_delay_days', 'freight_ratio', 'avg_review_score', 'is_late_delivery', 'customer_state', 'customer_city']:
                continue
            default_val = medians.get(col, 0)
            if col == 'num_items' or 'count' in col or 'orders' in col or 'days' in col:
                advanced_inputs[col] = st.number_input(f"{col}", value=int(default_val), step=1, key=f"adv1_{col}")
            else:
                advanced_inputs[col] = st.number_input(f"{col}", value=float(default_val), key=f"adv1_{col}")

input_df = build_customer_df(medians, feature_cols, review_score, delivery_delay_days, freight_ratio, selected_state, selected_city, advanced_inputs)
current_risk = get_risk(models, selected_model_name, input_df)

with col_results:
    st.subheader("Action Recommendation Engine")
    is_return = current_risk >= risk_threshold
    
    # Action Engine Logic
    if current_risk < risk_threshold:
        st.success(f"**Action: Fulfill Normally** | Risk: {current_risk*100:.1f}%")
    elif current_risk < risk_threshold + 0.25:
        st.warning(f"**Action: Send Preemptive Discount** | Risk: {current_risk*100:.1f}%")
        st.markdown("*Suggestion: Send a 10% coupon apologizing for shipping issues to save the sale.*")
    else:
        st.error(f"**Action: Hold Shipment & Call Customer** | Risk: {current_risk*100:.1f}%")
        st.markdown("*Suggestion: The risk is critically high. Verify customer intent before wasting freight costs.*")
        
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_risk * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "red" if is_return else "green"},
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': risk_threshold * 100}
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_gauge, width="stretch")
    
    st.subheader("Model Explainer: Why did the AI choose this?")
    try:
        if selected_model_name in ["XGBoost", "Random Forest", "Decision Tree"]:
            explainer = shap.TreeExplainer(selected_model)
            shap_values = explainer(input_df)
            
            if len(shap_values.values.shape) == 3: # RF
                 vals = shap_values.values[0, :, 1]
            else:
                 vals = shap_values.values[0] # XGBoost
                 
            shap_df = pd.DataFrame({'Feature': feature_cols, 'SHAP Impact': vals})
            shap_df['Absolute Impact'] = shap_df['SHAP Impact'].abs()
            shap_df = shap_df.sort_values(by='Absolute Impact', ascending=False).head(8)
            
            fig_shap = px.bar(
                shap_df, x='SHAP Impact', y='Feature', orientation='h',
                color='SHAP Impact', color_continuous_scale=px.colors.diverging.RdYlGn_r
            )
            fig_shap.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_shap, width="stretch")
        else:
            st.info("SHAP Explainer is only available for Tree-based models (XGBoost, Random Forest, Decision Tree).")
    except Exception as e:
        st.error(f"Could not generate SHAP explanation: {e}")

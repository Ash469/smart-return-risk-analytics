import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import load_assets, STATE_MAP, CITY_MAP, get_risk, build_customer_df, sidebar_settings

st.set_page_config(page_title="What-If Simulator", layout="wide")

models, medians, feature_cols, _ = load_assets()
selected_model_name, risk_threshold = sidebar_settings(models)

st.title("What-If Scenario Simulator")
st.markdown("Compare two different interventions side-by-side to see if a business action will save the sale.")

colA, colB = st.columns(2)

with colA:
    st.subheader("Scenario A: Current State")
    revA = st.slider("Review Score (A)", 1.0, 5.0, 3.0, step=1.0, key="revA")
    delA = st.number_input("Delivery Delay (A)", value=5, key="delA")
    freA = st.slider("Freight Ratio (A)", 0.0, 1.0, 0.20, step=0.01, key="freA")
    dfA = build_customer_df(medians, feature_cols, revA, delA, freA, list(STATE_MAP.keys())[25], list(CITY_MAP.keys())[1000])
    riskA = get_risk(models, selected_model_name, dfA)
    st.metric("Scenario A Risk", f"{riskA*100:.1f}%")
    
with colB:
    st.subheader("Scenario B: Expedited Shipping")
    revB = st.slider("Review Score (B)", 1.0, 5.0, 3.0, step=1.0, key="revB")
    delB = st.number_input("Delivery Delay (B)", value=-2, key="delB")
    freB = st.slider("Freight Ratio (B)", 0.0, 1.0, 0.35, step=0.01, key="freB")
    dfB = build_customer_df(medians, feature_cols, revB, delB, freB, list(STATE_MAP.keys())[25], list(CITY_MAP.keys())[1000])
    riskB = get_risk(models, selected_model_name, dfB)
    
    diff = (riskB - riskA) * 100
    st.metric("Scenario B Risk", f"{riskB*100:.1f}%", delta=f"{diff:.1f}% risk reduction", delta_color="inverse")
    
st.markdown("---")
st.subheader("Business Impact")
if riskA >= risk_threshold and riskB < risk_threshold:
    st.success("💰 **Excellent!** The intervention in Scenario B successfully drops the risk below your threshold. Action recommended!")
elif riskA >= risk_threshold and riskB >= risk_threshold:
    st.error("🛑 **Do not intervene.** Even after the intervention in Scenario B, the risk is STILL above your threshold. Save the money and accept the return.")
else:
    st.info("Both scenarios are safe. No urgent intervention needed.")

import streamlit as st

st.set_page_config(page_title="Smart Return Risk Analytics", layout="wide", initial_sidebar_state="expanded")

st.title("Smart Return Risk Analytics Dashboard")
st.markdown("""
Welcome to the AI-powered Return Risk Predictor. This enterprise dashboard connects directly to our advanced machine learning models to help you intercept high-risk e-commerce orders.

### Please select a tool from the sidebar to begin:

- **Single Order Predictor:** Analyze a single customer in real-time. View action recommendations and SHAP explanations for *why* the model made its decision.
- **What-If Simulator:** Side-by-side scenario simulation. Will upgrading shipping save the sale?
- **Historical Analytics:** Macro-level insights into how delivery delays and review scores impact our overall return rates.
""")
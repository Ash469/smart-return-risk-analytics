import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import load_assets

st.set_page_config(page_title="Historical Analytics", layout="wide")

_, _, _, historical_df = load_assets()

st.title("Historical Analytics")
st.markdown("Macro-level insights across the entire e-commerce dataset.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Return Rate by Review Score")
    agg1 = historical_df.groupby('review_score')['is_returned'].mean().reset_index()
    fig1 = px.bar(agg1, x='review_score', y='is_returned', labels={'is_returned': 'Return Rate', 'review_score': 'Review Score'})
    fig1.update_layout(yaxis_tickformat='.1%')
    st.plotly_chart(fig1, use_container_width=True)
    
with col2:
    st.subheader("Return Rate by Delivery Delay")
    # Bin the delays
    historical_df['Delay Bin'] = pd.cut(historical_df['delivery_delay_days'], bins=[-np.inf, -5, 0, 5, 10, 20, np.inf], labels=['Early >5d', 'Early 0-5d', 'Late 0-5d', 'Late 5-10d', 'Late 10-20d', 'Late >20d'])
    agg2 = historical_df.groupby('Delay Bin')['is_returned'].mean().reset_index()
    fig2 = px.line(agg2, x='Delay Bin', y='is_returned', markers=True, labels={'is_returned': 'Return Rate'})
    fig2.update_layout(yaxis_tickformat='.1%')
    st.plotly_chart(fig2, use_container_width=True)

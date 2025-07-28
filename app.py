import streamlit as st
from modules.customer_insights.customer_insights import run_customer_insights

st.set_page_config(page_title="Customer Insights", layout="wide")

# Run directly without any sidebar or selection
run_customer_insights()

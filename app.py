import streamlit as st
from modules.customer_360 import run as run_customer_360
from modules.customer_insights.customer_insights import run_customer_insights

st.set_page_config(page_title="Customer 360", layout="wide")

st.sidebar.title("🏠 Navigation")
selected = st.sidebar.radio("Navigate", [
    "Customer 360 View",
    "Customer Insights"
])

if selected == "Customer 360 View":
    run_customer_360()

elif selected == "Customer Insights":
    run_customer_insights()

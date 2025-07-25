
import streamlit as st
from modules.customer_360 import run as run_customer_360

st.set_page_config(page_title="Customer 360", layout="wide")

st.sidebar.title("Modules")
selected = st.sidebar.radio("Navigate", ["Customer 360 View"])

if selected == "Customer 360 View":
    run_customer_360()

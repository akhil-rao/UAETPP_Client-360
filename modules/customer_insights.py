import streamlit as st
import pandas as pd

def run_customer_insights():
    st.set_page_config(page_title="Customer Insights - Ahmed Hassan", layout="wide")
    st.title("👤 Customer Insights: Ahmed Hassan")

    # --- Top Row: Customer Profile ---
    st.markdown("### 🧾 Profile Summary")
    col1, col2, col3 = st.columns([1.5, 3, 2])

    with col1:
        st.image("https://via.placeholder.com/100", caption="Ahmed Hassan", width=100)
        st.markdown("**Date of Birth:** 4/12/1980")
        st.markdown("**Nationality:** UAE")

    with col2:
        st.metric("Relationship Score", "85")
        st.metric("Status", "Active")
        st.metric("Segment", "ACG")

    with col3:
        st.markdown("**Verified:** ✅")
        st.metric("Risk Level", "Low")
        st.markdown("**Open Finance Tag:** ✅")

    st.markdown("---")

    # --- Account Summary Section ---
    st.markdown("### 💳 Account Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Savings")
        st.metric("AED", "243,112")
        st.metric("USD", "$76,748")

    with col2:
        st.subheader("Mortgages")
        st.markdown("**Outstanding:** AED 1,20,000")
        st.markdown("**Loan Term:** 20 years")
        st.markdown("**EMI Rate:** 3.5%")
        st.markdown("**Next Payment:** AED 7,800 (3 May 2024)")

    with col3:
        st.subheader("Wealth Management")
        st.markdown("**Total:** AED 500,000")
        st.progress(0.46, text="46% Allocated")
        st.markdown("- 20% Internal\n- 49% Pencs")

    st.markdown("---")

    # --- Credit Score + Risk Signals ---
    st.markdown("### 📊 Credit Score & Risk Signals")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Open Finance Enhanced Credit Score")
        st.markdown("- ⭐⭐⭐⭐⭐ Income Stability (95/100)")
        st.markdown("- ⭐⭐⭐⭐ Payment Behavior (92/100)")
        st.markdown("- ⭐⭐⭐ Credit Management (78/100)")
        st.markdown("- ⭐⭐⭐⭐ Financial Resilience (88/100)")

    with col2:
        st.markdown("#### Risk Signals")
        st.success("✅ Consistent savings behavior")
        st.success("✅ Regular investment contributions")
        st.success("✅ Premium insurance policy payments")
        st.warning("⚠️ Increased entertainment spending")

    st.markdown("#### 🔍 Recommendations")
    st.markdown("""
    1. Personal loan / credit facilities (high approval probability)  
    2. Investment products (repeat demonstrated behavior every Sept)  
    3. Premium credit card upgrade
    """)

    st.markdown("---")

    # --- Wallet Share and Insights ---
    st.markdown("### 🧠 Wallet Share Analysis & Insights")
    st.markdown("**Primary Bank:** Emirates NBD (60%)")
    st.markdown("**Secondary:** ADCB (25%), FAB (12%)")

    st.markdown("#### 🔎 Insights")
    st.markdown("""
    - Strong financial discipline & planning  
    - Loyalty to financial service providers  
    - Low risk of credit migration  
    - High potential for cross-selling  
    """)

    st.markdown("**Predictive Risk Score:** 2.1% default probability (next 12 months)")
    st.markdown("**Recommended Credit Limit:** AED 250,000 (current: AED 150,000)")
    st.markdown("**Optimal Rate:** Prime + 1.5%")

    st.markdown("---")

    # --- Actions Section ---
    st.markdown("### 📝 RM Action Plan")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Immediate Actions (24–48h)")
        st.markdown("- Approve credit application with enhanced terms")
        st.markdown("- Prepare premium banking relationship pitch")
        st.markdown("- Schedule RM meeting for cross-selling")

    with col2:
        st.markdown("#### 📆 Medium-Term (1–3 months)")
        st.markdown("- Monitor spending pattern changes")
        st.markdown("- Proactive outreach for relationship pitch")
        st.markdown("- Review & increase credit facilities")

# Run directly for testing
if __name__ == "__main__":
    run_customer_insights()

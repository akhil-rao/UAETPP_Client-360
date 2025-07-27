import streamlit as st
import json
import os

def run_customer_insights():
    st.set_page_config(page_title="Customer Insights", layout="wide")
    st.title("👤 Customer Insights")

    # Load client data
    data_path = os.path.join("modules", "customer_insights", "data", "clients_data.json")
    with open(data_path, "r") as f:
        customers = json.load(f)

    # UAE ID dropdown (fixed with unique key)
    uae_ids = [cust.get("uae_id", f"Client-{i}") for i, cust in enumerate(customers)]
    selected_id = st.selectbox("Select UAE ID", uae_ids, key="customer_insights_uae_id")

    # Retrieve selected customer
    customer = next(c for c in customers if c.get("uae_id") == selected_id)
    profile = customer.get('profile', {})
    accounts = customer.get('accounts', {})
    credit = customer.get('credit_score', {})
    risk = customer.get('risk_signals', {})
    wallet = customer.get('wallet_share', {})
    insights = customer.get('insights', [])
    risk_data = customer.get('risk', {})
    actions = customer.get('actions', {})
    aum = customer.get('aum', {})

    # Avatar from randomuser.me
    gender = profile.get("gender", "male").lower()
    index = int(selected_id[:2], 16) % 100
    avatar_url = f"https://randomuser.me/api/portraits/{'women' if gender == 'female' else 'men'}/{index}.jpg"


    # --- Profile Section ---
    col1, col2, col3 = st.columns([1.5, 3, 2])
    with col1:
        st.image(avatar_url, width=100)
        st.markdown(f"**<span style='font-size: 22px'>{profile.get('name', 'Unknown')}</span>**", unsafe_allow_html=True)
        st.markdown(f"**Date of Birth:** {profile.get('dob', 'N/A')}")
        st.markdown(f"**Nationality:** {profile.get('nationality', 'N/A')}")
    with col2:
        st.metric("Relationship Score", profile.get("relationship_score", "N/A"))
        st.metric("Status", profile.get("status", "N/A"))
        st.metric("Segment", profile.get("segment", "N/A"))
    with col3:
        st.markdown("**Verified:** ✅" if profile.get("verified") else "❌")
        st.metric("Risk Level", profile.get("risk_level", "N/A"))
        st.markdown("**Open Finance Tag:** ✅")

    # --- Account Summary ---
    st.markdown("### 💳 Account Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Savings AED", f"AED {accounts.get('savings_aed', 0):,}")
        st.metric("Savings USD", f"${accounts.get('savings_usd', 0):,}")
    with col2:
        st.markdown(f"**Outstanding Mortgage:** AED {accounts.get('mortgage_outstanding', 'N/A'):,}")
        st.markdown(f"**Loan Term:** {accounts.get('loan_term_years', 'N/A')} years")
        st.markdown(f"**EMI Rate:** {accounts.get('emi_rate', 'N/A')}%")
        st.markdown(f"**Next Payment:** AED {accounts.get('next_payment_amount', 'N/A')} ({accounts.get('next_payment_date', 'N/A')})")
    with col3:
        st.markdown("**Total AUM:**")
        if "total" in aum:
            st.markdown(f"AED {aum.get('total', 0):,}")
            st.markdown(f"**Risk Alignment:** {aum.get('risk_alignment', 'N/A')}")
        else:
            st.markdown("_Not available_")

    # --- Credit Score & Risk Signals ---
    st.markdown("### 📊 Credit Score & Risk Signals")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- ⭐⭐⭐⭐⭐ Income Stability ({credit.get('income_stability', 0)}/100)")
        st.markdown(f"- ⭐⭐⭐⭐ Payment Behavior ({credit.get('payment_behavior', 0)}/100)")
        st.markdown(f"- ⭐⭐⭐ Credit Management ({credit.get('credit_management', 0)}/100)")
        st.markdown(f"- ⭐⭐⭐⭐ Financial Resilience ({credit.get('financial_resilience', 0)}/100)")
    with col2:
        for signal in risk.get('positive', []):
            st.success("✅ " + signal)
        for warning in risk.get('warnings', []):
            st.warning("⚠️ " + warning)

    # --- Recommendations ---
    st.markdown("### 🔍 Recommendations")
    for i, rec in enumerate(customer.get("recommendations", []), 1):
        st.markdown(f"{i}. {rec}")

    # --- Wallet Share ---
    st.markdown("### 🧠 Wallet Share Analysis")
    st.markdown(f"**Primary Bank:** {wallet.get('primary_bank', 'N/A')} ({wallet.get('primary_pct', 0)}% of transactions)")
    secondary = wallet.get("secondary_banks", {})
    secondary_line = " • ".join([f"{k} ({v}%)" for k, v in secondary.items()])
    st.markdown(f"**Secondary Accounts:** {secondary_line or 'N/A'}")

    # --- Insights ---
    st.markdown("### 🧩 Insights")
    for insight in insights:
        st.markdown("- " + insight)

    # --- Risk & Credit Info ---
    st.markdown("### 🔢 Risk & Credit Info")
    st.markdown(f"**Predictive Risk Score:** {risk_data.get('predictive_risk_score_pct', 'N/A')}%")
    st.markdown(f"**Recommended Credit Limit:** AED {risk_data.get('recommended_credit_limit', 0):,} (Current: AED {risk_data.get('current_applied_credit', 0):,})")
    st.markdown(f"**Optimal Interest Rate:** {risk_data.get('optimal_interest_rate', 'N/A')}")

    # --- Action Plan ---
    st.markdown("### 📝 Action Plan")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Immediate Actions (24–48h)**")
        for a in actions.get("immediate", []):
            st.markdown("- " + a)
    with col2:
        st.markdown("**Medium-Term (1–3 months)**")
        for a in actions.get("medium_term", []):
            st.markdown("- " + a)

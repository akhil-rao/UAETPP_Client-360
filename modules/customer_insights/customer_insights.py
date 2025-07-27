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

    # UAE ID dropdown
    uae_ids = [cust["uae_id"] for cust in customers]
    selected_id = st.selectbox("Select UAE ID", uae_ids)

    customer = next(c for c in customers if c["uae_id"] == selected_id)
    profile = customer['profile']
    accounts = customer['accounts']
    credit = customer['credit_score']
    risk = customer['risk_signals']
    wallet = customer['wallet_share']
    insights = customer['insights']
    risk_data = customer['risk']
    actions = customer['actions']

    # Generate realistic avatar using randomuser.me
    gender = "men" if int(selected_id[-1], 16) % 2 == 0 else "women"
    index = int(selected_id[:2], 16) % 100
    avatar_url = f"https://randomuser.me/api/portraits/{gender}/{index}.jpg"

    # --- Profile Section ---
    col1, col2, col3 = st.columns([1.5, 3, 2])
    with col1:
        st.image(avatar_url, caption=profile["name"], width=100)
        st.markdown(f"**Date of Birth:** {profile['dob']}")
        st.markdown(f"**Nationality:** {profile['nationality']}")
    with col2:
        st.metric("Relationship Score", profile["relationship_score"])
        st.metric("Status", profile["status"])
        st.metric("Segment", profile["segment"])
    with col3:
        st.markdown("**Verified:** ✅" if profile["verified"] else "❌")
        st.metric("Risk Level", profile["risk_level"])
        st.markdown("**Open Finance Tag:** ✅")

    st.markdown("### 💳 Account Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Savings AED", f"AED {accounts['savings_aed']:,}")
        st.metric("USD Equivalent", f"${accounts['savings_usd']:,}")
    with col2:
        st.markdown(f"**Outstanding Mortgage:** AED {accounts['mortgage_outstanding']:,}")
        st.markdown(f"**Loan Term:** {accounts['loan_term_years']} years")
        st.markdown(f"**EMI Rate:** {accounts['emi_rate']}%")
        st.markdown(f"**Next Payment:** AED {accounts['next_payment_amount']:,} ({accounts['next_payment_date']})")
    with col3:
        st.markdown(f"**Wealth Total:** AED {accounts['wealth_total']:,}")
        st.progress(accounts['wealth_allocation_percent'] / 100, text=f"{accounts['wealth_allocation_percent']}% Allocated")
        for k, v in accounts['wealth_allocations'].items():
            st.markdown(f"- {k.title()}: {v}%")

    st.markdown("### 📊 Credit Score & Risk Signals")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- ⭐⭐⭐⭐⭐ Income Stability ({credit['income_stability']}/100)")
        st.markdown(f"- ⭐⭐⭐⭐ Payment Behavior ({credit['payment_behavior']}/100)")
        st.markdown(f"- ⭐⭐⭐ Credit Management ({credit['credit_management']}/100)")
        st.markdown(f"- ⭐⭐⭐⭐ Financial Resilience ({credit['financial_resilience']}/100)")
    with col2:
        for signal in risk['positive']:
            st.success("✅ " + signal)
        for warning in risk['warnings']:
            st.warning("⚠️ " + warning)

    st.markdown("### 🔍 Recommendations")
    for i, rec in enumerate(customer["recommendations"], 1):
        st.markdown(f"{i}. {rec}")

    st.markdown("### 🧠 Wallet Share & Insights")
    st.markdown(f"**Primary Bank:** {wallet['primary_bank']} ({wallet['primary_pct']}%)")
    for bank, pct in wallet["secondary_banks"].items():
        st.markdown(f"**Secondary:** {bank} ({pct}%)")

    for insight in insights:
        st.markdown("- " + insight)

    st.markdown("### 🔢 Risk & Credit Info")
    st.markdown(f"**Predictive Risk Score:** {risk_data['predictive_risk_score_pct']}%")
    st.markdown(f"**Recommended Credit Limit:** AED {risk_data['recommended_credit_limit']:,} (Current: AED {risk_data['current_applied_credit']:,})")
    st.markdown(f"**Optimal Interest Rate:** {risk_data['optimal_interest_rate']}")

    st.markdown("### 📝 Action Plan")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Immediate Actions (24–48h)**")
        for a in actions["immediate"]:
            st.markdown("- " + a)
    with col2:
        st.markdown("**Medium-Term (1–3 months)**")
        for a in actions["medium_term"]:
            st.markdown("- " + a)

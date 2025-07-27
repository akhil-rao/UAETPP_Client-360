
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
    profile = customer.get('profile', {})
    accounts = customer.get('accounts', {})
    credit = customer.get('credit_score', {})
    risk = customer.get('risk_signals', {})
    wallet = customer.get('wallet_share', {})
    insights = customer.get('insights', [])
    risk_data = customer.get('risk', {})
    actions = customer.get('actions', {})
    aum = customer.get('aum', {})

    # Avatar
    gender = "men" if int(selected_id[-1], 16) % 2 == 0 else "women"
    index = int(selected_id[:2], 16) % 100
    avatar_url = f"https://randomuser.me/api/portraits/{gender}/{index}.jpg"

    # Profile Section
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
        st.markdown("**Verified:** ✅" if profile.get("verified", False) else "❌")
        st.metric("Risk Level", profile.get("risk_level", "N/A"))
        st.markdown("**Open Finance Tag:** ✅")

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

    st.markdown("### 🔍 Recommendations")
    for i, rec in enumerate(customer.get("recommendations", []), 1):
        st.markdown(f"{i}. {rec}")

    st.markdown("### 🧠 Wallet Share Analysis")
    st.markdown(f"**Primary Bank:** {wallet.get('primary_bank', 'N/A')} ({wallet.get('primary_pct', 0)}% of transactions)")
    secondary = wallet.get("secondary_banks", {})
    secondary_line = " • ".join([f"{k} ({v}%)" for k, v in secondary.items()])
    st.markdown(f"**Secondary Accounts:** {secondary_line or 'N/A'}")

    st.markdown("### 🧩 Insights")
    for insight in insights:
        st.markdown("- " + insight)

    st.markdown("### 🔢 Risk & Credit Info")
    st.markdown(f"**Predictive Risk Score:** {risk_data.get('predictive_risk_score_pct', 'N/A')}%")
    st.markdown(f"**Recommended Credit Limit:** AED {risk_data.get('recommended_credit_limit', 0):,} (Current: AED {risk_data.get('current_applied_credit', 0):,})")
    st.markdown(f"**Optimal Interest Rate:** {risk_data.get('optimal_interest_rate', 'N/A')}")

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
    aum = customer.get('aum', {})

    # Avatar
    gender = "men" if int(selected_id[-1], 16) % 2 == 0 else "women"
    index = int(selected_id[:2], 16) % 100
    avatar_url = f"https://randomuser.me/api/portraits/{gender}/{index}.jpg"

    # Profile Section
    col1, col2, col3 = st.columns([1.5, 3, 2])
    with col1:
        st.image(avatar_url, width=100)
        st.markdown(f"**<span style='font-size: 22px'>{profile['name']}</span>**", unsafe_allow_html=True)
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
        st.metric("Savings USD", f"${accounts['savings_usd']:,}")
    with col2:
        st.markdown(f"**Outstanding Mortgage:** AED {accounts['mortgage_outstanding']:,}")
        st.markdown(f"**Loan Term:** {accounts['loan_term_years']} years")
        st.markdown(f"**EMI Rate:** {accounts['emi_rate']}%")
        st.markdown(f"**Next Payment:** AED {accounts['next_payment_amount']:,} ({accounts['next_payment_date']})")
    with col3:
        st.markdown("**Total AUM:**")
        if "total" in aum:
            st.markdown(f"AED {aum['total']:,}")
            st.markdown(f"**Risk Alignment:** {aum['risk_alignment']}")
        else:
            st.markdown("_Not available_")

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

    st.markdown("### 🧠 Wallet Share Analysis")
    st.markdown(f"**Primary Bank:** {wallet['primary_bank']} ({wallet['primary_pct']}% of transactions)")
    secondary_line = " • ".join([f"{k} ({v}%)" for k, v in wallet["secondary_banks"].items()])
    st.markdown(f"**Secondary Accounts:** {secondary_line}")

    st.markdown("### 🧩 Insights")
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

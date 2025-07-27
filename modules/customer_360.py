import streamlit as st
import pandas as pd
import numpy as np


def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("Customer 360 View – Relationship & Risk Insights")

    # ---- Load Data
    @st.cache_data
    def load_data():
        lifestyle = pd.read_csv("data/enhanced_client_profile.csv")
        usage = pd.read_csv("data/multi_bank_profile.csv")
        return usage, lifestyle

    df_usage, df_life = load_data()

    # ---- Client Selection
    uae_ids = sorted(df_life["UAE ID"].unique())
    selected_id = st.selectbox("Select Client by UAE ID", uae_ids)

    client_core = df_usage[df_usage["UAE ID"] == selected_id]
    client_life = df_life[df_life["UAE ID"] == selected_id].iloc[0]
    client_name = client_life["Client Name"]
    bank_count = client_core["Bank"].nunique()

    # ---- Client Header
    st.markdown("### 👤 Client Overview")
    top1, top2, top3 = st.columns(3)
    with top1:
        st.markdown(f"**Client Name:** {client_name}")
        st.markdown(f"**UAE ID:** {selected_id}")
    with top2:
        st.markdown(f"**Nationality:** {client_life['Nationality']}")
        st.markdown(f"**Medical Insurance:** {client_life['Medical Insurance']}")
    with top3:
        st.markdown(f"**Property:** {client_life['Property Location']} – AED {client_life['Property Value']:,}")
        st.markdown(f"**Utility Bill:** AED {client_life['Utility Bill']}")

    # ---- Product Summary
    st.markdown("### 💼 Product Summary")
    ps1, ps2, ps3 = st.columns(3)
    ps1.metric("Accounts Held", client_core[client_core['Products Used'].str.contains("Account")].shape[0])
    ps2.metric("Loans", client_core[client_core['Products Used'].str.contains("Loan")].shape[0])
    ps3.metric("Credit Cards", client_core[client_core['Products Used'].str.contains("Credit Card")].shape[0])

    # ---- Risk Profiling Logic
    score = 0
    reasons = []
    if client_life["Nationality"] == "Expat":
        score += 2
        reasons.append("Expat profile (+2)")
    if client_life["Utility Bill"] > 1000:
        score += 2
        reasons.append(f"High utility bill: AED {client_life['Utility Bill']} (+2)")
    if client_life["Medical Insurance"] == "None":
        score += 2
        reasons.append("No medical insurance (+2)")
    if client_life["Property Value"] > 3000000:
        score += 1
        reasons.append(f"High-value property: AED {client_life['Property Value']:,} (+1)")
    if bank_count >= 4:
        score += 1
        reasons.append("Fragmented holdings across 4 banks (+1)")

    if score >= 5:
        risk_level = "High"
    elif score >= 3:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    # ---- Credit Score & Risk Signals
    st.markdown("### 🚨 Credit & Risk Insights")
    col3, col4 = st.columns([1, 3])
    with col3:
        st.metric(label="Risk Level", value=risk_level)
        st.metric(label="Risk Score", value=f"{score} / 8")
    with col4:
        st.write("**Scoring Breakdown:**")
        for r in reasons:
            st.write(f"- {r}")

    st.markdown("---")

    # ---- Relationship Summary
    st.markdown("### 🏦 Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(set(x)))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    rel_summary = rel_summary.reset_index(drop=True)
    rel_summary.index += 1
    rel_summary.index.name = "S.No."
    st.dataframe(rel_summary, use_container_width=True)

    # ---- Wallet Share
    st.markdown("### 💰 Wallet Share by Bank")
    wallet = client_core.groupby("Bank")["Products Used"].count()
    wallet_percent = (wallet / wallet.sum() * 100).round(1).reset_index()
    wallet_percent.columns = ["Bank", "% of Wallet"]
    st.dataframe(wallet_percent, use_container_width=True)

    # ---- Predictive Credit Signals
    st.markdown("### 🔍 Predictive Risk & Credit Indicators")
    pr1, pr2, pr3 = st.columns(3)
    pr1.metric("# of Banks", bank_count)
    pr2.metric("Recent Credit Inquiry", "Yes" if np.random.rand() > 0.6 else "No")
    pr3.metric("Likely Insurance Gap", "Yes" if client_life["Medical Insurance"] == "None" else "No")

    # ---- AI Recommendations
    st.markdown("### 🧠 AI Recommendations")
    ai_recos = []
    if client_life["Medical Insurance"] == "None":
        ai_recos.append({
            "Recommendation": "Offer Medical & Critical Illness Plan",
            "Reason": "No medical coverage",
            "Trigger": "Medical Insurance = None"
        })
    if client_life["Property Value"] > 3000000:
        ai_recos.append({
            "Recommendation": "Suggest Real Estate Investment Options",
            "Reason": "High-value property",
            "Trigger": "Property > AED 3M"
        })
    if client_life["Utility Bill"] > 1000:
        ai_recos.append({
            "Recommendation": "Green Energy Efficiency Loan",
            "Reason": "High utility usage",
            "Trigger": "Utility > AED 1000"
        })
    if "Air Tickets" in client_life["Credit Card Activity"]:
        ai_recos.append({
            "Recommendation": "Travel Insurance Add-on",
            "Reason": "Frequent air ticket purchases",
            "Trigger": "Credit Card Activity = Air Tickets"
        })
    if client_life["Nationality"] == "UAE":
        ai_recos.append({
            "Recommendation": "Waqf Savings or National Bonds",
            "Reason": "Eligible UAE National",
            "Trigger": "Nationality = UAE"
        })

    if ai_recos:
        ai_df = pd.DataFrame(ai_recos).reset_index(drop=True)
        ai_df.index += 1
        ai_df.index.name = "S.No."
        st.dataframe(ai_df, use_container_width=True)
    else:
        st.info("No AI-based recommendations triggered for this client.")

    # ---- RM Actions
    st.markdown("### 📌 RM Suggested Actions")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.write("**Follow-ups:**")
        st.write("- Contact client re: insurance plan")
        st.write("- Schedule RM call to review asset mix")
    with ac2:
        st.write("**Next Steps:**")
        st.write("- Generate portfolio stress test")
        st.write("- Offer tailored credit advisory")

    # ---- Product Records
    with st.expander("View Detailed Product Records"):
        product_df = client_core.reset_index(drop=True)
        product_df.index += 1
        product_df.index.name = "S.No."
        st.dataframe(product_df, use_container_width=True)

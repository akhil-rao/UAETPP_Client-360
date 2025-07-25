import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("Customer 360 View – Relationship & Risk Insights")

    # ---- Load Data
    @st.cache_data
    def load_data():
        lifestyle = pd.DataFrame([
            {"UAE ID": "784-1234-567890-1", "Client Name": "Fatima Al Mansouri", "Nationality": "UAE",
             "Property Location": "Dubai Marina", "Property Value": 3100000, "Utility Bill": 1450,
             "Medical Insurance": "None", "Credit Card Activity": "Air Tickets"},
            {"UAE ID": "784-9876-543210-2", "Client Name": "Omar Al Fardan", "Nationality": "Expat",
             "Property Location": "Sharjah Al Khan", "Property Value": 1200000, "Utility Bill": 650,
             "Medical Insurance": "Yes", "Credit Card Activity": "Online Shopping"},
            {"UAE ID": "784-2468-135790-3", "Client Name": "Salim Khan", "Nationality": "Expat",
             "Property Location": "Business Bay", "Property Value": 2150000, "Utility Bill": 980,
             "Medical Insurance": "None", "Credit Card Activity": "Dining"},
            {"UAE ID": "784-3698-147025-4", "Client Name": "Laila Hassan", "Nationality": "UAE",
             "Property Location": "Abu Dhabi Saadiyat", "Property Value": 5800000, "Utility Bill": 1950,
             "Medical Insurance": "Yes", "Credit Card Activity": "Travel"}
        ])
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

    # ---- Client Summary
    st.markdown("### Client Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Client Name:** {client_name}")
        st.write(f"**UAE ID:** {selected_id}")
        st.write(f"**Nationality:** {client_life['Nationality']}")
        st.write(f"**Medical Insurance:** {client_life['Medical Insurance']}")
    with col2:
        st.write(f"**Property Location:** {client_life['Property Location']}")
        st.write(f"**Property Value:** AED {client_life['Property Value']:,}")
        st.write(f"**Utility Bill:** AED {client_life['Utility Bill']}")
        st.write(f"**Credit Card Activity:** {client_life['Credit Card Activity']}")

    st.markdown("---")

    # ---- Risk Profile
    st.subheader("Client Risk Profile")
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
    st.subheader("Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(
        lambda x: ", ".join(sorted(set(x)))
    ).reset_index().rename(columns={"Products Used": "Products Held"})
    rel_summary = rel_summary.reset_index(drop=True)
    rel_summary.index += 1
    rel_summary.index.name = "S.No."
    st.dataframe(rel_summary, use_container_width=True)


    st.markdown("---")

    # ---- AI Recommendations
    st.subheader("AI Recommendations")

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
        ai_df = pd.DataFrame(ai_recos)
        ai_df = ai_df.reset_index(drop=True)
    ai_df.index += 1
    ai_df.index.name = "S.No."
    st.dataframe(ai_df, use_container_width=True)

    else:
        st.info("No AI-based recommendations triggered for this client.")

    st.markdown("---")

    # ---- Product Records
    with st.expander("View Detailed Product Records"):
        product_df = client_core.reset_index(drop=True)
    product_df.index += 1
    product_df.index.name = "S.No."
    st.dataframe(product_df, use_container_width=True)


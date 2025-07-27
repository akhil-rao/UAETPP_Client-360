import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Customer 360 View", layout="wide")
    st.title("Customer 360 View – Relationship & Risk Insights")

    @st.cache_data
    def load_data():
        lifestyle = pd.read_csv("data/enhanced_client_profile.csv")
        usage = pd.read_csv("data/multi_bank_profile.csv")
        return usage, lifestyle

    df_usage, df_life = load_data()

    selected_id = st.selectbox("Select Client by UAE ID", sorted(df_life["UAE ID"].unique()))
    client_core = df_usage[df_usage["UAE ID"] == selected_id]
    client_life = df_life[df_life["UAE ID"] == selected_id].iloc[0]

    st.subheader("Client Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.text(f"Name: {client_life['Client Name']}")
        st.text(f"UAE ID: {client_life['UAE ID']}")
        st.text(f"Nationality: {client_life['Nationality']}")
    with col2:
        st.text(f"Property: {client_life['Property Location']} ({client_life['Property Value']:,})")
        st.text(f"Utility Bill: AED {client_life['Utility Bill']}")
        st.text(f"Insurance: {client_life['Medical Insurance']}")

    st.markdown("### Relationship Summary Across Banks")
    rel_summary = client_core.groupby("Bank")["Products Used"].apply(lambda x: ", ".join(set(x))).reset_index()
    rel_summary.index += 1
    rel_summary.index.name = "S.No."
    st.dataframe(rel_summary, use_container_width=True)

    st.markdown("### AI Recommendations")
    ai = []
    if client_life["Medical Insurance"] == "None":
        ai.append(("Offer Medical Plan", "No insurance coverage"))
    if client_life["Property Value"] > 3000000:
        ai.append(("Real Estate Investments", "High property value"))
    if client_life["Utility Bill"] > 1000:
        ai.append(("Energy Efficiency Loan", "High utility bill"))
    if "Air Tickets" in client_life["Credit Card Activity"]:
        ai.append(("Travel Insurance Add-on", "Frequent air travel"))
    if client_life["Nationality"] == "UAE":
        ai.append(("Waqf Savings Plan", "UAE National"))

    if ai:
        ai_df = pd.DataFrame(ai, columns=["Recommendation", "Reason"])
        ai_df.index += 1
        ai_df.index.name = "S.No."
        st.dataframe(ai_df, use_container_width=True)
    else:
        st.info("No AI recommendations triggered.")

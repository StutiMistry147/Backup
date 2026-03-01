import streamlit as st
import polars as pl
import plotly.express as px
from llm.esg_agent import ask_esg_question

st.set_page_config(page_title="ESG Intelligence Dashboard", layout="wide")

st.title("ESG Intelligence Dashboard")

df = pl.read_csv("data/processed/final_esg_dataset.csv").to_pandas()

company = st.sidebar.selectbox(
    "Select Company",
    df["Company"].unique()
)

filtered_df = df[df["Company"] == company]

# KPIs
col1, col2 = st.columns(2)

col1.metric("Latest Emissions (Million Tons)",
            round(filtered_df.iloc[-1]["Emissions_Million_Tons"], 2))

col2.metric("Latest CO2 per Capita (USA)",
            round(filtered_df.iloc[-1]["CO2_per_Capita"], 2))

# Chart
fig = px.line(filtered_df,
              x="Year",
              y="Emissions_Million_Tons",
              title=f"{company} Carbon Emissions Trend")

st.plotly_chart(fig, use_container_width=True)

# AI Chat Section
st.markdown("## Ask ESG AI Assistant")

user_input = st.text_input("Ask a question about the ESG data")

if user_input:
    response = ask_esg_question(user_input, filtered_df)
    st.write(response)

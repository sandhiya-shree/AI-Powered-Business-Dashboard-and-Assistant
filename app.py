import streamlit as st
import main
import pandas as pd
st.set_page_config(
    page_title="Sunshine Shop AI",
    page_icon="🛍️",
    layout="wide"
)
st.markdown("""
<style>
.stApp{
[data-testid="stAppViewContainer"] {
    background-color: #F4F7FB !important;
}
}
h1{
colour:navy;
font:800;
}
h2, h3{
colour:steelblue;
}
[data-testid="st.metric"]{
background colour: white;
padding: 22px;
border-radius:12px;
border:1px solid lightgrey;
box-shadow:0 2px 8px rgba(0,0,0,0.04);
}
[data-testid="st.metricvalue"]{
colour:teal;
font-weight:700;
}
<style>
""",unsafe_allow_html=True
)
st.title("SUNSHINE SHOP AI ASSISTANT")
st.write("WELCOME TO BUSINESS DASHBOARD")
st.subheader("Business Overview")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Total sales",f"${main.Total_sales:,.0f}")
with col2:
    st.metric("Total cost",f"${main.Total_cost:,.0f}")
with col3:
    st.metric("Total profit",f"${main.Total_profit:,.0f}")

st.subheader("Monthly Business Performance")
st.bar_chart(
    {
        "Sales":[data["sales"] for data in main.monthly_data],
        "Profit":[
            data["sales"]-data["cost"]
            for data in main.monthly_data
        ]
    },
    x=None
)

st.subheader("Monthly Business Report")
st.dataframe(
    [
        {
            "Month":data["month"],
            "Sales":data["sales"],
            "Cost":data["cost"],
            "Profit":data["sales"]-data["cost"]
        }
        for data in main.monthly_data
    ],
    use_container_width=True
)

st.subheader("AI Business Assistant")
user_question = st.text_input("Ask a question about Sunshine Shop")

if st.button("Ask AI") and user_question:
    with st.spinner("Sunshine AI is thinking...."):
        answer = main.get_business_answer(user_question)
        st.write(answer)
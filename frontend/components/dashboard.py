# frontend/components/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

def display_dashboard(data):
    df = pd.DataFrame(data)
    st.subheader("Option Chain Data")
    st.dataframe(df)

    st.subheader("Premium Earned vs Strike Price")
    fig = px.bar(df, x='strike_price', y='premium_earned', color='side', title='Premium Earned per Strike Price')
    st.plotly_chart(fig)

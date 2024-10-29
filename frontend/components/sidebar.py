# frontend/components/sidebar.py
import streamlit as st
from datetime import datetime

def sidebar():
    st.sidebar.header("Input Parameters")
    instrument_name = st.sidebar.selectbox("Instrument", ["NIFTY", "BANKNIFTY"])
    expiry_date = st.sidebar.date_input("Expiry Date", min_value=datetime.now())
    expiry_date_str = expiry_date.strftime("%Y-%m-%d")
    side = st.sidebar.selectbox("Option Side", ["PE", "CE"])
    return instrument_name, expiry_date_str, side

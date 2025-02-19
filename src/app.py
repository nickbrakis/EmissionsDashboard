import streamlit as st
import pandas as pd
import os
import numpy as np
from plots.exceedances_per_year import exceedances_per_year
from utils.load_data import load_data


PIR_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PIR', '2021-2023')
PA1_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PA1', '2021-2023')
PA2_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PA2', '2021-2023')

cities = {"ΠΑΤΡΑ1" : PA1_DATA_DIR, "ΠΑΤΡΑ2" : PA2_DATA_DIR, "ΠΕΙΡΑΙΑΣ" : PIR_DATA_DIR}

def main():
    st.title("Emissions Dashboard")

    selected_city = st.selectbox("Select city:", cities.keys())

    selected_file = st.selectbox("Select a file:", os.listdir(cities[selected_city]), index=None)
    uploaded_file = st.file_uploader("Or upload a file", type=["csv"])

    if uploaded_file:
        data = load_data(uploaded_file)
        st.write(data)

    elif selected_file:
        data = load_data(os.path.join(cities[selected_city], selected_file))
        st.write(data)

    if 'data' in locals():
        # Plot selection
        plot_options = ['Number of exceedances of the daily limit']
        selected_plot = st.selectbox("Select a plot:", plot_options)

        if selected_plot == 'Number of exceedances of the daily limit':
            exceedances_per_year(data, 'PM10')

if __name__ == "__main__":
    main()
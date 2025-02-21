import streamlit as st
import pandas as pd
import os
import numpy as np
import logging
from utils.load_data import load_data
from plots.exceedances_per_year import exceedances_per_year_plotly
from plots.daily_concentrations import daily_concentrations
from plots.monthly_concentrations import monthly_concentrations
from plots.monthly_trend_all import monthly_trend_all
from plots.annual_trend import annual_trend

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PIR_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PIR')
PA1_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PA1')
PA2_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'PA2')
SMY_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'SMY')


cities = {"ΠΑΤΡΑ1" : PA1_DATA_DIR, "ΠΑΤΡΑ2" : PA2_DATA_DIR, "ΠΕΙΡΑΙΑΣ" : PIR_DATA_DIR, "ΝΕΑ ΣΜΥΡΝΗ" : SMY_DATA_DIR}

def main():
    st.title("Emissions Dashboard")

    selected_city = st.selectbox("Select city:", cities.keys())

    selected_file = st.selectbox("Select a file:", os.listdir(cities[selected_city]), index=None)
    uploaded_file = st.file_uploader("Or upload a file", type=["csv"])

    if uploaded_file:
        data = load_data(uploaded_file)
        # st.write(data)

    elif selected_file:
        data = load_data(os.path.join(cities[selected_city], selected_file))
        emission = selected_file.split('.')[0]
    

    if 'data' in locals():

        plot_options = [
            'Daily Concentrations with Standard Deviation',
            'Monthly Concentrations with Standard Deviation',
            'Trend Analysis of Monthly Concentrations (All Months Combined)',
            'Trend Analysis of Average Annual Concentration with 95% CI',
            'Number of exceedances of the daily limit',
        ]
        
        selected_plot = st.selectbox("Select a plot:", plot_options)

        if selected_plot == 'Daily Concentrations with Standard Deviation':
            daily_concentrations(data, emission)
        elif selected_plot == 'Monthly Concentrations with Standard Deviation':
            monthly_concentrations(data, emission)
        elif selected_plot == 'Trend Analysis of Monthly Concentrations (All Months Combined)':
            monthly_trend_all(data, emission)
        elif selected_plot == 'Number of exceedances of the daily limit':
            exceedances_per_year_plotly(data, emission)
        elif selected_plot == 'Trend Analysis of Average Annual Concentration with 95% CI':
            annual_trend(data, emission)


if __name__ == "__main__":
    main()
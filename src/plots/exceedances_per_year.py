import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def exceedances_per_year(df, emission, limit=50, threshold=35):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
    df['Exceedance'] = df['Daily_Average'] > limit
    df['Year'] = df['Date'].dt.year
    exceedances_per_year = df.groupby('Year')['Exceedance'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x='Year', 
        y='Exceedance', 
        data=exceedances_per_year, 
        color='orangered', 
        alpha=0.7, 
        edgecolor='black',
    )
    if threshold is not None:
        plt.axhline(y=threshold, color='red', linestyle='--', linewidth=1, label=f'Threshold: {threshold}')
    plt.xlabel('Year')
    plt.ylabel(f'Number of Exceedances')
    plt.title(f'Number of Exceedances of the Daily {emission} Limit ({limit} µg/m³) Per Year')
    plt.xticks(rotation=45)
    st.pyplot(plt)
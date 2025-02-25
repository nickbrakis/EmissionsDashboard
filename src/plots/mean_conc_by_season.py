import pandas as pd
import plotly.express as px
import streamlit as st

def mean_conc_by_season(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])

    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Autumn'

    df['Year'] = df['Date'].dt.year
    df['Season'] = df['Date'].dt.month.map(get_season)

    df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)

    grouped_data = df.groupby(['Year', 'Season'])['Daily_Average'].mean().reset_index()

    season_order = ['Winter', 'Spring', 'Summer', 'Autumn']

    fig = px.bar(
        grouped_data,
        x='Year',
        y='Daily_Average',
        color='Season',
        category_orders={'Season': season_order},
        labels={'Daily_Average': f'{emission} (μg/m³)', 'Year': 'Year'},
        title=f'Mean {emission} Concentration by Year for Each Season'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=f'{emission} (μg/m³)',
        legend_title_text='Season',
        barmode='group'  # Ensure bars are grouped side by side
    )

    st.plotly_chart(fig)
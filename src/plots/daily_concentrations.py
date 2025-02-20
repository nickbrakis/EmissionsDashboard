import pandas as pd
import plotly.express as px
import streamlit as st

def daily_concentrations(df, emission):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
    df['Daily_Std'] = df.iloc[:, 1:25].std(axis=1)

    fig = px.line(
        df,
        x='Date',
        y='Daily_Average',
        title=f'Daily {emission} Concentrations with Standard Deviation',
        labels={'Daily_Average': f'{emission} (μg/m³)', 'Date': 'Date'},
        line_shape='linear'
    )

    fig.update_traces(mode='lines+markers', line=dict(width=1))

    fig.add_scatter(
        x=df['Date'],
        y=df['Daily_Average'] + df['Daily_Std'],
        mode='lines',
        name='Upper Bound',
        line=dict(dash='dash', color='red'),
    )

    fig.add_scatter(
        x=df['Date'],
        y=df['Daily_Average'] - df['Daily_Std'],
        mode='lines',
        name='Lower Bound',
        line=dict(dash='dash', color='red'),

    )

    st.plotly_chart(fig)
import pandas as pd
import plotly.express as px
import streamlit as st

def monthly_concentrations(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)

    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]

    df['Month'] = df['Date'].dt.month
    monthly_data = df.groupby('Month')['Daily_Average'].agg(['mean', 'std']).reset_index()

    fig = px.line(
        monthly_data,
        x='Month',
        y='mean',
        title=f'Monthly {emission} Concentrations with Standard Deviation',
        labels={'mean': f'{emission} (μg/m³)', 'Month': 'Month'},
        line_shape='linear'
    )

    fig.update_traces(mode='lines+markers', line=dict(width=2))

    fig.add_scatter(
        x=monthly_data['Month'],
        y=monthly_data['mean'] + monthly_data['std'],
        mode='lines',
        name='Upper Bound',
        line=dict(dash='dash', color='red', width=1)
    )

    fig.add_scatter(
        x=monthly_data['Month'],
        y=monthly_data['mean'] - monthly_data['std'],
        mode='lines',
        name='Lower Bound',
        line=dict(dash='dash', color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(173, 216, 230, 0.3)'  # lightblue with alpha
    )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        )
    )

    st.plotly_chart(fig)
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def annual_concentrations(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
    df['Year'] = df['Date'].dt.year
    
    # Filter the data based on the selected date range
    df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    annual_data = df.groupby('Year')['Daily_Average'].agg(['mean', 'std']).reset_index()

    fig = go.Figure()

    # Add bar plot for annual averages with standard deviation
    fig.add_trace(
        go.Bar(
            x=annual_data['Year'],
            y=annual_data['mean'],
            error_y=dict(
                type='data',
                array=annual_data['std'],
                visible=True,
                color='black'
            ),
            name='Annual Mean',
            marker_color='green'
        )
    )

    fig.update_layout(
        title=f'Annual {emission} Concentrations with Standard Deviation',
        xaxis_title='Year',
        yaxis_title=f'{emission} (μg/m³)',
        xaxis=dict(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=annual_data['Year'].astype(str)
        ),
        showlegend=True
    )

    st.plotly_chart(fig)
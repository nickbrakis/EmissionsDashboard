import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def hourly_distribution(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter the data based on the selected date range
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
    df_long = df.melt(id_vars=['Date'], value_vars=range(1, 25), var_name='Hour', value_name='Concentration')
    hourly_means = df_long.groupby('Hour')['Concentration'].mean().reset_index()

    fig = go.Figure()

    # Add box plot for hourly concentrations
    fig.add_trace(
        go.Box(
            x=df_long['Hour'],
            y=df_long['Concentration'],
            name='Hourly Concentrations',
            marker_color='skyblue',
            boxmean=False
        )
    )

    # Add scatter plot for hourly means
    fig.add_trace(
        go.Scatter(
            x=hourly_means['Hour'],
            y=hourly_means['Concentration'],
            mode='markers+lines',
            name='Hourly Mean',
            marker=dict(color='red', size=8),
            line=dict(color='red', width=2)
        )
    )

    fig.update_layout(
        title=f'Hourly Distribution of {emission} Concentration with Hourly Means',
        xaxis_title='Hour of the Day',
        yaxis_title=f'{emission} (μg/m³)',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 25)),
            ticktext=[str(i) for i in range(1, 25)]
        ),
        showlegend=True
    )

    st.plotly_chart(fig)
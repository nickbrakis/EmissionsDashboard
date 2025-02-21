import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def monthly_distribution(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)

    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
    monthly_means = df.groupby(['Month'])['Daily_Average'].mean().reset_index()

    if emission == 'CO':
        units = '(mg/m³)'
    else:
        units = '(μg/m³)'

    fig = go.Figure()

    # Add box plot for daily concentrations
    fig.add_trace(
        go.Box(
            x=df['Month'],
            y=df['Daily_Average'],
            name='Daily Concentrations',
            marker_color='blue',
            boxmean=False
        )
    )

    # Add scatter plot for monthly means
    fig.add_trace(
        go.Scatter(
            x=monthly_means['Month'],
            y=monthly_means['Daily_Average'],
            mode='markers+lines',
            name='Monthly Mean',
            marker=dict(color='red', size=8),
            line=dict(color='red', width=2)
        )
    )

    fig.update_layout(
        title=f'Monthly Distribution of Daily {emission} Concentrations with Monthly Means',
        xaxis_title='Month',
        yaxis_title=f'{emission} {units}',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        showlegend=True
    )

    st.plotly_chart(fig)
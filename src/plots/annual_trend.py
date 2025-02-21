import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats
import numpy as np

def annual_trend(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)

    # Filter the data based on the selected date range
    df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    annual_means = df.groupby('Year')['Daily_Average'].mean().reset_index()

    slope, intercept, r_value, p_value, std_err = stats.linregress(annual_means['Year'], annual_means['Daily_Average'])
    trend_line = intercept + slope * annual_means['Year']

    n = len(annual_means)  # Number of data points
    t_value = stats.t.ppf(0.975, df=n-2)  # t-value for 95% CI (2-tailed)
    ci = t_value * std_err * np.sqrt(1/n + (annual_means['Year'] - np.mean(annual_means['Year']))**2 / np.sum((annual_means['Year'] - np.mean(annual_means['Year']))**2))
    ci_upper = trend_line + ci  # Upper bound of 95% CI
    ci_lower = trend_line - ci  # Lower bound of 95% CI

    slope_annual = slope  # Convert from μg/m³/year
    se_slope = std_err  # Standard error of the slope (annualized)
    ci_slope_lower = slope_annual - t_value * se_slope  # Lower bound of 95% CI for slope
    ci_slope_upper = slope_annual + t_value * se_slope  # Upper bound of 95% CI for slope

    trend_text = f'Trend: {slope_annual:.2f} μg/m³/year'
    ci_text = f'CI: {ci_slope_lower:.2f} to {ci_slope_upper:.2f}'

    fig = px.line(
        annual_means,
        x='Year',
        y='Daily_Average',
        title=f'Trend Analysis of Annual Mean {emission} Concentration with 95% Confidence Interval',
        labels={'Daily_Average': f'{emission} (μg/m³)', 'Year': 'Year'},
        line_shape='linear'
    )

    fig.add_scatter(
        x=annual_means['Year'],
        y=trend_line,
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=2)
    )

    fig.add_scatter(
        x=annual_means['Year'],
        y=ci_upper,
        mode='lines',
        name='Upper 95% CI',
        line=dict(dash='dash', color='red', width=1)
    )

    fig.add_scatter(
        x=annual_means['Year'],
        y=ci_lower,
        mode='lines',
        name='Lower 95% CI',
        line=dict(dash='dash', color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)'  # red with alpha
    )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=annual_means['Year'],
            ticktext=annual_means['Year'].astype(str)
        ),
        annotations=[
            dict(
                xref='paper', yref='paper', x=0.05, y=0.95,
                text=trend_text, showarrow=False, font=dict(size=12)
            ),
            dict(
                xref='paper', yref='paper', x=0.05, y=0.90,
                text=ci_text, showarrow=False, font=dict(size=12)
            )
        ]
    )

    st.plotly_chart(fig)
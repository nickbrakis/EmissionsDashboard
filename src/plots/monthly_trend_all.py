import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats
import numpy as np

def monthly_trend_all(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)

    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
    df['YearMonth'] = df['Date'].dt.to_period('M')

    monthly_avg = df.groupby('YearMonth')['Daily_Average'].mean().reset_index()
    monthly_avg['YearMonth'] = monthly_avg['YearMonth'].dt.to_timestamp()
    monthly_avg['Months'] = (monthly_avg['YearMonth'].dt.year - monthly_avg['YearMonth'].dt.year.min()) * 12 + monthly_avg['YearMonth'].dt.month

    slope, intercept, r_value, p_value, std_err = stats.linregress(monthly_avg['Months'], monthly_avg['Daily_Average'])
    trend_line = intercept + slope * monthly_avg['Months']

    n = len(monthly_avg)  # Number of data points
    t_value = stats.t.ppf(0.975, df=n-2)  # t-value for 95% CI (2-tailed)
    ci = t_value * std_err * np.sqrt(1/n + (monthly_avg['Months'] - np.mean(monthly_avg['Months']))**2 / np.sum((monthly_avg['Months'] - np.mean(monthly_avg['Months']))**2))
    ci_upper = trend_line + ci  # Upper bound of 95% CI
    ci_lower = trend_line - ci  # Lower bound of 95% CI

    slope_annual = slope * 12  # Convert from μg/m³/month to μg/m³/year
    se_slope = std_err * 12  # Standard error of the slope (annualized)
    ci_slope_lower = slope_annual - t_value * se_slope  # Lower bound of 95% CI for slope
    ci_slope_upper = slope_annual + t_value * se_slope  # Upper bound of 95% CI for slope

    trend_text = f'Trend: {slope_annual:.2f} μg/m³/year'
    ci_text = f'CI: {ci_slope_lower:.2f} to {ci_slope_upper:.2f}'

    fig = px.line(
        monthly_avg,
        x='YearMonth',
        y='Daily_Average',
        title=f'Trend Analysis of Monthly {emission} Concentrations with 95% CI (All Months Combined)',
        labels={'Daily_Average': f'{emission} (μg/m³)', 'YearMonth': 'Date (Year-Month)'},
        line_shape='linear'
    )

    fig.add_scatter(
        x=monthly_avg['YearMonth'],
        y=trend_line,
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=2)
    )

    fig.add_scatter(
        x=monthly_avg['YearMonth'],
        y=ci_upper,
        mode='lines',
        name='Upper 95% CI',
        line=dict(dash='dash', color='red', width=1)
    )

    fig.add_scatter(
        x=monthly_avg['YearMonth'],
        y=ci_lower,
        mode='lines',
        name='Lower 95% CI',
        line=dict(dash='dash', color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)'  # red with alpha
    )

    fig.update_layout(
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
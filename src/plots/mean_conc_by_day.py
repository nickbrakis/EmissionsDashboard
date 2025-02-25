import pandas as pd
import plotly.express as px
import streamlit as st

def mean_conc_by_day(df, emission, start_year, end_year):
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
    df['Year'] = df['Date'].dt.year
    df['DayOfWeek'] = df['Date'].dt.day_name()  # Full day names (e.g., Monday, Tuesday)
    
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
    
    grouped_data = df.groupby(['Year', 'DayOfWeek'])['Daily_Average'].mean().reset_index()
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = px.bar(
        grouped_data,
        x='DayOfWeek',
        y='Daily_Average',
        color='Year',
        category_orders={'DayOfWeek': day_order},
        labels={'Daily_Average': f'{emission} (μg/m³)', 'DayOfWeek': 'Day of the Week'},
        title=f'Mean {emission} Concentration by Day of the Week for Each Year'
    )
    
    fig.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title=f'{emission} (μg/m³)',
        xaxis=dict(
            tickmode='array',
            tickvals=day_order,
            ticktext=[day[:3] for day in day_order]
        ),
        legend_title_text='Year',
        barmode='group'  # Ensure bars are grouped side by side
    )
    
    st.plotly_chart(fig)
import pandas as pd
import plotly.express as px
import streamlit as st

def exceedances_per_year_plotly(df, emission, limit=50, threshold=35):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
    df['Exceedance'] = df['Daily_Average'] > limit
    df['Year'] = df['Date'].dt.year.astype(int)
    exceedances_per_year = df.groupby('Year')['Exceedance'].sum().reset_index()

    fig = px.bar(
        exceedances_per_year,
        x='Year',
        y='Exceedance',
        title=f'Number of Exceedances of the Daily {emission} Limit ({limit} µg/m³) Per Year',
        labels={'Exceedance': 'Number of Exceedances', 'Year': 'Year'},
        color_discrete_sequence=['lightblue']
    )
    fig.update_layout(xaxis_type='category')

    if threshold is not None:
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text=f'Threshold: {threshold}', annotation_position="top left")

    st.plotly_chart(fig)

    exceedance_days = df[df['Exceedance']]
    exceedance_days['Date'] = exceedance_days['Date'].dt.strftime('%Y-%m-%d')

  # Display the filtered DataFrame below the plot without the index and excluding the 'Exceedance' column
    st.write("Days with Exceedances:")
    st.write(exceedance_days[['Date', 'Daily_Average']].reset_index(drop=True))
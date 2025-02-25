import pandas as pd
import plotly.express as px
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def exceedances_per_year_plotly(df, emission, start_year, end_year, limit=50, threshold=None):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year.astype(int)

    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]

    if emission == 'NO2' or emission == 'SO2':
        # Check for exceedances per hour
        exceedances_per_hour = df.iloc[:, 1:25] > limit
        df['Exceedance'] = exceedances_per_hour.sum(axis=1)
        measure = 'Hourly'
    else:
        # Check for exceedances per day
        df['Daily_Average'] = df.iloc[:, 1:25].mean(axis=1)
        df['Exceedance'] = df['Daily_Average'] > limit
        measure = 'Daily'


    exceedances_per_year = df.groupby('Year')['Exceedance'].sum().reset_index()


    fig = px.bar(
        exceedances_per_year,
        x='Year',
        y='Exceedance',
        title=f'Number of Exceedances of the {measure} {emission} Limit ({limit} µg/m³) Per Year',
        labels={'Exceedance': 'Number of Exceedances', 'Year': 'Year'},
        color_discrete_sequence=['lightblue']
    )
    fig.update_layout(xaxis_type='category')

    if threshold is not None:
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text=f'Threshold: {threshold}', annotation_position="top left")

    st.plotly_chart(fig)

    exceedance_days = df[df['Exceedance'] > 0]
    exceedance_days['Date'] = exceedance_days['Date'].dt.strftime('%Y-%m-%d')

    col1, col2 = st.columns(2)
   
    with col1:
        st.write("Days with Exceedances:")
        gb = GridOptionsBuilder.from_dataframe(exceedance_days[['Date', 'Exceedance']])
        gb.configure_selection('single', use_checkbox=True)
        grid_options = gb.build()

        grid_response = AgGrid(
            exceedance_days[['Date', 'Exceedance']].reset_index(drop=True),
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            # theme='light'
        )

        selected_rows = grid_response['selected_rows']
       
    with col2:
        if type(selected_rows) == type(None):
            st.write(f"Select a date for weather info.")

        elif selected_rows is not None and len(selected_rows) > 0:
            selected_date = selected_rows.iloc[0][0]
            st.write(f"Selected date: {selected_date}")

            weather_info = get_weather_info(selected_date)  # Replace with your function to get weather info
            st.write(f"Weather info for {selected_date}:")
            st.write(weather_info)

def get_weather_info(date):

    st.write("Not available ... Looks like this:")

    return {
        "Temperature": "20°C",
        "Humidity": "60%",
        "Wind Speed": "15 km/h",
        "Condition": "Sunny"
    }
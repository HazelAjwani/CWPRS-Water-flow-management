import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Load dataset
dam_data = pd.read_csv('water_flow_data.csv')

# Ensure date_recorded is in datetime format
dam_data['date_recorded'] = pd.to_datetime(dam_data['date_recorded'], errors='coerce')

# Extracting Hour, Day, and Month for visualization
dam_data['hour'] = dam_data['date_recorded'].dt.hour
dam_data['day'] = dam_data['date_recorded'].dt.date
dam_data['month'] = dam_data['date_recorded'].dt.to_period('M')

# Unique dam locations for selection
dam_types = dam_data['dam_location'].unique()

# Sidebar for Navigation
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Input Data", "View Trends"])

# Title and Branding
st.markdown("<h1 style='text-align: center; color: #2e7d32;'>CWPRS Water Volume Observation</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Dashboard Section
if menu == "Dashboard":
    st.header("🔹 Dashboard")

    # Select Dam Location
    dam_selected = st.selectbox("Select Dam Location", dam_types, help="Choose a dam from the list to view its data.")
    
    # Filter data for selected dam
    dam_data_filtered = dam_data[dam_data['dam_location'] == dam_selected]

    # Option to select between Day or Month
    trend_type = st.radio("View Rate of Flow By:", ("Day", "Month"), help="Select a time period for trend analysis.")

    if trend_type == "Month":
        # Month Selection
        month_selected = st.selectbox("Select Month", dam_data['month'].unique(), help="Choose a month to view rate of flow trends.")
        
        # Filter the data for selected month
        month_filtered_data = dam_data_filtered[dam_data_filtered['month'] == month_selected]
        
        if not month_filtered_data.empty:
            st.subheader(f"🌊 Rate of Flow Trends for {dam_selected} in {month_selected}")
            st.metric("Average Rate of Flow", f"{month_filtered_data['rate_of_flow'].tail(1).values[0]:.2f} m³/s")
            
            # Calculate the last rate of flow and the change from the previous one
            sorted_month_data = month_filtered_data.sort_values(by=['day', 'hour'])
            last_two_data = sorted_month_data.tail(2)

            if len(last_two_data) == 2:
                last_rof = last_two_data['rate_of_flow'].iloc[-1]
                prev_rof = last_two_data['rate_of_flow'].iloc[0]
                change = last_rof - prev_rof
                st.metric("Last Rate of Flow", f"{last_rof:.2f} m³/s", delta=f"{change:.2f} m³/s")
            else:
                st.warning("Not enough data to calculate change.")
                
            # Group by day and calculate mean rate of flow for each day
            monthly_data = month_filtered_data.groupby('day')['rate_of_flow'].mean().reset_index()
            monthly_data = monthly_data.sort_values(by='day')
            st.line_chart(monthly_data.set_index('day'), use_container_width=True)
        else:
            st.warning("No data available for the selected month.")
    
    elif trend_type == "Day":
        # Day Selection
        day_selected = st.date_input("Select Date", min_value=min(dam_data['date_recorded']), max_value=max(dam_data['date_recorded']))
        
        # Filter the data for selected day
        day_filtered_data = dam_data_filtered[dam_data_filtered['day'] == day_selected]
        
        if not day_filtered_data.empty:
            st.subheader(f"🌅 Rate of Flow Trends for {dam_selected} on {day_selected}")
            daily_data = day_filtered_data.groupby('hour')['rate_of_flow'].mean().reset_index()
            st.line_chart(daily_data.set_index('hour'), use_container_width=True)
        else:
            st.warning("No data available for the selected day.")

    # Map Visualization
    st.subheader(f"📍 Location of {dam_selected}")

    # Preparing map data
    map_data = dam_data_filtered[['dam_lat_coords', 'dam_long_coords']].rename(
        columns={'dam_lat_coords': 'lat', 'dam_long_coords': 'lon'}
    )

    # Displaying the map
    if not map_data.empty:
        st.map(map_data)
    else:
        st.warning("Location data not available for the selected dam.")

# Input Data Section
elif menu == "Input Data":
    st.header("📥 Enter Water Levels")
    initial_level = st.number_input("Initial Water Level (m)", min_value=300, help="Enter the initial water level in meters.")
    final_level = st.number_input("Final Water Level (m)", min_value=800, help="Enter the final water level in meters.")
    date = st.date_input("Date", datetime.today())
    location = st.selectbox("Location", dam_types, help="Select the dam location for the data entry.")
    
    st.write(f"Data Recorded for {location} on {date}")
    
    # Format the date to match the required format
    date = date.strftime('%Y-%m-%d')
    
    # Temporary formula to calculate rate of flow
    rof = (final_level - initial_level) * np.random.uniform(0.8, 1.2)
    dam_shape = dam_data[dam_data['dam_location'] == location].iloc[0]['dam_shape']
    
    if st.button("Save Data", use_container_width=True):
        # Save the new data entry to the dam data
        new_entry = {
            'date_recorded': date,
            'initial_water_level': initial_level,
            'final_water_level': final_level,
            'dam_shape': dam_shape,
            'dam_location': location,
            'dam_lat_coords': dam_data[dam_data['dam_location'] == location].iloc[0]['dam_lat_coords'],
            'dam_long_coords': dam_data[dam_data['dam_location'] == location].iloc[0]['dam_long_coords'],
            'cross_sectional_area': dam_data[dam_data['dam_location'] == location].iloc[0]['cross_sectional_area'],
            'rate_of_flow': rof
        }
        
        # Convert new_entry to a DataFrame and append it using concat
        new_entry_df = pd.DataFrame([new_entry])
        dam_data = pd.concat([dam_data, new_entry_df], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        dam_data.to_csv('water_flow_data.csv', index=False)

        # Show success message
        st.success("✅ Data Saved Successfully")

        # Optionally, you can display the newly added data
        st.write(f"New Entry: {new_entry}")

# View Trends Section
elif menu == "View Trends":
    st.header("📊 Historical Rate of Flow Trends")
    dam_selected = st.selectbox("Select Dam Location", dam_types)
    dam_data_filtered = dam_data[dam_data['dam_location'] == dam_selected]
    
    st.subheader(f"Rate of Flow Trends for {dam_selected}")
    st.bar_chart(dam_data_filtered[['date_recorded', 'rate_of_flow']].set_index('date_recorded'), use_container_width=True)

import streamlit as st
import pandas as pd
import json
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="RetroScan AI GIS Dashboard", layout="wide")

def load_data():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'latest_run.json')
    if os.path.exists(db_path):
        with open(db_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()

def main():
    st.title("RetroScan AI : GIS Dashboard & Intelligence")
    st.markdown("Real-time automated retroreflectivity (RA) monitoring of highway infrastructure.")

    df = load_data()

    if df.empty:
        st.warning("No data found. Please run main.py to generate sensor data.")
        return

    # Top KPI Metrics
    total_assets = len(df)
    danger_count = len(df[df['irc_status'] == 'DANGER'])
    warning_count = len(df[df['irc_status'] == 'WARNING'])
    safe_count = len(df[df['irc_status'] == 'SAFE'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets Scanned", total_assets)
    col2.metric("SAFE Assets", safe_count)
    col3.metric("WARNING Assets", warning_count)
    col4.metric("DANGER (Immediate Fix)", danger_count)

    st.markdown("---")

    # Map Visualization setup
    st.subheader("Highway GIS Map")
    colA, colB = st.columns([2, 1])

    with colA:
        # Create map centered at mean coordinates
        m = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=15)

        # Color mapping logic
        color_map = {'SAFE': 'green', 'WARNING': 'orange', 'DANGER': 'red'}

        for idx, row in df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lng']],
                radius=6,
                popup=f"{row['object_type']}<br>RA: {row['ra_value']}<br>Status: {row['irc_status']}<br>Days to Fail: {row['days_to_failure']}",
                color=color_map.get(row['irc_status'], 'blue'),
                fill=True,
                fill_opacity=0.7
            ).add_to(m)

        st_folium(m, width=700, height=500)

    with colB:
        st.subheader("Predictive Maintenance (LSTM)")
        st.markdown("Assets predicted to fail within 30 days:")
        critical_assets = df[(df['days_to_failure'] < 30) & (df['irc_status'] != 'DANGER')].sort_values(by='days_to_failure')
        
        if critical_assets.empty:
            st.success("No assets predicted to fail in the next 30 days!")
        else:
            st.dataframe(critical_assets[['object_type', 'ra_value', 'days_to_failure']], use_container_width=True)

    st.markdown("---")
    st.subheader("Detailed Scan Records")
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()

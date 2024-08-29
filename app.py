import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(page_title="World Freight Financial Dashboard", page_icon="🚢", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background-color: #191a1a;
        color: #FFFFFF;
        font-family: 'Arial, sans serif';
    }
    .css-18e3th9 {
        padding: 2rem;
    }
    .css-1v3fvcr {
        background: #7A8A99;  /* Lighter gray-blue background */
        color: #FFFFFF !important;  /* White font with !important to override */
        padding: 0.5rem 1rem;
        text-align: center;
        border-radius: 20px;
        margin: 0 5px;
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        border: 1px solid #7A8A99;
        transition: background 0.3s, border 0.3s;
    }
    .css-1v3fvcr:hover {
        background: #657988;  /* Slightly darker gray-blue on hover */
        border: 1px solid #657988;
    }
    h1, h2, h3, h4 {
        color: #7A8A99;
        text-transform: uppercase;
        font-weight: bold;
    }
    .st-bj {
        background-color: #333333 !important;
    }
    .st-bw {
        color: #FFFFFF !important;
    }
    .st-ae {
        color: #FFFFFF !important;
    }
    .st-ci {
        color: #FFFFFF !important;
    }
    .section-divider {
        border-top: 2px solid #7A8A99;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Navigation
st.markdown("<h1 style='text-align: center;'>Routes & Financial Dashboard</h1>", unsafe_allow_html=True)
st.write('')

st.markdown("<div style='text-align: center;'><a href='#overview' class='css-1v3fvcr'>📊 Overview</a> | <a href='#financial-metrics' class='css-1v3fvcr'>📈 Financial Metrics</a> | <a href='#profit-loss' class='css-1v3fvcr'>💰 Profit & Loss</a> | <a href='#cash-flow' class='css-1v3fvcr'>💵 Cash Flow</a> | <a href='#routes' class='css-1v3fvcr'>🚢 Shipping Routes</a></div>", unsafe_allow_html=True)
st.write('')
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.write('')
st.subheader("Main Shipping Routes")
# Example Form with Parameters (Placed Between Title and Map/Table)
with st.form(key="settings_form"):
    col1, col2, col3 = st.columns([3, 1, 1])

    location = col1.text_input("Shipping Location", value="New York")
    distance = col2.slider("Shipping Distance (km)", min_value=100, max_value=10000, value=5000)
    route_type = col3.selectbox("Route Type", options=["Ocean", "Air", "Land"])


    expander = st.expander("Advanced Settings")
    with expander:
        col1_adv, col2_adv = st.columns(2)
        
        currency = col1_adv.radio("Currency", options=["USD", "EUR", "CNY", "MXN"])
        year = col2_adv.selectbox("Year", options=[2022, 2023, 2024])

        display_title = col1_adv.checkbox("Display Title", value=True)
        title_color = col2_adv.color_picker("Title Color", value="#7A8A99")

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

        show_map = col1_adv.checkbox("Show Map", value=True)
        contour_width = col2_adv.slider("Map Contour Width", min_value=0, max_value=10, value=2)
        
    st.form_submit_button(label="Apply Settings")


# Updated Data for Map (Filtered for USA, Mexico, Europe, and China)
addresses_data = {
    "Location": [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
        "Paris", "Lyon", "Marseille", "Berlin", "Munich",
        "Shanghai", "Beijing", "Guangzhou", "Shenzhen", "Tianjin",
        "Mexico City", "Guadalajara", "Monterrey", "Tijuana", "Cancun",
        "London", "Manchester", "Birmingham", "Dublin", "Frankfurt",
        "Hamburg", "Milan", "Rome", "Barcelona", "Madrid",
        "Warsaw", "Prague", "Budapest", "Vienna", "Zurich",
        "San Francisco", "Dallas", "Miami", "Boston", "Seattle",
        "Toronto", "Vancouver", "Montreal"
    ],
    "Country": [
        "USA"] * 5 + ["France"] * 5 + ["China"] * 5 + ["Mexico"] * 5 + ["UK", "UK", "UK", "Ireland", "Germany"] + 
        ["Germany", "Italy", "Italy", "Spain", "Spain"] + 
        ["Poland", "Czech Republic", "Hungary", "Austria", "Switzerland"] + ["USA"] * 5 + ["Canada"] * 3
    ,
    "Address": [
        "123 Main St", "456 Elm St", "789 Maple Ave", "101 Oak St", "102 Pine St", 
        "1 Rue de Rivoli", "2 Rue de la République", "3 Rue de Rome", "4 Alexanderplatz", "5 Marienplatz",
        "1 Nanjing Road", "2 Chang'an Street", "3 Zhongshan Avenue", "4 Shennan Boulevard", "5 Hebei Street",
        "1 Reforma Ave", "2 Juarez Ave", "3 Constitucion Ave", "4 Insurgentes Ave", "5 Kukulcan Blvd",
        "1 Oxford Street", "2 Piccadilly", "3 Regent Street", "4 O'Connell Street", "5 Zeil",
        "1 Jungfernstieg", "2 Via Montenapoleone", "3 Via Condotti", "4 La Rambla", "5 Gran Via",
        "1 Nowy Świat", "2 Wenceslas Square", "3 Andrássy Avenue", "4 Kärntner Strasse", "5 Bahnhofstrasse",
        "1 Market St", "2 Commerce St", "3 Biscayne Blvd", "4 Beacon St", "5 Pike St",
        "1 Yonge St", "2 Granville St", "3 Rue Sainte-Catherine"
    ]
}

df_addresses = pd.DataFrame(addresses_data)

routes_data = {
    "Route": ["Route A", "Route B", "Route C", "Route D", "Route E", "Route F"],
    "Start": ["New York", "Los Angeles", "Hamburg", "Shanghai", "Mexico City", "Paris"],
    "End": ["Rotterdam", "Tokyo", "Singapore", "Berlin", "Madrid", "Beijing"],
    "LatStart": [40.7128, 34.0522, 53.5511, 31.2304, 19.4326, 48.8566],
    "LonStart": [-74.0060, -118.2437, 9.9937, 121.4737, -99.1332, 2.3522],
    "LatEnd": [51.9225, 35.6895, 1.3521, 52.5200, 40.4168, 39.9042],
    "LonEnd": [4.47917, 139.6917, 103.8198, 13.4050, -3.7038, 116.4074]
}

df_routes = pd.DataFrame(routes_data)

# Combine start and end locations into a single DataFrame for st.map
df_map = pd.DataFrame({
    'lat': df_routes['LatStart'].tolist() + df_routes['LatEnd'].tolist(),
    'lon': df_routes['LonStart'].tolist() + df_routes['LonEnd'].tolist(),
    'Location': df_routes['Start'].tolist() + df_routes['End'].tolist(),
    'Type': ['Start']*len(df_routes['LatStart']) + ['End']*len(df_routes['LatEnd'])
})

# Display Map and Table Side by Side
col1, col2 = st.columns([2, 1])

with col1:
    
    if show_map:
        st.map(df_map[['lat', 'lon']])

with col2:
    st.dataframe(df_addresses)  # Removed the title

# Define the DataFrame for Financial Metrics
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
revenue = np.random.randint(80, 200, size=12).astype(float)
expenses = revenue - np.random.randint(20, 50, size=12)

# Introducing gaps
revenue[[2, 5, 8]] = np.nan
expenses[[1, 6, 9]] = np.nan

financial_data = {
    "Month": months,
    "Revenue": revenue,
    "Expenses": expenses,
}

df = pd.DataFrame(financial_data)

# Financial Metrics
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.subheader("Revenue and Expenses Over the Year")
fig = px.bar(df, x='Month', y=['Revenue', 'Expenses'], barmode='group', title="Monthly Revenue and Expenses", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='text-align: center; margin-top: 50px;'>© 2024 Made by Yoluko Solutions - Alexandre Kocev</div>", unsafe_allow_html=True)

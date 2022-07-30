import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from PIL import Image
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden; }
#         footer {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown("""
<style>
.new-font {
    font-size:15px !important;
    align: center;
}
</style>
""", unsafe_allow_html=True)
# col1, col2, col3 = st.columns(3)
data_url = ("Motor_Vehicle_Collisions_.csv")
# st.markdown("<h1 style='text-align: center'>Motor Vehicles Collisions in New York City</h1>", unsafe_allow_html=True)
html_temp = """
<div style="background-color:#9593D9;padding:10px">
<h1 style="color:white;text-align:center;">Motor Vehicles Collisions</h1>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)
original_data = data
dataset_old1=load_data(100000)
dataset_old=pd.DataFrame(dataset_old1.iloc[:,1:22])
dat_cat = pd.DataFrame(dataset_old.iloc[:,10:16].idxmax(axis=1,skipna=True),columns=['category'])
col = [dataset_old,dat_cat]
dataset = pd.concat(col,axis=1)



st.markdown("<h2 style='text-align: center'>Time Series Analysis</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>How many collisions occured during a given time of a day?</h3>", unsafe_allow_html=True)
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("<h4 style='text-align: center'>Vehicle Collisions between %i:00 and %i:00</h4>" % (hour, (hour + 1) % 24), unsafe_allow_html=True)
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
    "latitude": midpoint[0],
    "longitude": midpoint[1],
    "zoom": 11,
    "pitch": 50,
    },
    layers=[
    pdk.Layer(
    "HexagonLayer",
    data=data[['date/time', 'latitude', 'longitude']],
    get_position=['longitude', 'latitude'],
    radius=100,     #radius of bar
    extruded=True, #for 3d view
    pickable=True,
    elevation_scale=4,
    elevation_range=[0, 1000],
    ),
    ],
))

st.markdown("<h3 style='text-align: center'>Breakdown by minute between %i:00 and %i:00</h3>" % (hour, (hour + 1) %24), unsafe_allow_html=True)
filtered = data[
    (data['date/time'].dt.hour >= hour & (data['date/time'].dt.hour < (hour+1)))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig2 = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
col7, col8, col9 = st.columns(3)
with col7:
    st.write(' ')
with col8:
    st.write(fig2)
with col9:
    st.write(' ')


col10, col11, col12 = st.columns(3)
with col10:
    st.markdown("<h3 style='text-align: center'>Collision by Year</h3>", unsafe_allow_html=True)
    image4 = Image.open('screenshots/pic4.png')
    st.image(image4, caption='Collision by Year', width=550)
with col11:
    st.write(' ')
with col12:
    st.markdown("<h3 style='text-align: center'>Monthly Trends for each Borough</h3>", unsafe_allow_html=True)
    image5 = Image.open('screenshots/pic5.png')
    st.image(image5, caption='Collision by Year',width=550)


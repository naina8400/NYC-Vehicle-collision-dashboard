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
st.markdown('<p class="new-font">This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in NYC 🗽 </p>', unsafe_allow_html=True)
image = Image.open('screenshots/homepic.png')
st.image(image, caption='traffic',use_column_width=True)


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

###Adding the Category column###


dat_cat = pd.DataFrame(dataset_old.iloc[:,10:16].idxmax(axis=1,skipna=True),columns=['category'])
col = [dataset_old,dat_cat]
dataset = pd.concat(col,axis=1)
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
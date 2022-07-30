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






# st.markdown("<h2 style='text-align: center'> Fatality Analysis </h3>", unsafe_allow_html=True) 


# col16, col17, col18 = st.columns(3)
# with col16:
#     st.markdown("<h3 style='text-align: center'>Factors Responsible for Accidents</h3>", unsafe_allow_html=True)
#     image6 = Image.open('screenshots/pic6.png')
#     st.image(image6, caption='Collision by Year',width=500)
# with col17:
#     st.write(' ')
# with col18:
#     st.markdown("<h3 style='text-align: center'> Accident Rate for each Borough</h3>", unsafe_allow_html=True)
#     image7 = Image.open('screenshots/pic7.png')
#     st.image(image7, caption='Collision by Year',width=500)

col16, col17, col18 = st.columns(3)
with col16:
    st.write(' ')
with col17:
    st.markdown("<h3 style='text-align: center'>Factors Responsible for Accidents</h3>", unsafe_allow_html=True)
    image6 = Image.open('screenshots/pic6.png')
    st.image(image6, caption='Collision by Year',width=500)
with col18:
    st.write(' ')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.markdown("<h3 style='text-align: center'> Accident Rate for each Borough</h3>", unsafe_allow_html=True)
    image7 = Image.open('screenshots/pic7.png')
    st.image(image7, caption='Collision by Year',width=500)
with col3:
    st.write(' ')
    
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.markdown("<h3 style='text-align: center'> Types of Vehicle Involved</h3>", unsafe_allow_html=True)
    image7 = Image.open('screenshots/pic14.png')
    st.image(image7, caption='Collision by Year',width=500)
with col3:
    st.write(' ')

st.markdown("<h3 style='text-align: center'>Injury Rate and Death Rate</h3>", unsafe_allow_html=True)
image8 = Image.open('screenshots/pic8.png')
image9 = Image.open('screenshots/pic9.png')
col22, col23, col24 = st.columns(3)
with col22:
    st.image(image8,width=500)
with col23:
    st.write(' ')
with col24:
    st.image(image9,width=500)




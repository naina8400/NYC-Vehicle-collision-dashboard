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


st.markdown("<h2 style='text-align: center'>Collision Prone Areas</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>Where are the most people injured in NYC?</h3>", unsafe_allow_html=True)
injured_people = st.slider("Number of persons injured in collision  💥 🚗", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))
st.markdown("<h3 style='text-align: center'>Dangerous Streets in New York City</h3>", unsafe_allow_html=True)
street_count=data["on_street_name"].value_counts()
street_datafrm=pd.Series.to_frame(street_count) 
street_datafrm['id']=list(street_datafrm.index)
fig1 = px.histogram(street_datafrm.iloc[0:20,:],x="id",y="on_street_name",height=500,width=900,)

col7, col8, col9 = st.columns(3)
with col7:
    st.write(' ')
with col8:
    st.write(fig1)
with col9:
    st.write(' ')



st.markdown("<h3 style='text-align: center'>Top 5 dangerous streets by affected type</h3>", unsafe_allow_html=True)
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])

st.markdown("<h3 style='text-align: center'>Dangerous ZipCodes for each Borough</h3>", unsafe_allow_html=True)
image2 = Image.open('screenshots/pic2.png')
col4, col5, col6 = st.columns(3)
with col4:
    st.write(' ')
with col5:
    st.image(image2, caption='Dangerous ZipCodes',width=600)
with col6:
    st.write(' ')

image3 = Image.open('screenshots/pic3.png')
st.image(image3, caption='Dangerous ZipCodes over years',use_column_width=True)

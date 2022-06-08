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
    align: justify;
}
</style>
""", unsafe_allow_html=True)

data_url = ("Motor_Vehicle_Collisions_.csv")
st.title("Motor Vehicles Collisions in New York City")
st.markdown('<p class="new-font">This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in NYC 🗽 </p>', unsafe_allow_html=True)

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

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in collision  💥 🚗", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))


st.header("How many collisions occured during a given time of a day?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
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

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered = data[
    (data['date/time'].dt.hour >= hour & (data['date/time'].dt.hour < (hour+1)))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header(" Area and Category wise Analysis ") 
st.write("*This section will help you understand the specific areas of NYC with" 
    "the most number of accidents in the entire dataset along with category wise distribution.*")
pidata1 = dataset['borough'].value_counts()
pie_frame1 = pd.Series.to_frame(pidata1)
pie_frame1['Name'] = list(pie_frame1.index)
    #st.write(pie_frame1)
fig = px.pie(pie_frame1, values="borough",names="Name", title="Long-Form Input")
    #st.write(fig)
pidata2 =dataset['category'].value_counts()
pie_frame2 =pd.Series.to_frame(pidata2)
pie_frame2['Name']=list(pie_frame2.index)
    #st.write(pie_frame2)
fig = go.Figure()
fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},  {'type':'domain'}]],
            subplot_titles=['Area Wise Count',' ','Category Wise Count'])

fig.add_trace(go.Pie(labels=pie_frame1['Name'], values=pie_frame1['borough'], name="Area Wise Count",showlegend=False,
            textinfo='label+percent',insidetextorientation='radial',
            ),1, 1)

fig.add_trace(go.Pie(labels=pie_frame2['Name'], values=pie_frame2['category'], name="Category Wise Count",
            showlegend=False,textinfo='label+percent',insidetextorientation='radial',
            ),1, 3)

fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(hole=.4, hoverinfo="label+percent+name")
fig.update_layout(
    autosize=False,
    width=850,
    height=400,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
       
    ))
st.write(fig)


### BAR GRAPH FOR DANGEORUS STREETS ###
    

street_count=data["on_street_name"].value_counts()
street_datafrm=pd.Series.to_frame(street_count) 
street_datafrm['id']=list(street_datafrm.index)
fig = px.histogram(street_datafrm.iloc[0:20,:],x="id",y="on_street_name",height=500,width=900,)
st.write(fig)


st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)


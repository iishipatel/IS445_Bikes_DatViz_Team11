import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import plotly_express as px



st.title('Bike Rides Data Explorartion for IS445: Data Visualization')
st.header('Team Members: Aradhya Seth, Iishi Patel, Manvi Malhotra, Mitchell Lazarow, Yujin Sonn')

 # Loading and transforming data set

@st.cache
def load_data(nrows):
    df_ny = pd.read_csv("citibike_oct22.csv")
    df_wash = pd.read_csv('capitalbike_oct22.csv', on_bad_lines='skip')
    df_ny['city'] = 'New York'
    df_wash['city'] = 'Washington DC'
    df = pd.concat([df_ny, df_wash])
    df = df.dropna()
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    df['trip_duration'] = df['ended_at'] - df['started_at']
    df['date'] = df.started_at.dt.date
    print(df.tail())
    return df

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# Visualization 1

st.header('Daily Comparisons')
st.subheader('Number of Rides on daily basis')
option = st.selectbox(
    'Data For',
    ('All', 'New York', 'Washington DC'))

chart_data = data.groupby(['date', 'city']).size().reset_index(name='counts')
fig = px.bar(chart_data, x='date', y='counts',
             hover_data=['counts'], color='city',color_discrete_sequence=["blue", "red"], height=400)
if option == 'New York':
    chart_data = data[data['city']== 'New York'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data, x='date', y='counts',
             hover_data=['counts'],color_discrete_sequence=["blue"], height=400)
elif option == 'Washington DC':
    chart_data = data[data['city']== 'Washington DC'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data, x='date', y='counts',
             hover_data=['counts'],color_discrete_sequence=["red"], height=400)

st.plotly_chart(fig)

# Visualization 2

st.subheader('Daily Rides based on type of bike')
option1 = st.selectbox(
    'Data For',
    ('All', 'Classic Bike', 'Electric Bike', 'Docked Bike'))

chart_data1 = data.groupby(['date', 'rideable_type']).size().reset_index(name='counts')
fig = px.line(chart_data1, x='date', y='counts',
             hover_data=['counts', 'rideable_type'], color='rideable_type',color_discrete_sequence=['pink', 'orange', 'maroon'], height=400)
if option1 == 'Classic Bike':
    chart_data1 = data[data['rideable_type']=='classic_bike'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data1, x='date', y='counts',
             hover_data=['counts'], color_discrete_sequence=['pink'], height=400)
elif option1 == 'Electric Bike':
    chart_data1 = data[data['rideable_type']== 'electric_bike'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data1, x='date', y='counts',
             hover_data=['counts'], color_discrete_sequence=['orange'], height=400)
elif option1 == 'Docked Bike':
    chart_data1 = data[data['rideable_type']== 'docked_bike'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data1, x='date', y='counts',
             hover_data=['counts'], color_discrete_sequence=['maroon'], height=400)

st.plotly_chart(fig)

# Visualization 3

st.subheader('Daily Rides based on type of user')
option2 = st.selectbox(
    'Data For',
    ('All', 'Member', 'Casual'))

chart_data2 = data.groupby(['date', 'member_casual']).size().reset_index(name='counts')
fig = px.bar(chart_data2, x='date', y='counts',
             hover_data=['counts', 'member_casual'], color='member_casual',color_discrete_sequence=['green', 'purple'], height=400)
if option2 == 'Member':
    chart_data2 = data[data['member_casual']== 'member'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data2, x='date', y='counts',
             hover_data=['counts'],color_discrete_sequence=['purple'], height=400)
elif option2 == 'Casual':
    chart_data2 = data[data['member_casual']== 'casual'].groupby(['date']).size().reset_index(name='counts')
    fig = px.bar(chart_data2, x='date', y='counts',
             hover_data=['counts'],color_discrete_sequence=['green'], height=400)

st.plotly_chart(fig)

# Visualization 4
st.header('Map Visualizations')

start_date = st.slider(
    "Which date?",
    min_value=date(2022, 10, 1), 
    max_value = date(2022,10,31))

option3 = st.selectbox(
    'City',
    ('All', 'New York', 'Washington DC'))

st.subheader('Map of all starting locations on ' + str(start_date))

filtered_data1 = data[data['date'] == start_date][['start_lat', 'start_lng']]
if option3 != 'All':
    filtered_data1 = data[(data['date'] == start_date) & (data['city'] == option3)][['start_lat', 'start_lng']]
filtered_data1.rename(columns = {'start_lat':'lat', 'start_lng':'lon'}, inplace = True)

st.map(filtered_data1)

st.subheader('Map of all ending locations on ' + str(start_date))

filtered_data2 = data[data['date'] == start_date][['end_lat', 'end_lng']]
if option3 != 'All':
    filtered_data2 = data[(data['date'] == start_date) & (data['city'] == option3)][['end_lat', 'end_lng']]
filtered_data2.rename(columns = {'end_lat':'lat', 'end_lng':'lon'}, inplace = True)

st.map(filtered_data2)

# Visualization 5

st.header('Top N Popular Stations')
st.subheader('Start Stations')

n = st.slider(
    "Top N Start Stations?",
    min_value=1, 
    max_value = 20)

option4 = st.selectbox(
    'City for Start Station',
    ('New York', 'Washington DC'))

start_station_frequency = pd.DataFrame(data[data['city']==option4].start_station_name.value_counts())
start_station_frequency.rename(columns = {'index':'start_station_name', 'start_station_name':'frequency'}, inplace = True)
start_station_frequency = start_station_frequency.sort_values(by=['frequency'], ascending=False)# even sorted dataframe is not able to plot sorted bar chart

st.bar_chart(start_station_frequency.head(n))

st.subheader('End Stations')

n1 = st.slider(
    "Top N End Stations?",
    min_value=1, 
    max_value = 20)

option5 = st.selectbox(
    'City for End Station',
    ('New York', 'Washington DC'))

end_station_frequency = pd.DataFrame(data[data['city']==option5].end_station_name.value_counts())
end_station_frequency.rename(columns = {'index':'end_station_name', 'end_station_name':'frequency'}, inplace = True)
end_station_frequency = end_station_frequency.sort_values(by=['frequency'], ascending=False) # even sorted dataframe is not able to plot sorted bar chart

st.bar_chart(end_station_frequency.head(n1))


# Visualization 6

st.header('Distribution of bike types opted by users and their usage in New York and Washington DC')

df_top_station_bike_choice = data.groupby(['rideable_type', 'city']).size().reset_index(name='counts')

fig = px.bar(df_top_station_bike_choice, x='rideable_type', y='counts',
             hover_data=['counts', 'city'], color='city', height=400, color_discrete_map =
             {'Washington DC':'red', 'New York':'blue'})

# Plot!
st.plotly_chart(fig)

# Visualization 7

st.header('Distribution of bike types opted by users and their usage in New York and Washington DC')

df_top_station_bike_choice = data.groupby(['rideable_type', 'city']).size().reset_index(name='counts')

fig = px.bar(df_top_station_bike_choice, x='rideable_type', y='counts',
             hover_data=['counts', 'city'], color='city', height=400, color_discrete_map =
             {'Washington DC':'red', 'New York':'blue'})

st.plotly_chart(fig)


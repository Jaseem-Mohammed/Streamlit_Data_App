import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


#Seting title, sidebar title...
st.title("500 Most Valuable Players")
st.markdown('Analysing 500 most valuable players in world football according to transfermarkt.com')

st.sidebar.title('Analysing the most valuable players')


#loading the dataset
@st.cache(persist=True)
def load_data():
    data = pd.read_csv('C:/Users/JCM/Desktop/Python/Test_CSV_Files/MVP_TM_11-20.csv')
    return data


data = load_data()

#creating a radio for selecting different positions
st.sidebar.subheader('Playing Position of Players')
position = st.sidebar.radio('Position',
                            ['Left Winger', 'Right Winger', 'Centre-Forward',
                             'Attacking Midfield', 'Right-Back', 'Goalkeeper',
                             'Defensive Midfield', 'Second Striker', 'Left-Back',
                             'Centre-Back', 'Central Midfield', 'Right Midfield',
                             'Left Midfield'])


#create a dataframe with different country, players counts and names
@st.cache(persist=True)
def load_country():

    temp = data[data['Position'] == position]

    country_df = pd.DataFrame(temp.Country.value_counts()).reset_index()
    try:
        country_df =country_df[:10]
    except:
        country_df = country_df

    names = []
    for i in range(country_df.shape[0]):
        n = []
        c = country_df.iloc[i, 0]
        d = data.loc[(data['Country'] == c) & (data['Position'] == position)]
        for name in d['Name']:
            n.append(name)
        names.append(n)

    country_df['Names'] = names

    return country_df


country_df = load_country()

#creating checkbox to show or hide the country info
if st.sidebar.checkbox(f'Show top Countries with most players at {position} position', True, key=2):

    #selectbox for visualization type
    vis_country = st.selectbox('Visualization type', ['Bar Chart', 'List'], key=1)

    if vis_country == 'List':
        for i in range(country_df.shape[0]):
            st.markdown(f'**{country_df.iloc[i,0]} : {country_df.iloc[i,1]}**')

    else:
        fig = px.bar(country_df, x='index', y='Country', color='Country',
                     hover_data=['Names'], labels={'Country': 'Players count', 'index': 'Country'},
                     title=f"Countries with most players at {position}")
        st.plotly_chart(fig)


#create a dataframe with different clubs, players counts and names
@st.cache(persist=True)
def load_club():

    temp = data[data['Position']==position]
    club_df = pd.DataFrame(temp.club.value_counts()).reset_index()
    try:
        club_df = club_df[:10]
    except:
        club_df = club_df

    names = []
    for i in range(club_df.shape[0]):
        n = []
        c = club_df.iloc[i, 0]
        d = data.loc[(data['club'] == c) & (data['Position'] == position)]
        for name in d['Name']:
            n.append(name)
        names.append(n)

    club_df['Names'] = names

    return club_df


club_df = load_club()

if st.sidebar.checkbox(f'Show top Clubs with most players at {position} position', True, key=2):

    # selectbox for visualization type
    vis_club = st.selectbox('Visualization type', ['Bar Chart', 'List'], key=2)

    if vis_club == 'List':
        for i in range(club_df.shape[0]):
            st.markdown(f'**{club_df.iloc[i, 0]} : {club_df.iloc[i, 1]}**')

    else:
        fig = px.bar(club_df, x='index', y='club', color='club',
                     hover_data=['Names'], labels={'club': 'Players count', 'index': 'Club'},
                     title=f"Countries with most players at {position}")
        st.plotly_chart(fig)


#a slider for selecting age
st.sidebar.subheader('Select Age')
age = st.sidebar.slider('Age of the player', 17, 35)
player_data = data[data['Age'] == age][:1]

if age == 34:
    st.markdown('**There are no players in the list aged 34**')
else:
    if st.sidebar.checkbox('Show Best Player at the selected age',True, key=3):
        st.subheader(f'Most valuable player currently at the age of {age}')
        st.markdown(f'Name: {player_data.Name.values[0]}')
        st.markdown(f'Club: {player_data.club.values[0]}')
        st.markdown(f'Country: {player_data.Country.values[0]}')
        st.markdown(f'Market Value: £{player_data["Value"].values[0]}millions')
        st.markdown(f'Position: {player_data.Position.values[0]}')


if st.sidebar.checkbox('Show overall players Data at the age', False, key=4):
    st.subheader(f'Overall players Data at the age of {age}')
    if age == 34:
        st.markdown('')
    else:
        age_data = data[data['Age'] == age]
        st.markdown(f'Average market Value at the age of {age} = £{round(age_data.Value.mean(),2)}millions')
        st.markdown(f'Total number of players in the list aged {age} = {age_data.shape[0]}')
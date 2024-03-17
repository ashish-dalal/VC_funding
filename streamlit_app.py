import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Start-up Funding (India)", page_icon="🪙", layout="wide")


st.sidebar.title('Menu')
st.sidebar.divider()

startup_data = pd.read_csv('startup_cleaned.csv')
df = startup_data.copy()
df['investors'] = df['investors'].fillna('Not Known')

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df.drop(columns=['date'], inplace=True)




cities = {
    'Bangalore': [12.9716, 77.5946],
    'Gurgaon': [28.4595, 77.0266],
    'New Delhi': [28.6139, 77.2090],
    'Mumbai': [19.0760, 72.8777],
    'Chennai': [13.0827, 80.2707],
    'Pune': [18.5204, 73.8567],
    'Noida': [28.5355, 77.3910],
    'Faridabad': [28.4089, 77.3178],
    'San Francisco': [37.7749, -122.4194],
    'San Jose': [37.3387, -121.8853],
    'Amritsar': [31.6340, 74.8723],
    'Hyderabad': [17.4065, 78.4772],
    'Burnsville': [44.7677, -93.2777],
    'Menlo Park': [37.4529, -122.1817],
    'Palo Alto': [37.4419, -122.1430],
    'Santa Monica': [34.0242, -118.4965],
    'Singapore': [1.3521, 103.8198],
    'Haryana': [29.0588, 76.0856],
    'New York': [40.7128, -74.0060],
    'Karnataka': [15.3173, 75.7139],
    'Bhopal': [23.2599, 77.4126],
    'India': [20.5937, 78.9629],
    'Jaipur': [26.9124, 75.7873],
    'Nagpur': [21.1458, 79.0882],
    'Indore': [22.7196, 75.8577],
    'California': [36.7783, -119.4179],
    'Rourkela': [22.2604, 84.8544],
    'Srinagar': [34.0837, 74.7973],
    'Bhubaneswar': [20.2961, 85.8245],
    'Chandigarh': [30.7333, 76.7794],
    'Kolkata': [22.5726, 88.3639],
    'Coimbatore': [11.0168, 76.9558],
    'Udaipur': [24.5854, 73.7125],
    'Ahemdabad': [23.0225, 72.5714],
    'Surat': [21.1702, 72.8311],
    'Goa': [15.2993, 74.1240],
    'Uttar Pradesh': [27.1303, 80.8597],
    'Gaya': [24.7969, 85.0070],
    'Vadodara': [22.3072, 73.1812],
    'Trivandrum': [8.5241, 76.9366],
    'Missourie': [37.9643, -91.8318],
    'Panaji': [15.4909, 73.8278],
    'Gwalior': [26.2183, 78.1828],
    'Karur': [10.9606, 78.0810],
    'Udupi': [13.3409, 74.7421],
    'Kochi': [9.9312, 76.2673],
    'Agra': [27.1767, 78.0081],
    'Hubli': [15.3647, 75.1240],
    'Kerala': [10.8505, 76.2711],
    'Kozhikode': [11.2588, 75.7804],
    'USA': [37.0902, -95.7129],
    'Siliguri': [26.7271, 88.3953],
    'Lucknow': [26.8500, 80.9500],
    'Kanpur': [26.4499, 80.3319],
    'London': [51.5074, -0.1278],
    'Varanasi': [25.3176, 82.9739],
    'Jodhpur': [26.2389, 73.0243],
    'Boston': [42.3601, -71.0589],
    'Belgaum': [15.8497, 74.4977]
}

city_df = pd.DataFrame.from_dict(cities, orient='index', columns=['latitude', 'longitude'])
city_df.sort_index(inplace=True)
city_df.reset_index(inplace=True)
city_df['color'] = 1
city_df['color'] = city_df['color'].apply(lambda x: (random.random(),random.random(),random.random()))







def investor_details(investor):
    "### " + investor
    
    investor_mask = df['investors'].str.contains(investor)

    "#### ✅ *Recent Investments*"
    ""
    st.dataframe(startup_data[investor_mask][['date','startup','industry','city','round','amount']].set_index('startup').head(), use_container_width=True)


    
    "#### ✅ *Highest Investment*"
    ""
    highest_investments_df = df[investor_mask].groupby('startup').sum()['amount']
    
    highest_investment = df[df['investors'].str.contains(investor)].groupby('startup').sum().sort_values('amount', ascending=False).reset_index()

    figbar = px.bar(highest_investment.head(5) ,x='startup', y='amount', text_auto=True)
    figbar.update_traces(marker_color='#eabe6c')
    st.plotly_chart(figbar, use_container_width=True)
    
    ""
    col1, col2 = st.columns(2)
    with col1:
        "#### ✅ *Industry-wise Investments*"
        fig = px.pie(df[investor_mask].groupby('industry').sum().reset_index(), 
        values='amount', names='industry', hole=0.35, color_discrete_sequence=px.colors.sequential.Peach)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        "#### ✅ *Round-wise Investments*"
        fig2 = px.pie(df[investor_mask].groupby('round').sum().reset_index(), 
        values='amount', names='round', hole=0.35, color_discrete_sequence=px.colors.sequential.Purp)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    ""
    "#### ✅ *YoY Investment*"
    
    yoy_investor = df[investor_mask].groupby('year')['amount'].sum()

    temp_dict = dict()

    for i in range(2015,2021):    
        try:
            temp_dict[i] = yoy_investor.loc[i]
        except KeyError as e:
            temp_dict[i] = 0

    yoy_investment_correct = pd.DataFrame.from_dict(temp_dict, orient='index', columns=['amount']).reset_index().rename(columns={"index":"year"})

    figYoY = px.line(yoy_investment_correct, x="year", y="amount", text="amount", markers=True)
    figYoY.update_traces(textposition="bottom right")
    st.plotly_chart(figYoY, use_container_width=True)

    ""
    "#### ✅ *City and Industry wise Investments*"
    city_and_industry_df = df[df['investors'].str.contains(investor)].groupby(['city','industry']).sum().drop(columns='year').reset_index()
    city_and_industry_df['amount'] = city_and_industry_df['amount']/10**2

    figScatter = px.scatter(city_and_industry_df, x="city", y="industry", size="amount", color="city", size_max=70, 
        color_discrete_sequence=px.colors.qualitative.Light24, height=750)
    st.plotly_chart(figScatter, use_container_width=True)
        
def startup_details(startup):
    "## " + startup
    startup_mask = df['startup'].str.contains(startup)
    
    ""
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.metric("Industry", df[startup_mask].iloc[0,1])
    with col3:
        st.metric('Vertical', df[startup_mask].iloc[0,2])    
    with col1:
        if ((df[startup_mask]['amount'].sum()/1000000)<1):
            st.metric("Total Amount Raised", "$ {:.0f}".format(df[startup_mask]['amount'].sum()/1000)+"K")
        else:
            st.metric("Total Amount Raised", "$ {:.0f}".format(df[startup_mask]['amount'].sum()/1000000)+" Million")

    
    
    ""
    "## Based in " + df[startup_mask].iloc[0,3]
    #latitide = df[startup_mask]['latitude'].iloc[0]
    #longitude = df[startup_mask]['longitude'].iloc[0]
    
    #m = folium.Map(location=[latitide,longitude], zoom_start=10, width=400, height=400)
    st.map(df[startup_mask][['latitude','longitude']], size=(40,40), use_container_width=True)

        
    ""

    "### ✅ Past Investments"
    
    figBarh = px.bar(df[startup_mask].sort_values('amount'),x='amount',y='investors', orientation='h', text_auto=True)
    figBarh.update_traces(marker_color='#063970')
    st.plotly_chart(figBarh, use_container_width=True)

    col21, col22 = st.columns(2)
    
    with col21:
        "#### Funding Amount from Investors"
        figInvPie = px.pie(df[startup_mask].groupby('investors')['amount'].sum().reset_index(), 
            values='amount', names='investors', hole=0.35, color_discrete_sequence=px.colors.sequential.Purp)
        figInvPie.update_traces(textposition='outside', textinfo='label+percent')
        figInvPie.update_layout(showlegend=False)
        st.plotly_chart(figInvPie, use_container_width=True)

    with col22:
        "#### Funds Raised in Different Rounds"
        figRound = px.pie(df[startup_mask].groupby('round')['amount'].sum().reset_index(), 
            values='amount', names='round', hole=0.35, color_discrete_sequence=px.colors.sequential.Peach)
        figRound.update_traces(textposition='inside', textinfo='percent+label')
        figRound.update_layout(showlegend=False)
        st.plotly_chart(figRound, use_container_width=True)
    
    ""
    "## ✅ YoY Funding"
    funding_yoy = df[startup_mask].groupby('year')['amount'].sum()

    temp_dict2 = dict()

    for i in range(2015,2021):    
        try:
            temp_dict2[i] = funding_yoy.loc[i]
        except KeyError as e:
            temp_dict2[i] = 0

    funding_yoy_correct = pd.DataFrame.from_dict(temp_dict2, orient='index', columns=['amount']).reset_index().rename(columns={"index":"year"})

    figFundingYoY = px.line(funding_yoy_correct, x="year", y="amount", text="amount", markers=True)
    figFundingYoY.update_traces(textposition="bottom right")
    st.plotly_chart(figFundingYoY, use_container_width=True)

def overall():
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Total Funding Received', "$ "+str(round(df['amount'].sum()/1000000000))+" Billion")
    with col2:
        st.metric('Maximum Funds Raised', "$ "+str(round(df.groupby('startup')['amount'].sum().max()/1000000000))+" Billion")
    with col3:
        st.metric('Overall Average Funding', "$ "+str(round(df.groupby('startup')['amount'].sum().mean()/1000000))+" Million")


    ""
    "### ✅ *Total Investment Made (MoM)*"
    overallMoM = df.copy()
    temp = overallMoM.groupby(['year','month'])['amount'].sum().reset_index()
    temp['x-axis'] = temp['month'].astype('str') + "-" + temp['year'].astype('str')
    
    figOverall = go.Figure() 
    figOverall.add_trace(go.Scatter(x=temp['x-axis'], y=temp['amount'], mode='lines+markers', line=dict(color='#f8f1e9')))
    st.plotly_chart(figOverall, use_container_width=True)

    ""
    "### ✅ *Number of Investments (MoM)*"
    temp2 = overallMoM.groupby(['year','month'])['amount'].count().reset_index()
    temp2['x-axis'] = temp2['month'].astype('str') + "-" + temp2['year'].astype('str')
    
    figCount = px.bar(temp2, x='x-axis', y='amount', text_auto=True)
    figCount.update_traces(marker_color='#ffc6a5')
    st.plotly_chart(figCount, use_container_width=True)

    ""
    "### ✅ Top Startups and Investors"
    ""
    col6, col7 = st.columns(2)
    with col6:
        "#### Startups"
        figTopStartup = px.bar(df.groupby('startup').sum().sort_values('amount',ascending=False).head(9).reset_index().iloc[::-1,:], 
             orientation='h',
             x='amount',
             y='startup',
             text_auto=True)
        figTopStartup.update_traces(marker_color='#012677')
        st.plotly_chart(figTopStartup, use_container_width=True)
    with col7:
        "#### Investors"
        figTopInvestor = px.bar(df.groupby('investors').sum().sort_values('amount',ascending=False).head(9).reset_index().iloc[::-1,:], 
             orientation='h',
             x='amount',
             y='investors',
             text_auto=True,
             width=900)
        figTopInvestor.update_traces(marker_color='#012677')
        st.plotly_chart(figTopInvestor, use_container_width=True)


    ""
    "### ✅ *Industry Analysis*"
    industry = df.groupby('industry')
    ""
    col4, col5 = st.columns(2)

    with col4:
        "#### 1. Top 15 industry by total funding received"
        figPie1 = px.pie(industry['amount'].sum().sort_values(ascending=False).reset_index().head(15), names='industry', values='amount', height=550, width=550,hole=0.35, color_discrete_sequence=px.colors.sequential.Agsunset)
        figPie1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(figPie1, use_container_width=True)
    with col5:
        "#### 2. Top 15 industry by number of startups funded"
        figPie2 = px.pie(industry['amount'].count().sort_values(ascending=False).reset_index().head(15), names='industry', values='amount', height=550, width=550, hole=0.35, color_discrete_sequence=px.colors.sequential.YlGnBu)
        figPie2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(figPie2, use_container_width=True)
    

    "#### 3. Top 15 Industry Max vs Average funding"
    indusBarMax = industry['amount'].max().sort_values(ascending=False).head(20)
    top15indus = list(industry['amount'].max().sort_values(ascending=False).head(20).keys())

    indusBarMean = industry['amount'].mean().loc[top15indus]

    fig = go.Figure()
    fig.add_trace(go.Bar(orientation='v',x=indusBarMax.reset_index()['industry'], y=indusBarMax.reset_index()['amount'], name='Industry Max', marker_color='indianred'))
    fig.add_trace(go.Bar(orientation='v',x=indusBarMean.reset_index()['industry'], y=indusBarMean.reset_index()['amount'], name='Industry Average',marker_color='lightsalmon'))
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    ""
    #m = folium.Map(location=[28.6139, 77.2090], zoom_start=8)
    temp_city = df.groupby('city')['amount'].sum().reset_index()
    city_df['amount'] = temp_city['amount']/100000
    st.map(city_df,
    latitude='latitude',
    longitude='longitude', 
    size='amount',
    color='color')

    ""
    "### ✅ *Most Funded Investment Rounds*"
    
    rounds = df.groupby('round')
    
    col8, col9 = st.columns(2)
    with col8:
        "#### 1. By Number of Investments"
        figRoundPie = px.pie(rounds['amount'].count().sort_values(ascending=False).reset_index().head(8), 
                names='round', values='amount', 
                height=400 ,hole=0.35, 
                color_discrete_sequence=px.colors.sequential.Agsunset)
        figRoundPie.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(figRoundPie, use_container_width=True)
    
    with col9:
        "#### By Total Amount of Investment"
        figRoundPie2 = px.pie(rounds['amount'].sum().sort_values(ascending=False).reset_index().head(8), 
             names='round', values='amount', 
             height=400 ,hole=0.35, 
             color_discrete_sequence=px.colors.sequential.YlGnBu)
        figRoundPie2.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(figRoundPie2, use_container_width=True)

    
     
    





st.session_state.option = st.sidebar.selectbox('Type', ['Start-up','Investor','Overall'], key='analysis')

MainSidebarOption = st.session_state.option

if MainSidebarOption == 'Overall':
    st.title('Overall Analysis')
    st.divider()
    st.sidebar.write('')
    st.sidebar.write('')
    btn1 = st.sidebar.button('Go')

    if btn1:
        overall()

elif MainSidebarOption == 'Start-up':
    selected_startup = st.sidebar.selectbox('Start-up', sorted(list(df['startup'].unique())))
    st.sidebar.write('')
    st.sidebar.write('')
    btn2 = st.sidebar.button('Go')
    st.title('Start-up')
    st.divider()

    if btn2:
        startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Investors', sorted(set(df['investors'].str.split(',').sum())))
    st.sidebar.write('')
    st.sidebar.write('')
    btn3 = st.sidebar.button('Go')
    st.title('Investor')
    st.divider()

    if btn3:
        investor_details(selected_investor)

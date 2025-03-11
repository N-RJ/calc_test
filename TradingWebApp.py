import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
from PySimFin import PySimFin

# Load Data
df3=pd.read_csv("sharepricesss.csv")
@st.cache_data
def load_data():
    companies = pd.read_csv("companiess.csv")  # Use the actual CSV data
    return companies

companies = load_data()

# Sidebar Navigation
st.sidebar.title("Trading System Dashboard")
page = st.sidebar.radio("Navigate", ["Home", "Company Info", "Predictions", "Meet the team!"])

# Function to display team member profiles
def display_team_member(name, role, bio, fun_fact, image_path):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_path, width=150)
    with col2:
        st.subheader(name)
        st.markdown(f"**Role:** {role}")
        st.write(bio)
        st.markdown(f"🎉 **Fun Fact:** {fun_fact}")

if page == "Home":
    st.title("📈 Share Price Predictor")

    # System Overview
    st.markdown("## Overview")
    st.markdown(
        """
        Welcome to the **Automated Daily Trading System**, a cutting-edge platform designed 
        to analyze stock market trends and generate predictive insights. This system integrates 
        financial data analytics and machine learning to provide real-time stock market 
        predictions and investment guidance.
        """
    )

    # System Purpose and Objectives
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown("## System Purpose & Objectives")
    st.markdown(
        """
        - **Market Forecasting**: Utilize historical stock data to predict future market trends.
        - **Investment Insights**: Support investors in making data-driven decisions.
        - **Real-time Monitoring**: Provide updated stock price information and company analytics.
        - **User-Friendly Interface**: Enable intuitive interaction with stock predictions and analytics.
        """
    )

    # Dropdown to select a company
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown("## Select a company for the study:")


# Load Data
@st.cache_data
def load_data():
    companies = pd.read_csv("companiess.csv")
    return companies

companies= load_data()


if page == "Company Info":
    st.title("📊 Company Info")

    # Dropdown to select a stock
    st.markdown("### Select a Company to View Stock Performance")
    selected_comp_name = st.selectbox("Choose a company name:", df3["Company Name"].unique())

    # Filter data for the selected stock
    stock_df = df3[df3["Company Name"] == selected_comp_name]

    # Display selected company details
    company_info = companies[companies["Company Name"] == selected_comp_name]
    if not company_info.empty:
        st.markdown(f"### 📌 {company_info.iloc[0]['Company Name']}")
        st.write(f"**Industry ID:** {company_info.iloc[0]['IndustryId']}")
        st.write(f"**Number of Employees:** {int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A':,}".replace(",","."))
        st.write(f"**Market:** {company_info.iloc[0]['Market']}")
        st.write(f"**Currency:** {company_info.iloc[0]['Main Currency']}")

    # Get latest stock data
    latest_data = stock_df.iloc[-1]

    # Handle Missing 'Change' Column
    if 'Change' in stock_df.columns:
        change_value = f"{latest_data['Change']}%"
    else:
        if len(stock_df) > 1:
            change_value = f"{((latest_data['Close'] - stock_df.iloc[-2]['Close']) / stock_df.iloc[-2]['Close'] * 100):.2f}%"
        else:
            change_value = "N/A"

    # Display Stock Metrics
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.metric(label="Current Price", value=f"${latest_data['Close']:.2f}", delta=change_value)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Open", f"${latest_data['Open']:.2f}")
    col2.metric("📉 Low", f"${latest_data['Low']:.2f}")
    col3.metric("📊 High", f"${latest_data['High']:.2f}")
    col4.metric("🔄 Volume", f"{latest_data['Volume']:,}")

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown("### 📊 Candlestick Chart")
    fig_candle = go.Figure(data=[
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name=selected_comp_name
        )
    ])
    fig_candle.update_layout(title=f"{selected_comp_name}", template="plotly_dark",xaxis_title="Date",yaxis_title="Close")
    st.plotly_chart(fig_candle, use_container_width=True)

    st.markdown("### 📊 Compare Stocks")
    tickers_selected = st.multiselect("Select multiple stocks:", df3["Company Name"].unique(), default=[selected_comp_name])
    
    if tickers_selected:
        compare_df = df3[df3["Company Name"].isin(tickers_selected)]
        fig_compare = px.line(compare_df, x="Date", y="Close", color="Ticker", title="Stock Comparison")
        st.plotly_chart(fig_compare, use_container_width=True)

elif page == "Predictions":
    st.title("🔮 Market Predictions")
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    predict_comp_name = st.selectbox("Please choose the desired company name:", df3["Company Name"].unique())
    predict_df = df3[df3["Company Name"] == predict_comp_name]
    comp_tick=predict_df["Ticker"][0]
    min_date = datetime.date(2018, 1, 1)
    max_date = datetime.date.today()
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        start_date=st.date_input('Please insert start date',min_value=min_date,max_value=max_date)
    with col2:
        end_date=st.date_input('Please insert end date',min_value=min_date,max_value=max_date)
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.title("Prediction result:")
    #input_data=PySimFin(comp_tick,start_date,end_date)


elif page == "Meet the team!":
    st.markdown("## 👥 Meet the Team!")
    st.markdown("Our team brings together expertise in machine learning, financial analytics, business strategy, and web development.")

    # Team Members
    display_team_member(
        "Leonardo V. Kietzell", 
        "🚀 Lead Business Strategist", 
        "🇩🇪 Leonardo is from Germany and brings **years of consulting and business strategy insights** to the project. 📊 His expertise in **decision-making & market analysis** helped shape the vision of our trading system.", 
        "🏃‍♂️ He is currently training for the **Tokyo Marathon**! 🎌", 
        "Leonardo.jpeg"
    )

    display_team_member(
        "Gizela Thomas", 
        "💻 Streamlit Developer", 
        "🇺🇸 Gizela is from the USA and has **experience in consulting** but primarily works in the **health sector**. 🏥 She was responsible for building the **Streamlit interface**, ensuring a smooth and user-friendly experience.", 
        "📰 She has been on the **front page of Yahoo News**! 🌟", 
        "gizela.jpeg"
    )

    display_team_member(
        "Nitin Jangir", 
        "🤖 Machine Learning Engineer", 
        "🇮🇳 Nitin is from India and is using his **master’s degree** to strengthen his technical skills. 🎓 He worked on **building predictive analytics models** and wants to pursue a career in **data engineering**. 📊", 
        "🍳 Since moving to Spain, he started **eating eggs for the first time** despite being a lifelong vegetarian! 🥚", 
        "nitin.jpeg"
    )

    display_team_member(
        "Santiago Ruiz Hernández", 
        "📌 Project Point Lead", 
        "🇪🇸 Santiago is from Valencia, Spain, and worked on **various aspects of the project**, acting as a key **point lead** to keep everything running smoothly. 🔄 His contributions touched on multiple areas of **EDA, strategy, and technical implementation**.", 
        "🎾 He **loves playing padel** and is a **natural redhead**! 🔥", 
        "santi.jpeg"
    )

    display_team_member(
        "Santiago Botero", 
        "📈 EDA & Financial Insights", 
        "🇨🇴 Santiago is from Colombia, has a **finance background**, and is currently pursuing a **dual MBA**. 🎓 He was responsible for **exploratory data analysis (EDA)**, ensuring the financial data was properly analyzed and interpreted. 📉", 
        "🌍 He speaks **four languages fluently**! 🗣️🌎", 
        "santiago.jpeg"
    )

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np








# Load Data
@st.cache_data
def load_data():
    companies = pd.read_csv("companies.csv")  # Use the actual CSV data
    return companies

companies = load_data()

# Sidebar Navigation
st.sidebar.title("Trading System Dashboard")
page = st.sidebar.radio("Navigate", ["Home", "Company Info", "Stock Prices", "Predictions", "Personal Profile"])

# Function to display the banner
def display_banner():
    st.image("stockimage.jpg", use_column_width=True)

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

### ✅ FIXED: Keep everything inside the `if page == "Home":` block ###
if page == "Home":
    st.title("📈 Automated Daily Trading System")

    # Display Banner
    display_banner()

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
    st.markdown("## System Purpose & Objectives")
    st.markdown(
        """
        - **Market Forecasting**: Utilize historical stock data to predict future market trends.
        - **Investment Insights**: Support investors in making data-driven decisions.
        - **Real-time Monitoring**: Provide updated stock price information and company analytics.
        - **User-Friendly Interface**: Enable intuitive interaction with stock predictions and analytics.
        """
    )

    # ✅ Move "Meet the Team" inside the "Home" page
    st.markdown("## 👥 Meet the Team")
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
        "🎾 He **loves playing tennis** and is a **natural redhead**! 🔥", 
        "santi.jpeg"
    )

    display_team_member(
        "Santiago Botero", 
        "📈 EDA & Financial Insights", 
        "🇨🇴 Santiago is from Colombia, has a **finance background**, and is currently pursuing a **dual MBA**. 🎓 He was responsible for **exploratory data analysis (EDA)**, ensuring the financial data was properly analyzed and interpreted. 📉", 
        "🌍 He speaks **four languages fluently**! 🗣️🌎", 
        "santiago.jpeg"
    )












# ✅ Company Info Page (Now correctly after `if`)
elif page == "Company Info":
    display_banner()
    st.title("🏢 Company Information")

    st.markdown("""
        Explore detailed **company profiles** listed in our trading system.
        
        - View **industry classification**.
        - Check the **number of employees**.
        - See **market & currency details**.
    """)
    # KPIs
    total_companies = companies.shape[0]
    avg_employees = companies["Number Employees"].mean()
    top_industries = companies["IndustryId"].value_counts().head(5)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Companies Listed", total_companies)
    col2.metric("Avg. Employees per Company", f"{avg_employees:,.0f}")

    # Dropdown to select a company
    ticker = st.selectbox("Select a Company Ticker", companies["Ticker"].unique())
    company_info = companies[companies["Ticker"] == ticker]

    # Display company details
    if not company_info.empty:
        st.write(f"### {company_info.iloc[0]['Company Name']}")
        st.write(f"**Industry ID:** {company_info.iloc[0]['IndustryId']}")
        st.write(f"**Number of Employees:** {int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A'}")
        st.write(f"**Market:** {company_info.iloc[0]['Market']}")
        st.write(f"**Currency:** {company_info.iloc[0]['Main Currency']}")
    else:
        st.write("No company data available.")



    
    # Filters
    st.sidebar.markdown("### 🔍 Filter Companies")
    selected_ticker = st.sidebar.selectbox("Select a Company", ["All"] + list(companies["Company Name"].dropna().unique()))
    selected_year = st.sidebar.selectbox("Filter by Financial Year-End", ["All"] + sorted(companies["End of financial year (month)"].dropna().astype(int).unique()))
    selected_size = st.sidebar.slider("Filter by Number of Employees", min_value=0, max_value=int(companies["Number Employees"].max()), value=(0, int(companies["Number Employees"].max())))
    
    # Apply Filters
    filtered_companies = companies.copy()
    if selected_ticker != "All":
        filtered_companies = filtered_companies[filtered_companies["Company Name"] == selected_ticker]
    if selected_year != "All":
        filtered_companies = filtered_companies[filtered_companies["End of financial year (month)"] == selected_year]
    filtered_companies = filtered_companies[(filtered_companies["Number Employees"] >= selected_size[0]) & (filtered_companies["Number Employees"] <= selected_size[1])]
    
    # Industry Distribution Chart
    st.markdown("### 🏢 Industry Distribution")
    industry_counts = filtered_companies["IndustryId"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Company Count"]
    fig = px.bar(industry_counts, x="Industry", y="Company Count", title="Top Industries by Number of Companies")
    st.plotly_chart(fig)
    
    # Top Companies by Employees
    st.markdown("### 🏆 Top Companies by Employee Count")
    top_companies = filtered_companies.nlargest(10, "Number Employees")[["Company Name", "Number Employees"]]
    st.dataframe(top_companies)

    # Industry Distribution Chart (Fixed)
    st.markdown("### 🏢 Industry Distribution")

    # Convert IndustryId to string (prevents it from being treated as a number)
    filtered_companies["IndustryId"] = filtered_companies["IndustryId"].astype(str)

    # Count the number of companies in each industry
    industry_counts = filtered_companies["IndustryId"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Company Count"]

    # Take the top 10 industries for better readability
    industry_counts = industry_counts.head(10).sort_values(by="Company Count", ascending=False)

    # Plot fixed bar chart
    fig = px.bar(
        industry_counts, 
        x="Industry", 
        y="Company Count", 
        title="Top Industries by Number of Companies",
        text="Company Count",  # Display company count on bars
        template="plotly_white"  # Use a cleaner layout
    )

    # Improve layout
    fig.update_traces(marker_color="blue", textposition="outside")
    fig.update_xaxes(title_text="Industry", tickangle=-45)  # Rotate labels for readability
    fig.update_yaxes(title_text="Company Count")

    # Show fixed chart
    st.plotly_chart(fig)











# ✅ Stock Prices Page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load Data
@st.cache_data
def load_data():
    companies = pd.read_csv("companies.csv")  
    stock_data = pd.read_csv("shareprices.csv")
    return companies, stock_data

companies, stock_data = load_data()


# Ensure there is an `if` before `elif`


if page == "Stock Prices":  # ✅ This must be properly indented
    st.title("📊 Stock Price Data")

    # Dropdown to select a stock
    st.markdown("### Select a Company to View Stock Performance")
    selected_ticker = st.selectbox("Choose a stock ticker:", stock_data["Ticker"].unique())

    # Filter data for the selected stock
    stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

    # Display selected company details
    company_info = companies[companies["Ticker"] == selected_ticker]
    if not company_info.empty:
        st.markdown(f"### 📌 {company_info.iloc[0]['Company Name']}")
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
    st.metric(label="Current Price", value=f"${latest_data['Close']:.2f}", delta=change_value)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Open", f"${latest_data['Open']:.2f}")
    col2.metric("📉 Low", f"${latest_data['Low']:.2f}")
    col3.metric("📊 High", f"${latest_data['High']:.2f}")
    col4.metric("🔄 Volume", f"{latest_data['Volume']:,}")

    # 📊 Line Chart for Stock Prices Over Time
    st.markdown("### 📈 Stock Price Trend")
    fig = px.line(stock_df, x="Date", y="Close", title=f"{selected_ticker} Stock Price Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # ✅ Fixed Candlestick Chart using `go.Figure()`
    st.markdown("### 📊 Candlestick Chart")
    fig_candle = go.Figure(data=[
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name=selected_ticker
        )
    ])
    fig_candle.update_layout(title=f"{selected_ticker} Candlestick Chart", template="plotly_dark")
    st.plotly_chart(fig_candle, use_container_width=True)

    # 🔍 Compare Multiple Stocks
    st.markdown("### 📊 Compare Stocks")
    tickers_selected = st.multiselect("Select multiple stocks:", stock_data["Ticker"].unique(), default=[selected_ticker])
    
    if tickers_selected:
        compare_df = stock_data[stock_data["Ticker"].isin(tickers_selected)]
        fig_compare = px.line(compare_df, x="Date", y="Close", color="Ticker", title="Stock Comparison")
        st.plotly_chart(fig_compare, use_container_width=True)

elif page == "Predictions":
    st.title("🔮 Market Predictions")
    st.write("This feature is coming soon!")

















 

# ✅ Predictions Page
elif page == "Predictions":
    display_banner()
    st.title("🔮 Predictive Analytics")
    st.markdown("📌 **Feature Coming Soon!**")

# ✅ Personal Profile Page
elif page == "Personal Profile":
    display_banner()
    st.title("👤 Personal Profile")
    st.markdown("📌 **Feature Coming Soon!**")

# ✅ Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed with ❤️ using Streamlit")

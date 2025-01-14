import streamlit as st
import time
import pandas as pd
import requests
import altair as alt
import calendar
from millify import millify  # type: ignore
from jamaibase import JamAI, protocol as p  # type: ignore

def about_page():
    print('\n\n')
    print('---------------------------------------------Runing page About---------------------------------------------')
    st.markdown("""
    # **About This Web Application ℹ️**

    ---

    ### **Overview**
    This Streamlit Web application is part of a **Data Science project** aimed at exploring the impact of climate variability on palm oil yields in Malaysia. By leveraging advanced machine learning models and historical climate data, the application offers actionable insights into the yields of **Fresh Fruit Bunches (FFB)** and **Crude Palm Oil (CPO)**.  
    
    🌟 The goal of this project is to **help stakeholders assess the effects of climate variability** and plan for future scenarios to ensure sustainable palm oil production.

    The project uses **climate projections** and key climate variables such as precipitation, temperature, humidity, and drought indices to provide accurate yield forecasts and uncover patterns that influence palm oil yields over time.

    ---

    ### **✨ Features**
    - 📊 **Dashboard**: 
        - Visualize historical and current palm oil yields alongside climate trends.
        - Explore key metrics such as Fresh Fruit Bunch (FFB) and Crude Palm Oil (CPO) yields over time.
        - Generate dynamic AI summaries to gain actionable insights.
    - 🔮 **Yield Prediction Tool**: 
        - Predict future yields based on manual input or climate projections.
        - Analyze "what-if" scenarios for strategic decision-making.

    ---

    ### **🛠️ How to Use**
    1. **Navigate**:
        - Use the **sidebar** to access different sections of the app.
    2. **Dashboard**:
        - **Select a year** to view specific yield metrics and trends.
        - **Choose a commodity**: Fresh Fruit Bunches Yield, Crude Palm Oil Yield, or Fresh Fruit Bunches Production.
        - **Generate AI Summary**: Obtain automated insights and trends for the selected year and commodity.

    3. **Yield Prediction Tool**:
        - **Select a prediction method**: 
            - **Manual Input**:
                - Adjust sliders to simulate specific climate conditions.
                - View the resulting yield predictions for FFB and CPO.
            - **Climate Projection**:
                - Choose a Shared Socioeconomic Pathway (SSP) scenario.
                - Select the **month** and **year** using sliders.
                - View projected climate conditions and corresponding yield predictions.

    ---

    """)
about_page()
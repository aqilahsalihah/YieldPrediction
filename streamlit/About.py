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
    This Streamlit Web application leverages advanced machine learning models and historical climate data to provide actionable insights into palm oil yields.  
    🌟 Designed for stakeholders to **assess the impacts of climate variability** and plan for future scenarios.

    ---

    ### **✨ Features**
    - 📊 **Dashboard**: 
        - Visualize historical and current palm oil yields alongside climate trends.
        - Explore key metrics such as Fresh Fruit Bunch (FFB) and Crude Palm Oil (CPO) yields over time.
    - 🔮 **Yield Prediction Tool**: 
        - Predict future yields based on manual input or climate projections.
        - Analyze "what-if" scenarios for strategic decision-making.

    ---

    ### **🛠️ How to Use**
    1. **Navigate**:
        - Use the **sidebar** to access different sections of the app.
    2. **Dashboard**:
        - Explore key metrics, historical trends, and monthly yield comparisons.
    3. **Yield Prediction Tool**:
        - Enter climate variables manually or use predefined climate scenarios to forecast future yields.

    ---

    ### **🔍 About the Models**
    The predictive models are trained using **historical climate and yield data**, incorporating climate variables such as:
    - ☔ **Precipitation**: Annual and monthly rainfall totals.
    - 🌡️ **Temperature**: Includes average, maximum, and minimum temperatures.
    - 🌵 **Drought Index (SPEI12)**: Measures water deficits considering evapotranspiration.
    - 🏜️ **Cumulative Dry Days**:  Number of consecutive  days where precipitation < 1mm
    - 🌧️ **Cumulative Wet Days**: Number of consecutive  days where precipitation >= 1mm

    Models such as **Random Forest Regressor** and **Extra Trees Regressor** predict:
    - Fresh Fruit Bunch (FFB) yield (tons/ha).
    - Crude Palm Oil (CPO) yield (tons/ha).

    """)
about_page()
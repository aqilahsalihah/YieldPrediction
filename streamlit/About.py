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
    st.title("About This App ℹ️")
    st.markdown("""
    ## Overview
    This Streamlit app is designed to provide insights and predictions related to palm oil yield. It leverages machine learning models to forecast the yield of Fresh Fruit Bunches (FFB) and Crude Palm Oil (CPO) based on various climate variables.

    ## Features
    - **Dashboard**: Visualize historical and current yield data, including key metrics and trends.
    - **Yield Prediction Tool**: Predict future yields based on manual input or climate projections.

    ## How to Use
    1. **Navigate**: Use the sidebar to navigate between different pages of the app.
    2. **Dashboard**: View key metrics, trends, and monthly yield comparisons.
    3. **Yield Prediction Tool**: Input climate data manually or use climate projections to predict future yields.

    ## About the Models
    The prediction models are trained using historical climate and yield data. They utilize a wide range of climate variables, including precipitation, temperature, and humidity, to provide accurate yield forecasts.
    """)
about_page()
    # - **AI Insights**: Generate AI-driven summaries using LLM models to understand the impact of climate conditions on palm oil yield.
    # 4. **AI Insights**: Click the "Generate AI Insights" button to get AI-driven insights based on the collected data.
import streamlit as st
import time
import pandas as pd
import requests
import altair as alt
import joblib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import calendar
from millify import millify

st.set_page_config(
    page_title="Palm Yield Insight Dashboard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded")

pages = {
    'Navigation': [
        st.Page('About.py', title='About'),
        st.Page('Dashboard.py', title='Dashboard'),
        st.Page('PredictionTool.py', title='Prediction Tool'),
    ]
}

pg = st.navigation(pages)
pg.run()

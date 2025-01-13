import joblib  # type: ignore
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data

def load_model(path):
    model = joblib.load(path)
    return model

def page2():
    print('\n\n')
    print('---------------------------------------------Runing page Prediction Tool---------------------------------------------')
    st.title('Yield Prediction Tool 🔨')
    
    # Load the prediction models
    ffb_model = load_model('streamlit/ffb_yield_model2.pkl')
    cpo_model = load_model('streamlit/cpo_yield_model2.pkl') 
    cpo_model_new = load_model('streamlit/cpo_yield_model5.pkl') 
    ffb_model_new = load_model('streamlit/ffb_yield_model5.pkl') 
     

        
    tabs = st.tabs(['Model Overview', 'Manual input', 'Climate Projections'])
    with tabs[0]:
        st.markdown("""
                    <div style="text-align: justify;">
                        <h3 style="color: #4CAF50; font-size: 24px;">🌟 Model Overview</h3>
                        <p>
                            This prediction tool utilizes <b>machine learning</b> to forecast the yield of <b>Fresh Fruit Bunches (FFB)</b> and <b>Crude Palm Oil (CPO)</b> based on a wide range of climate variables. It is designed to help stakeholders understand the impact of climate variability on palm oil production and plan accordingly.
                        </p>
                        <p>
                            The model integrates the following key climate variables:
                            <ul style="margin-left: 20px;">
                                <li><b>🌧️ Precipitation:</b> Total rainfall amounts.</li>
                                <li><b>🌡️ Temperature:</b> Includes average, maximum, and minimum temperatures.</li>
                                <li><b>💧 Humidity:</b> Atmospheric moisture levels.</li>
                                <li><b>📉 SPEI12:</b> The Standardized Precipitation Evapotranspiration Index, which measures long-term (12-month) water deficits considering temperature-driven evapotranspiration.</li>
                                <li><b>🔥 CDD (Cumulative Dry Days):</b> The total number of consecutive days with precipitation < 1 mm, representing prolonged dry periods.</li>
                                <li><b>🌧️ CWD (Cumulative Wet Days):</b> The total number of consecutive days with precipitation ≥ 1 mm, representing prolonged wet conditions.</li>
                            </ul>
                        </p>
                        <p>
                            Trained on <b>historical climate and yield data</b>, the model achieves:
                            <ul style="margin-left: 20px;">
                                <li>Validation Score: <b>0.70</b> for FFB and <b>0.69</b> for CPO.</li>
                                <li>Mean Error (MSE): <b>0.10</b> for both models.</li>
                            </ul>
                            These metrics demonstrate the model's robust performance in capturing complex relationships between climate factors and palm oil yields.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    with tabs[1]:    
        st.subheader('Manual Input')
        st.write('Input the climate data to predict the FFB yield')
        col = st.columns((1, 1, 1), gap='medium')

        with col[0]:
            month = st.slider("Select Month of Harvest", min_value=1, max_value=12, value=1, step=1)
            pr = st.slider("Precipitation (mm)", min_value=0.0, max_value=500.0, value=100.0, step=0.001)
            pr_3y = pr * 36
            pr_2y = pr * 24
            pr_1y = pr * 12
            tas = st.slider("Temperature (°C)", min_value=24.0, max_value=30.0, value=25.0, step=0.001)
            tasmin = st.slider("Minimum Temperature (°C)", min_value=22.0, max_value=tas, value=25.0, step=0.001)
            tasmax = st.slider("Maximum Temperature (°C)", min_value=tas, max_value=35.0, value=30.0, step=0.001)
            tas_range = tasmax - tasmin

        # Place sliders in the second column
        with col[1]:
            hurs = st.slider("Humidity (%)", min_value=70.0, max_value=100.0, value=80.0, step=1.0)
            spei12 = st.slider("Drought index", min_value=-1.2, max_value=1.2, value=0.0, step=0.01)
            prpercnt = st.slider("Precipitation Percent Change", min_value=-45.0, max_value=62.0, value=50.0, step=0.1) + 100
            cdd = st.slider("Consecutive Dry Days", min_value=0.0, max_value=15.0, value=2.0, step=0.5)
            cwd = st.slider("Consecutive Wet Days", min_value=5.0, max_value=31.0, value=25.0, step=0.5)
            # sd = st.slider("Summer Days (num of days where tmax > 25°C)", min_value=0.0, max_value=12.0, value=6.0, step=0.1)

        
        with col[2]:
            st.subheader('Predicted Yield')
            # ffb_input_df = pd.DataFrame([[month, pr, pr_3y, tas, tasmin, tasmax, tas_range, hurs]], columns=['Month','pr', 'rolling_pr_3y', 'tas', 'tasmin', 'tasmax', 'tas_range', 'hurs'])
            ffb_input_df = pd.DataFrame([[month, pr, prpercnt, hurs, spei12, tas, tasmin, tasmax, cdd, cwd, 30, tas_range, pr_3y, pr_2y, pr_1y]], columns=['Month', 'pr', 'prpercnt', 'hurs', 'spei12', 'tas', 'tasmin', 'tasmax','cdd', 'cwd', 'sd', 'tas_range', 'rolling_pr_3y', 'rolling_pr_2y', 'rolling_pr_1y'])
            ffb_pred = ffb_model_new.predict(ffb_input_df)[0]
            threshold_ffb = 1.38
            st.metric(label="Predicted FFB Yield", 
                      value=f"{ffb_pred:.2f}  (tons/ha)", 
                      delta=f"{ffb_pred - threshold_ffb:.2f} compared to historical average",
                      border = True)
            st.divider()
            st.divider()
                
            # cpo_input_df = pd.DataFrame([[month, pr, pr_3y, tas, tasmin, tasmax, tas_range, hurs]], columns=['Month','pr', 'rolling_pr_3y', 'tas', 'tasmin', 'tasmax', 'tas_range', 'hurs'])
            cpo_input_df = pd.DataFrame([[month, pr, prpercnt, hurs, spei12, tas, tasmin, tasmax, cdd, cwd, 30, tas_range, pr_3y, pr_2y, pr_1y]], columns=['Month', 'pr', 'prpercnt', 'hurs', 'spei12', 'tas', 'tasmin', 'tasmax','cdd', 'cwd', 'sd', 'tas_range', 'rolling_pr_3y', 'rolling_pr_2y', 'rolling_pr_1y'])
            
            cpo_pred = cpo_model_new.predict(cpo_input_df)[0]
            threshold_cpo = 0.27
            st.metric(label="Predicted CPO Yield", 
                      value=f"{cpo_pred:.2f}  (tons/ha)", 
                      delta=f"{(cpo_pred - threshold_cpo):.2f} compared to historical average",
                      border = True)

        
    with tabs[2]:
        cols = st.columns((1, 1, 1), gap='medium')
        with cols[0]:
            # selct climate projections
            st.subheader('Climate Projections')
            selected_ssp = st.segmented_control('Select SSP Scenario', options=['SSP126', 'SSP245', 'SSP370', 'SSP585'], default='SSP126')
            selected_years = st.slider('Select Year', min_value=2025, max_value=2100, value=2025, step=1)
            selected_month = st.slider('Select Month', min_value=1, max_value=12, value=1, step=1)
            # Explanation of SSP
            st.markdown("""
                <h4>What is SSP?</h4>
                <p style="text-align: justify;">SSP stands for <b>Shared Socioeconomic Pathways</b>. These are scenarios created by scientists to imagine how human actions, policies, and development might affect climate change in the future.</p>
            """, unsafe_allow_html=True)

            # Define SSP scenarios
            ssp_scenarios = {
                'SSP126': {
                    'title': 'SSP126: A Very Sustainable World',
                    'description': """
                        <ul>
                            <li>Low greenhouse gas emissions</li>
                            <li>Rapid adoption of clean energy</li>
                            <li>Global cooperation</li>
                            <li>Eco-friendly lifestyles</li>
                            <li>Minimal climate impacts due to successful emission reductions</li>
                        </ul>
                    """
                },
                'SSP245': {
                    'title': 'SSP245: A Middle-of-the-Road World',
                    'description': """
                        <ul>
                            <li>Moderate greenhouse gas emissions</li>
                            <li>Some progress on clean energy</li>
                            <li>Balance between sustainability and business-as-usual practices</li>
                            <li>Not enough to significantly reduce climate risks</li>
                        </ul>
                    """
                },
                'SSP370': {
                    'title': 'SSP370: A Fragmented World',
                    'description': """
                        <ul>
                            <li>High greenhouse gas emissions</li>
                            <li>Weak global cooperation</li>
                            <li>Slow adoption of clean energy</li>
                            <li>Economic and political challenges</li>
                            <li>Limited climate action, worsening climate impacts</li>
                        </ul>
                    """
                },
                'SSP585': {
                    'title': 'SSP585: A Fossil-Fuel-Heavy World',
                    'description': """
                        <ul>
                            <li>Extremely high greenhouse gas emissions</li>
                            <li>Heavy reliance on fossil fuels</li>
                            <li>Limited climate action</li>
                            <li>Severe and widespread climate impacts</li>
                        </ul>
                    """
                }
            }
            
            # Display the selected SSP scenario
            if selected_ssp in ssp_scenarios:
                scenario = ssp_scenarios[selected_ssp]
                st.markdown(f"""
                            
                        <h5>{scenario['title']}</h5>
                        {scenario['description']}
                """, unsafe_allow_html=True)
            
        with cols[1]:
            # fetch SSP data 
            ssp_df = pd.read_csv(f'streamlit/data/{selected_ssp.lower()}_climate3.csv')
            ssp_df = pd.read_csv(f'streamlit/data/{selected_ssp.lower()}_climate4.csv')
            ssp_input = ssp_df[(ssp_df['Year'] == selected_years) & (ssp_df['Month'] == selected_month)]
            ssp_input = ssp_input[['Month', 'pr', 'prpercnt', 'hurs', 'spei12', 'tas', 'tasmin', 'tasmax','cdd', 'cwd', 'sd', 'tas_range', 'rolling_pr_3y', 'rolling_pr_2y', 'rolling_pr_1y']]
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            month_name = month_names[selected_month - 1]
            st.write(f'<h4>Projected Climate Data for {month_name} {selected_years}: </h4>', unsafe_allow_html=True)
            climate_data = {
                'Metric': ['Precipitation (mm)', 'Temperature (°C)', 'Humidity (%)', 'Drought Index', 'Consecutive Dry Days', 'Consecutive Wet Days', 'Precipitation Percent Change', 'Temperature Range (°C)', 'Rolling Precipitation 3 Years (mm)', 'Rolling Precipitation 2 Years (mm)', 'Rolling Precipitation 1 Year (mm)'],
                'Value': [f"{ssp_input['pr'].values[0]:.3f}", f"{ssp_input['tas'].values[0]:.3f}", f"{ssp_input['hurs'].values[0]:.3f}", f"{ssp_input['spei12'].values[0]:.3f}", f"{ssp_input['cdd'].values[0]:.3f}", f"{ssp_input['cwd'].values[0]:.3f}", f"{ssp_input['prpercnt'].values[0]:.3f}", f"{ssp_input['tas_range'].values[0]:.3f}", f"{ssp_input['rolling_pr_3y'].values[0]:.3f}", f"{ssp_input['rolling_pr_2y'].values[0]:.3f}", f"{ssp_input['rolling_pr_1y'].values[0]:.3f}"]
            }
            climate_df = pd.DataFrame(climate_data)
            st.table(climate_df)
            
            
        with cols[2]:
            st.subheader('Predicted Yield')
            ffb_pred = ffb_model_new.predict(ssp_input)[0]
            threshold_ffb = 1.38
            st.metric(label="Predicted FFB Yield", 
                      value=f"{ffb_pred:.2f}  (tons/ha)", 
                      delta=f"{ffb_pred - threshold_ffb:.2f} compared to historical average",
                      border = True)
            st.divider()
                
            cpo_pred = cpo_model_new.predict(ssp_input)[0]
            threshold_cpo = 0.27
            st.metric(label="Predicted CPO Yield", 
                      value=f"{cpo_pred:.2f}  (tons/ha)", 
                      delta=f"{cpo_pred - threshold_cpo:.2f} compared to historical average",
                      border = True)
page2()
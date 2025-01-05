import joblib
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
     
    cols = st.columns((2.5, 7), gap='medium')
    
    with cols[0]:
        # Overview of the Model
        st.markdown("""
        <div style="text-align: justify;">
            <h3>Model Overview</h3>
            This prediction tool leverages <b>machine learning</b> to forecast the yield of <b>Fresh Fruit Bunches (FFB)</b> and <b>Crude Palm Oil (CPO)</b> based on climate data. It is designed to help understand the impact of climate conditions on palm oil yield.
        </div>
        <div style="text-align: justify;">
            The model utilizes a wide range of climate variables, including:
                <ul>
                    <li><b>Precipitation</b></li>
                    <li><b>Temperature</b></li>
                    <li><b>Humidity</b></li>
                </ul>
            The model has been trained using <b>historical climate and yield data</b>, ensuring robust learning of the relationship between weather conditions and yield. with a validation score of 0.70 for the FFB model and 0.69 for the CPO model and Error of 0.10 both models.
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        
        tabs = st.tabs(['Manual input', 'Climate Projections'])
        with tabs[0]:    
            cols = st.columns((1, 1), gap='large')
            with cols[0]:
                st.subheader('Manual Input')
                st.write('Input the climate data to predict the FFB yield')
                month = st.slider("Select Month of Harvest", min_value=1, max_value=12, value=1, step=1)
                pr_3y = st.slider("Total Precipitation up to Harvset Year(mm)", min_value=6800.000, max_value=8000.000, value=7000.0, step=0.5)
                tas = st.slider("Temperature (°C)", min_value=24.0, max_value=30.0, value=25.0, step=0.001) 
                pr = st.slider("Precipitation (mm)", min_value=0.0, max_value=500.0, value=100.0, step=0.001)
                hurs = st.slider("Humidity (%)", min_value=70.0, max_value=100.0, value=80.0, step=1.0)
                tasmin = tas - 1.6
                tasmax = tas + 1.6
                tas_range = tasmax - tasmin
                
            with cols[1]:
                st.subheader('Predicted Yield')
                ffb_input_df = pd.DataFrame([[month, pr, pr_3y, tas, tasmin, tasmax, tas_range, hurs]], columns=['Month','pr', 'rolling_pr_3y', 'tas', 'tasmin', 'tasmax', 'tas_range', 'hurs'])
                ffb_pred = ffb_model.predict(ffb_input_df)[0]
                threshold_ffb = 1.40
                colour = 'green' if ffb_pred > threshold_ffb else 'red'
                st.markdown(
                    f"""
                    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                        <h2 style="color: {colour};">FFB Yield</h2>
                        <p style="font-size: 24px; color: {colour};"><strong>{ffb_pred:.2f} tons/ha</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )   
                st.divider()
                    
                cpo_input_df = pd.DataFrame([[month, pr, pr_3y, tas, tasmin, tasmax, tas_range, hurs]], columns=['Month','pr', 'rolling_pr_3y', 'tas', 'tasmin', 'tasmax', 'tas_range', 'hurs'])
                cpo_pred = cpo_model.predict(cpo_input_df)[0]
                threshold_cpo = 0.3
                colour = 'green' if cpo_pred > threshold_cpo else 'red'
                
                
                st.markdown(
                    f"""
                    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                        <h2 style="color: {colour};">CPO Yield</h2>
                        <p style="font-size: 24px; color: {colour};"><strong>{cpo_pred:.2f} tons/ha</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )    

            
        with tabs[1]:
            cols = st.columns((1.5, 1), gap='large')
            with cols[0]:
                # selct climate projections
                st.subheader('Climate Projections')
                selected_ssp = st.segmented_control('Select SSP Scenario', options=['SSP126', 'SSP245', 'SSP370', 'SSP585'], default='SSP126')
                selected_years = st.slider('Select Year', min_value=2025, max_value=2100, value=2025, step=1)
                selected_month = st.slider('Select Month', min_value=1, max_value=12, value=1, step=1)
                
                # fetch SSP data 
                ssp_df = pd.read_csv(f'streamlit/data/{selected_ssp.lower()}_climate3.csv')
                ssp_input = ssp_df[(ssp_df['Year'] == selected_years) & (ssp_df['Month'] == selected_month)]
                ssp_input = ssp_input[['Month','pr', 'rolling_pr_3y', 'tas', 'tasmin', 'tasmax', 'tas_range', 'hurs']]
                st.write(f'Pojected Climate Data for {selected_month}, {selected_years}: ')
                st.write('Precipitation:', ssp_input['pr'].values[0])
                st.write('Temperature:', ssp_input['tas'].values[0])
                st.write('Humidity:', ssp_input['hurs'].values[0])
                
                with cols[1]:
                    st.subheader('Predicted Yield')
                    ffb_pred = ffb_model.predict(ssp_input)[0]
                    threshold_ffb = 1.40
                    colour = 'green' if ffb_pred > threshold_ffb else 'red'
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                            <h2 style="color: {colour};">FFB Yield</h2>
                            <p style="font-size: 24px; color: {colour};"><strong>{ffb_pred:.2f} tons/ha</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )   
                    st.divider()
                        
                    cpo_pred = cpo_model.predict(ssp_input)[0]
                    threshold_cpo = 0.3
                    colour = 'green' if cpo_pred > threshold_cpo else 'red'
                    
                    
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                            <h2 style="color: {colour};">CPO Yield</h2>
                            <p style="font-size: 24px; color: {colour};"><strong>{cpo_pred:.2f} tons/ha</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )           
page2()
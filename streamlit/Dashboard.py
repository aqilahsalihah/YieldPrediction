import streamlit as st
import time
import pandas as pd
import requests
import altair as alt
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime, timedelta
import calendar
from millify import millify # type: ignore
from jamaibase import JamAI, protocol as p # type: ignore


# load the data
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

def get_month_name(data):
    data['Month_Name'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    return data

def filter_data_by_year(palm_oil, selected_year):
    return palm_oil[palm_oil['Year'] <= selected_year]

def calculate_yearly_yield(palm_oil):
    return palm_oil.groupby('Year').sum().reset_index()

def harvest_category(value, avg_value, highest_value):
    if value < avg_value:
        return 'Below Average'
    elif value == highest_value:
        return 'Peak Harvest'
    else:
        return 'Above Average'
      
palm_oil = load_data('data/palm_oil.csv')
palm_oil = get_month_name(palm_oil)

climate_info = load_data('data/historical_climate_v2.csv')
climate_2 = load_data('data\ssp126_climate3.csv')

climate_info = pd.concat([climate_info, climate_2], ignore_index=True)
climate_info = get_month_name(climate_info)

years = list(palm_oil['Year'].unique())


def process_data(selected_years):
    # filter data based on selected years
    palm_oil_filtered = filter_data_by_year(palm_oil, selected_years)
    climate_info_filtered = filter_data_by_year(climate_info, selected_years)

    yearly_yield = calculate_yearly_yield(palm_oil_filtered)
    latest_year = yearly_yield['Year'].max()
    earliest_year = max(latest_year - 9, yearly_yield['Year'].min())
    prev_year = latest_year - 1
    yearly_yield = yearly_yield[yearly_yield['Year'] >= earliest_year]
    yearly_yield['Year'] = yearly_yield['Year'].astype(int)

    monthly_yield = palm_oil_filtered[palm_oil_filtered['Year'] >= prev_year].reset_index(drop=True)
    climate_info_filtered = climate_info_filtered[climate_info_filtered['Year'] >= earliest_year].reset_index(drop=True)

    # Metrics
    latest_ffb = yearly_yield[yearly_yield['Year'] == latest_year]['FFB_Yield'].values[0]
    prev_ffb = yearly_yield[yearly_yield['Year'] == prev_year]['FFB_Yield'].values[0]
    ffb_change_pct = ((latest_ffb - prev_ffb) / prev_ffb) * 100

    latest_cpo = yearly_yield[yearly_yield['Year'] == latest_year]['CPO_Yield'].values[0]
    prev_cpo = yearly_yield[yearly_yield['Year'] == prev_year]['CPO_Yield'].values[0]
    cpo_change_pct = ((latest_cpo - prev_cpo) / prev_cpo) * 100

    latest_prod = yearly_yield[yearly_yield['Year'] == latest_year]['FFB_production'].values[0]
    prev_prod = yearly_yield[yearly_yield['Year'] == prev_year]['FFB_production'].values[0]
    prod_change_pct = ((latest_prod - prev_prod) / prev_prod) * 100

    this_year = monthly_yield[monthly_yield['Year'] == latest_year]

    # Calculate highest monthly yield
    highest_monthly_ffb = this_year['FFB_Yield'].max()
    highest_monthly_cpo = this_year['CPO_Yield'].max()
    highest_monthly_prod = this_year['FFB_production'].max()

    # Calculate average monthly yield
    avg_monthly_ffb = this_year['FFB_Yield'].mean()
    avg_monthly_cpo = this_year['CPO_Yield'].mean()
    avg_monthly_prod = this_year['FFB_production'].mean()

    # add harvest category column
    this_year['FFB_Yield_Category'] = this_year['FFB_Yield'].apply(harvest_category, args=(avg_monthly_ffb, highest_monthly_ffb))
    this_year['CPO_Yield_Category'] = this_year['CPO_Yield'].apply(harvest_category, args=(avg_monthly_cpo, highest_monthly_cpo))
    this_year['FFB_Production_Category'] = this_year['FFB_production'].apply(harvest_category, args=(avg_monthly_prod, highest_monthly_prod))

    return {
        'yearly_yield': yearly_yield,
        'monthly_yield': monthly_yield,
        'this_year': this_year,
        'latest_year': latest_year,
        'prev_year': prev_year,
        'latest_ffb': latest_ffb,
        'prev_ffb': prev_ffb,
        'ffb_change_pct': ffb_change_pct,
        'latest_cpo': latest_cpo,
        'prev_cpo': prev_cpo,
        'cpo_change_pct': cpo_change_pct,
        'latest_prod': latest_prod,
        'prev_prod': prev_prod,
        'prod_change_pct': prod_change_pct,
        'avg_monthly_ffb': avg_monthly_ffb,
        'avg_monthly_cpo': avg_monthly_cpo,
        'avg_monthly_prod': avg_monthly_prod
    }



color_palette = ["#fd8d3c", "#a1d99b", "#ffffcc"]
def trend_10(yearly_yield, var, domain):
    ffb_chart = alt.Chart(yearly_yield).mark_line(point=True).encode(
                x=alt.X('Year:O', title='', axis=alt.Axis(labelAngle=0)),
                y=alt.Y(f'{var}_Yield:Q', title=f'{var} Yield (tonnes/ha)'),
                color=alt.Color('Yield_Type:N', scale=alt.Scale(range=color_palette), legend=None)
            ).properties(
                width=600,
                height=200
            )
    
    return ffb_chart
def month_bar(data, y_value, color_value, millify_values=False):
    bars = alt.Chart(data).mark_bar(size=25).encode(
        x=alt.X('Month_Name:N', title='', axis=alt.Axis(labelAngle=0), sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
        y=alt.Y(f'{y_value}:Q', title=y_value.replace('_', ' ')),
        color=alt.Color(
            f'{color_value}:N', 
            scale=alt.Scale(
                domain=["Peak Harvest", "Above Average", "Below Average"],
                range= color_palette),
            legend=alt.Legend(title='', orient='top')
        )
    ).properties(
        width=600,
        height=150
    )
    
    # Add text annotations
    if millify_values:
        text = bars.mark_text(
            align='center',
            baseline='middle',
            dy=-10  # Adjust vertical position
        ).encode(
            text=alt.Text(f'{y_value}:Q', format='.2s')  # Display y_value values with millify
        )
    else:
        text = bars.mark_text(
            align='center',
            baseline='middle',
            dy=-10  # Adjust vertical position
        ).encode(
            text=alt.Text(f'{y_value}:Q', format='.2f')  # Display y_value values
        )
    
    # Layer the bar chart and text annotations
    monthly_chart = alt.layer(bars, text).configure_mark(
        opacity=0.7,
        color='black'
    )
    
    return monthly_chart

def month_comparison(monthly_yield, var):
    lines = alt.Chart(monthly_yield).mark_line(point=True).encode(
                x=alt.X('Month_Name:N', title='', axis=alt.Axis(labelAngle=0), sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
                y=alt.Y(f'{var}_Yield:Q', title=f'{var} Yield (tonnes/ha)'),
                color=alt.Color('Year:N', title='Year', scale=alt.Scale(range=color_palette), legend=alt.Legend(title='', orient='top')),
                detail='Year:N'
            ).properties(
                width=600,
                height=300
            )
    
    return lines

# print(monthly_yield)
# print(this_year)
# Malaysia Palm Oil Yield Dashboard
    
def page1():
    print('\n\n')
    print('---------------------------------------------Runing page Dashboard---------------------------------------------')
    st.title("Palm Oil Yield Dashboard 📊")
    col1, col2 = st.columns((4.8,5), gap='medium')
    with col1:
        st.write("")
        st.write("<div style='text-align: justify;'><b>Fresh Fruit Bunches (FFB)</b> are the primary raw material for palm oil production. They are harvested from oil palm trees and processed to extract <b>Crude Palm Oil (CPO)</b>.</div>", unsafe_allow_html=True)
        st.write("")
        st.write("<div style='text-align: justify;'><b>Crude Palm Oil (CPO)</b> is the unrefined oil extracted from the pulp of the fruit of oil palms. It is used in various food and non-food products after refining.</div>", unsafe_allow_html=True)
    with col2:
        st.subheader("Select a Year")
        selected_years = st.slider("", (min(years)+1), max(years), value=2023)
    
    data = process_data(selected_years)
    yearly_yield = data['yearly_yield']
    monthly_yield = data['monthly_yield']
    this_year = data['this_year']
    latest_year = data['latest_year']
    prev_year = data['prev_year']
    latest_ffb = data['latest_ffb']
    prev_ffb = data['prev_ffb']
    ffb_change_pct = data['ffb_change_pct']
    latest_cpo = data['latest_cpo']
    prev_cpo = data['prev_cpo']
    cpo_change_pct = data['cpo_change_pct']
    latest_prod = data['latest_prod']
    prev_prod = data['prev_prod']
    prod_change_pct = data['prod_change_pct']
    avg_monthly_ffb = data['avg_monthly_ffb']
    avg_monthly_cpo = data['avg_monthly_cpo']
    avg_monthly_prod = data['avg_monthly_prod']
    
    st.divider()
    col = st.columns((2, 5, 1.8), gap='medium')


    with col[0]: # metrics

        st.subheader("Key Metrics")
        st.metric(
            label=f"FFB Yield {latest_year}",
            value=f"{latest_ffb:.2f}%",
            delta=f"{(latest_ffb - prev_ffb):.2f} ({ffb_change_pct:.2f}%)",
            border=True
        )
        st.metric(
            label=f"CPO Yield {latest_year}",
            value=f"{latest_cpo:.2f}%",
            delta=f"{(latest_cpo - prev_cpo):.2f} ({cpo_change_pct:.2f}%)",
            border=True
        )
        st.metric(
            label=f'FFB Production (tons)',
            value=f"{millify(latest_prod, precision=2)}",
            delta=f"{millify(latest_prod - prev_prod, precision=2)} ({prod_change_pct:.2f}%)",
            border=True
        )
        st.divider()
        st.subheader("Monthly Yield")
        st.metric(
            label=f"Avg Monthly FFB Yield {latest_year}",
            value=f"{avg_monthly_ffb:.2f} tons/ha",
            border=True
        )
        st.metric(
            label="Avg Monthly CPO Yield",
            value=f"{avg_monthly_cpo:.2f} tons/ha",
            border=True
        )
        st.metric(
            label="Avg Monthly FFB Production",
            value=f"{millify(avg_monthly_prod, precision=2)} tons",
            border=True
        )
    with col[1]: # yearly yield and monthly yield

        ffb, cpo, prod = st.tabs(['Fresh Fruit Bunches Yield', 'Crude Palm Oil Yield', 'Fresh Fruit Bunches Production'])
        with ffb:
            # past years trend
            st.subheader(f"FFB Yield {len(yearly_yield)} years trend")
            chart = trend_10(yearly_yield, 'FFB', (10.0, 20.0))
            st.altair_chart(chart, use_container_width=True)
            
            # Monthly Yield
            st.subheader("Monthly Yield")
            chart = month_bar(this_year, 'FFB_Yield', 'FFB_Yield_Category')
            st.altair_chart(chart, use_container_width=True)
            
            # compare the monthly yield for the latest year with prev year
            lines = month_comparison(monthly_yield, 'FFB')

            st.subheader("Monthly Yield Comparison")
            st.altair_chart(lines, use_container_width=True)
        
            
        with cpo:
            st.subheader("CPO Yield 10 years trend")
            chart = trend_10(yearly_yield, 'CPO', (2.0, 4.0))
            st.altair_chart(chart, use_container_width=True)
            
            st.subheader("Monthly Yield")
            cpo_yield_chart = month_bar(this_year, 'CPO_Yield', 'CPO_Yield_Category')
            st.altair_chart(cpo_yield_chart, use_container_width=True)
            
            # compare the monthly yield for the latest year with prev year
            
            lines = alt.Chart(monthly_yield).mark_line(point=True).encode(
                x=alt.X('Month_Name:N', title='', axis=alt.Axis(labelAngle=0), sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
                y=alt.Y('CPO_Yield:Q', title='CPO Yield (tonnes/ha)'),
                color=alt.Color('Year:N', title='Year', legend=alt.Legend(title='', orient='top')),
                detail='Year:N'
            ).properties(
                width=600,
                height=300
            )

            st.subheader("Monthly Yield Comparison")
            lines = month_comparison(monthly_yield, 'CPO')
            st.altair_chart(lines, use_container_width=True)
            
        with prod:
            st.subheader("FFB Yield 10 years trend")
            chart = alt.Chart(yearly_yield).mark_line(
                point=alt.OverlayMarkDef(filled=True, fill='lightblue', strokeWidth=2)
                ).encode(
                x=alt.X('Year:O', title='', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('FFB_production:Q', title='FFB production (tonnes)'),
                color=alt.Color('Yield_Type:N', scale=alt.Scale(range=color_palette), legend=None)
            ).properties(
                width=600,
                height=250
            )
            st.altair_chart(chart, use_container_width=True)
            
            st.subheader("Monthly Yield")
            ffb_production_chart = month_bar(this_year, 'FFB_production', 'FFB_Production_Category', millify_values=True)
            st.altair_chart(ffb_production_chart, use_container_width=True)
            
            # compare the monthly yield for the latest year with prev year
            lines = alt.Chart(monthly_yield).mark_line(point=True).encode(
                x=alt.X('Month_Name:N', title='', axis=alt.Axis(labelAngle=0), sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
                tooltip=[alt.Tooltip('FFB_production:Q', format='.2s')],
                y=alt.Y('FFB_production:Q', title='FFB production (tonnes)', axis=alt.Axis(format='.2s')),
                color=alt.Color('Year:N', title='Year', scale=alt.Scale(range=color_palette), legend=alt.Legend(title='', orient='top')),
                detail='Year:N'
            ).properties(
                width=600,
                height=300
            )

            st.subheader("Monthly Yield Comparison")
            st.altair_chart(lines, use_container_width=True)

    with col[2]: # AI insights
        @st.cache_data
        def collect_dashboard_data():
            key_metrics = {
                'FFB Yield': {
                    'Latest Year': latest_ffb,
                    'Previous Year': prev_ffb,
                    'Change (%)': ffb_change_pct
                },
                'CPO Yield': {
                    'Latest Year': latest_cpo,
                    'Previous Year': prev_cpo,
                    'Change (%)': cpo_change_pct
                },
                'FFB Production': {
                    'Latest Year': latest_prod,
                    'Previous Year': prev_prod,
                    'Change (%)': prod_change_pct
                }
            }

            trends = {
                'FFB Yield': yearly_yield[['Year', 'FFB_Yield']],
                'CPO Yield': yearly_yield[['Year', 'CPO_Yield']],
                'FFB Production': yearly_yield[['Year', 'FFB_production']]
            }

            monthly  = {
                'FFB': this_year[['Month_Name', 'FFB_Yield', 'FFB_Yield_Category']],
                'CPO': this_year[['Month_Name', 'CPO_Yield', 'CPO_Yield_Category']],
                'FFB Production': this_year[['Month_Name', 'FFB_production', 'FFB_Production_Category']]
            }

            climate_data = {
                'Precipitation': climate_info[['Year','Month_Name', 'pr']],
                'Temperature': climate_info[['Year','Month_Name', 'tas']],
                'Humidity': climate_info[['Year','Month_Name', 'hurs']],
                'Max Temperature': climate_info[['Year','Month_Name', 'tasmax']],
                'Min Temperature': climate_info[['Year','Month_Name', 'tasmin']],
            }

            data = {
                'key_metrics': str(key_metrics),
                'trends': str(trends),
                'monthly': str(monthly),
                'climate': str(climate_data)
            }
            return data

        project_id = st.secrets['jamAIbase']["project_id"]
        pat = st.secrets['jamAIbase']["pat"]

        client = JamAI(project_id, pat)
        def generate_insights(input_data):         
            
            response = client.table.add_table_rows(
                table_type=p.TableType.action,
                request=p.RowAddRequest(
                    table_id="AI_insights1",
                    data=[input_data],
                    stream=False,
                ),
            )
            
            return {
                "message": response.rows[0].columns['Insight'].text
        }
        
        def stream_data(input):
            for word in input.split(" "):
                yield word + " "
                time.sleep(0.02)
        
        st.subheader("AI Summary")
        dashboard_data = collect_dashboard_data()
            
        
        # st.write(dashboard_data)
        if st.button('Generate AI Summary'):
            with st.spinner("Generating AI Summary..."):
                ai_insight = generate_insights(dashboard_data)
                to_write = ai_insight.get('message')
                st.write_stream(stream_data(to_write))
                

page1()
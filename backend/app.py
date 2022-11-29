import pandas as pd
import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from streamlit_timeline import timeline # pip install streamlit-timeline, timeline module
from io import StringIO, BytesIO  # Standard Python Module
import requests
import json
import altair as alt

# import pmdarima as pm #pip install pmdarima
# from pmdarima.model_selection import train_test_split #for forecasting
# import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib
# matplotlib.use('TkAgg')

import prophet
from prophet import Prophet

# def generate_excel_download_link(df):
#     # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
#     towrite = BytesIO()
#     df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
#     towrite.seek(0)  # reset pointer
#     b64 = base64.b64encode(towrite.read()).decode()
#     href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
#     return st.markdown(href, unsafe_allow_html=True)

# def generate_html_download_link(fig):
#     # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
#     towrite = StringIO()
#     fig.write_html(towrite, include_plotlyjs="cdn")
#     towrite = BytesIO(towrite.getvalue().encode())
#     b64 = base64.b64encode(towrite.read()).decode()
#     href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
#     return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='MIRAI 未来', layout="wide")
st.title('MIRAI 未来')
st.subheader('Feed me with your Sales Data and I will tell you the future')

# Load news file:
response_API = requests.get('https://raw.githubusercontent.com/beatriceyapsm/deploytest/main/example.json')
data = json.loads(response_API.text)
news = pd.json_normalize(data['events'])
news = news.drop(['media.url','media.caption','text.text'],axis=1)
news['date']=news['start_date.year']+"-"+news['start_date.month']+"-"+news['start_date.day']
news.rename(columns={'text.headline':'event'}, inplace=True)
news = news.drop(['start_date.year','start_date.month','start_date.day'],axis=1)
col = ['date','event']
news = news[col]

#Get files from user
uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    df['ds'] = pd.to_datetime(df['ds']).dt.date

    #forecast using Prophet
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=6, freq='M')
    future = future.tail(6)
    # st.dataframe(future)
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast['ds'] = pd.to_datetime(forecast['ds']).dt.date
    st.dataframe(forecast)
    # fig1 = m.plot(forecast, xlabel='Date', ylabel='Sales Quantity')
    # fig2 = m.plot_components(forecast)
    forecast1=forecast.drop(['yhat_lower'], axis=1)
    forecast1['yhat_lower']=forecast['yhat_upper']
    forecast2 = forecast.append(forecast1)

    
    #Plot Charts
    def get_chart(data):
        hover = alt.selection_single(
            fields=["ds"],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        lines = (
            alt.Chart(data, title="Forecast Demand")
            .mark_line()
            .encode(
                x="ds",
                y="y"
            )
        )

        # Draw points on the line, and highlight based on selection
        points = lines.transform_filter(hover).mark_circle(size=65)

        # Draw a rule at the location of the selection
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="ds",
                y="y",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("ds", title="Date"),
                    alt.Tooltip("y", title="Price (USD)"),
                ],
            )
            .add_selection(hover)
        )
        return (lines + points + tooltips).interactive()
        
    def fchart(data):
        hover = alt.selection_single(
            fields=["ds"],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        lines = (
            alt.Chart(data, title="Forecast Demand")
            .mark_line()
            .encode(
                x="ds",
                y="yhat",
                color=alt.value("#FFAA00")
            )
        )

        # Draw points on the line, and highlight based on selection
        points = lines.transform_filter(hover).mark_circle(size=65)

        # Draw a rule at the location of the selection
        tooltips = (
            alt.Chart(data)
            .mark_circle()
            .encode(
                x="ds",
                y="yhat",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("ds", title="Date"),
                    alt.Tooltip("yhat", title="Price (USD)")
                ],
            )
            .add_selection(hover)
        )
        return (lines + points + tooltips).interactive()
    
    def fspots(data):

        spots = (
            alt.Chart(data, title="Forecast Demand")
            .mark_circle()
            .encode(
                x="ds",
                y="yhat_lower",
                color=alt.value("#FFAA00")
            )
        )


        return (spots).interactive()

    chart = get_chart(df)
    chart2 = fchart(forecast)
    chart3 = fspots(forecast2)

    # ANNOTATIONS = [
    #     ("Sep 26, 2022", "ANNUAL EV SALES UP “TENFOLD” POST-PANDEMIC"),
    #     ("Nov 14, 2022", "EV BATTERY RECYCLING – CIRCULAR ECONOMY CHARGES UP"),
    #     ("Nov 16, 2022", "INDONESIA'S INDIKA, TAIWAN'S FOXCONN MULL EV PARTNERSHIP WITH THAI FIRM"),
    #     ("Dec 16, 2022", "BLAHBLAH"),  
    #     ("Dec 30, 2022", "BLAHBLAH"),
    # ]
    # annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
   
    annotations_df = news
    annotations_df.date = pd.to_datetime(annotations_df.date)
    annotations_df["y"] = forecast['yhat_upper'].max()

    annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=20, text="⬇", color='red', dx=-8, dy=-10, align="left")
    .encode(
        x="date:T",
        y=alt.Y("y:Q"),
        tooltip=["date","event"],
    )
    .interactive()
    )
    
    st.altair_chart(
    (chart+ chart2+ chart3+ annotation_layer).interactive(),
    use_container_width=True
    )
    
    

# -- TIMELINE SECTION
# Streamlit Timeline Component Example
# use full page width
#st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
# with open('example.json', "r") as f:
#     data = f.read()


# render timeline
timeline(data, height=800)


# --Table Section
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid
from st_aggrid import GridUpdateMode

proj_nums = ["10%~30%","N/A","N/A","N/A","-1%~-5%","4%~5%","4%~5%","-1%~-5%","N/A","-2%~-3%","5%~10%","N/A","N/A","-5%~10%","1%~2%"]

if 'y' in news.columns:
    news_impact = news.assign(Projected_Impact=proj_nums, Estimated_Impact=" ", Business_Strategy=" ")
    news_drop = news_impact.drop(columns=['y'])
    AgGrid(news_drop, editable=True, fit_columns_on_grid_load=True)
else:
    news_impact = news.assign(Projected_Impact=proj_nums, Estimated_Impact=" ", Business_Strategy=" ")
    AgGrid(news_impact, editable=True, fit_columns_on_grid_load=True)

st.button ("Update")



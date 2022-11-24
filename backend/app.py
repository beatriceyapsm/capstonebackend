import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from streamlit_timeline import timeline # pip install streamlit-timeline, timeline module
from io import StringIO, BytesIO  # Standard Python Module
import requests
import json

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


st.set_page_config(page_title='MIRAI 未来')
st.title('MIRAI 未来')
st.subheader('Feed me with your Sales Data and I will tell you the future')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    # df = df.sort_values(by='Order Date', ascending=True)
    # st.dataframe(df)
    # groupby_column = st.selectbox(
    #     'What would you like to analyse?',
    #     ('Order Date', 'Month', 'Year'),
    # )
 
    # -- GROUP DATAFRAME
    # output_columns = ['Quantity']
    # df_grouped = df.groupby(by=[groupby_column], as_index=False).agg({'Quantity':'sum'})

    # -- FORECASTING
    # train, test = train_test_split(df, train_size=round(len(df)*0.8,None))
    # sns.set()
    # # train = btc[btc.index < pd.to_datetime("2020-11-01", format='%Y-%m-%d')]
    # # test = btc[btc.index > pd.to_datetime("2020-11-01", format='%Y-%m-%d')]

    # plt.plot(train, color = "black")
    # plt.plot(test, color = "red")
    # plt.ylabel('Sales')
    # plt.xlabel('Date')
    # plt.xticks(df['Order Date'])
    # plt.title("Train/Test split for Sales Data")
    # plt.show()

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=6, freq='M')
    future = future.tail(6)
    # st.dataframe(future)
    forecast = m.predict(future)
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    st.dataframe(forecast)
    fig1 = m.plot(forecast, xlabel='Date', ylabel='Sales Quantity')
    # fig2 = m.plot_components(forecast)

    st.write(fig1)

    # -- PLOT DATAFRAME
    # fig = px.line(
    #     df_grouped,
    #     x=groupby_column,
    #     y='Quantity',
    #     # color='Category',
    #     # template='plotly_white',
    #     title=f'<b>Sales by {groupby_column}</b>'
    # )
    # st.plotly_chart(fig)

    # -- DOWNLOAD SECTION
    # st.subheader('Downloads:')
    # generate_excel_download_link(df_grouped)
    # generate_html_download_link(fig)

# -- TIMELINE SECTION
# Streamlit Timeline Component Example
# use full page width
#st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
# with open('example.json', "r") as f:
#     data = f.read()

    
response_API = requests.get('https://raw.githubusercontent.com/beatriceyapsm/deploytest/main/example.json')
data = json.loads(response_API.text)

# render timeline
timeline(data, height=800)

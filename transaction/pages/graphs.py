import altair as alt 
import streamlit as st 
import pandas as pd  
import datetime
from datetime import date ,timedelta
#import matplotlib.pyplot as plt
st.set_page_config(page_title="Charts", 
page_icon="📈")

st.title("Chart Maker")


paymentstatus = st .selectbox(
    'What Payment Status Would You Like to See',
    ('All','Charge','Refund','chargeback')
)

paymentsMethad = st .selectbox(
    'What Payment Status Would You Like to See',
    ('All','Goods and Service','Friends & Family',)
)

paymentDevice = st .selectbox(
    'What Payment Device  Would You Like to See',
    ('All','Desktop','Tablet','Phone')
)

paymentCountry = st .selectbox(
    'What Payment Country  Would You Like to See',
    ('All','US','UK','AU')
)

today=datetime.datetime.now()
days180=date.today()-timedelta(days=180)

StartDate= st.date_input('Start date(default 180 days prior)',days180)
EndDate= st.date_input('End date(default Today)',today)

dfpreclean=st.file_uploader('Selected CSV File')

if dfpreclean is not None:
    dfpreclean= pd.read_csv(dfpreclean)
else:    
    st.stop()

dfpreclean.drop(['Transaction_ID','Auth_code'],axis=1,inplace=True)
dfpreclean2=dfpreclean[dfpreclean['Success']==1]
dfpreclean2['Transaction_Notes'].fillna('N/A',inplace=True)
dfpreclean2['Day']=pd.to_datetime(dfpreclean2['Day'])
df=dfpreclean2.loc[:,['Total','Transaction_Type','Type', 'Country', 'Source','Day','Customer_Name', 'Transaction_Notes']]

df['int_created_date']=df['Day'].dt.year*100+df['Day'].dt.month


if paymentstatus =='Charge':
    df=df[df['Type']=='Charge']
elif paymentstatus =='Refund':
    df=df[df['Type']=='Refund']
elif paymentstatus == 'chargeback':
    df=df[df['Type']=='Chargeback']  
else:
    pass         

if paymentsMethad == 'Goods and Services':
    df = df[df['Transaction_Type'] == 'Goods and Services']
elif paymentsMethad == 'Friends & Family':
    df = df[df['Transaction_Type'] == 'Friends & Family']
else:
    pass

if paymentDevice == 'Desktop':
    df = df[df['Source'] == 'Desktop']
elif paymentDevice== 'Tablet':
    df = df[df['Source'] == 'Tablet']
elif paymentDevice== 'Phone':
    df = df[df['Source'] == 'Phone']
else:
    pass

if paymentCountry == 'US':
    df = df[df['Country'] == 'US']
elif paymentCountry == 'UK':
    df = df[df['Country'] == 'UK']
elif paymentCountry == 'AU':
    df = df[df['Country'] == 'AU']
else:
    pass
StartDate=pd.to_datetime(StartDate)
EndDate=pd.to_datetime(EndDate)

df=df[(df['Day']>=StartDate)&(df['Day']<=EndDate)]

chart1= alt.Chart(df).mark_bar().encode(
    alt.X('Total:Q',bin=True),
    y='count()',
).properties(
    title={
        'text':['count of transaction'],
        'subtitle':[f"Payment Status: {paymentstatus}", f"Payment Method: {paymentsMethad}", f"Payment Application: {paymentCountry}", f"Payment Country: {paymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)
chart2= alt.Chart(df).mark_boxplot(extent='min-max').encode(
    alt.X('int_created_data:O'),
    y='Total:Q',
).properties(
    title={
        'text':['Box & Whisker By Month'],
        'subtitle':[f"Payment Status: {paymentstatus}", f"Payment Method: {paymentsMethad}", f"Payment Application: {paymentCountry}", f"Payment Country: {paymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)
bar3 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('sum(Total):Q', title='Total'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart3 = (bar3).properties(
    title={
        "text": ["Box Plot Mean Transaction Per Month"], 
        'subtitle':[f"Payment Status: {paymentstatus}", f"Payment Method: {paymentsMethad}", f"Payment Application: {paymentCountry}", f"Payment Country: {paymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)
bar4 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('count(Total):Q', title='Count'),
    color=alt.Color('Type:N', title='Payment Type')

)
chart4 = (bar4).properties(
    title={
      "text": ["Box Plot Transaction Count Per Month"], 
       'subtitle':[f"Payment Status: {paymentstatus}", f"Payment Method: {paymentsMethad}", f"Payment Application: {paymentCountry}", f"Payment Country: {paymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)
tab1, tab2, tab3, tab4 = st.tabs(["Histogram", "Box and Whiskers", "Box Plot Sum", "Box Plot Count"])
with tab1:
    st.altair_chart(chart1, use_container_width=True)
with tab2:
   st.altair_chart(chart2, use_container_width=True)
with tab3:
    st.altair_chart(chart3, use_container_width=True)
with tab4:
    st.altair_chart(chart4, use_container_width=True)


























 # streamlit run graphs.py   
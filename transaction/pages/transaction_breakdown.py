import streamlit as st 
import pandas as pd 
import numpy as np 
import  datetime
from datetime import date , timedelta
import xlsxwriter
import io

st.set_page_config(page_title="Transactions", page_icon="🛒")

st.title("Transaction Breakdown")


filename = st.text_input("Filename", key="filename")
firstname = st.text_input("Enter Name", key="firstname1")

highticketstring = st.number_input("Enter High Ticket INTEGER ONLY", key="highticket")

uploaded_file = st.file_uploader("Please Upload CSV File", type=['csv'])

if uploaded_file is not None:
    
    highticketval= int(highticketstring)
    dfpreclean=pd.read_csv(uploaded_file)
    buffer = io.BytesIO( )

 #clean a  data 
    dfpreclean=pd.read_csv('Paypal_Transactions3.csv')
 #print(dfpreclean.head())

    dfpreclean.drop(['Transaction_ID','Auth_code'],axis=1,inplace=True)
    dfpreclean2=dfpreclean[dfpreclean['Success']==1]

    dfpreclean2['Transaction_Notes'].fillna('N/A',inplace=True)
    dfpreclean2['Day']=pd.to_datetime(dfpreclean2['Day'])

 #print(dfpreclean2.columns)
 #'Type', 'Transaction_Type', , 'Total', 'Success', ,'Transaction_Notes', 'Source', 'Type']

    df=dfpreclean2.loc[:,['Total','Transaction_Type','Type', 'Country', 'Source','Day','Customer_Name', 'Transaction_Notes']]
    #print(df.head())

    totalsum=np.sum(df['Total'])
    total_transactions=df['Type'].count()

    mean_transaction=np.mean(df['Total'])
    median_transaction=np.median(df['Total'])
    max_transaction=np.max(df['Total'])

    total_unique_Customer=df['Customer_Name'].nunique()

    chargeonlytransactions=df[df['Type']=='Charge']
    refundonlytransactions=df[df['Type']=='Refund']
    chargebackonlytransactions=df[df['Type']=='Chargeback']

    days90=pd.to_datetime(date.today()-timedelta(days=90))
    days180=pd.to_datetime(date.today()-timedelta(days=180))

    chargetotal=np.sum(chargeonlytransactions['Total'])
    charge90days=np.sum(chargeonlytransactions[chargeonlytransactions['Day']>days90]['Total'])
    charge180days=np.sum(chargeonlytransactions[chargeonlytransactions['Day']>days180]['Total'])

    refundtotal=np.sum(refundonlytransactions['Total'])
    refund90days=np.sum(refundonlytransactions[refundonlytransactions['Day']>days90]['Total'])
    refund180days=np.sum(refundonlytransactions[refundonlytransactions['Day']>days180]['Total'])

    charbackgebacktotal=np.sum(chargebackonlytransactions['Total'])
    chargeback90days=np.sum(chargebackonlytransactions[chargebackonlytransactions['Day']>days90]['Total'])
    chargeback180days=np.sum(chargebackonlytransactions[chargebackonlytransactions['Day']>days180]['Total'])

    refundratelifetime=(refundtotal/refundtotal)
    refundrate90days=(refund90days/charge90days)
    refundrate180days=(refund180days/charge180days)

    charbackgebackratelifetime=(charbackgebacktotal/charge180days)
    charbackgebackrate90days=(chargeback90days/charge180days)
    charbackgebackrate180days=(chargeback180days/charge180days)

    pivottablenames = pd.pivot_table(df, index=['Customer_Name'], aggfunc={'Total': np.sum, 'Customer_Name': 'count',})
    pivottablenames = pivottablenames.rename(columns={"Customer_Name": "count_of_total", "Total": "sum_of_total"})
    pivottablenames=pivottablenames.loc[:, ['sum_of_total', "count_of_total"]]
    #print(pivottablenames)
    total_unique_customers = pivottablenames['sum_of_total'].count()

    avg_trans_count_per_customer=np.mean(pivottablenames['count_of_total'])
    avg_trans_sum_per_customer=np.mean(pivottablenames['sum_of_total'])

    pivottabletransactiontype=pd.pivot_table(df,index=['Transaction_Type'],aggfunc={'Transaction_Type':'count','Total':np.sum})
    pivottabletransactiontype['totalpercent']= (pivottabletransactiontype['Total']/totalsum).apply('{:.2%}'.format)
    #print(pivottabletransactiontype)

    pivottabltransactioncountry = pd.pivot_table(df,index=['Country'], aggfunc={'Country': 'count', 'Total': np.sum})
    pivottabltransactioncountry['totalpercent'] = (pivottabltransactioncountry['Total']/totalsum).apply('{:.2%}'.format)


    namefinal=df[df['Customer_Name'].str.contains(firstname,case=False)]
    #print(namefinal)

    payment_note=df[df['Transaction_Notes'].isna()==False]

    flagged_words='raffle|razz|lottery'
    payment_note_final=df[df['Transaction_Notes'].str.contains(flagged_words,case=False)]
    #print(payment_note_final)
    #highticketval=3500
    highticket=df[df['Total']>=highticketval].copy()
    highticket=highticket.sort_values(by='Total',ascending=False)
    #print(highticket)

    dup=df.copy()
    dup['Customer_Name_next']=dup['Customer_Name'].shift(1)
    dup['Customer_Name_prev']=dup['Customer_Name'].shift(-1)
   #print(dup)

    dup['created_at_day']=dup['Day']
    dup['created_at_dayprev']=dup['Day'].shift(-1)
    dup['created_at_daynext']=dup['Day'].shift(1)
    dup2 = dup.query('(created_at_day == created_at_dayprev | created_at_day == created_at_daynext) & (Customer_Name == Customer_Name_next | Customer_Name == Customer_Name_prev)')
    #print(dup2)

    dup3=dup2.query('(Customer_Name == Customer_Name_next) | (Customer_Name== Customer_Name_prev)')
    #print(dup3)

    dfcalc=pd.DataFrame({
            'totalsum':[totalsum],
            'mean_transaction':[mean_transaction],
            'median_transaction':[median_transaction], 
            'max_transaction':[max_transaction],
            'total_transactions':[total_transactions],
            'chargetotal':[chargetotal],
            'charge90days':[charge90days],
            'charge180days':[charge180days],
            'refundtotal':[refundtotal],
            'refund90days':[refund90days],
            'refund180days':[refund180days],
            'refundrateliefetime':[refundratelifetime],
            'refundrate90days':[refundrate90days],
            'refundrate180days':[refundrate180days],
             'chargebacktotal':[ charbackgebacktotal],
             'chargeback90days':[chargeback90days],
             'chargeback180days':[chargeback180days],
            'chargebackrateliefetime':[charbackgebackratelifetime],
            'chargebackrate90days':[charbackgebackrate90days],
            'chargebackrate180days':[charbackgebackrate180days],
            'total_unique_customer_names':[total_unique_customers],                      
            'avg_transactions_count_per_customer_name':[avg_trans_count_per_customer],
            'avg_transactions_sum_per_customer_name':[avg_trans_sum_per_customer],
            '90 Days':[days90],
            '180 Days':[days180],
    })

    format_mapping = {"totalsum": '${:,.2f}',
        "mean_transaction": '${:,.2f}',
        "median_transaction": '${:,.2f}',
        "max_transaction": '${:,.2f}',
        "total_transactions": '{:,.0f}', 
        'chargetotal': '${:,.2f}',
        'charge90days': '${:,.2f}',
        'charge180days': '${:,.2f}',
        'refundtotal': '${:,.2f}',
        'refund90days': '${:,.2f}',
        'refund180days': '${:,.2f}',
        'refundrateliefetime':'{:,.2%}',
        'refundrate90days':'{:,.2%}',
        'refundrate180days':'{:,.2%}',
        'chargebacktotal':'${:,.2f}',
        'chargeback90days':'${:,.2f}',
        'chargeback180days':'${:,.2f}',
        'chargebackrateliefetime':'{:,.2%}',
        'chargebackrate90days':'{:,.2%}',
        'chargebackrate180days':'{:,.2%}',
        "total_unique_customer_names": '{:,.0f}',
        "avg_transactions_count_per_customer_name": '{:,.2f}',
        "avg_transactions_sum_per_customer_name": '${:,.2f}',                  
        }
    for key,value in format_mapping.items():
            dfcalc[key]=dfcalc[key].apply(value.format)
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            # Write each dataframe to a different worksheet.
            df.to_excel(writer,sheet_name='clean_Data')
            dfcalc.to_excel(writer,sheet_name='Calculation')
            pivottablenames.to_excel(writer,sheet_name='Names')
            pivottabletransactiontype.to_excel(writer,sheet_name='Transaction_type')
            pivottabltransactioncountry.to_excel(writer,sheet_name='country')
            payment_note_final.to_excel(writer,sheet_name='payment_notes')
            highticket.to_excel(writer,sheet_name='High_Ticket')
            namefinal.to_excel(writer,sheet_name='name_checker')
            dup3.to_excel(writer,sheet_name='double_Transaction')
    writer.close()
    st.download_button(
              label='Download Excel File',
              data=buffer,
              file_name=f"{st.session_state.filename}.xlsx",
              mime="application/vnd.ms-excel"
            )
else:
    st.warning('you need to upload a csv')


#streamlit run project2_paypal.py
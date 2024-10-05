import streamlit as st
st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)
st.write("# Welcome to Paypal Reviews")
st.sidebar.success("select a page ")

st.markdown(
    """
    These 2 Apps Help us review transactions from a customer

    **👈 Select an app from the sidebar** to get started
   """
)
#streamlit run transaction/hello.py
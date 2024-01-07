import streamlit as st 
import pandas as pd
import uuid
import json

st.set_page_config(layout='wide')

def heading(st,body,size=1,align='center'):
    st.markdown(f'<h{size} style="text-align:{align};">{body}</h{size}><br>',unsafe_allow_html=True) 

heading(st,'Resource Assessment Tools')

st.sidebar.title("About")
st.sidebar.info(
    """
    - Web App URL: **Not available**
    - [GitHub repository](https://github.com/pierecnlnd/geothermal-resource-assessment)
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Mesias Piere
    \n[GitHub](https://github.com/pierecnlnd) | [LinkedIn](https://www.linkedin.com/in/mesias-canilandi-33541a228/) | [YouTube](https://www.youtube.com/channel/UCHY7QuZJb_mZsqhZpIovRgw)
    """
)

st.write('These are resource assessment tools for Geothermal development plan.\nYou can use any methods here.')

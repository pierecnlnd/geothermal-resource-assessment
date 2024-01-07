from backbone.heat_stored import *
import time
import streamlit as st

st.set_page_config(layout='wide')

def heading(st,body,size=1,align='center'):
    st.markdown(f'<h{size} style="text-align:{align};">{body}</h{size}><br>',unsafe_allow_html=True) 

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

# ---- HEAT STORED METHOD ----
heading(st,'Heat Stored Method')

df_input = pd.DataFrame({
        'input_data':[
          'Area (km²)',
          'Thickness (m)',
          'Porosity (fraction)',
          'Rock Density (kg/m³)',
          'Rock Heat Capacity (kJ/kgᵒC)',
          'Initial Temperature (ᵒC)',
          'Final Temperature (ᵒC)',
          'Initial Water Saturation (fraction)',
          'Final Water Saturation (fraction)',
          'Recovery Factor (fraction)',
          'Electricity Conversion Factor (fraction)',
          'Life Time (years)'
        ],
        'min':[0.0 for i in range(12)],
        'max':[0.0 for i in range(12)],
        'most':[0.0 for i in range(12)],
        'reference':['' for i in range(12)]
})

def upload_data(df_edited,n):
    a = {}
    a['min'] = df_edited['min'].values[0]
    a['max'] = df_edited['max'].values[0]
    a['most'] = df_edited['most'].values[0]
    
    h = {}
    h['min'] = df_edited['min'].values[1]
    h['max'] = df_edited['max'].values[1]
    h['most'] = df_edited['most'].values[1]
    # if h['most'] != 0 and not np.isnan(h['most']):
    #     st.write('lose')

    phi = {}
    phi['min'] = df_edited['min'].values[2]
    phi['max'] = df_edited['max'].values[2]
    phi['most'] = df_edited['most'].values[2]
    
    rho_r = {}
    rho_r['min'] = df_edited['min'].values[3]
    rho_r['max'] = df_edited['max'].values[3]
    rho_r['most'] = df_edited['most'].values[3]
    
    cr = {}
    cr['min'] = df_edited['min'].values[4]
    cr['max'] = df_edited['max'].values[4]
    cr['most'] = df_edited['most'].values[4]
    
    rf = {}
    rf['min'] = df_edited['min'].values[9]
    rf['max'] = df_edited['max'].values[9]
    rf['most'] = df_edited['most'].values[9]
    
    ti = {}
    ti['min'] = df_edited['min'].values[5]
    ti['max'] = df_edited['max'].values[5]
    ti['most'] = df_edited['most'].values[5]
    
    tf = {}
    tf['min'] = df_edited['min'].values[6]
    tf['max'] = df_edited['max'].values[6]
    tf['most'] = df_edited['most'].values[6]
    
    ec = {}
    ec['min'] = df_edited['min'].values[10]
    ec['max'] = df_edited['max'].values[10]
    ec['most'] = df_edited['most'].values[10]

    swi = {}
    swi['min'] = df_edited['min'].values[7]
    swi['max'] = df_edited['max'].values[7]
    swi['most'] = df_edited['most'].values[7]
    
    swf = {}
    swf['min'] = df_edited['min'].values[8]
    swf['max'] = df_edited['max'].values[8]
    swf['most'] = df_edited['most'].values[8]
    
    t = {}
    t['min'] = df_edited['min'].values[11]
    t['max'] = df_edited['max'].values[11]
    t['most'] = df_edited['most'].values[11]

    res = Qel(a,h,phi,rho_r,cr,ti,tf,swi,swf,rf,ec,t,n)
    df, fig1 = create_freq_table(res)

    return res,df,fig1

@st.cache_data
def download_df(df):
    return df.to_csv().encode('utf-8')

project_name = ''
df = ''
fig1 = ''

left, right = st.columns([4,7])

with left:
    with st.form("monte_form"):
        project_name = st.text_input('Project Name')
        st.write('Input Data')
        df_edited = st.data_editor(
            df_input,
            column_config={
                'input_data':'Data Input',
                'min':'Min Value',
                'max':'Max Value',
                'most':'Most Value',
                'reference':'Reference'
            },
            use_container_width=True,
            hide_index=True,
            height=459
        )
        number_of_iterations = st.number_input('Number of Iterations',value=50000)

        col1,col2,col3 = st.columns(3)
        submitted = col2.form_submit_button("Submit")
        df_done = False
        if submitted:
            with st.spinner('Wait for it...'):
                res,df,fig1 = upload_data(df_edited,number_of_iterations)
                st.success('Succeeded!')
                df_done = True

with right:
    if df_done:              
        left_pad, mid_pad, right_pad = st.columns(3)
        with left_pad:
            heading(st,f'{project_name} Result',size=3,align='left')
            download_file = download_df(df)
            st.download_button(
                label="Download result as CSV",
                data=download_file,
                file_name='result.csv',
                mime='text/csv',
            )
            st.data_editor(df,hide_index=True)
        with mid_pad:
            st.plotly_chart(fig1)
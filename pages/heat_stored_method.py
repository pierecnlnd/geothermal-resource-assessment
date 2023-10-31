from backbone.heat_stored import *
import time
import streamlit as st

def heading(st,body,size=1,align='center'):
    st.markdown(f'<h{size} style="text-align:{align};">{body}</h{size}><br>',unsafe_allow_html=True) 

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
        'most':[0.0 for i in range(12)]
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

project_name = ''

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
        },
        use_container_width=True,
        hide_index=True
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

if df_done:      
    heading(st,f'{project_name} Result',size=3,align='left')
    st.dataframe(df,hide_index=True,use_container_width=True)
    st.plotly_chart(fig1,use_container_width=True)
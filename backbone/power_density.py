from pyXSteam.XSteam import XSteam
from plotly.subplots import make_subplots
from scipy import interpolate
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st_ = XSteam(XSteam.UNIT_SYSTEM_MKS)

def create_rand_arr(dict_,n):
    dict_['max'] = float(dict_['max'])
    dict_['min'] = float(dict_['min'])
    dict_['most'] = float(dict_['most'])
    if dict_['max'] != 0 and not np.isnan(dict_['max']):
        if dict_['most'] != 0 and not np.isnan(dict_['most']):
            res = np.random.triangular(dict_['min'],dict_['most'],dict_['max'],n)
        else:
            res = np.random.uniform(dict_['min'],dict_['max'],n)
    else:
        res = np.array([dict_['min'] for i in range(n)])
    return res

def Qel(a,PD,n=5000):
    a = create_rand_arr(a,n)
    PD = create_rand_arr(PD,n)
    return a*PD

def create_freq_table(res):
    res = np.sort(res)
    min_ = np.min(res)
    max_ = np.max(res)
    count_ = len(res)
    print(res)
    bin_range = int(1+10/3*np.log10(count_))
    interval_ = (max_-min_)/bin_range
    hist, bin_edges = np.histogram(res, bins=bin_range)
    cumulative_percent = np.cumsum(hist) / np.sum(hist)
    df_cum_freq = pd.DataFrame({
        'Qel (MWe)':bin_edges[:-1],
        'Frequency':hist,
        'Cumulative (%)':cumulative_percent*100
    })
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_edges[:-1],
        y=hist,
        marker_color='#EB89B5',
        opacity=0.75,
        name='Frequency'
    ))
    fig.add_trace(go.Scatter(
        x=bin_edges[:-1], 
        y=cumulative_percent,
        mode='lines',
        line_color='red',
        name='Cumulative Distribution (%)',
        yaxis='y2'
    ))
    fig.update_layout(
        title='Monte Carlo Simulation',
        width=700,
        height=500,
        font_family='Times New Roman',
        xaxis=dict(title='Qel (MWe)',griddash='solid'), 
        yaxis=dict(title='Count', gridcolor='rgba(0, 0, 0, 0)',griddash='solid'),
        yaxis2=dict(title='Cumulative (%)',tickformat='.2%', overlaying="y", side='right',griddash='solid'),
        bargap=0.2,
    )
    fig.update_xaxes(
        griddash='solid'
    )
    fig.update_yaxes(
        griddash='solid'
    )
    probs = np.linspace(0,100,11,endpoint=True)
    df = pd.DataFrame({
        'Percentile':[f'P{int(_)}' for _ in probs],
        'Qel (MWe)':[np.percentile(res,_) for _ in probs],
    }) 
    return df, fig
    
            



                
    


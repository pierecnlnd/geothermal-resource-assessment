from pyXSteam.XSteam import XSteam
from plotly.subplots import make_subplots
from scipy import interpolate
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def interpolate_xy(x,y,x_interp):
    f = interpolate.interp1d(x,y)
    return f(x_interp)

st_ = XSteam(XSteam.UNIT_SYSTEM_MKS)

def create_rand_arr(dict_,n):
    dict_['max'] = float(dict_['max'])
    dict_['min'] = float(dict_['min'])
    dict_['most'] = float(dict_['most'])
    if dict_['max'] != 0:
        if dict_['most'] != 0:
            res = np.random.triangular(dict_['min'],dict_['most'],dict_['max'],n)
        else:
            res = np.random.uniform(dict_['min'],dict_['max'],n)
    else:
        res = np.array([dict_['min'] for i in range(n)])
    return res

def Qe(a,h,phi,rho_r,cr,t,sw):
    Qr = a * 10 ** 6 * h * (1 - phi) * rho_r * cr * t
    
    Ql = a * 10 ** 6 * h * phi * sw * np.array([st_.rhoL_t(i) for i in t]) * np.array([st_.uL_t(i) for i in t])
    Qv = a * 10 ** 6 * h * phi * (1-sw) * np.array([st_.rhoV_t(i) for i in t]) * np.array([st_.uV_t(i) for i in t])
    return Qr+Ql+Qv

def Qth(a,h,phi,rho_r,cr,ti,tf,swi,swf):
    Qf = Qe(a, h, phi, rho_r, cr, tf, swf)
    Qi = Qe(a, h, phi, rho_r, cr, ti, swi)
    return Qi - Qf

def Qel(a,h,phi,rho_r,cr,ti,tf,swi,swf,rf,ec,t,n=5000):
    a = create_rand_arr(a,n)
    h = create_rand_arr(h,n)
    phi = create_rand_arr(phi,n)
    rho_r = create_rand_arr(rho_r,n)
    cr = create_rand_arr(cr,n)
    ti = create_rand_arr(ti,n)
    tf = create_rand_arr(tf,n)
    swi = create_rand_arr(swi,n)
    swf = create_rand_arr(swf,n)
    rf = create_rand_arr(rf,n)
    ec = create_rand_arr(ec,n)
    t = create_rand_arr(t,n)
    res = rf*Qth(a,h,phi,rho_r,cr,ti,tf,swi,swf)*ec/(t*365*24*3600*1000)
    return res

def create_freq_table(res):
    res = np.sort(res)
    min_ = np.min(res)
    max_ = np.max(res)
    count_ = len(res)
    bin_range = 1+10/3*np.log10(count_)
    interval_ = (max_-min_)/bin_range
    value_range_arr = np.arange(min_,max_+1,interval_)
    freq = []
    for i in range(len(value_range_arr)):
        n = 0
        for j in range(len(res)):
            if i == 0:
                if res[j] == value_range_arr[i]:
                    n += 1
            else:
                if res[j] <= value_range_arr[i] and res[j] > value_range_arr[i-1]:
                    n += 1
        freq.append(n)
    cum_freq = []
    cum = 0
    for i in range(len(freq)):
        cum += freq[i]
        cum_freq.append(cum/np.sum(freq)*100) 
    df = pd.DataFrame({
        'Qel (MWe)':value_range_arr,
        'Freq':freq,
        'Cum. Freq (%)':cum_freq
    })
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(
        x=res,
        xbins=dict( # bins used for histogram
            start=min_,
            end=max_,
            size=interval_
        ),
        marker_color='#EB89B5',
        opacity=0.75,
        name='Frequency'
    ))
    fig1.add_trace(go.Scatter(
        x=df['Qel (MWe)'],
        y=df['Cum. Freq (%)'].values/100,
        name='Cumulative',
        yaxis='y2'
    ))
    fig1.update_layout(
        title='Resource assessment result',
        xaxis=dict(
            title='Qel (MWe)',
        ), 
        yaxis=dict(title='Count', gridcolor='rgba(0, 0, 0, 0)'),
        yaxis2=dict(title='Cumulative (%)',tickformat='%', overlaying="y", side='right',),
        bargap=0.2, # gap between bars of adjacent location coordinates
    )
    probs = np.arange(10,110,10)
    qel = interpolate_xy(cum_freq,value_range_arr,probs)
    df = pd.DataFrame({
        'Percentile':[f'P{_}' for _ in probs],
        'Qel (MWe)':qel,
    }) 
    return df, fig1
    
            



                
    


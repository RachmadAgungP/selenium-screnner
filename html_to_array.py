import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
from ast import literal_eval
import pandas as pd 
from pandas import DataFrame
from datetime import datetime
import talib as tb 
from plotly.subplots import make_subplots
start= '02/09/2020'
end = "08/07/2020"
P_SMA = 20
saham ="TLKM"
page = requests.get("https://www.indopremier.com/module/saham/include/json-charting.php?code=%s&start=%s&end=%s"% (saham,start,end))
soup = BeautifulSoup(page.content, 'html.parser')
def technical_indicators_df(daily_data):
    """
    Assemble a dataframe of technical indicator series for a single stock
    """
    o = daily_data['Open'].values
    c = daily_data['Close'].values
    h = daily_data['High'].values
    l = daily_data['Low'].values
    v = daily_data['Vol'].astype(float).values
    # define the technical analysis matrix

    # Most data series are normalized by their series' mean
    ta = pd.DataFrame()
    ta['MA5'] = tb.SMA(c,timeperiod=5)
    
    ta['BBANDS_U'],ta['BBANDS_M'],ta['BBANDS_L']= tb.BBANDS(c, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    # ta['BBANDS_M'] = tb.BBANDS(c, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1] / \
    #                     tb.BBANDS(c, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1].mean()
    # ta['BBANDS_L'] = tb.BBANDS(c, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2] / \
    #                     tb.BBANDS(c, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2].mean()
    ta['AD'] = tb.AD(h, l, c, v) / tb.AD(h, l, c, v).mean()
    ta['ATR'] = tb.ATR(h, l, c, timeperiod=14) / tb.ATR(h, l, c, timeperiod=14).mean()
    ta['HT_DC'] = tb.HT_DCPERIOD(c) / tb.HT_DCPERIOD(c).mean()
    ta["High/Open"] = h / o
    ta["Low/Open"] = l / o
    ta["Close/Open"] = c / o
    return ta
    
def lines_ta(data_x,data_y,modes,names,colors,legends=None,showlegends=True,fillcolors=None,fills=None):
    obj = go.Scatter(
            x=data_x,
            y=data_y,
            mode=modes,
            name=names,
            line=dict(
                color=colors
            ),
            legendgroup=legends,
            showlegend=showlegends,
            fillcolor=fillcolors,
            fill=fills
        )

    return obj


if page.status_code==200:
    t = soup.prettify()
    data = literal_eval(t)
    data = DataFrame(data,columns=["Date","Open","High","Low","Close","Vol"])
    data["Date"] = pd.to_datetime(data["Date"],unit='ms')
    # data = pd.read_csv("CLAY.JK.csv")
    sma = tb.SMA(data['Close'].values,P_SMA)
    tach = technical_indicators_df(data)
    print (tach['BBANDS_M'])
    print (tach['BBANDS_L'])
    print (tach['MA5'])
    fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True, 
                    vertical_spacing=0.02,row_heights=[0.7, 0.3])
    
    fig.add_trace(
        go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
                ),row=1, col=1
    )

    close =  lines_ta(data['Date'],data['Close'],"lines","Close","orange") 
    fig.add_trace(
        close,row=1, col=1
    )

    upper_bound = go.Scatter(
        name='Upper Bound',
        x=data['Date'],
        y=tach['BBANDS_U'],
        mode='lines',
        legendgroup="group",
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
    fig.add_trace(
       upper_bound,row=1, col=1
    )
    trace = go.Scatter(
        name='Measurement',
        x=data['Date'],
        y=tach['BBANDS_M'],
        mode='lines',
        # legendgroup="group",
        line=dict(color='rgb(31, 119, 180)'),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
    fig.add_trace(
       trace,row=1, col=1
    )
    lower_bound = go.Scatter(
        name='Lower Bound',
        x=data['Date'],
        y=tach['BBANDS_L'],
        marker=dict(color="#444"),
        line=dict(width=0),
        # legendgroup="group",
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')

    fig.add_trace(
       lower_bound,row=1, col=1
    )

    ma = lines_ta(data['Date'],tach['MA5'],"lines","MA5","red") 
    fig.add_trace(
       ma,row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=data['Date'],
            y=data['Vol'],
            name="vol",
        ),row=2, col=1
    )
    
    fig.update_yaxes(title_text="Harga", row=1, col=1)
    fig.update_yaxes(title_text="volume", row=2, col=1)
    fig.update_layout(xaxis_rangeslider_visible=False,title_text=saham)
    
fig.show()

# INCREASING_COLOR = '#17BECF'
# DECREASING_COLOR = '#7F7F7F'
# for b in range(len(data)):
#     
#     print("dt_object =", data)




from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import streamlit as st

def ChartOrder_Generic(Kbar_df, TR, title="", indicators=None):
    # 指標線 (例如 RSI/MACD/Bollinger Bands)
    indicators = indicators or []

    # 紀錄下單點
    BTR = [ i for i in TR if i[0]=='Buy' or i[0]=='B' ]
    STR = [ i for i in TR if i[0]=='Sell' or i[0]=='S' ]

    def extract_points(records, direction):
        Order_date, Order_price, Cover_date, Cover_price = [], [], [], []
        for date, Low, High in zip(Kbar_df['time'], Kbar_df['low'], Kbar_df['high']):
            if date in [ i[2] for i in records ]:
                Order_date.append(date)
                Order_price.append(Low * 0.999 if direction == "Buy" else High * 1.001)
            else:
                Order_date.append(np.nan)
                Order_price.append(np.nan)
            if date in [ i[4] for i in records ]:
                Cover_date.append(date)
                Cover_price.append(High * 1.001 if direction == "Buy" else Low * 0.999)
            else:
                Cover_date.append(np.nan)
                Cover_price.append(np.nan)
        return Order_date, Order_price, Cover_date, Cover_price

    BuyOrder_date, BuyOrder_price, BuyCover_date, BuyCover_price = extract_points(BTR, "Buy")
    SellOrder_date, SellOrder_price, SellCover_date, SellCover_price = extract_points(STR, "Sell")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=Kbar_df['time'], open=Kbar_df['open'], high=Kbar_df['high'], low=Kbar_df['low'], close=Kbar_df['close'], name='K線'), secondary_y=True)

    for ind in indicators:
        fig.add_trace(go.Scatter(x=Kbar_df['time'], y=Kbar_df[ind['col']], mode='lines', line=dict(color=ind['color'], width=2), name=ind['name']), secondary_y=False)

    fig.add_trace(go.Scatter(x=BuyOrder_date, y=BuyOrder_price, mode='markers', marker=dict(color='red', symbol='triangle-up', size=10), name='作多進場點'), secondary_y=False)
    fig.add_trace(go.Scatter(x=BuyCover_date, y=BuyCover_price, mode='markers', marker=dict(color='blue', symbol='triangle-down', size=10), name='作多出場點'), secondary_y=False)
    fig.add_trace(go.Scatter(x=SellOrder_date, y=SellOrder_price, mode='markers', marker=dict(color='green', symbol='triangle-down', size=10), name='作空進場點'), secondary_y=False)
    fig.add_trace(go.Scatter(x=SellCover_date, y=SellCover_price, mode='markers', marker=dict(color='black', symbol='triangle-up', size=10), name='作空出場點'), secondary_y=False)

    fig.layout.yaxis2.showgrid = True
    st.subheader(f"策略圖表: {title}")
    st.plotly_chart(fig, use_container_width=True)

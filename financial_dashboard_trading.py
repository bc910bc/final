# -*- coding: utf-8 -*-
"""
金融資料視覺化看板

@author: 
"""

# 載入必要模組
import os
#import haohaninfo
#from order_Lo8 import Record
import numpy as np
#from talib.abstract import SMA,EMA, WMA, RSI, BBANDS, MACD
#import sys
import indicator_f_Lo2_short,datetime, indicator_forKBar_short
import pandas as pd
import streamlit as st 
import streamlit.components.v1 as stc 
from order_streamlit import Record
import matplotlib.pyplot as plt
import matplotlib

#%%
####### (1) 開始設定 #######
###### 設定網頁標題介面 
# 自訂 CSS 樣式 (淺色主題 + 元件美化)
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .stApp {
            background-color: #ffffff;
            font-family: "Helvetica Neue", sans-serif;
            color: #2c3e50;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        .st-expander {
            border: 1px solid #b0c4de;
            border-radius: 10px;
            background-color: #e6f0ff;
            box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
        }
        .css-1d391kg {
            background-color: #e6f0ff;
        }
    </style>
""", unsafe_allow_html=True)

# 精美標題區塊
html_temp = """
    <div style="background-color:#4a90e2;padding:20px;border-radius:12px;margin-bottom:20px">
        <h1 style="color:white;text-align:center;margin-bottom:0;">🎯 K線獵人：智慧交易看板</h1>
        <h3 style="color:white;text-align:center;margin-top:5px;">📊 程式化交易決策平台</h3>
    </div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

# 額外標示開發者身份（平台內呈現）
st.markdown("#### 👨‍💻 製作人：資科三B 吳東翰")



###### 讀取資料
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def load_data(path):
    df = pd.read_pickle(path)
    return df
# ##### 讀取 excel 檔
# df_original = pd.read_excel("kbars_2330_2022-01-01-2022-11-18.xlsx")


###### 選擇金融商品
st.subheader("選擇金融商品: ")
choices = ['華碩: 2023.4.17 至 2025.4.16', '聯電期貨: 2023.4.17 至 2025.4.16', '富邦金期貨: 2023.4.15 至 2025.4.16']
choice = st.selectbox('選擇金融商品', choices, index=0)
##### 读取Pickle文件
if choice == '華碩: 2023.4.17 至 2025.4.16':
    df_original = load_data('kbars_1h_2357_2023-04-17_To_2025-04-16.pkl')
    product_name = '華碩2357'
    # df_original = load_data('kbars_2330_2022-01-01-2024-04-09.pkl')
    # df_original = load_data('kbars_2330_2022-01-01-2022-11-18.pkl')  
    # df_original = pd.read_pickle('kbars_2330_2022-01-01-2022-11-18.pkl')
    #df.columns  ## Index(['Unnamed: 0', 'time', 'open', 'low', 'high', 'close', 'volume','amount'], dtype='object')
    # df_original = df_original.drop('Unnamed: 0',axis=1)
# if choice == '大台指2024.12到期: 2024.1 至 2024.4.9':
#     df_original = load_data('kbars_TXF202412_2024-01-01-2024-04-09.pkl')  
if choice == '聯電期貨: 2023.4.17 至 2025.4.16':
    df_original = load_data('kbars_1h_CCF_2023-04-17_To_2025-04-16.pkl')
    product_name = '聯電期貨'
if choice == '富邦金期貨: 2023.4.15 至 2025.4.16':
    df_original = load_data('kbars_1h_CEF_2023-04-15_To_2025-04-16.pkl')
    product_name = '富邦金期貨'



###### 選擇資料區間
st.subheader("選擇資料時間區間")
if choice == '華碩: 2023.4.17 至 2025.4.16':
    start_date = st.text_input('輸入開始日期(日期格式: 2023-04-17), 區間: 2023.4.17 至 2025.4.16', '2023-04-17')
    end_date = st.text_input('輸入結束日期 (日期格式: 2025-04-16), 區間: 2023.4.17 至 2025.4.16', '2025-04-16')
if choice == '聯電期貨: 2023.4.17 至 2025.4.16':
    start_date = st.text_input('輸入開始日期(日期格式: 2023-04-17), 區間: 2023.4.17 至 2025.4.16', '2023-04-17')
    end_date = st.text_input('輸入結束日期 (日期格式: 2025-04-16), 區間: 2023.4.17 至 2025.4.16', '2025-04-16')
if choice == '富邦金期貨: 2023.4.15 至 2025.4.16':
    start_date = st.text_input('輸入開始日期(日期格式: 2023-04-15), 區間:2023.4.15 至 2025.4.16', '2023-04-15')
    end_date = st.text_input('輸入結束日期 (日期格式: 2025-04-16), 區間:2023.4.15 至 2025.4.16', '2025-04-16')




start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
# 使用条件筛选选择时间区间的数据
df = df_original[(df_original['time'] >= start_date) & (df_original['time'] <= end_date)]


#%%
####### (2) 轉化為字典 #######
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def To_Dictionary_1(df, product_name):
    KBar_dic = df.to_dict()
    KBar_open_list = list(KBar_dic['open'].values())
    KBar_dic['open']=np.array(KBar_open_list)
    
    KBar_dic['product'] = np.repeat(product_name, KBar_dic['open'].size)
    #KBar_dic['product'].size   ## 1596
    #KBar_dic['product'][0]      ## 'tsmc'
    
    KBar_time_list = list(KBar_dic['time'].values())
    KBar_time_list = [i.to_pydatetime() for i in KBar_time_list] ## Timestamp to datetime
    KBar_dic['time']=np.array(KBar_time_list)
    
    KBar_low_list = list(KBar_dic['low'].values())
    KBar_dic['low']=np.array(KBar_low_list)
    
    KBar_high_list = list(KBar_dic['high'].values())
    KBar_dic['high']=np.array(KBar_high_list)
    
    KBar_close_list = list(KBar_dic['close'].values())
    KBar_dic['close']=np.array(KBar_close_list)
    
    KBar_volume_list = list(KBar_dic['volume'].values())
    KBar_dic['volume']=np.array(KBar_volume_list)
    
    KBar_amount_list = list(KBar_dic['amount'].values())
    KBar_dic['amount']=np.array(KBar_amount_list)
    
    return KBar_dic

KBar_dic = To_Dictionary_1(df, product_name)


#%%
#######  (3) 改變 KBar 時間長度 & 形成 KBar 字典 (新週期的) & Dataframe #######
###### 定義函數: 進行 K 棒更新  &  形成 KBar 字典 (新週期的): 設定cycle_duration可以改成你想要的 KBar 週期
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def Change_Cycle(Date,cycle_duration,KBar_dic,product_name):
    ###### 進行 K 棒更新
    KBar = indicator_forKBar_short.KBar(Date,cycle_duration)    ## 設定cycle_duration可以改成你想要的 KBar 週期
    for i in range(KBar_dic['time'].size):
        #time = datetime.datetime.strptime(KBar_dic['time'][i],'%Y%m%d%H%M%S%f')
        time = KBar_dic['time'][i]
        #prod = KBar_dic['product'][i]
        open_price= KBar_dic['open'][i]
        close_price= KBar_dic['close'][i]
        low_price= KBar_dic['low'][i]
        high_price= KBar_dic['high'][i]
        qty =  KBar_dic['volume'][i]
        amount = KBar_dic['amount'][i]
        #tag=KBar.TimeAdd(time,price,qty,prod)
        tag=KBar.AddPrice(time, open_price, close_price, low_price, high_price, qty)
    
    ###### 形成 KBar 字典 (新週期的):
    KBar_dic = {}
    KBar_dic['time'] =  KBar.TAKBar['time']   
    #KBar_dic['product'] =  KBar.TAKBar['product']
    KBar_dic['product'] = np.repeat(product_name, KBar_dic['time'].size)
    KBar_dic['open'] = KBar.TAKBar['open']
    KBar_dic['high'] =  KBar.TAKBar['high']
    KBar_dic['low'] =  KBar.TAKBar['low']
    KBar_dic['close'] =  KBar.TAKBar['close']
    KBar_dic['volume'] =  KBar.TAKBar['volume']
    
    return KBar_dic
    

###### 改變日期資料型態
Date = start_date.strftime("%Y-%m-%d")  ## 變成字串


st.subheader("設定技術指標視覺化圖形之相關參數:")

###### 設定 K 棒的時間長度(分鐘): 
with st.expander("設定K棒相關參數:"):
    choices_unit = ['以分鐘為單位','以日為單位','以週為單位','以月為單位']
    choice_unit = st.selectbox('選擇計算K棒時間長度之單位', choices_unit, index=1)
    if choice_unit == '以分鐘為單位':
        cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:分鐘, 一日=1440分鐘)', value=1, key="KBar_duration_分")
        cycle_duration = float(cycle_duration)
    if choice_unit == '以日為單位':
        cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:日)', value=1, key="KBar_duration_日")
        cycle_duration = float(cycle_duration)
        cycle_duration = cycle_duration*1440
    if choice_unit == '以週為單位':
        cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:週)', value=1, key="KBar_duration_週")
        cycle_duration = float(cycle_duration)
        cycle_duration = cycle_duration*7*1440
    if choice_unit == '以月為單位':
        cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:月, 一月=30天)', value=1, key="KBar_duration_月")
        cycle_duration = float(cycle_duration)
        cycle_duration = cycle_duration*30*1440


###### 進行 K 棒更新  & 形成 KBar 字典 (新週期的)
KBar_dic = Change_Cycle(Date,cycle_duration,KBar_dic,product_name)   ## 設定cycle_duration可以改成你想要的 KBar 週期

###### 將K線 Dictionary 轉換成 Dataframe
KBar_df = pd.DataFrame(KBar_dic)


#%%
####### (4) 計算各種技術指標 #######

#%%
######  (i) 移動平均線策略 
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def Calculate_MA(df, period=10):
    ##### 計算長短移動平均線
    ma = df['close'].rolling(window=period).mean()
    return ma
  
#####  設定長短移動平均線的 K棒 長度:
with st.expander("設定長短移動平均線的 K棒 長度:"):
    # st.subheader("設定計算長移動平均線(MA)的 K棒週期數目(整數, 例如 10)")
    LongMAPeriod=st.slider('設定計算長移動平均線(MA)的 K棒週期數目(整數, 例如 10)', 0, 100, 10, key='visualization_MA_long')
    # st.subheader("設定計算短移動平均線(MA)的 K棒週期數目(整數, 例如 2)")
    ShortMAPeriod=st.slider('設定計算短移動平均線(MA)的 K棒週期數目(整數, 例如 2)', 0, 100, 2, key='visualization_MA_short')

##### 計算長短移動平均線
KBar_df['MA_long'] = Calculate_MA(KBar_df, period=LongMAPeriod)
KBar_df['MA_short'] = Calculate_MA(KBar_df, period=ShortMAPeriod)

##### 尋找最後 NAN值的位置
last_nan_index_MA = KBar_df['MA_long'][::-1].index[KBar_df['MA_long'][::-1].apply(pd.isna)][0]


#%%
######  (ii) RSI 策略 
##### 假设 df 是一个包含价格数据的Pandas DataFrame，其中 'close' 是KBar週期收盤價
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def Calculate_RSI(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
  
##### 順勢策略
#### 設定長短 RSI 的 K棒 長度:
with st.expander("設定長短 RSI 的 K棒 長度:"):
    # st.subheader("設定計算長RSI的 K棒週期數目(整數, 例如 10)")
    LongRSIPeriod=st.slider('設定計算長RSI的 K棒週期數目(整數, 例如 10)', 0, 1000, 10, key='visualization_RSI_long')
    # st.subheader("設定計算短RSI的 K棒週期數目(整數, 例如 2)")
    ShortRSIPeriod=st.slider('設定計算短RSI的 K棒週期數目(整數, 例如 2)', 0, 1000, 2, key='visualization_RSI_short')

#### 計算 RSI指標長短線, 以及定義中線
KBar_df['RSI_long'] = Calculate_RSI(KBar_df, LongRSIPeriod)
KBar_df['RSI_short'] = Calculate_RSI(KBar_df, ShortRSIPeriod)
KBar_df['RSI_Middle']=np.array([50]*len(KBar_dic['time']))

#### 尋找最後 NAN值的位置
last_nan_index_RSI = KBar_df['RSI_long'][::-1].index[KBar_df['RSI_long'][::-1].apply(pd.isna)][0]


# ##### 逆勢策略
# #### 建立部位管理物件
# OrderRecord=Record() 
# #### 計算 RSI指標, 天花板與地板
# RSIPeriod=5
# Ceil=80
# Floor=20
# MoveStopLoss=30
# KBar_dic['RSI']=RSI(KBar_dic,timeperiod=RSIPeriod)
# KBar_dic['Ceil']=np.array([Ceil]*len(KBar_dic['time']))
# KBar_dic['Floor']=np.array([Floor]*len(KBar_dic['time']))

# #### 將K線 Dictionary 轉換成 Dataframe
# KBar_RSI_df=pd.DataFrame(KBar_dic)


#%%
######  (iii) Bollinger Band (布林通道) 策略 
##### 假设df是包含价格数据的Pandas DataFrame，'close'列是每日收盘价格
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def Calculate_Bollinger_Bands(df, period=20, num_std_dev=2):
    df['SMA'] = df['close'].rolling(window=period).mean()
    df['Standard_Deviation'] = df['close'].rolling(window=period).std()
    df['Upper_Band'] = df['SMA'] + (df['Standard_Deviation'] * num_std_dev)
    df['Lower_Band'] = df['SMA'] - (df['Standard_Deviation'] * num_std_dev)
    return df


#####  設定布林通道(Bollinger Band)相關參數:
with st.expander("設定布林通道(Bollinger Band)相關參數:"):
    # st.subheader("設定計算布林通道(Bollinger Band)上中下三通道之K棒週期數目(整數, 例如 20)")
    period = st.slider('設定計算布林通道(Bollinger Band)上中下三通道之K棒週期數目(整數, 例如 20)', 0, 100, 20, key='BB_period')
    # st.subheader("設定計算布林通道(Bollinger Band)上中(或下中)通道之帶寬(例如 2 代表上中通道寬度為2倍的標準差)")
    num_std_dev = st.slider('設定計算布林通道(Bollinger Band)上中(或下中)通道之帶寬(例如 2 代表上中通道寬度為2倍的標準差)', 0, 100, 2, key='BB_heigh')

##### 計算布林通道上中下通道:
KBar_df = Calculate_Bollinger_Bands(KBar_df, period, num_std_dev)

##### 尋找最後 NAN值的位置
last_nan_index_BB = KBar_df['SMA'][::-1].index[KBar_df['SMA'][::-1].apply(pd.isna)][0]


#%%
######  (iv) MACD(異同移動平均線) 策略 
# 假设df是包含价格数据的Pandas DataFrame，'price'列是每日收盘价格
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def Calculate_MACD(df, fast_period=12, slow_period=26, signal_period=9):
    df['EMA_Fast'] = df['close'].ewm(span=fast_period, adjust=False).mean()
    df['EMA_Slow'] = df['close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD'] = df['EMA_Fast'] - df['EMA_Slow']  ## DIF
    df['Signal_Line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()   ## DEA或信號線
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']  ## MACD = DIF-DEA
    return df

#####  設定MACD三種週期的K棒長度:
with st.expander("設定MACD三種週期的K棒長度:"):
    # st.subheader("設定計算 MACD的快速線週期(例如 12根日K)")
    fast_period = st.slider('設定計算 MACD快速線的K棒週期數目(例如 12根日K)', 0, 100, 12, key='visualization_MACD_quick')
    # st.subheader("設定計算 MACD的慢速線週期(例如 26根日K)")
    slow_period = st.slider('設定計算 MACD慢速線的K棒週期數目(例如 26根日K)', 0, 100, 26, key='visualization_MACD_slow')
    # st.subheader("設定計算 MACD的訊號線週期(例如 9根日K)")
    signal_period = st.slider('設定計算 MACD訊號線的K棒週期數目(例如 9根日K)', 0, 100, 9, key='visualization_MACD_signal')

##### 計算MACD:
KBar_df = Calculate_MACD(KBar_df, fast_period, slow_period, signal_period)

##### 尋找最後 NAN值的位置
# last_nan_index_MACD = KBar_df['MACD'][::-1].index[KBar_df['MACD'][::-1].apply(pd.isna)][0]
#### 試著找出最後一個 NaN 值的索引，但在這之前要檢查是否有 NaN 值
nan_indexes_MACD = KBar_df['MACD'][::-1].index[KBar_df['MACD'][::-1].apply(pd.isna)]
if len(nan_indexes_MACD) > 0:
    last_nan_index_MACD = nan_indexes_MACD[0]
else:
    last_nan_index_MACD = 0




# ####### (5) 將 Dataframe 欄位名稱轉換(第一個字母大寫)  ####### 
# KBar_df_original = KBar_df
# KBar_df.columns = [ i[0].upper()+i[1:] for i in KBar_df.columns ]


#%%
####### (5) 畫圖 #######
st.subheader("技術指標視覺化圖形")
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
#from plotly.offline import plot
# import plotly.offline as pyoff


###### K線圖, 移動平均線MA
with st.expander("K線圖, 移動平均線"):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    
    #### include candlestick with rangeselector
    fig1.add_trace(go.Candlestick(x=KBar_df['time'],
                    open=KBar_df['open'], high=KBar_df['high'],
                    low=KBar_df['low'], close=KBar_df['close'], name='K線'),
                   secondary_y=True)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    #### include a go.Bar trace for volumes
    fig1.add_trace(go.Bar(x=KBar_df['time'], y=KBar_df['volume'], name='成交量', marker=dict(color='#a3b8d1')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
    fig1.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA+1:], y=KBar_df['MA_long'][last_nan_index_MA+1:], mode='lines',line=dict(color='#3aa17e', width=2), name=f'{LongMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=True)
    fig1.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA+1:], y=KBar_df['MA_short'][last_nan_index_MA+1:], mode='lines',line=dict(color='#f5a623', width=2), name=f'{ShortMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=True)
    
    fig1.layout.yaxis2.showgrid=True
    st.plotly_chart(fig1, use_container_width=True)


###### K線圖, RSI
with st.expander("長短 RSI"):
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    #### include candlestick with rangeselector
    # fig2.add_trace(go.Candlestick(x=KBar_df['Time'],
    #                 open=KBar_df['Open'], high=KBar_df['High'],
    #                 low=KBar_df['Low'], close=KBar_df['Close'], name='K線'),
    #                secondary_y=True)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    fig2.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_RSI+1:], y=KBar_df['RSI_long'][last_nan_index_RSI+1:], mode='lines',line=dict(color='red', width=2), name=f'{LongRSIPeriod}-根 K棒 移動 RSI'), 
                  secondary_y=False)
    fig2.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_RSI+1:], y=KBar_df['RSI_short'][last_nan_index_RSI+1:], mode='lines',line=dict(color='blue', width=2), name=f'{ShortRSIPeriod}-根 K棒 移動 RSI'), 
                  secondary_y=False)
    
    fig2.layout.yaxis2.showgrid=True
    st.plotly_chart(fig2, use_container_width=True)
    

###### K線圖, Bollinger Band    
with st.expander("K線圖,布林通道"):
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Candlestick(x=KBar_df['time'],
                    open=KBar_df['open'], high=KBar_df['high'],
                    low=KBar_df['low'], close=KBar_df['close'], name='K線'),
                    secondary_y=True)    
    fig3.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_BB+1:], y=KBar_df['SMA'][last_nan_index_BB+1:], mode='lines',line=dict(color='#7f8c8d', width=2), name='布林通道中軌道'), 
                  secondary_y=False)
    fig3.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_BB+1:], y=KBar_df['Upper_Band'][last_nan_index_BB+1:], mode='lines',line=dict(color='#e74c3c', width=2), name='布林通道上軌道'), 
                  secondary_y=False)
    fig3.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_BB+1:], y=KBar_df['Lower_Band'][last_nan_index_BB+1:], mode='lines',line=dict(color='#2980b9', width=2), name='布林通道下軌道'), 
                  secondary_y=False)
    
    fig3.layout.yaxis2.showgrid=True

    st.plotly_chart(fig3, use_container_width=True)



###### MACD
with st.expander("MACD(異同移動平均線)"):
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    
    # #### include candlestick with rangeselector
    # fig4.add_trace(go.Candlestick(x=KBar_df['Time'],
    #                 open=KBar_df['Open'], high=KBar_df['High'],
    #                 low=KBar_df['Low'], close=KBar_df['Close'], name='K線'),
    #                secondary_y=True)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    #### include a go.Bar trace for volumes
    fig4.add_trace(go.Bar(x=KBar_df['time'], y=KBar_df['MACD_Histogram'], name='MACD Histogram', marker=dict(color='#a3b8d1')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
    fig4.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MACD+1:], y=KBar_df['Signal_Line'][last_nan_index_MACD+1:], mode='lines',line=dict(color='#f5a623', width=2), name='訊號線(DEA)'), 
                  secondary_y=True)
    fig4.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MACD+1:], y=KBar_df['MACD'][last_nan_index_MACD+1:], mode='lines',line=dict(color='#3aa17e', width=2), name='DIF'), 
                  secondary_y=True)
    
    fig4.layout.yaxis2.showgrid=True
    st.plotly_chart(fig4, use_container_width=True)



#%%
####### (6) 程式交易 #######
st.subheader("程式交易:")
from ChartOrder_Generic import ChartOrder_Generic
###### 函數定義: 繪製K線圖加上MA以及下單點位
# @st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def ChartOrder_MA(Kbar_df,TR):
    # # 將K線轉為DataFrame
    # Kbar_df=KbarToDf(KBar)
    # 買(多)方下單點位紀錄
    BTR = [ i for i in TR if i[0]=='Buy' or i[0]=='B' ]
    BuyOrderPoint_date = [] 
    BuyOrderPoint_price = []
    BuyCoverPoint_date = []
    BuyCoverPoint_price = []
    for date,Low,High in zip(Kbar_df['time'],Kbar_df['low'],Kbar_df['high']):
        # 買方進場
        if date in [ i[2] for i in BTR ]:
            BuyOrderPoint_date.append(date)
            BuyOrderPoint_price.append(Low * 0.999)
        else:
            BuyOrderPoint_date.append(np.nan)
            BuyOrderPoint_price.append(np.nan)
        # 買方出場
        if date in [ i[4] for i in BTR ]:
            BuyCoverPoint_date.append(date)
            BuyCoverPoint_price.append(High * 1.001)
        else:
            BuyCoverPoint_date.append(np.nan)
            BuyCoverPoint_price.append(np.nan)
    # # 將下單點位加入副圖物件
    # if [ i for i in BuyOrderPoint if not np.isnan(i) ] !=[]:
    #     addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=50,marker='^',color='red'))  ## 200
    #     addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=50,marker='v',color='blue')) ## 200
    # 賣(空)方下單點位紀錄
    STR = [ i for i in TR if i[0]=='Sell' or i[0]=='S' ]
    SellOrderPoint_date = []
    SellOrderPoint_price = []
    SellCoverPoint_date = []
    SellCoverPoint_price = []
    for date,Low,High in zip(Kbar_df['time'],Kbar_df['low'],Kbar_df['high']):
        # 賣方進場
        if date in [ i[2] for i in STR]:
            SellOrderPoint_date.append(date)
            SellOrderPoint_price.append(High * 1.001)
        else:
            SellOrderPoint_date.append(np.nan)
            SellOrderPoint_price.append(np.nan)
        # 賣方出場
        if date in [ i[4] for i in STR ]:
            SellCoverPoint_date.append(date)
            SellCoverPoint_price.append(Low * 0.999)
        else:
            SellCoverPoint_date.append(np.nan)
            SellCoverPoint_price.append(np.nan)
    # # 將下單點位加入副圖物件
    # if [ i for i in SellOrderPoint if not np.isnan(i) ] !=[]:
    #     addp.append(mpf.make_addplot(SellOrderPoint,scatter=True,markersize=50,marker='v',color='green'))  ## 200
    #     addp.append(mpf.make_addplot(SellCoverPoint,scatter=True,markersize=50,marker='^',color='pink'))   ## 200
    # 開始繪圖
    # ChartKBar(KBar,addp,volume_enable)
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    
    #### include candlestick with rangeselector
    # fig5.add_trace(go.Candlestick(x=KBar_df['time'],
    #                 open=KBar_df['open'], high=KBar_df['high'],
    #                 low=KBar_df['low'], close=KBar_df['close'], name='K線'),
    #                 secondary_y=False)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    #### include a go.Bar trace for volumes
    # fig5.add_trace(go.Bar(x=KBar_df['time'], y=KBar_df['volume'], name='成交量', marker=dict(color='black')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
    fig5.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA_trading+1:], y=KBar_df['MA_long'][last_nan_index_MA_trading+1:], mode='lines',line=dict(color='orange', width=2), name=f'{LongMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=False)
    fig5.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA_trading+1:], y=KBar_df['MA_short'][last_nan_index_MA_trading+1:], mode='lines',line=dict(color='pink', width=2), name=f'{ShortMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=False)
    fig5.add_trace(go.Scatter(x=BuyOrderPoint_date, y=BuyOrderPoint_price, mode='markers',  marker=dict(color='red', symbol='triangle-up', size=10),  name='作多進場點'), secondary_y=False)
    fig5.add_trace(go.Scatter(x=BuyCoverPoint_date, y=BuyCoverPoint_price, mode='markers',  marker=dict(color='blue', symbol='triangle-down', size=10),  name='作多出場點'), secondary_y=False)
    fig5.add_trace(go.Scatter(x=SellOrderPoint_date, y=SellOrderPoint_price, mode='markers',  marker=dict(color='green', symbol='triangle-down', size=10),  name='作空進場點'), secondary_y=False)
    fig5.add_trace(go.Scatter(x=SellCoverPoint_date, y=SellCoverPoint_price, mode='markers',  marker=dict(color='black', symbol='triangle-up', size=10),  name='作空出場點'), secondary_y=False)
 
    fig5.layout.yaxis2.showgrid=True
    st.plotly_chart(fig5, use_container_width=True)

###### 選擇不同交易策略:
choices_strategy = ['<進場>: 移動平均線黃金交叉作多,死亡交叉作空. <出場>: 結算平倉(期貨), 移動停損.',
    '<進場>: RSI低於20作多, 高於80作空. <出場>: RSI反向穿越50或結算平倉.',
    '<進場>: 收盤跌破布林下軌作多, 突破上軌作空. <出場>: 回到中軌或結算平倉.',
    '<進場>: DIF上穿DEA作多, 下穿DEA作空. <出場>: DIF反向穿越DEA或結算平倉.']
choice_strategy = st.selectbox('選擇交易策略', choices_strategy, index=0)

##### 各別不同策略
if choice_strategy == '<進場>: 移動平均線黃金交叉作多,死亡交叉作空. <出場>: 結算平倉(期貨), 移動停損.':
    #### 選擇參數
    with st.expander("<策略參數設定>: 交易停損量、長移動平均線(MA)的K棒週期數目、短移動平均線(MA)的K棒週期數目、購買數量"):
        MoveStopLoss = st.slider('選擇程式交易停損量(股票:每股價格; 期貨(大小台指):台股指數點數. 例如: 股票進場做多時, 取30代表停損價格為目前每股價格減30元; 大小台指進場做多時, 取30代表停損指數為目前台股指數減30點)', 0, 100, 30, key='MoveStopLoss')
        LongMAPeriod_trading=st.slider('設定計算長移動平均線(MA)的 K棒週期數目(整數, 例如 10)', 0, 100, 10, key='trading_MA_long')
        ShortMAPeriod_trading=st.slider('設定計算短移動平均線(MA)的 K棒週期數目(整數, 例如 2)', 0, 100, 2, key='trading_MA_short')
        Order_Quantity = st.slider('選擇購買數量(股票單位為張數(一張為1000股); 期貨單位為口數)', 1, 100, 1, key='Order_Quantity')
    
        ### 計算長短移動平均線
        KBar_df['MA_long'] = Calculate_MA(KBar_df, period=LongMAPeriod_trading)
        KBar_df['MA_short'] = Calculate_MA(KBar_df, period=ShortMAPeriod_trading)
        
        ### 尋找最後 NAN值的位置
        last_nan_index_MA_trading = KBar_df['MA_long'][::-1].index[KBar_df['MA_long'][::-1].apply(pd.isna)][0]


        
        ### 建立部位管理物件
        OrderRecord=Record() 
        
        # ###### 變為字典
        # # KBar_dic = KBar_df_original.to_dict('list')
        # KBar_dic = KBar_df.to_dict('list')
        
    #### 開始回測
    for n in range(1,len(KBar_df['time'])-1):
        # 先判斷long MA的上一筆值是否為空值 再接續判斷策略內容
        if not np.isnan( KBar_df['MA_long'][n-1] ) :
            ## 進場: 如果無未平倉部位 
            if OrderRecord.GetOpenInterest()==0 :
                # 多單進場: 黃金交叉: short MA 向上突破 long MA
                if KBar_df['MA_short'][n-1] <= KBar_df['MA_long'][n-1] and KBar_df['MA_short'][n] > KBar_df['MA_long'][n] :
                    OrderRecord.Order('Buy', KBar_df['product'][n+1],KBar_df['time'][n+1],KBar_df['open'][n+1],Order_Quantity)
                    OrderPrice = KBar_df['open'][n+1]
                    StopLossPoint = OrderPrice - MoveStopLoss
                    continue
                # 空單進場:死亡交叉: short MA 向下突破 long MA
                if KBar_df['MA_short'][n-1] >= KBar_df['MA_long'][n-1] and KBar_df['MA_short'][n] < KBar_df['MA_long'][n] :
                    OrderRecord.Order('Sell', KBar_df['product'][n+1],KBar_df['time'][n+1],KBar_df['open'][n+1],Order_Quantity)
                    OrderPrice = KBar_df['open'][n+1]
                    StopLossPoint = OrderPrice + MoveStopLoss
                    continue
            # 多單出場: 如果有多單部位   
            elif OrderRecord.GetOpenInterest()>0 :
                ## 結算平倉(期貨才使用, 股票除非是下市櫃)
                if KBar_df['product'][n+1] != KBar_df['product'][n] :
                    OrderRecord.Cover('Sell', KBar_df['product'][n],KBar_df['time'][n],KBar_df['close'][n],OrderRecord.GetOpenInterest())
                    continue
                # 逐筆更新移動停損價位
                if KBar_df['close'][n] - MoveStopLoss > StopLossPoint :
                    StopLossPoint = KBar_df['close'][n] - MoveStopLoss
                # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
                elif KBar_df['close'][n] < StopLossPoint :
                    OrderRecord.Cover('Sell', KBar_df['product'][n+1],KBar_df['time'][n+1],KBar_df['open'][n+1],OrderRecord.GetOpenInterest())
                    continue
            # 空單出場: 如果有空單部位
            elif OrderRecord.GetOpenInterest()<0 :
                ## 結算平倉(期貨才使用, 股票除非是下市櫃)
                if KBar_df['product'][n+1] != KBar_df['product'][n] :
               
                    OrderRecord.Cover('Buy', KBar_df['product'][n],KBar_df['time'][n],KBar_df['close'][n],-OrderRecord.GetOpenInterest())
                    continue
                # 逐筆更新移動停損價位
                if KBar_df['close'][n] + MoveStopLoss < StopLossPoint :
                    StopLossPoint = KBar_df['close'][n] + MoveStopLoss
                # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
                elif KBar_df['close'][n] > StopLossPoint :
                    OrderRecord.Cover('Buy', KBar_df['product'][n+1],KBar_df['time'][n+1],KBar_df['open'][n+1],-OrderRecord.GetOpenInterest())
                    continue
    #### 繪製K線圖加上MA以及下單點位    
    ChartOrder_MA(KBar_df,OrderRecord.GetTradeRecord())
    
elif choice_strategy == choices_strategy[1]:
    st.subheader("RSI 策略參數")
    Floor = st.slider('超賣區(多單進場)', 0, 50, 20)
    Ceil = st.slider('超買區(空單進場)', 50, 100, 80)
    rsi_period = st.slider('RSI 計算週期', 2, 50, 14)
    
    OrderRecord = Record()
    KBar_df['RSI'] = Calculate_RSI(KBar_df, rsi_period)

    for i in range(1, len(KBar_df) - 1):
        rsi = KBar_df['RSI'][i]
        prev_rsi = KBar_df['RSI'][i-1]

        if np.isnan(prev_rsi): continue

        if OrderRecord.GetOpenInterest() == 0:
            if rsi < Floor:
                OrderRecord.Order('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)
            elif rsi > Ceil:
                OrderRecord.Order('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() > 0 and rsi > 50 and prev_rsi <= 50:
            OrderRecord.Cover('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() < 0 and rsi < 50 and prev_rsi >= 50:
            OrderRecord.Cover('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

    ChartOrder_Generic(KBar_df, OrderRecord.GetTradeRecord(), title="RSI 策略",
    indicators=[
        {"col": "RSI_long", "name": "長期RSI", "color": "red"},
        {"col": "RSI_short", "name": "短期RSI", "color": "blue"}
    ])
elif choice_strategy == choices_strategy[2]:
    st.subheader("布林通道策略參數")
    bb_period = st.slider('布林通道週期', 5, 50, 20)
    bb_std = st.slider('布林通道寬度(倍數)', 1, 5, 2)

    OrderRecord = Record()
    KBar_df = Calculate_Bollinger_Bands(KBar_df, bb_period, bb_std)

    for i in range(1, len(KBar_df) - 1):
        close = KBar_df['close'][i]
        up = KBar_df['Upper_Band'][i]
        down = KBar_df['Lower_Band'][i]
        mid = KBar_df['SMA'][i]

        if np.isnan(up) or np.isnan(down): continue

        if OrderRecord.GetOpenInterest() == 0:
            if close < down:
                OrderRecord.Order('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)
            elif close > up:
                OrderRecord.Order('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() > 0 and close > mid:
            OrderRecord.Cover('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() < 0 and close < mid:
            OrderRecord.Cover('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

    ChartOrder_Generic(KBar_df, OrderRecord.GetTradeRecord(), title="布林通道策略",
    indicators=[
        {"col": "Upper_Band", "name": "上軌", "color": "red"},
        {"col": "Lower_Band", "name": "下軌", "color": "blue"},
        {"col": "SMA", "name": "中軌", "color": "gray"}
    ])
elif choice_strategy == choices_strategy[3]:
    st.subheader("MACD 策略參數")
    fast = st.slider('快速線週期', 2, 20, 12)
    slow = st.slider('慢速線週期', 5, 50, 26)
    signal = st.slider('訊號線週期', 2, 20, 9)

    OrderRecord = Record()
    KBar_df = Calculate_MACD(KBar_df, fast, slow, signal)

    for i in range(1, len(KBar_df) - 1):
        dif = KBar_df['MACD'][i]
        dea = KBar_df['Signal_Line'][i]
        dif_prev = KBar_df['MACD'][i-1]
        dea_prev = KBar_df['Signal_Line'][i-1]

        if np.isnan(dif) or np.isnan(dea) or np.isnan(dif_prev) or np.isnan(dea_prev): continue

        if OrderRecord.GetOpenInterest() == 0:
            if dif_prev <= dea_prev and dif > dea:
                OrderRecord.Order('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)
            elif dif_prev >= dea_prev and dif < dea:
                OrderRecord.Order('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() > 0 and dif < dea and dif_prev >= dea_prev:
            OrderRecord.Cover('Sell', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

        elif OrderRecord.GetOpenInterest() < 0 and dif > dea and dif_prev <= dea_prev:
            OrderRecord.Cover('Buy', KBar_df['product'][i+1], KBar_df['time'][i+1], KBar_df['open'][i+1], 1)

    ChartOrder_Generic(KBar_df, OrderRecord.GetTradeRecord(), title="MACD 策略",
    indicators=[
        {"col": "MACD", "name": "DIF", "color": "green"},
        {"col": "Signal_Line", "name": "訊號線", "color": "orange"}
    ])
##### 繪製K線圖加上MA以及下單點位
# @st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
# def ChartOrder_MA(Kbar_df,TR):
#     # # 將K線轉為DataFrame
#     # Kbar_df=KbarToDf(KBar)
#     # 買(多)方下單點位紀錄
#     BTR = [ i for i in TR if i[0]=='Buy' or i[0]=='B' ]
#     BuyOrderPoint_date = [] 
#     BuyOrderPoint_price = []
#     BuyCoverPoint_date = []
#     BuyCoverPoint_price = []
#     for date,Low,High in zip(Kbar_df['time'],Kbar_df['low'],Kbar_df['high']):
#         # 買方進場
#         if date in [ i[2] for i in BTR ]:
#             BuyOrderPoint_date.append(date)
#             BuyOrderPoint_price.append(Low * 0.999)
#         else:
#             BuyOrderPoint_date.append(np.nan)
#             BuyOrderPoint_price.append(np.nan)
#         # 買方出場
#         if date in [ i[4] for i in BTR ]:
#             BuyCoverPoint_date.append(date)
#             BuyCoverPoint_price.append(High * 1.001)
#         else:
#             BuyCoverPoint_date.append(np.nan)
#             BuyCoverPoint_price.append(np.nan)
#     # # 將下單點位加入副圖物件
#     # if [ i for i in BuyOrderPoint if not np.isnan(i) ] !=[]:
#     #     addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=50,marker='^',color='red'))  ## 200
#     #     addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=50,marker='v',color='blue')) ## 200
#     # 賣(空)方下單點位紀錄
#     STR = [ i for i in TR if i[0]=='Sell' or i[0]=='S' ]
#     SellOrderPoint_date = []
#     SellOrderPoint_price = []
#     SellCoverPoint_date = []
#     SellCoverPoint_price = []
#     for date,Low,High in zip(Kbar_df['time'],Kbar_df['low'],Kbar_df['high']):
#         # 賣方進場
#         if date in [ i[2] for i in STR]:
#             SellOrderPoint_date.append(date)
#             SellOrderPoint_price.append(High * 1.001)
#         else:
#             SellOrderPoint_date.append(np.nan)
#             SellOrderPoint_price.append(np.nan)
#         # 賣方出場
#         if date in [ i[4] for i in STR ]:
#             SellCoverPoint_date.append(date)
#             SellCoverPoint_price.append(Low * 0.999)
#         else:
#             SellCoverPoint_date.append(np.nan)
#             SellCoverPoint_price.append(np.nan)
#     # # 將下單點位加入副圖物件
#     # if [ i for i in SellOrderPoint if not np.isnan(i) ] !=[]:
#     #     addp.append(mpf.make_addplot(SellOrderPoint,scatter=True,markersize=50,marker='v',color='green'))  ## 200
#     #     addp.append(mpf.make_addplot(SellCoverPoint,scatter=True,markersize=50,marker='^',color='pink'))   ## 200
#     # 開始繪圖
#     # ChartKBar(KBar,addp,volume_enable)
#     fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    
#     #### include candlestick with rangeselector
#     # fig5.add_trace(go.Candlestick(x=KBar_df['time'],
#     #                 open=KBar_df['open'], high=KBar_df['high'],
#     #                 low=KBar_df['low'], close=KBar_df['close'], name='K線'),
#     #                 secondary_y=False)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
#     #### include a go.Bar trace for volumes
#     # fig5.add_trace(go.Bar(x=KBar_df['time'], y=KBar_df['volume'], name='成交量', marker=dict(color='black')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
#     fig5.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA_trading+1:], y=KBar_df['MA_long'][last_nan_index_MA_trading+1:], mode='lines',line=dict(color='orange', width=2), name=f'{LongMAPeriod}-根 K棒 移動平均線'), 
#                   secondary_y=False)
#     fig5.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MA_trading+1:], y=KBar_df['MA_short'][last_nan_index_MA_trading+1:], mode='lines',line=dict(color='pink', width=2), name=f'{ShortMAPeriod}-根 K棒 移動平均線'), 
#                   secondary_y=False)
#     fig5.add_trace(go.Scatter(x=BuyOrderPoint_date, y=BuyOrderPoint_price, mode='markers',  marker=dict(color='red', symbol='triangle-up', size=10),  name='作多進場點'), secondary_y=False)
#     fig5.add_trace(go.Scatter(x=BuyCoverPoint_date, y=BuyCoverPoint_price, mode='markers',  marker=dict(color='blue', symbol='triangle-down', size=10),  name='作多出場點'), secondary_y=False)
#     fig5.add_trace(go.Scatter(x=SellOrderPoint_date, y=SellOrderPoint_price, mode='markers',  marker=dict(color='green', symbol='triangle-down', size=10),  name='作空進場點'), secondary_y=False)
#     fig5.add_trace(go.Scatter(x=SellCoverPoint_date, y=SellCoverPoint_price, mode='markers',  marker=dict(color='black', symbol='triangle-up', size=10),  name='作空出場點'), secondary_y=False)
 
#     fig5.layout.yaxis2.showgrid=True
#     st.plotly_chart(fig5, use_container_width=True)


# ChartOrder_MA(KBar_df,OrderRecord.GetTradeRecord())






###### 計算績效:
# OrderRecord.GetTradeRecord()          ## 交易紀錄清單
# OrderRecord.GetProfit()               ## 利潤清單


def 計算績效_股票():
    單位倍數 = 1000
    交易總盈虧 = OrderRecord.GetTotalProfit() * 單位倍數
    平均每次盈虧 = OrderRecord.GetAverageProfit() * 單位倍數
    平均投資報酬率 = OrderRecord.GetAverageProfitRate()
    平均獲利_只看獲利的 = OrderRecord.GetAverEarn() * 單位倍數
    平均虧損_只看虧損的 = OrderRecord.GetAverLoss() * 單位倍數
    勝率 = OrderRecord.GetWinRate()
    最大連續虧損 = OrderRecord.GetAccLoss() * 單位倍數
    最大盈虧回落_MDD = OrderRecord.GetMDD() * 單位倍數                 ## 最大利潤(盈虧)回落(MDD). 這個不是一般的 "資金" 或 "投資報酬率" 的回落
    if 最大盈虧回落_MDD>0:
        報酬風險比 = 交易總盈虧/最大盈虧回落_MDD
    else:
        報酬風險比='資料不足無法計算'
    return 交易總盈虧,平均每次盈虧,平均投資報酬率,平均獲利_只看獲利的,平均虧損_只看虧損的,勝率,最大連續虧損,最大盈虧回落_MDD,報酬風險比


def 計算績效_股票期貨():
    單位倍數 = 2000  # 股票期貨一口 = 2000 股
    交易總盈虧 = OrderRecord.GetTotalProfit() * 單位倍數
    平均每次盈虧 = OrderRecord.GetAverageProfit() * 單位倍數
    平均投資報酬率 = OrderRecord.GetAverageProfitRate()
    平均獲利_只看獲利的 = OrderRecord.GetAverEarn() * 單位倍數
    平均虧損_只看虧損的 = OrderRecord.GetAverLoss() * 單位倍數
    勝率 = OrderRecord.GetWinRate()
    最大連續虧損 = OrderRecord.GetAccLoss() * 單位倍數
    最大盈虧回落_MDD = OrderRecord.GetMDD() * 單位倍數                ## 最大利潤(盈虧)回落(MDD). 這個不是一般的 "資金" 或 "投資報酬率" 的回落
    if 最大盈虧回落_MDD>0:
        報酬風險比 = 交易總盈虧/最大盈虧回落_MDD
    else:
        報酬風險比='資料不足無法計算'
    return 交易總盈虧,平均每次盈虧,平均投資報酬率,平均獲利_只看獲利的,平均虧損_只看虧損的,勝率,最大連續虧損,最大盈虧回落_MDD,報酬風險比


if choice == '華碩: 2023.4.17 至 2025.4.16':
    交易總盈虧,平均每次盈虧,平均投資報酬率,平均獲利_只看獲利的,平均虧損_只看虧損的,勝率,最大連續虧損,最大盈虧回落_MDD,報酬風險比 = 計算績效_股票()
    # 交易總盈虧 = OrderRecord.GetTotalProfit()*1000          ## 取得交易總盈虧
    # 平均每次盈虧 = OrderRecord.GetAverageProfit()*1000         ## 取得交易 "平均" 盈虧(每次)
    # 平均投資報酬率 = OrderRecord.GetAverageProfitRate()    ## 取得交易 "平均" 投資報酬率(每次)  
    # 平均獲利_只看獲利的 = OrderRecord.GetAverEarn()*1000              ## 平均獲利(只看獲利的) 
    # 平均虧損_只看虧損的 = OrderRecord.GetAverLoss()*1000              ## 平均虧損(只看虧損的)
    # 勝率 = OrderRecord.GetWinRate()              ## 勝率
    # 最大連續虧損 = OrderRecord.GetAccLoss()*1000               ## 最大連續虧損
    # 最大盈虧回落_MDD = OrderRecord.GetMDD()*1000                   ## 最大利潤(盈虧)回落(MDD). 這個不是一般的 "資金" 或 "投資報酬率" 的回落
    # if 最大盈虧回落_MDD>0:
    #     報酬風險比 = 交易總盈虧/最大盈虧回落_MDD
    # else:
    #     報酬風險比='資料不足無法計算'

if choice == '聯電期貨: 2023.4.17 至 2025.4.16':
    交易總盈虧,平均每次盈虧,平均投資報酬率,平均獲利_只看獲利的,平均虧損_只看虧損的,勝率,最大連續虧損,最大盈虧回落_MDD,報酬風險比 = 計算績效_股票期貨()

    # 交易總盈虧 = OrderRecord.GetTotalProfit()*200          ## 取得交易總盈虧
    # 平均每次盈虧 = OrderRecord.GetAverageProfit() *200       ## 取得交易 "平均" 盈虧(每次)
    # 平均投資報酬率 = OrderRecord.GetAverageProfitRate()    ## 取得交易 "平均" 投資報酬率(每次)  
    # 平均獲利_只看獲利的 = OrderRecord.GetAverEarn() *200            ## 平均獲利(只看獲利的) 
    # 平均虧損_只看虧損的 = OrderRecord.GetAverLoss()*200             ## 平均虧損(只看虧損的)
    # 勝率 = OrderRecord.GetWinRate()              ## 勝率
    # 最大連續虧損 = OrderRecord.GetAccLoss()*200              ## 最大連續虧損
    # 最大盈虧回落_MDD = OrderRecord.GetMDD()*200                  ## 最大利潤(盈虧)回落(MDD). 這個不是一般的 "資金" 或 "投資報酬率" 的回落
    # if 最大盈虧回落_MDD>0:
    #     報酬風險比 = 交易總盈虧/最大盈虧回落_MDD
    # else:
    #     報酬風險比='資料不足無法計算'

if choice == '富邦金期貨: 2023.4.15 至 2025.4.16':
    交易總盈虧,平均每次盈虧,平均投資報酬率,平均獲利_只看獲利的,平均虧損_只看虧損的,勝率,最大連續虧損,最大盈虧回落_MDD,報酬風險比 = 計算績效_股票期貨()
    # 交易總盈虧 = OrderRecord.GetTotalProfit()*50          ## 取得交易總盈虧
    # 平均每次盈虧 = OrderRecord.GetAverageProfit() *50       ## 取得交易 "平均" 盈虧(每次)
    # 平均投資報酬率 = OrderRecord.GetAverageProfitRate()    ## 取得交易 "平均" 投資報酬率(每次)  
    # 平均獲利_只看獲利的 = OrderRecord.GetAverEarn() *50            ## 平均獲利(只看獲利的) 
    # 平均虧損_只看虧損的 = OrderRecord.GetAverLoss()*50             ## 平均虧損(只看虧損的)
    # 勝率 = OrderRecord.GetWinRate()              ## 勝率
    # 最大連續虧損 = OrderRecord.GetAccLoss()*50              ## 最大連續虧損
    # 最大盈虧回落_MDD = OrderRecord.GetMDD()*50                  ## 最大利潤(盈虧)回落(MDD). 這個不是一般的 "資金" 或 "投資報酬率" 的回落
    # if 最大盈虧回落_MDD>0:
    #     報酬風險比 = 交易總盈虧/最大盈虧回落_MDD
    # else:
    #     報酬風險比='資料不足無法計算'



##### 将投資績效存储成一个DataFrame並以表格形式呈現各項績效數據
if len(OrderRecord.Profit)>0:
    data = {
        "項目": ["交易總盈虧(元)", "平均每次盈虧(元)", "平均投資報酬率", "平均獲利(只看獲利的)(元)", "平均虧損(只看虧損的)(元)", "勝率", "最大連續虧損(元)", "最大盈虧回落(MDD)(元)", "報酬風險比(交易總盈虧/最大盈虧回落(MDD))"],
        "數值": [交易總盈虧, 平均每次盈虧, 平均投資報酬率, 平均獲利_只看獲利的, 平均虧損_只看虧損的, 勝率, 最大連續虧損, 最大盈虧回落_MDD, 報酬風險比]
    }
    df = pd.DataFrame(data)
    if len(df)>0:
        st.write(df)
else:
    st.write('沒有交易記錄(已經了結之交易) !')






###### 累計盈虧 & 累計投資報酬率
with st.expander("累計盈虧 & 累計投資報酬率"):
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    
    #### include a go.Bar trace for volumes
    # fig4.add_trace(go.Bar(x=KBar_df['time'], y=KBar_df['MACD_Histogram'], name='MACD Histogram', marker=dict(color='black')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
    fig4.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MACD+1:], y=KBar_df['Signal_Line'][last_nan_index_MACD+1:], mode='lines',line=dict(color='orange', width=2), name='訊號線(DEA)'), 
                  secondary_y=True)
    fig4.add_trace(go.Scatter(x=KBar_df['time'][last_nan_index_MACD+1:], y=KBar_df['MACD'][last_nan_index_MACD+1:], mode='lines',line=dict(color='pink', width=2), name='DIF'), 
                  secondary_y=True)
    
    fig4.layout.yaxis2.showgrid=True
    st.plotly_chart(fig4, use_container_width=True)



#### 定義圖表
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
ax1 = plt.subplot(2,1,1)
ax2 = plt.subplot(2,1,2)




##### 畫累計盈虧圖:
if choice == '華碩: 2023.4.17 至 2025.4.16':
    OrderRecord.GeneratorProfitChart(choice='stock',StrategyName='MA')
if choice == '聯電期貨: 2023.4.17 至 2025.4.16':
    OrderRecord.GeneratorProfitChart(choice='future1',StrategyName='MA')
if choice == '富邦金期貨: 2023.4.15 至 2025.4.16':
    OrderRecord.GeneratorProfitChart(choice='future2',StrategyName='MA')

    

# matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# plt.figure()

# #### 計算累計績效
# TotalProfit=[0]
# for i in OrderRecord.Profit:
#     TotalProfit.append(TotalProfit[-1]+i)

# #### 繪製圖形
# if choice == '台積電: 2022.1.1 至 2024.4.9':
#     # ax.plot( TotalProfit[1:]  , '-', marker='o', linewidth=1 )
#     plt.plot( TotalProfit[1:]*1000  , '-', marker='o', linewidth=1 )
# if choice == '大台指2024.12到期: 2024.1 至 2024.4.9':
#     # ax.plot( TotalProfit[1:]  , '-', marker='o', linewidth=1 )
#     plt.plot( TotalProfit[1:]*200  , '-', marker='o', linewidth=1 )


# ####定義標頭
# # # ax.set_title('Profit')
# # ax.set_title('累計盈虧')
# # ax.set_xlabel('交易編號')
# # ax.set_ylabel('累計盈虧(元/每股)')
# plt.title('累計盈虧(元)')
# plt.xlabel('交易編號')
# plt.ylabel('累計盈虧(元)')
# # if choice == '台積電: 2022.1.1 至 2024.4.9':
# #     plt.ylabel('累計盈虧(元/每股)')
# # if choice == '大台指2024.12到期: 2024.1 至 2024.4.9':
# #     plt.ylabel('累計盈虧(元/每口)')

# #### 设置x轴的刻度
# ### 获取TotalProfit的长度
# length = len(TotalProfit)
# ### 创建新的x轴刻度列表，每个值都加1
# new_ticks = range(1, length + 1)
# ### 应用新的x轴刻度
# plt.xticks(ticks=range(length), labels=new_ticks)

# #### 顯示繪製圖表
# # plt.show()    # 顯示繪製圖表
# # plt.savefig(StrategyName+'.png') #儲存繪製圖表
# ### 在Streamlit中显示
# st.pyplot(plt)






##### 畫累計投資報酬率圖:
OrderRecord.GeneratorProfit_rateChart(StrategyName='MA')
# matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# plt.figure()

# #### 計算累計計投資報酬
# TotalProfit_rate=[0]
# for i in OrderRecord.Profit_rate:
#     TotalProfit_rate.append(TotalProfit_rate[-1]+i)

# #### 繪製圖形
# plt.plot( TotalProfit_rate[1:]  , '-', marker='o', linewidth=1 )
# # if choice == '台積電: 2022.1.1 至 2024.4.9':
# #     # ax.plot( TotalProfit[1:]  , '-', marker='o', linewidth=1 )
# #     plt.plot( TotalProfit_rate[1:]  , '-', marker='o', linewidth=1 )
# # if choice == '大台指2024.12到期: 2024.1 至 2024.4.9':
# #     # ax.plot( TotalProfit[1:]  , '-', marker='o', linewidth=1 )
# #     plt.plot( TotalProfit_rate[1:]  , '-', marker='o', linewidth=1 )


# ####定義標頭
# plt.title('累計投資報酬率')
# plt.xlabel('交易編號')
# plt.ylabel('累計投資報酬率')
# # if choice == '台積電: 2022.1.1 至 2024.4.9':
# #     plt.ylabel('累計投資報酬率')
# # if choice == '大台指2024.12到期: 2024.1 至 2024.4.9':
# #     plt.ylabel('累計投資報酬率')

# #### 设置x轴的刻度
# ### 获取TotalProfit的长度
# length = len(TotalProfit_rate)
# ### 创建新的x轴刻度列表，每个值都加1
# new_ticks = range(1, length + 1)
# ### 应用新的x轴刻度
# plt.xticks(ticks=range(length), labels=new_ticks)

# #### 顯示繪製圖表
# # plt.show()    # 顯示繪製圖表
# # plt.savefig(StrategyName+'.png') #儲存繪製圖表
# ### 在Streamlit中显示
# st.pyplot(plt)


#%%
####### (7) 呈現即時資料 #######







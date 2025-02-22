# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:25:29 2024

@author: Nima
"""
 
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:25:29 2024

@author: Nima
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf

# تنظیمات گرافیکی matplotlib
import matplotlib as mpl
from matplotlib import cycler
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
colors = cycler('color',
                ['#669FEE', '#66EE91', '#9988DD',
                 '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('figure', facecolor='#313233')
plt.rc('axes', facecolor="#313233", edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors,
       labelcolor='gray')
plt.rc('grid', color='474A4A', linestyle='solid')
plt.rc('xtick', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('legend', facecolor="#313233", edgecolor="#313233")
plt.rc("text", color="#C9C9C9")
plt.rcParams['figure.figsize'] = [20, 8]

# مسیر فایل
# مسیر فایل
filename = r"C:\Users\Nima\OneDrive - Anglia Ruskin University\Documents\MEGA\AAAAA trade\backtester mkhushi\trading_strategies\time_close_csv_test.csv"

# چک کردن وجود فایل
if os.path.exists(filename) and os.stat(filename).st_size != 0:
    try:
        # خواندن فایل و پردازش محتوا
        with open(filename, encoding='utf-16') as f:
            contents = f.read()
            contents = contents.splitlines()
            contents = [x.split('\t') for x in contents]
        
        # تبدیل مقادیر به انواع داده مناسب
        for i in range(len(contents)):
            contents[i][0] = datetime.strptime(contents[i][0], '%Y.%m.%d %H:%M:%S')  # time
            contents[i][1] = float(contents[i][1])  # open
            contents[i][2] = float(contents[i][2])  # high
            contents[i][3] = float(contents[i][3])  # low
            contents[i][4] = float(contents[i][4])  # close
            contents[i][5] = int(contents[i][5])    # tick volume
            contents[i][6] = str(contents[i][6])    # position
        
        # تبدیل به DataFrame
        df = pd.DataFrame(contents, columns=["time", "open", "high", "low", "close", "tick_volume", "pos"])
        df["time"] = pd.to_datetime(df["time"])  # تبدیل ستون زمان به datetime

        # محاسبه ستون‌های اضافی
        df["Candle way"] = -1
        df.loc[(df["open"] - df["close"]) < 0, "Candle way"] = 1
        df["amplitude"] = np.abs(df["close"] - df["open"])
        
        # Bullish Engulfing
        df["Bullish Engulfing"] = np.nan
        df.loc[
            (df["Candle way"].shift(5) == -1) &
            (df["Candle way"].shift(4) == -1) &
            (df["Candle way"].shift(3) == -1) &
            (df["Candle way"].shift(2) == -1) &
            (df["Candle way"].shift(1) == -1) &
            (df["Candle way"] == 1),
            "Bullish Engulfing"
        ] = 1

        # انتخاب بازه تاریخی خاص
        df["Bullish Engulfing"].dropna()
        
        
        df["Bearish Engulfing"] = np.nan

        df.loc[
        # 5 consequtive increasing candlestick and Today decrease
        (df["Candle way"].shift(5) == 1) &\
        (df["Candle way"].shift(4) == 1) &\
        (df["Candle way"].shift(3) == 1) &\
        (df["Candle way"].shift(2) == 1) &\
        (df["Candle way"].shift(1) == 1) &\
        (df["Candle way"] == -1) &\
 
        # Close of the last increasing candlestick = Open of today decrease candlestick
        (df["close"].shift(1) < df["open"]*(1+0.5/100)) &\
        (df["close"].shift(1) > df["open"]*(1-0.5/100)) &\
 

        # Last increaing candlestick is less strong than the Today decreasing candlestick
        (df["amplitude"].shift(1) * 1.5< df["amplitude"]), "Bearish Engulfing"] = -1
        df["Bearish Engulfing"].dropna() 
        
        
        df.loc[(df["low"].shift(5) > df["low"].shift(4)) &
              (df["low"].shift(4) > df["low"].shift(3)) &
              (df["low"].shift(3) > df["low"].shift(2)) &
              (df["low"].shift(2) > df["low"].shift(1)) &
              (df["low"].shift(1) > df["low"].shift(0)), "support"] = df["low"]

        df.loc[(df["high"].shift(5) < df["high"].shift(4)) &
              (df["high"].shift(4) < df["high"].shift(3)) &
              (df["high"].shift(3) < df["high"].shift(2)) &
              (df["high"].shift(2) < df["high"].shift(1)) &
              (df["high"].shift(1) < df["high"].shift(0)), "resistance"] = df["high"]


        # Create Simple moving average 30 days
        df["SMA fast"] = df["close"].rolling(10).mean()
      
        # Create Simple moving average 60 days
        df["SMA slow"] = df["close"].rolling(60).mean()


        
        df["smooth resistance"] = df["resistance"].ffill()
        df["smooth support"] = df["support"].ffill()
        df["smooth Bullish Engulfing"]=df["Bullish Engulfing"].ffill()
        df["smooth Bearish Engulfing"]=df["Bearish Engulfing"].ffill()
        
      
      
        condition_1_buy = (df["close"].shift(1) < df["smooth resistance"].shift(1)) & \
                          (df["smooth resistance"]*(1+0.5/100) < df["close"])
        condition_2_buy = df["SMA fast"] > df["SMA slow"]
      
        condition_3_buy   =df["smooth Bullish Engulfing"]==1
      
        condition_1_sell = (df["close"].shift(1) > df["smooth support"].shift(1)) & \
                          (df["smooth support"]*(1+0.5/100) > df["close"])
        condition_2_sell = df["SMA fast"] < df["SMA slow"]
      
        condition_3_sell =        df["smooth Bearish Engulfing"]== -1

      
      

        df.loc[condition_2_buy & condition_3_buy  , "signal"] = 1
        df.loc[condition_1_sell & condition_2_sell & condition_3_sell, "signal"] = -1        
        """        
        
        df.loc[condition_1_buy & condition_2_buy   , "signal"] = 1
        df.loc[condition_1_sell & condition_2_sell , "signal"] = -1              
        """              
        duration=5
        spread=0.03
        # Compute the profits
        df["pct"] = df["close"].pct_change(1)
        
        df["return"] = np.array([df["pct"].shift(i) for i in range(duration)]).sum(axis=0) * (df["signal"].shift(duration))
        df.loc[df["return"]==-1, "return"] = df["return"]-spread
        df.loc[df["return"]==1, "return"] = df["return"]-spread

        df["return"].cumsum().plot(figsize=(15,8))
        
############################################        
        
        df = df.set_index("time")  # زمان را به عنوان اندیس قرار می‌دهیم
        
        # تعداد کندل‌های قبل و بعد برای رسم
        n_before = 3  # تعداد کندل‌های قبل
        n_after = 3   # تعداد کندل‌های بعد
        
        # شناسایی موقعیت کندل‌های Bullish Engulfing
        indices = df[df["Bullish Engulfing"] == 1].index
        
        # دیتافریم نهایی برای نگه‌داری کندل‌ها
        df_selected = pd.DataFrame()
        
        # حلقه برای انتخاب کندل‌های قبل و بعد
        for idx in indices:
            start_idx = max(0, df.index.get_loc(idx) - n_before)  # کندل شروع
            end_idx = min(len(df), df.index.get_loc(idx) + n_after + 1)  # کندل پایان
            df_selected = pd.concat([df_selected, df.iloc[start_idx:end_idx]])
        
        # حذف تکرارهای احتمالی
        df_selected = df_selected.drop_duplicates()
        
        # اضافه کردن مارکر برای Bullish Engulfing
        markers = [np.nan] * len(df_selected)
        for idx in indices:
            if idx in df_selected.index:
                markers[df_selected.index.get_loc(idx)] = df_selected.loc[idx, "close"]  # محل قرارگیری مارکر
        
        # تنظیمات برای نمودار
        ap = [mpf.make_addplot(markers, type='scatter', marker='o', color='red', markersize=100)]
        
        # رسم نمودار کندل استیک
        if not df_selected.empty:
            mpf.plot(df_selected, type='candle', style='charles',
                     title="Bullish Engulfing with Markers",
                     ylabel="Price",
                     volume=False, mav=(3, 6), addplot=ap)
        else:
            print("No candles to plot.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("File does not exist or is empty.")

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:23:39 2024

@author: Nima
"""
#این کد باید کپی بعد پیست بشه انتهای فایل price_action.py جهت تست توابع

import os
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf    


filename = r"C:\Users\Nima\OneDrive - Anglia Ruskin University\Documents\MEGA\AAAAA trade\backtester mkhushi\trading_strategies\time_close_csv_test.csv"

if os.path.exists(filename) and os.stat(filename).st_size != 0:
    try:
        with open(filename, encoding='utf-16') as f:
            contents = f.read()
            contents = contents.splitlines()
            contents = [x.split('\t') for x in contents]
        
        for i in range(len(contents)):
            contents[i][0] = datetime.strptime(contents[i][0], '%Y.%m.%d %H:%M:%S')  # time
            contents[i][1] = float(contents[i][1])  # open
            contents[i][2] = float(contents[i][2])  # high
            contents[i][3] = float(contents[i][3])  # low
            contents[i][4] = float(contents[i][4])  # close
            contents[i][5] = int(contents[i][5])    # tick volume
            contents[i][6] = str(contents[i][6])    # position
        
            df = pd.DataFrame(contents, columns=["time", "open", "high", "low", "close", "tick_volume", "pos"])
            df["time"] = pd.to_datetime(df["time"])  # تبدیل ستون زمان به datetime
    except Exception as e:
     print(f"An error occurred: {e}")
     
     
# Run price action
pa = Price_action(df)
result_df = pa.run_price_action()

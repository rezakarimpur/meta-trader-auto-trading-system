# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 12:05:36 2024

@author: Nima
"""        


import pandas as pd
import numpy as np

class Price_action:
    def __init__(self, file_path):
     
        #self.self.df = pd.read_csv(file_path)
        self.df = pd.DataFrame(file_path, columns=("time", "open", "high", "low", "close", "tick_volume","pos"))
        self.high = self.df['high']
        self.low = self.df['low']
        self.close = self.df['close']
    
        #print(self.df.head())  # اصلاح دسترسی به head
        
        
        
    def calculate_engulf(self):
        self.df["Candle way"] = -1
        self.df.loc[( self.df["open"] -  self.df["close"]) < 0, "Candle way"] = 1
        self.df["amplitude"] = np.abs( self.df["close"] -  self.df["open"])
        
        # Bullish Engulfing
        self. df["Bullish Engulfing"] = np.nan
        self.df.loc[
            ( self.df["Candle way"].shift(5) == -1) &
            ( self.df["Candle way"].shift(4) == -1) &
            ( self.df["Candle way"].shift(3) == -1) &
            ( self.df["Candle way"].shift(2) == -1) &
            ( self.df["Candle way"].shift(1) == -1) &
            ( self.df["Candle way"] == 1),
            "Bullish Engulfing"
        ] = 1

        # انتخاب بازه تاریخی خاص
        self.df["Bullish Engulfing"].dropna()
        
        
        self.df["Bearish Engulfing"] = np.nan

        self.df.loc[
        # 5 consequtive increasing candlestick and Today decrease
        ( self.df["Candle way"].shift(5) == 1) &\
        ( self.df["Candle way"].shift(4) == 1) &\
        ( self.df["Candle way"].shift(3) == 1) &\
        ( self.df["Candle way"].shift(2) == 1) &\
        ( self.df["Candle way"].shift(1) == 1) &\
        ( self.df["Candle way"] == -1) &\
 
        # Close of the last increasing candlestick = Open of today decrease candlestick
        ( self.df["close"].shift(1) <  self.df["open"]*(1+0.5/100)) &\
        ( self.df["close"].shift(1) >  self.df["open"]*(1-0.5/100)) &\
 

        # Last increaing candlestick is less strong than the Today decreasing candlestick
        ( self.df["amplitude"].shift(1) * 1.5<  self.df["amplitude"]), "Bearish Engulfing"] = -1
        self.df["Bearish Engulfing"].dropna() 
        #print("calculate_engulf is done..............................")
       # print(self.df.head())  # اصلاح دسترسی به head
        
    def calculate_support_resistance(self):
        
        self.df.loc[(self.df["low"].shift(5) > self.df["low"].shift(4)) &
              (self.df["low"].shift(4) > self.df["low"].shift(3)) &
              (self.df["low"].shift(3) > self.df["low"].shift(2)) &
              (self.df["low"].shift(2) > self.df["low"].shift(1)) &
              (self.df["low"].shift(1) > self.df["low"].shift(0)), "support"] = self.df["low"]

        self.df.loc[(self.df["high"].shift(5) < self.df["high"].shift(4)) &
              (self.df["high"].shift(4) < self.df["high"].shift(3)) &
              (self.df["high"].shift(3) < self.df["high"].shift(2)) &
              (self.df["high"].shift(2) < self.df["high"].shift(1)) &
              (self.df["high"].shift(1) < self.df["high"].shift(0)), "resistance"] = self.df["high"]
        
        self.df["smooth Bullish Engulfing"]=self.df["Bullish Engulfing"].ffill()
        self.df["smooth Bearish Engulfing"]=self.df["Bearish Engulfing"].ffill()
        #print("calculate_support_resistance is done..............................")

        
        
        
    def calculate_fast_slow_ema(self):
        # Create Simple moving average 30 days
        self.df["SMA fast"] = self.df["close"].rolling(10).mean()
      
        # Create Simple moving average 60 days
        self.df["SMA slow"] = self.df["close"].rolling(60).mean()
        self.df["smooth resistance"] = self.df["resistance"].ffill()
        self.df["smooth support"] = self.df["support"].ffill()
       # print("calculate_fast_slow_ema is done..............................")

    def determine_signal(self, dframe):

        # initialise signal to hold: 0
        signal = 0
    
        # شرایط خرید
        condition_1_buy = (dframe["close"].shift(1) < dframe["smooth resistance"].shift(1)) & \
                          (dframe["smooth resistance"] * (1 + 0.5 / 100) < dframe["close"])
        condition_2_buy = dframe["SMA fast"] > dframe["SMA slow"]
        condition_3_buy = dframe["Bullish Engulfing"] == 1
    
        # شرایط فروش
        condition_1_sell = (dframe["close"].shift(1) > dframe["smooth support"].shift(1)) & \
                           (dframe["smooth support"] * (1 + 0.5 / 100) > dframe["close"])
        condition_2_sell = dframe["SMA fast"] < dframe["SMA slow"]
        condition_3_sell = dframe["Bearish Engulfing"] == -1
    
        # condition_1_buy &    condition_1_sell &
        buy_condition = condition_1_buy & condition_2_buy & condition_3_buy
        sell_condition =  condition_1_sell & condition_2_sell & condition_3_sell
    
        # بررسی اینکه آیا حداقل یک سطر شرایط را برآورده می‌کند
        if buy_condition.any():
            signal = 1
        elif sell_condition.any():
            signal = -1
    
        # چاپ پیام و بازگشت نتیجه
       # print("determine_signal is done..............................")
        return signal, dframe['close'].iloc[-1]     

    def run_price_action(self):
        self.calculate_engulf()
        self.calculate_support_resistance()
        self.calculate_fast_slow_ema()
        signal = self.determine_signal(self.df)
        print("signal is ",signal)
        return signal, self.df
    






# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:50:15 2024

@author: Nima
"""





import pandas as pd
from datetime import datetime
import  ta
from joblib import dump, load  # یا می‌توانید pickle استفاده کنید
import os



class ML:
 

    def __init__(self, file_path):
        
        #self.self.df = pd.read_csv(file_path)
        self.df = pd.DataFrame(file_path, columns=("Datetime", "Open", "High", "Low", "Close", "Volume","pos"))
        self.df.set_index('Datetime', inplace=True)
        self.model = load(os.path.join(os.path.dirname(__file__), 'XGBClassifier.joblib'))

  #      self.model = load('XGBClassifier.joblib')   
        print("1-model is loaded") 
       # self.Datetime=self.df['Datetime']
    
        



    
    def calculate_features(self):
        # Try-except block for reading and processing the file
        
               # Apply feature calculations
            #dfwithFeatures = calculate_features(df)
            self.df['sma5'] = ta.trend.sma_indicator(self.df['Close'], window=5)
            self.df['sma10'] = ta.trend.sma_indicator(self.df['Close'], window=10)
            self.df['sma15'] = ta.trend.sma_indicator(self.df['Close'], window=15)
            self.df['sma20'] = ta.trend.sma_indicator(self.df['Close'], window=20)
            self.df['sma30'] = ta.trend.sma_indicator(self.df['Close'], window=30)
            self.df['sma50'] = ta.trend.sma_indicator(self.df['Close'], window=50)
            self.df['sma80'] = ta.trend.sma_indicator(self.df['Close'], window=80)
            self.df['sma100'] = ta.trend.sma_indicator(self.df['Close'], window=100)
            self.df['sma200'] = ta.trend.sma_indicator(self.df['Close'], window=200)
    
            # Adding Price to Simple Moving Averages Ratios
            self.df['sma5_ratio'] = self.df['Close'] / self.df['sma5']
            self.df['sma10_ratio'] = self.df['Close'] / self.df['sma10']
            self.df['sma20_ratio'] = self.df['Close'] / self.df['sma20']
            self.df['sma30_ratio'] = self.df['Close'] / self.df['sma30']
            self.df['sma50_ratio'] = self.df['Close'] / self.df['sma50']
            self.df['sma80_ratio'] = self.df['Close'] / self.df['sma80']
            self.df['sma100_ratio'] = self.df['Close'] / self.df['sma100']
            self.df['sma200_ratio'] = self.df['Close'] / self.df['sma200']
            #print(self.df)
            # Adding RSI, CCI, Bollinger Bands, and OBV
            self.df['rsi'] = ta.momentum.RSIIndicator(self.df['Close']).rsi()
            self.df['cci'] = ta.trend.cci(self.df['High'], self.df['Low'], self.df['Close'], window=20, constant=0.015)
            bb_indicator = ta.volatility.BollingerBands(self.df['Close'])
            self.df['bb_high'] = bb_indicator.bollinger_hband()
            self.df['bb_low'] = bb_indicator.bollinger_lband()
            self.df['obv'] = ta.volume.OnBalanceVolumeIndicator(close=self.df['Close'], volume=self.df['Volume']).on_balance_volume()
    
            # Adding Features Derived from Indicators
            self.df['rsi_overbought'] = (self.df['rsi'] >= 70).astype(int)
            self.df['rsi_oversold'] = (self.df['rsi'] <= 30).astype(int)
            self.df['above_bb_high'] = (self.df['Close'] >= self.df['bb_high']).astype(int)
            self.df['below_bb_low'] = (self.df['Close'] <= self.df['bb_low']).astype(int)
            self.df['obv_divergence_10_days'] = self.df['obv'].diff().rolling(10).sum() - self.df['Close'].diff().rolling(10).sum()
            self.df['obv_divergence_20_days'] = self.df['obv'].diff().rolling(20).sum() - self.df['Close'].diff().rolling(20).sum()
            self.df['cci_high'] = (self.df['cci'] >= 120).astype(int)
            self.df['cci_low'] = (self.df['cci'] <= -120).astype(int)
    
            # Adding SMA Comparisons
            self.df['sma5 > sma10'] = (self.df['sma5'] > self.df['sma10']).astype(int)
            self.df['sma10 > sma15'] = (self.df['sma10'] > self.df['sma15']).astype(int)
            self.df['sma15 > sma20'] = (self.df['sma15'] > self.df['sma20']).astype(int)
            self.df['sma20 > sma30'] = (self.df['sma20'] > self.df['sma30']).astype(int)
            self.df['sma30 > sma50'] = (self.df['sma30'] > self.df['sma50']).astype(int)
            self.df['sma50 > sma80'] = (self.df['sma50'] > self.df['sma80']).astype(int)
            self.df['sma80 > sma100'] = (self.df['sma80'] > self.df['sma100']).astype(int)
            self.df['sma100 > sma200'] = (self.df['sma100'] > self.df['sma200']).astype(int)
    
            # Adding Close_Shift and Returns
            self.df['Close_Shift'] = self.df['Close'].shift(1)
            self.df['Return'] = (self.df['Close'] / self.df['Close_Shift'] - 1) * 100
            # Removing NaN values
            self.df.bfill(inplace=True)  # Backward fill
            # لیست ستون‌های مورد انتظار مدل
            expected_columns =['Open', 'High', 'Low', 'Close', 'Volume', 'Close_Shift', 'Return',
           'sma5', 'sma10', 'sma15', 'sma20', 'sma30', 'sma50', 'sma80', 'sma100',
           'sma200', 'sma5_ratio', 'sma10_ratio', 'sma20_ratio', 'sma30_ratio',
           'sma50_ratio', 'sma80_ratio', 'sma100_ratio', 'sma200_ratio', 'rsi',
           'cci', 'bb_high', 'bb_low', 'obv', 'rsi_overbought', 'rsi_oversold',
           'above_bb_high', 'below_bb_low', 'obv_divergence_10_days',
           'obv_divergence_20_days', 'cci_high', 'cci_low', 'sma5 > sma10',
           'sma10 > sma15', 'sma15 > sma20', 'sma20 > sma30', 'sma30 > sma50',
           'sma50 > sma80', 'sma80 > sma100', 'sma100 > sma200']
    
            self.df = self.df[expected_columns]
    
    
            print("2-In feature calculation")
    
            return self.df

    
    def determine_signal(self, dframe):
      probabilities = self.model.predict_proba(dframe)[:, 1]  # اگر مدل از احتمال پشتیبانی می‌کند
      perdiction=probabilities[-1] 
      # Defining Buy signal (1)
      if ((perdiction > 0.493) & (perdiction <= 0.568)):
         signal = 1  # Buy signal

      elif  ((perdiction > 0.468) & (perdiction <= 0.493)) :
         signal = 1  # Buy signal
      else:
        signal = 0
  
      return signal, dframe['Close'].iloc[-1] 
      
      
        
    def run_ML(self):
        self.calculate_features()
        signal = self.determine_signal(self.df)
        """
        filtered_df = self.df[['Open', 'High', 'Low', 'Close', 'Volume']]
        """
        self.df.rename(columns={"Close": "close"}, inplace=True)

        print("signal and close price is ",signal)
        return signal, self.df
 

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:50:15 2024

@author: Nima
"""





import pandas as pd
from datetime import datetime
import  ta
from joblib import dump, load  # یا می‌توانید pickle استفاده کنید









contents=[]
def calculate_features(file_path):
    # Try-except block for reading and processing the file
    df=[]
    try:
        with open(file_path, encoding='utf-16') as f:
            contents = f.read()

        # Split lines and columns
        contents = contents.splitlines()
        contents = [x.split('\t') for x in contents]
        print(contents)
        # Process each row
        for i in range(len(contents)):
            contents[i][0] = datetime.strptime(contents[i][0], '%Y.%m.%d %H:%M:%S')  # datetime
            contents[i][1] = float(contents[i][1])  # open
            contents[i][2] = float(contents[i][2])  # high
            contents[i][3] = float(contents[i][3])  # low
            contents[i][4] = float(contents[i][4])  # close
            contents[i][5] = int(contents[i][5])    # tick_value
            contents[i][6] = str(contents[i][6])    # positions
        # Extract last row data

        # Convert to DataFrame
        df = pd.DataFrame(contents, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'position'])
        df.set_index('Datetime', inplace=True)

        # Drop the position column
        df.drop(columns=['position'], inplace=True)


        # Apply feature calculations
        #dfwithFeatures = calculate_features(df)
        df['sma5'] = ta.trend.sma_indicator(df['Close'], window=5)
        df['sma10'] = ta.trend.sma_indicator(df['Close'], window=10)
        df['sma15'] = ta.trend.sma_indicator(df['Close'], window=15)
        df['sma20'] = ta.trend.sma_indicator(df['Close'], window=20)
        df['sma30'] = ta.trend.sma_indicator(df['Close'], window=30)
        df['sma50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['sma80'] = ta.trend.sma_indicator(df['Close'], window=80)
        df['sma100'] = ta.trend.sma_indicator(df['Close'], window=100)
        df['sma200'] = ta.trend.sma_indicator(df['Close'], window=200)

        # Adding Price to Simple Moving Averages Ratios
        df['sma5_ratio'] = df['Close'] / df['sma5']
        df['sma10_ratio'] = df['Close'] / df['sma10']
        df['sma20_ratio'] = df['Close'] / df['sma20']
        df['sma30_ratio'] = df['Close'] / df['sma30']
        df['sma50_ratio'] = df['Close'] / df['sma50']
        df['sma80_ratio'] = df['Close'] / df['sma80']
        df['sma100_ratio'] = df['Close'] / df['sma100']
        df['sma200_ratio'] = df['Close'] / df['sma200']
        #print(df)
        # Adding RSI, CCI, Bollinger Bands, and OBV
        df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['cci'] = ta.trend.cci(df['High'], df['Low'], df['Close'], window=20, constant=0.015)
        bb_indicator = ta.volatility.BollingerBands(df['Close'])
        df['bb_high'] = bb_indicator.bollinger_hband()
        df['bb_low'] = bb_indicator.bollinger_lband()
        df['obv'] = ta.volume.OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()

        # Adding Features Derived from Indicators
        df['rsi_overbought'] = (df['rsi'] >= 70).astype(int)
        df['rsi_oversold'] = (df['rsi'] <= 30).astype(int)
        df['above_bb_high'] = (df['Close'] >= df['bb_high']).astype(int)
        df['below_bb_low'] = (df['Close'] <= df['bb_low']).astype(int)
        df['obv_divergence_10_days'] = df['obv'].diff().rolling(10).sum() - df['Close'].diff().rolling(10).sum()
        df['obv_divergence_20_days'] = df['obv'].diff().rolling(20).sum() - df['Close'].diff().rolling(20).sum()
        df['cci_high'] = (df['cci'] >= 120).astype(int)
        df['cci_low'] = (df['cci'] <= -120).astype(int)

        # Adding SMA Comparisons
        df['sma5 > sma10'] = (df['sma5'] > df['sma10']).astype(int)
        df['sma10 > sma15'] = (df['sma10'] > df['sma15']).astype(int)
        df['sma15 > sma20'] = (df['sma15'] > df['sma20']).astype(int)
        df['sma20 > sma30'] = (df['sma20'] > df['sma30']).astype(int)
        df['sma30 > sma50'] = (df['sma30'] > df['sma50']).astype(int)
        df['sma50 > sma80'] = (df['sma50'] > df['sma80']).astype(int)
        df['sma80 > sma100'] = (df['sma80'] > df['sma100']).astype(int)
        df['sma100 > sma200'] = (df['sma100'] > df['sma200']).astype(int)

        # Adding Close_Shift and Returns
        df['Close_Shift'] = df['Close'].shift(1)
        df['Return'] = (df['Close'] / df['Close_Shift'] - 1) * 100
        # Removing NaN values
        df.fillna(method='bfill', inplace=True)  # پر کردن به روش backward fill
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

        df = df[expected_columns]



        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




# فایل ورودی
file_path = 'time_close_csv_test.csv'

# فراخوانی تابع و محاسبه ویژگی‌ها
processed_data = calculate_features(file_path)

processed_data


model = load('XGBClassifier.joblib')

probabilities = model.predict_proba(processed_data)[:, 1]  # اگر مدل از احتمال پشتیبانی می‌کند
perdiction=probabilities[-1]


# Defining Buy signal (1)
if ((perdiction > 0.493) & (perdiction <= 0.568)):
   signal = 1  # Buy signal

elif  ((perdiction > 0.468) & (perdiction <= 0.493)) :
   signal = 1  # Buy signal
else:
  signal = 0

print(signal)


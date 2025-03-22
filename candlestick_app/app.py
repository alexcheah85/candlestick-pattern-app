import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# Function to detect basic candlestick patterns
def detect_candlestick_patterns(df):
    df['Body'] = abs(df['Close'] - df['Open'])
    df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
    df['Lower_Shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
    df['Pattern'] = 'None'

    # Doji
    df.loc[(df['Body'] <= 0.1 * (df['High'] - df['Low'])) & 
           (df['Upper_Shadow'] > 0) & (df['Lower_Shadow'] > 0), 'Pattern'] = 'Doji'
    
    # Hammer
    df.loc[(df['Body'] <= 0.3 * (df['High'] - df['Low'])) & 
           (df['Lower_Shadow'] > 2 * df['Body']) & 
           (df['Upper_Shadow'] < df['Body']), 'Pattern'] = 'Hammer'
    
    # Shooting Star
    df.loc[(df['Body'] <= 0.3 * (df['High'] - df['Low'])) & 
           (df['Upper_Shadow'] > 2 * df['Body']) & 
           (df['Lower_Shadow'] < df['Body']), 'Pattern'] = 'Shooting_Star'
    
    # Bullish Engulfing
    df.loc[(df['Close'] > df['Open']) & 
           (df['Close'].shift(1) < df['Open'].shift(1)) & 
           (df['Close'] > df['Open'].shift(1)) & 
           (df['Open'] < df['Close'].shift(1)), 'Pattern'] = 'Bullish_Engulfing'
    
    # Bearish Engulfing
    df.loc[(df['Close'] < df['Open']) & 
           (df['Close'].shift(1) > df['Open'].shift(1)) & 
           (df['Close'] < df['Open'].shift(1)) & 
           (df['Open'] > df['Close'].shift(1)), 'Pattern'] = 'Bearish_Engulfing'
    
    return df

# Prediction function
def predict_movement(df, trend="neutral"):
    df['Prediction'] = 'Hold'
    
    if trend in ["uptrend", "downtrend", "neutral"]:
        df.loc[df['Pattern'].isin(['Bullish_Engulfing', 'Hammer']), 'Prediction'] = 'Up'
        df.loc[df['Pattern'].isin(['Bearish_Engulfing', 'Shooting_Star']), 'Prediction'] = 'Down'
    
...     return df
... 
... # Streamlit App
... st.title("Real-Time Candlestick Pattern Detector & Predictor")
... 
... # User Inputs
... stock_symbol = st.text_input("Enter Stock Symbol", "AAPL")
... period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y"])
... interval = st.selectbox("Select Interval", ["1d", "1h", "15m"])
... trend = st.selectbox("Select Market Trend", ["neutral", "uptrend", "downtrend"])
... 
... if st.button("Analyze"):
...     # Fetch data from yfinance
...     data = yf.download(tickers=stock_symbol, period=period, interval=interval)
...     
...     if data.empty:
...         st.error("No data found. Please try another stock symbol or change the settings.")
...     else:
...         # Prepare DataFrame
...         df = data[['Open', 'High', 'Low', 'Close']]
...         
...         # Detect Patterns
...         df = detect_candlestick_patterns(df)
...         
...         # Make Predictions
...         df = predict_movement(df, trend)
...         
...         # Display DataFrame
...         st.write("Pattern Detection & Prediction:")
...         st.dataframe(df[['Open', 'High', 'Low', 'Close', 'Pattern', 'Prediction']].tail(10))
...         
...         # Plot Candlestick Chart
...         st.subheader(f"Candlestick Chart for {stock_symbol}")
...         fig, ax = plt.subplots(figsize=(10, 5))
...         mpf.plot(df, type='candle', ax=ax, style='charles', title=f"{stock_symbol} Candlestick Chart")
...         st.pyplot(fig)

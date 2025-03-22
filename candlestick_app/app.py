import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go

# Function to detect basic candlestick patterns
def detect_candlestick_patterns(df):
    """
    Detects candlestick patterns in a DataFrame with OHLC data.
    Columns: 'Open', 'High', 'Low', 'Close'
    Returns a DataFrame with pattern labels.
    """
    df['Body'] = abs(df['Close'] - df['Open'])
    df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
    df['Lower_Shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
    df['Pattern'] = 'None'
    
    # Doji: Small body relative to range
    df.loc[(df['Body'] <= 0.1 * (df['High'] - df['Low'])) & 
           (df['Upper_Shadow'] > 0) & (df['Lower_Shadow'] > 0), 'Pattern'] = 'Doji'
    
    # Hammer: Small body, long lower shadow, in downtrend
    df.loc[(df['Body'] <= 0.3 * (df['High'] - df['Low'])) & 
           (df['Lower_Shadow'] > 2 * df['Body']) & 
           (df['Upper_Shadow'] < df['Body']), 'Pattern'] = 'Hammer'
    
    # Bullish Engulfing: Current candle engulfs previous bearish candle
    df.loc[(df['Close'] > df['Open']) & 
           (df['Close'].shift(1) < df['Open'].shift(1)) & 
           (df['Close'] > df['Open'].shift(1)) & 
           (df['Open'] < df['Close'].shift(1)), 'Pattern'] = 'Bullish_Engulfing'
    
    # Bearish Engulfing: Current candle engulfs previous bullish candle
    df.loc[(df['Close'] < df['Open']) & 
           (df['Close'].shift(1) > df['Open'].shift(1)) & 
           (df['Close'] < df['Open'].shift(1)) & 
           (df['Open'] > df['Close'].shift(1)), 'Pattern'] = 'Bearish_Engulfing'
    
    return df

# Prediction function based on pattern and trend
def predict_movement(df, trend="neutral"):
    """
    Predicts stock movement based on candlestick patterns and trend.
    Trend: 'uptrend', 'downtrend', or 'neutral'
    Returns 'Up', 'Down', or 'Hold'.
    """
    df['Prediction'] = 'Hold'
    
    if trend == "uptrend":
        df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
    
    elif trend == "downtrend":
        df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
    
    else:
        df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
        df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
    
    return

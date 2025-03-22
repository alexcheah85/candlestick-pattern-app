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
    df.loc[(df['Body'] <= 0.1

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
    
    return df

# Plot candlestick chart
def plot_candlestick_chart(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlesticks'
    )])
    
    # Adding detected patterns
    patterns = df[df['Pattern'] != 'None']
    for i, row in patterns.iterrows():
        fig.add_annotation(
            x=i,
            y=row['Close'],
            text=row['Pattern'],
            showarrow=True,
            arrowhead=1,
            yshift=10,
            font=dict(color="red", size=10)
        )
    
    fig.update_layout(
        title='Candlestick Chart with Pattern Detection',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark'
    )
    
    st.plotly_chart(fig)

# Streamlit UI
st.title("Candlestick Pattern Detection & Prediction")
st.write("Upload your CSV file with 'Date', 'Open', 'High', 'Low', 'Close' columns.")

uploaded_file = st.file_uploader("Choose a file", type="csv")
trend = st.selectbox("Select the trend", ["neutral", "uptrend", "downtrend"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['Date'], index_col='Date')
    
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        st.write("Original Data:")
        st.dataframe(df)
        
        # Detect patterns
        df = detect_candlestick_patterns(df)
        
        # Predict movement
        df = predict_movement(df, trend)
        
        # Plot chart
        plot_candlestick_chart(df)
        
        # Show processed data
        st.write("Processed Data with Patterns & Predictions:")
        st.dataframe(df)
        
        # Download CSV button
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download Processed Data",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )
        
    else:
        st.error("The uploaded file does not contain the required columns: 'Open', 'High', 'Low', 'Close'.")

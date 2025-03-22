import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

st.set_page_config(page_title="Candlestick Pattern Detector", layout="wide")

# Title and Description
st.title("📈 Candlestick Pattern Detector")
st.markdown("Identify candlestick patterns and predict stock movements using historical data.")

# Sidebar Inputs
st.sidebar.header("Stock Data Settings")
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL):", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2025-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-03-21"))
trend = st.sidebar.selectbox("Select Market Trend", ["uptrend", "downtrend", "neutral"])
st.sidebar.markdown("---")

# Fetch Stock Data
st.subheader(f"Fetching data for {symbol} from {start_date} to {end_date}")
try:
    df = yf.download(symbol, start=start_date, end=end_date)
    
    if df.empty:
        st.error("No data fetched. Please check the stock symbol or date range.")
    else:
        st.success("Data successfully fetched!")
        st.write(df.tail())

        # Plotting the stock price
        st.subheader("Price Chart")
        fig, ax = plt.subplots(figsize=(10, 5))
        mpf.plot(df, type='candle', style='charles', ax=ax)
        st.pyplot(fig)
        
        # Function to detect candlestick patterns
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

        # Apply pattern detection
        df = detect_candlestick_patterns(df)

        # Function to predict stock movement
        def predict_movement(df, trend="neutral"):
            df['Prediction'] = 'Hold'
            
            if trend == "uptrend":
                df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Doji', 'Prediction'] = 'Hold'
                df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
            
            elif trend == "downtrend":
                df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Doji', 'Prediction'] = 'Hold'
                df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
            
            else:
                df.loc[df['Pattern'] == 'Bullish_Engulfing', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Hammer', 'Prediction'] = 'Up'
                df.loc[df['Pattern'] == 'Bearish_Engulfing', 'Prediction'] = 'Down'
                df.loc[df['Pattern'] == 'Doji', 'Prediction'] = 'Hold'
            
            return df

        # Apply prediction function
        df = predict_movement(df, trend)

        # Display Detected Patterns
        st.subheader("Detected Patterns & Predictions")
        st.write(df[['Open', 'High', 'Low', 'Close', 'Pattern', 'Prediction']].tail(10))

except Exception as e:
    st.error(f"An error occurred: {e}")

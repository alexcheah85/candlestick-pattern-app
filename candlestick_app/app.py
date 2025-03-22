import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from io import BytesIO

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
        
        # Save the candlestick chart to a buffer
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        
        # Download button for candlestick chart
        st.download_button(
            label="Download Candlestick Chart",
            data=buffer,
            file_name=f"{symbol}_candlestick_chart.png",
            mime="image/png"
        )

        # Function to detect candlestick patterns
        def detect_candlestick_patterns(df):
            df['Body'] = abs(df['Close'] - df['Open'])
            df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
            df['Lower_Shadow']_

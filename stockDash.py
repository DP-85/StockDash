# STOCKDASH VERSION: 0

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD

# INITIAL PAGE CONFIGURATION - THIS SHOULD BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="📈 Stock Dashboard", layout="centered")

def format_number(n):
    """FORMATS A NUMBER INTO CRORE, LAKH, OR THOUSANDS WITH COMMAS."""
    if isinstance(n, (int, float)):
        if n >= 1e7:
            return f"{n/1e7:.2f} Cr"
        elif n >= 1e5:
            return f"{n/1e5:.2f} Lakh"
        else:
            return f"{n:,.0f}"
    return "N/A"

def bordered_chart(title: str, fig: go.Figure):
    """DISPLAYS A PLOTLY FIGURE WITH A TITLE AND A BORDER AROUND IT."""
    st.markdown(f"### {title}")
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>StockDash</h1>", unsafe_allow_html=True)
st.title("📈 Live Stock Price Tracker")

# GET USER INPUT FOR STOCK TICKER
ticker = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS, TCS.NS, INFY.NS)", "RELIANCE.NS")

try:
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    # FETCH AND DISPLAY STOCK DATA
    current_price = stock_info.get("currentPrice")
    previous_close = stock_info.get("previousClose")
    day_high = stock_info.get("dayHigh", "N/A")
    day_low = stock_info.get("dayLow", "N/A")
    volume = stock_info.get("volume", "N/A")
    market_cap = stock_info.get("marketCap", "N/A")

    # DISPLAY STOCK NAME AND METRICS
    st.subheader(f" {stock_info.get('longName', 'Unknown')} ({ticker})")

    # ERROR HANDLING: ENSURE PRICES ARE AVAILABLE BEFORE CALCULATING CHANGE
    if current_price and previous_close:
        price_change = round(current_price - previous_close, 2)
        percent_change = round((price_change / previous_close) * 100, 2)
        st.metric(label="💰 Current Price", value=f"₹{current_price}", delta=f"{price_change} ({percent_change}%)")
    elif current_price:
        st.metric(label="💰 Current Price", value=f"₹{current_price}", delta="N/A")
    else:
        st.metric(label="💰 Current Price", value="Price not available", delta="N/A")


    st.markdown("### 📊 Additional Stats")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"🔼 **Day's High:** ₹{day_high}")
        st.write(f"🔽 **Day's Low:** ₹{day_low}")

    with col2:
        st.write(f"📊 **Volume:** {format_number(volume)}")
        st.write(f"💼 **Market Cap:** {format_number(market_cap)}")

    st.markdown('### Historical Price Chart')

    # LET USER SELECT THE TIME PERIOD
    period = st.selectbox(
        "Select Time Period",
        options=["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"],
        index=3  # DEFAULT IS "6mo"
    )

    # FETCH HISTORICAL DATA BASED ON THE SELECTED PERIOD
    hist_data = stock.history(period=period)

    if not hist_data.empty:

        with st.container(border=True):
            # PLOT THE HISTORICAL DATA AND SMA
            # ADD A 20-DAY SIMPLE MOVING AVERAGE (SMA)
            hist_data["SMA_20"] = hist_data["Close"].rolling(window=20).mean()

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data["Close"],
                mode="lines",
                name="Closing Price",
                line=dict(color="royalblue")
            ))

            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data["SMA_20"],
                mode="lines",
                name="20-Day SMA",
                line=dict(color="orange", dash="dash")
            ))

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (INR)",
                showlegend=True,
                template="plotly_white",
                height=400
            )
            # CORRECTED THE CHART TITLE FROM "PIE CHART" TO "PRICE CHART"
            #bordered_chart("", fig)

        # CALCULATE AND PLOT RSI (RELATIVE STRENGTH INDEX)
        rsi = RSIIndicator(close=hist_data["Close"], window=14)
        hist_data["RSI"] = rsi.rsi()

        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data["RSI"],
            mode="lines",
            name="RSI",
            line=dict(color="purple")
        ))

        # ADD OVERBOUGHT AND OVERSOLD LINES
        rsi_fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="top right")
        rsi_fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom right")

        rsi_fig.update_layout(
            yaxis_title="RSI Value",
            xaxis_title="Date",
            template="plotly_white",
            height=300,
            showlegend=False
        )
        bordered_chart("💡 RSI (Relative Strength Index)", rsi_fig)

        # CALCULATE AND PLOT MACD (MOVING AVERAGE CONVERGENCE DIVERGENCE)
        macd = MACD(close=hist_data["Close"])
        hist_data["MACD"] = macd.macd()
        hist_data["MACD_Signal"] = macd.macd_signal()
        hist_data["MACD_Hist"] = macd.macd_diff()

        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data["MACD"],
            mode="lines",
            name="MACD Line",
            line=dict(color="yellow")
        ))
        macd_fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data["MACD_Signal"],
            mode="lines",
            name="Signal Line",
            line=dict(color="orange")
        ))
        # ADD THE MACD HISTOGRAM AS BARS
        macd_fig.add_trace(go.Bar(
            x=hist_data.index,
            y=hist_data["MACD_Hist"],
            name="MACD Histogram",
            marker_color="gray",
            opacity=0.4
        ))
        macd_fig.update_layout(
            yaxis_title="MACD Value",
            xaxis_title="Date",
            showlegend=True,
            template="plotly_white",
            height=300
        )
        bordered_chart("📈 MACD (Moving Average Convergence Divergence)", macd_fig)
    else:
        st.warning("No historical data available for this ticker and time period.")

# EXCEPTION HANDLING FOR INVALID TICKERS OR DATA FETCHING ERRORS
except Exception as e:
    st.error(f"Couldn't fetch data for '{ticker}'. Please check the ticker symbol and your network connection.")
    # st.error(e) # UNCOMMENT THIS LINE FOR DETAILED DEBUGGING
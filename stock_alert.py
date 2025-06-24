import yfinance as yf
from twilio.rest import Client
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_FROM_NUMBER")
your_number = os.getenv("MY_PHONE_NUMBER")

client = Client(account_sid, auth_token)

stocks = {
    'SOXL': {'rsi_buy': 30, 'rsi_sell': 70},
    'NVDA': {'rsi_buy': 35, 'rsi_sell': 75},
}

def get_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def send_sms(message):
    client.messages.create(
        body=f"[Stock Alert] {message}",
        from_=twilio_number,
        to=your_number
    )

def main():
    for ticker, levels in stocks.items():
        stock = yf.download(ticker, period='1mo', interval='1d', auto_adjust=True)
        
        # If no data, skip
        if stock.empty or 'Close' not in stock.columns:
            print(f"{ticker}: No stock data available.")
            continue

        rsi_series = get_rsi(stock)

        # Drop NaNs
        rsi_series = rsi_series.dropna()

        if rsi_series.empty:
            print(f"{ticker}: Not enough data to calculate RSI.")
            continue

        current_rsi = round(rsi_series.iloc[-1], 2)
        current_price = round(stock['Close'].iloc[-1], 2)

        print(f"{ticker} | Price: ${current_price} | RSI: {current_rsi}")

        if current_rsi < levels['rsi_buy']:
            send_sms(f"{ticker} RSI is {current_rsi}. Consider BUYING. Price: ${current_price}")
        elif current_rsi > levels['rsi_sell']:
            send_sms(f"{ticker} RSI is {current_rsi}. Consider SELLING. Price: ${current_price}")
        else:
            print(f"{ticker}: RSI {current_rsi} = neutral")

if __name__ == "__main__":
    main()

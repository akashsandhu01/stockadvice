from twilio.rest import Client
from dotenv import load_dotenv
import os
import random

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_FROM_NUMBER")
your_number = os.getenv("MY_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# Top trending tickers (change or rotate as needed)
weekly_watchlist = ['PLTR', 'TSLA', 'RIOT', 'AMD', 'QQQ', 'SOXL', 'NVDA', 'SPY', 'META', 'AVGO']

def send_watchlist():
    picks = random.sample(weekly_watchlist, 3)
    message = f"📈 Weekly Watchlist: {', '.join(picks)}\nKeep an eye on these for entry points."
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=your_number
    )

if __name__ == "__main__":
    send_watchlist()

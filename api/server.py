from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS"
]

@app.route("/stocks")
def get_stocks():

    try:
        data = yf.download(
            tickers=" ".join(stocks),
            period="1d",
            interval="1m",
            group_by="ticker",
            progress=False
        )

        result = []

        for symbol in stocks:
            price = data[symbol]["Close"].dropna().iloc[-1]

            result.append({
                "name": symbol,
                "price": round(float(price), 2)
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

# IMPORTANT FOR VERCEL
app = app

from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route("/api/stocks")
def stocks():
    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    data = {}

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        price = ticker.info.get("currentPrice")
        data[symbol] = price

    return jsonify(data)

# IMPORTANT for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

portfolio = []

@app.route("/api/stocks")
def stocks():

    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    result = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)

            price = ticker.fast_info.get("last_price")

            if price is None:
                price = ticker.info.get("currentPrice")

            result.append({
                "name": symbol,
                "price": price
            })

        except:
            result.append({
                "name": symbol,
                "price": None
            })

    return jsonify(result)


@app.route("/api/portfolio")
def get_portfolio():
    return jsonify(portfolio)


@app.route("/api/buy", methods=["POST"])
def buy():
    portfolio.append(request.json)
    return jsonify({"status": "bought"})


@app.route("/api/sell", methods=["POST"])
def sell():
    name = request.json["name"]

    global portfolio
    portfolio = [p for p in portfolio if p["name"] != name]

    return jsonify({"status": "sold"})


# REQUIRED FOR VERCEL
app = app

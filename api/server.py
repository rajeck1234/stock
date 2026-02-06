from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__, static_folder="../public", static_url_path="")

@app.route("/")
def serve_home():
    return app.send_static_file("index.html")

# app = Flask(__name__)

portfolio = []

# @app.route("/")
# def home():
#     return "Live Trading Server Running 🚀"

@app.route("/api/stocks")
def stocks():

    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    result = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)

            price = ticker.fast_info.get("last_price")

            # fallback if fast_info fails
            if price is None:
                price = ticker.info.get("currentPrice")

            result.append({
                "name": symbol,
                "price": price
            })

        except Exception as e:
            result.append({
                "name": symbol,
                "price": None
            })

    return jsonify(result)

# @app.route("/api/stocks")
# def stocks():

#     symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

#     result = []

#     for symbol in symbols:
#         try:
#             ticker = yf.Ticker(symbol)
#             price = ticker.fast_info.get("last_price")

#             result.append({
#                 "name": symbol,
#                 "price": price
#             })

#         except:
#             result.append({
#                 "name": symbol,
#                 "price": None
#             })

#     return jsonify(result)


# @app.route("/api/portfolio")
# def get_portfolio():
#     return jsonify(portfolio)


@app.route("/api/buy", methods=["POST"])
def buy():
    data = request.json
    portfolio.append(data)
    return jsonify({"status": "bought"})


@app.route("/api/sell", methods=["POST"])
def sell():
    name = request.json["name"]

    global portfolio
    portfolio = [p for p in portfolio if p["name"] != name]

    return jsonify({"status": "sold"})


def handler(request):
    return app(request.environ, lambda *args: None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

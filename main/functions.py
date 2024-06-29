import yfinance as yf

def get_latest_stock_price(symbol):
    # Create a Ticker object for the stock
    ticker = yf.Ticker(symbol)

    # Get the latest price
    latest_price = ticker.history(period='1d')['Close'].iloc[-1]

    return latest_price
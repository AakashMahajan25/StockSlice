from django.shortcuts import render
import yfinance as yf
import plotly.graph_objects as go
from .functions import get_latest_stock_price

from django.contrib.auth import logout
from django.shortcuts import redirect

# from .dash_app import dash_app

# def index(request):
#     symbol = '^NSEI'

#     # You can pass other context data if needed
#     context = {
#         'chart_html': dash_app,
#         'latest_price': get_latest_stock_price(symbol),
#         # Add other context data as needed
#     }

#     return render(request, 'index.html', context)




def index(request):
    # Replace 'RELIANCE.NS' with the stock symbol of your choice
    symbol = '^NSEI'

    # Specify the date range for historical data
    start_date = '2022-01-01'
    end_date = '2023-10-23'

    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date)

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                      open=data['Open'],
                      high=data['High'],
                      low=data['Low'],
                      close=data['Close'])])

    # Customize the layout
    fig.update_layout(
        title=f'{symbol} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Stock Price',
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),  # Set text color to white
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)'),  # Set x-axis grid color to faded white
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)')   # Set y-axis grid color to faded white
    )

    # Convert the figure to HTML
    chart_html = fig.to_html(full_html=False)

    latest_price = get_latest_stock_price(symbol)

    return render(request, 'index.html', {'chart_html': chart_html,'latest_price':latest_price})

def custom_logout(request):
    logout(request)
    return redirect('home')
# dash_integration/dash_app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
from datetime import datetime, timedelta
from django_plotly_dash import DjangoDash

# Initialize the Dash app
dash_app = DjangoDash('dash_integration', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
dash_app.suppress_callback_exceptions = True  # Set suppress_callback_exceptions directly

# Define the layout of the Dash app
dash_app.layout = html.Div([
    dcc.Graph(id='live-candlestick-chart'),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Define callback to update the chart
@dash_app.callback(
    Output('live-candlestick-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_chart(n_intervals):
    # Replace 'RELIANCE.NS' with the stock symbol of your choice
    symbol = '^NSEI'

    # Get the current date and time
    now = datetime.now()

    # Specify the time range for live data (e.g., last 30 minutes)
    start_time = now - timedelta(minutes=30)

    # Fetch live data for the specified time range
    live_data = yf.download(symbol, start=start_time, end=now)

    # Create a candlestick chart
    figure = {
        'data': [{
            'x': live_data.index,
            'open': live_data['Open'],
            'high': live_data['High'],
            'low': live_data['Low'],
            'close': live_data['Close'],
            'type': 'candlestick'
        }],
        'layout': {
            'title': f'{symbol} Live Candlestick Chart',
            'xaxis': {
                'rangeslider': {'visible': False}
            },
            'yaxis': {'title': 'Stock Price'},
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black'
        }
    }

    return figure

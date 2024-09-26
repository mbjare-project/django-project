import requests
from django.conf import settings

# Function to fetch stock data from Alpha Vantage
def get_stock_data(symbol):
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'Time Series (Daily)' in data:
            daily_data = data['Time Series (Daily)']
            latest_date = list(daily_data.keys())[0]
            latest_data = daily_data[latest_date]

            return {
                'symbol': symbol,
                'date': latest_date,
                'open': latest_data['1. open'],
                'high': latest_data['2. high'],
                'low': latest_data['3. low'],
                'close': latest_data['4. close'],
                'volume': latest_data['5. volume'],
            }
        elif 'Note' in data:
            print(f"Rate limit hit for {symbol}. Message: {data['Note']}")
        elif 'Error Message' in data:
            print(f"Invalid API call for {symbol}. Message: {data['Error Message']}")
        else:
            print(f"Unexpected error for {symbol}. Data: {data}")
        return None
    except Exception as e:
        print(f"Error fetching data for {symbol}. Exception: {str(e)}")
        return None

# Function to get Nifty 50 stock data (existing)
def get_nifty_50_data():
    nifty_50_stocks = [
        'RELIANCE.BSE', 'TCS.BSE', 'INFY.BSE', 'HDFCBANK.BSE', 'ICICIBANK.BSE',
        'HINDUNILVR.BSE', 'KOTAKBANK.BSE', 'ITC.BSE', 'HDFC.BSE', 'BHARTIARTL.BSE',
        # add all 50 stocks here...
    ]
    
    stock_data_list = []
    for stock in nifty_50_stocks:
        stock_data = get_stock_data(stock)
        if stock_data:
            stock_data_list.append(stock_data)
    
    if stock_data_list:
        return stock_data_list
    else:
        print("Error: Failed to retrieve Nifty 50 data.")
        return None

# Function to get Nifty Bank stock data (new)
def get_nifty_bank_data():
    nifty_bank_stocks = [
        'HDFCBANK.BSE', 'ICICIBANK.BSE', 'KOTAKBANK.BSE', 'AXISBANK.BSE',
        'SBIN.BSE', 'INDUSINDBK.BSE', 'YESBANK.BSE', 'PNB.BSE',
        'BANKBARODA.BSE', 'CANBK.BSE', 'UNIONBANK.BSE', 'IDFCFIRSTB.BSE'
    ]
    
    stock_data_list = []
    for stock in nifty_bank_stocks:
        stock_data = get_stock_data(stock)
        if stock_data:
            stock_data_list.append(stock_data)
    
    if stock_data_list:
        return stock_data_list
    else:
        print("Error: Failed to retrieve Nifty Bank data.")
        return None

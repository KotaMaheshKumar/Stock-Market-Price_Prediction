import yfinance as yf
import datetime


tickers = [
    'SPY',  # SPDR S&P 500 ETF Trust,
    'DIA',  # Dow Jones Industrial Average,
    '^IXIC',  # Nasdaq Composite,
    '^GSPC',  # S&P 500
   '^DJI'

]

today = datetime.date.today()
print(today, type(today))
tickers_string = " ".join(tickers)
print(tickers_string, type(tickers_string))
start_date = "2026-10-27"

historical_data = yf.download(tickers_string, start=start_date, end=today) # type: ignore

print(historical_data, type(historical_data))

historical_data_dict = {}
for ticker in tickers:
    print("Ticker", ticker)
    ticker_df = historical_data.xs(ticker, level = 'Ticker', axis = 1)
    print("Ticker_df",ticker_df )
    ticker_df.attrs['name'] = f"{ticker}_data"
    print("ticker_df_Atts", ticker_df, ticker_df.columns)
    # 3. Creating key-value pair of ticker and respective historical data 
    historical_data_dict[f"{ticker}"] = ticker_df    

    print("Hist_DF", historical_data_dict)

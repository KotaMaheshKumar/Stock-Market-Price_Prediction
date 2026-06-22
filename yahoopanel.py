import pandas as pd
import yfinance as yf
import datetime

from globallocalvar import *

class YahooPanel:

    # def __init__(self, ticker : str):
    #     self.ticker = ticker

    def get_today(self):
        now = datetime.datetime.now()
        today = datetime.date.today()
        return today
    

    
    def get_historical_data(self, tickers : list, start_date : str):
        today = self.get_today()

        #1. Join list of tickers into a single string separated by spaces
        tickers_string = " ".join(tickers)

        historical_data = yf.download(tickers_string, start=start_date, end=today)
        
        '''
        # STORING HISTORICAL DATA IN A DICTIONARY

        The tickers list will be levelled individually 
        in the multi-index of the columns of the historical_data DataFrame.  
        
        '''
        historical_data_dict = {}
        for ticker in tickers:
            # 2. Removing the multi-index and keeping only the data for the specific ticker
            ticker_df =  historical_data.xs(ticker, level= 'Ticker', axis=1)

            # Adding the metadata tag
            ticker_df.attrs['name'] = f"{ticker}_data"

            # 3. Creating key-value pair of ticker and respective historical data 
            historical_data_dict[f"{ticker}"] = ticker_df          

        return historical_data_dict
    
       
    def us_index_panel(self, start_date : str):
        us_market_data = self.get_historical_data(US_MARKET_INDICES, start_date)

        ## Creating a DataFrame to store the US market indices data

        dataframes = { key.replace("^", "").lower(): pd.DataFrame(value) 
                for key, value in us_market_data.items() 
                }
       
        spy_data, dia_data, ixic_data, gspc_data, dji_data = (
            dataframes.get(
            index.replace("^", "").lower(),
            pd.DataFrame()
            )
            for index in US_MARKET_INDICES
        )

        return spy_data, dia_data, ixic_data, gspc_data, dji_data
    

    def european_index_panel(self, start_date : str):
        european_market_data = self.get_historical_data(EUROPEAN_MARKET_INDICES, start_date)

        dataframes = { key.replace("^", "").lower(): pd.DataFrame(value) 
                for key, value in european_market_data.items() 
                }
       
        gdaxi_data, fchi_data = (
            dataframes.get(
            index.replace("^", "").lower(),
            pd.DataFrame()
            )
            for index in EUROPEAN_MARKET_INDICES
        )

        return gdaxi_data, fchi_data
    


    def asian_index_panel(self, start_date : str):
        asian_market_data = self.get_historical_data(ASIAN_MARKET_INDICES, start_date)

        dataframes = { key.replace("^", "").lower(): pd.DataFrame(value) 
                for key, value in asian_market_data.items() 
                }
       
        n225_data, hsi_data, aord_data = (
            dataframes.get(
            index.replace("^", "").lower(),
            pd.DataFrame()
            )
            for index in ASIAN_MARKET_INDICES
        )

        return n225_data, hsi_data, aord_data
    


    def global_index_panel(self,start_date : str):

        # US exchanges index
        spy_data, dia_data, Nasdaq_composite, sp500, dji_data = self.us_index_panel(start_date)

        # European market index 
        Daxi_data, Cac40_data = self.european_index_panel(start_date)

        # Asian market index
        n225_data, hsi_data, aord_data = self.asian_index_panel(start_date)

        # Global market index panel
        GlobalPanel=pd.DataFrame(index=spy_data.index)
        GlobalPanel['spy']= spy_data['Open'].shift(-1)-spy_data['Open']
        GlobalPanel['spy_lag1']=  GlobalPanel['spy'].shift(1)
        GlobalPanel['sp500']=  sp500["Open"]- sp500['Open'].shift(1)
        GlobalPanel['nasdaq']=  Nasdaq_composite['Open']- Nasdaq_composite['Open'].shift(1)
        GlobalPanel['dji']= dji_data['Open']- dji_data['Open'].shift(1)

        #European Market
        GlobalPanel['cac40']= Cac40_data['Open']- Cac40_data['Open'].shift(1)
        GlobalPanel['daxi']= Daxi_data['Open']- Daxi_data['Open'].shift(1)

        #Asian Market
        GlobalPanel['hsi'] = hsi_data['Close'] - hsi_data['Open']
        GlobalPanel['nikkei'] = n225_data['Close'] - n225_data['Open'] 
        GlobalPanel['aord'] = aord_data['Close']- aord_data['Open']

        GlobalPanel['Price'] = spy_data['Open']

        return GlobalPanel

    


    

   




    



    


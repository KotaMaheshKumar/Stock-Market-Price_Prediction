import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import numbers

from scipy.stats import norm

import warnings 
warnings.filterwarnings("ignore")

from yahoopanel import YahooPanel

class StockFeatureEngineering:
    def __init__(self, stock_data):
        self.stock_data = stock_data

    def observational_stats(self, variable : str):
        sample_size = self.stock_data[variable].shape[0]
        sample_mean = self.stock_data[variable].mean()
        sample_standard_deviation = self.stock_data[variable].std()
        sample_standard_error = sample_standard_deviation.std(ddof = 1) / sample_size ** 0.5

        return sample_size, sample_mean , sample_standard_deviation, sample_standard_error
    

    def calculate_moving_average(self, window=20):
        self.stock_data['Moving_Average'] = self.stock_data['Close'].rolling(window=window).mean()
        return self.stock_data

    def calculate_volatility(self, window=20):
        self.stock_data['Volatility'] = self.stock_data['Close'].rolling(window=window).std()
        return self.stock_data

    def calculate_rsi(self, window=14):
        delta = self.stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.stock_data['RSI'] = 100 - (100 / (1 + rs))
        return self.stock_data

    def calculate_bollinger_bands(self, window=20):
        rolling_mean = self.stock_data['Close'].rolling(window=window).mean()
        rolling_std = self.stock_data['Close'].rolling(window=window).std()
        self.stock_data['Bollinger_Upper'] = rolling_mean + (rolling_std * 2)
        self.stock_data['Bollinger_Lower'] = rolling_mean - (rolling_std * 2)
        return self.stock_data


    def calculate_macd(self, fast=12, slow=26, signal=9):
        exp1 = self.stock_data['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = self.stock_data['Close'].ewm(span=slow, adjust=False).mean()
        self.stock_data['MACD'] = exp1 - exp2
        self.stock_data['MACD_Signal'] = self.stock_data['MACD'].ewm(span=signal, adjust=False).mean()
        return self.stock_data
    
    def calculate_features(self):
        self.calculate_moving_average()
        self.calculate_volatility()
        self.calculate_rsi()
        self.calculate_bollinger_bands()
        self.calculate_macd()
        return self.stock_data
    
    def get_features(self):
        return self.stock_data[['Date', 'Close', 'Moving_Average', 'Volatility', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower', 'MACD', 'MACD_Signal']]
    
    def day_returns(self):
        self.stock_data['PriceDiff'] = self.stock_data.Close.shift(-1) - self.stock_data.Close
        # For Daily returns
        self.stock_data['DailyReturn'] = self.stock_data.PriceDiff / self.stock_data.Close

        return self.stock_data
    
    def stock_direction(self):
        self.stock_data['Direction'] = [1 if self.stock_data['PriceDiff'].loc[element] > 0 else 0 for element in self.stock_data.index]
        return self.stock_data
    
    def holiding_shares(self):
        # Calculating moving averages for 60, 20 days
        self.stock_data['MA60'] = self.calculate_moving_average(window = 60)
        self.stock_data['MA20'] = self.calculate_moving_average(window = 20)

        # Shares to long based on measuring 0 --> 1  of the stock moving averages
        self.stock_data['Shares'] = [1 if self.stock_data.loc[element,'MA20'] > self.stock_data.loc[element, 'MA60'] else 0 for element in self.stock_data.index]

        return self.stock_data
    
    def individual_stock_profit(self):
        self.stock_data['Close1'] = self.stock_data.Close.shift(-1)
        # 'Profit': Daily profit using 'Shares' column
        self.stock_data['Profit'] = [self.stock_data.loc[element, 'Close1'] - self.stock_data.loc[element, 'Close'] if self.stock_data.loc[element, 'Shares'] == 1 else 0 for element in self.stock_data.index]

        return self.stock_data

    def wealth_cumulation(self):
        self.stock_data['Wealth'] = self.stock_data.Profit.cumsum()
        
        return self.stock_data
    
    def log_returns_distribution(self):
        self.stock_data['LogReturn'] = np.log(self.stock_data['Close'].shift(-1)) - np.log(self.stock_data['Close'])
        # Distribution statistics
        mu_log = self.stock_data.LogReturn.mean()
        std_log = self.stock_data.LogRetun.std(ddof = 1)

        density_df = pd.DataFrame()
        density_df['x'] = np.arange(self.stock_data['LogReturn'].min(),self.stock_data['LogReturn'].max(), 0.001)
        density_df['pdf'] = norm.pdf(density_df['x'], mu_log, std_log)

        # In this case, we would like to calculate the mean, stdeviation for a working year i.e 252 for the same variable 
        mu_252 = mu_log * 252
        std_252 = std_log * 252

        return self.stock_data, mu_log, std_log, mu_252, std_252, density_df
    
    def percentile_and_point_function(self, func_type : str, value : int | float | numbers.Real, mu , sigma):
        distribution = norm(loc = mu, scale = sigma) 
        try:
            method = getattr(distribution, func_type.lower().strip())
            output_value = method(value)
            return output_value
        except AttributeError:
            raise ValueError(f"Invalid function type '{func_type}'. Choose 'cdf', 'ppf', etc.")    


    def hypothesis_testing(self, variable : str, alpha : int | float):
        sample_size, sample_mean , sample_standard_deviation, sample_standard_error = self.observational_stats(variable)

        # H0 is null hypothesis
        z_hat = (sample_mean - 0) / (sample_standard_deviation/ sample_size ** 0.5)
        z_left = norm.ppf(alpha/2, 0, 1)
        z_right = - z_left
        
        # Shall we accept or reject H0
        print('At significance level of {}, shall we reject {}'.format(alpha, z_hat < z_left or z_hat > z_right ))

        # Decision Criteria
        zright = norm.ppf(1 - alpha, 0, 1)
        print('At significant level of {}, we shall reject {}').format(alpha, z_hat > zright)

        # For p-value
        p = 1 - norm.cdf(abs(z_hat), 0, 1)
        print('At significant level of {}, shall we reject {}'.format(alpha, p < alpha))








       






        


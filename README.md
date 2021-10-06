# Stock Market-Financial-Analysis


Stock market analysis is requisite and important to gain knowledge of the equity market to arrive at true value of a stock. Generally, it is conducted in two types: Fundamental Research and Technical Research. Here, it is an attempt to establish generic models, practical for the stock market analysis by using mathematics concepts statistics and programming language python.

    

CONTENTS

∙ Introduction
∙ Libraries used
∙ Data Description
∙ Exploratory Analysis(EDA)
∙ Simple Trading Strategy to estimate the wealth generation by investing over a stock in a period of time.
∙ Model of stock returns using regression models
∙ Multi regression model to predict the price change in the SPY using different global markets.
∙ Using LSTM predicting the future price of amazon stock.


Introduction
> Understanding the importance of stock market analysis and its components.

Libraries used
1. Yahoo Finance -----  To download the stock data
2. Pandas        -----  Handling DataFrames in python
3. Numpy         -----  Numerical Python
4. Matplotlib    -----  Plotting graphs
5. seaborn       -----  Plotting graphs
6. stats         -----  python built-in library for statistics

Data Description
> The downloaded daily stock prices data using YahooFinance API provides the information about,
Open: Price of stock when market opens in the morning
Close: Price of stock when the market closes in the evening
Adj Close: Price of stock adjusted to reflect the stock's value after accounting any corporate actions.
High: Highest price the stock registered trading on that day
Low: Lowest price the stock is traded on that day.
Volume: Total amount of stocks traded on that day.

EDA
> Exploratory data analysis is an approach of analyzing the stock data to summarize data characteristics by doing data manipulation(statistical) and visualisation methods.

Simple Trading Strategy to estimate the wealth generation by investing over a stock in a period of time
> Created a trading strategy, assuming investment over a stock only on profits day(model created) to estimate the wealth generation in a period of time i.e day of investment to buying out day.

Model of stock returns using regression models
> By using advanced statistics understanding the distribution of stock data, average return and checking the efficency. 

Multi regression model to predict the price change in the SPY using different global markets
> Created an multiregression model to predict the price in change of SPY with different global markets which opens and closes at their geographical locations.
> Divided the markets into three types: US markets, EUROPEAN markets, ASIAN markets.


Using LSTM predicting the future price of amazon stock
> Created an LongShort term memory model stores past information and predicts the future price of amazon stock.


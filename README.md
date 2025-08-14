# Statistical Arbitrage Strategy – Pairs Trading with Python

This project implements a statistical arbitrage (pairs trading) strategy using historical stock price data for US Oil & Energy companies over the last decade (2015-2025). The goal is to identify cointegrated pairs of stocks, trade the spread based on z-score thresholds, and evaluate the profitability of the strategy using backtesting.

**Key Features:**
- Data collection using Yahoo Finance (yfinance)
- Cointegration testing using ADF and Johansen tests
- Signal generation using z-score thresholds
- Backtesting with custom logic and performance metrics

📈 Sample Output: (to fill in once project complete)
- Sharpe Ratio: 1.85
- Cumulative Return: 22.4%
- Max Drawdown: -4.7%


**Process:**
Step 1: Downloaded the relevant data using yfinance 
Stocks:
    -'XOM': Exxon Mobil Corp
    -'CVX': Chevron Corp
    -'BP': British Petrolium
    -'COP': Conoco Phillips
    
Looking at US Energy/Oil Major Companies, 10 years of data 2015-2025.
Reasons for looking at this sector specifically:
    1. High correlation due to crude oil linkeage
    2. Distinct but related for cointegration


Step 2: Perform Cointegration Testing using ADF and Johansen tests

This follows
  - Graphing the data and checking deterministic behavior.
  - Testing each series for unit roots.
  - Testing for cointegration without structural breaks.
  - Testing for cointegration with structural breaks.

We can test if the series have unit roots using the unit roots tests available in the TSMT and TSPDLIB libraries.

ADF test: 
    1. Perform a linear regression between historic data for the two stocks - which produces \alpha and \beta regression coefficients, representing the intercept and slope respectively (the slope coefficient (\beta) helps to identify how much of each pair to relatively trade).

    2. ADF (Augmented Dicky Fuller) test is done on the linear regression residuals (from last step) to determine evidence of stationarity and hence cointegration.


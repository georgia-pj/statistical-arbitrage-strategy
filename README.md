# Statistical Arbitrage Strategy – Pairs Trading with Python

This project implements a **statistical arbitrage (pairs trading) strategy** using historical stock price data. The goal is to identify cointegrated pairs of stocks, construct and trade the spread based on z-score thresholds, and evaluate the profitability of the strategy using backtesting.

**Key Features:**
- Data collection of historical price series (via yfinance)
- Johansen cointegration test to identify tradable pairs
- Spread construction & stationarity validation (ADF test)
- Mean-reversion backtest with entry/exit rules
- Performance evaluation with cumulative returns & risk metrics

**Tech Stack:**
- **Python** (pandas, numpy, statsmodels, matplotlib)
- **Spyder** for analysis & visualisation
- **yfinance** for data sourcing

## Results
### Spread with ±2σ bands:
![Spread - APPL & MSFT](images/Cointegration%20Spread%20Z-Score%20Normalized.png)

### Strategy Cumulative Returns:
![Backtest Results](images/mean_reversion_backtest.png)


## Process:
### Step 1: Downloaded the relevant data using yfinance 
Initially looked at US Energy/Oil Major Companies, 10 years of data 2015-2025.
Reasons for looking at this sector specifically:
    1. High correlation due to crude oil linkeage
    2. Distinct but related for cointegration  

But, was struggling to find stocks cointegrated over long periods of time, so settled for the good old pair of Apple (APPL) and Microsoft (MSFT).  


### Step 2: Perform Cointegration Testing using ADF and Johansen tests  
**ADF test:**  
    1. Perform a linear regression between historic data for the two stocks - which produces $\alpha$ and $\beta$ regression coefficients, representing the intercept and slope respectively (the slope coefficient ($\beta$) helps to identify how much of each pair to relatively trade).\
    \
    2. ADF (Augmented Dicky Fuller) test is done on the linear regression residuals (from last step) to determine evidence of stationarity and hence cointegration.\
    \
    3. If the p value is < 0.05, the spread is stationary, so the stocks are likely cointegrated.\
    

**Johansen test:**  
The Johansen test is more useful in this case than the ADF test, as it can analyse the cointegration of multiple stocks simultaneously, whereas ADF can only compare two as it requires regressions (one stock regressed on the other).  
    1. If the test statistic (lr1) > critical value (crv) at 95%, cointegration exists  
    2. In the Johansen test, the rank is the number of distinct cointegrating relationships among the set of stocks (time series). With n time-series (eg 4 stock price series in this case), the Johansen test will determine how many linear combinations of them are stationary (mean-reverting). The rank can be defined as follows:  
        0 -> No cointegration (no stationary linear combination)\
        1 -> One stationary linear combination\
        2 -> Two independent stationary combinations, and so on  


14 August 2025:  
Using the Johansen test with the tickers 'XOM', 'CVX', 'BP', 'COP' from 1 Jan 2024 to 1 Feb 2024, I have the results:
Rank 0: Cointegration exists\
Rank 1: Not cointegrated\
Rank 2: Not cointegrated\
Rank 3: Not cointegrated\

So, there is at exactly one cointegrating relationship. Thus, the set of 4 stocks share one stationary linear combination.  

Using johansen_result.evec, can get the weights for each of the stocks. Normalise them, and build a spread (adj_close.dot(normalised_weights)).  

Use an ADF test to check if it stationary. I then plotted a graph with the spread over time, with the mean and mean +/- 2 standard deviations.  








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


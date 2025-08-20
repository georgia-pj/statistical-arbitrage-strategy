import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np


#tickers = ['XOM', 'CVX', 'BP', 'COP']  
tickers = ['AAPL', 'MSFT']
data = yf.download(tickers, start='2011-01-01', end='2013-01-01', auto_adjust=False)
adj_close = data['Adj Close'].dropna()  # Select only adjusted close prices, clean missing data
#print(data.head())



#ADF TEST FOR COINTEGRATION
def ADF_test(stock1, stock2):

    #Step 1: Regress XOM on BP
    x = sm.add_constant(adj_close[str(stock1)])
    model = sm.OLS(adj_close[str(stock2)], x).fit()
    spread = model.resid
    
    #Step 2: ADF on residuals
    adf_result = adfuller(spread)
    print(f"ADF Statistic: {adf_result[0]}")
    #the more negative the statistic is, the more likely it is stationary
    print(f"p-value: {adf_result[1]}")
    
    #if p value is < 0.05, spread is stationary so likely cointegrated
    if adf_result[1] < 0.05:
        print("Likely cointegrated (spread is stationary)")
    else:
        print("Not cointegrated")
        



#JOHANSEN TEST FOR COINTEGRATION
def Johansen():
    johansen_result = coint_johansen(adj_close, det_order=0, k_ar_diff=1)
    print("Johansen eigenvalues:", johansen_result.lr1)
    print("Critical values (90%, 95%, 99%):\n", johansen_result.cvt)
    
    #if test statistic > critical value at 95%, cointegration exists
    
    lr1 = johansen_result.lr1 #NumPy array of test statistics for each rank
    cvt = johansen_result.cvt
    
    #Rank is the number of distinct cointegrating relationships
    for idx in range(len(lr1)):
        if lr1[idx] > cvt[idx, 1]:
            print(f"Rank {idx}: Cointegration exists")
            #print(johansen_result.evec)
            rank = idx
        else:
            print(f"Rank {idx}: Not cointegrated")
            
    return johansen_result, rank
        
               

def mean_reversion():
    johansen_result, rank = Johansen()
    weight = johansen_result.evec 
    #positive weight = long the asset in the spread, negative weight = short the asset
    #spread should be kept stationary over time
    vec = weight[:, 0]
    norm_vec= vec / vec[-1] #normalised the cointegration vectors (weight for rank 0)
    print(f"Cointegration vector: {vec}")
    print(f"Normalised cointegration vector: {norm_vec}")
    
    spread = adj_close.dot(vec) #build the spread
    
    #ADF test to check stationary
    adf_result = adfuller(spread)
    print("ADF Statistic: ", adf_result[0])
    print("p-value: ", adf_result[1])
    
    #Plot spread with mean ± 2σ bands
    mean = spread.mean()
    std = spread.std()
    z_score = (spread - mean) / std #so in units of σ

    
    plt.plot(z_score, label='spread (z-score)')
    plt.axhline(0, color='black', linestyle='--', label='Mean')
    plt.axhline(2, color='red', linestyle='--', label='+2σ')
    plt.axhline(-2, color='green', linestyle='--', label='-2σ')
    plt.title('Cointegration Spread with ±2σ Bands (Z-Score Normalised)')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Date')
    plt.ylabel('Standard Deviations (σ)')
    plt.legend(fontsize='small')
    plt.show()
    
    return spread, norm_vec
    

def mean_reversion_backtest(adj_close, weights, entry_z=0.5, exit_z=0, window=5):
    """
    adj_close: DataFrame of asset prices
    weights: normalized cointegration vector
    entry_z: threshold (in std deviations) to enter trades
    exit_z: threshold to exit trades (usually 0 = mean)
    window: for rolling z-score -> 20 days so not cumulating over all history
    """
    
    # Compute spread
    #scale stock prices so spread not dominated by higher stock prices
    # Use log prices to avoid domination by high-priced stocks
    log_prices = np.log(adj_close)
    spread = log_prices.dot(weights)

    
    # Compute z-score of spread (how many std's away the data point is from mean)
    rolling_mean = spread.rolling(window).mean()
    rolling_std = spread.rolling(window).std()
    z_score = (spread - rolling_mean) / rolling_std

    
    #4. Generate signals (if under threshold = long the stock, if over threshold = short)
    # 1=long, -1=short, 0=flat
    positions = pd.Series(0, index=spread.index)
    positions[z_score < -entry_z] = 1 #long
    positions[z_score > entry_z] = -1 #short
    
    #Close for positions when spread crosses mean
    for t in range(1, len(positions)):
        if positions[t-1] == 1 and z_score[t] >= exit_z:
            positions[t] = 0
        elif positions[t-1] == -1 and z_score[t] <= exit_z:
            positions[t] = 0
        elif positions[t] == 0:
            positions[t] = positions[t-1]
            
            
    #Compute daily returns of the spread
    spread_returns = spread.diff().fillna(0)
    strategy_returns = positions.shift(1) * spread_returns #lag by 1 day
    cum_ret = strategy_returns.cumsum() #Compute cumulative returns
    cum_ret_perc = (1 + strategy_returns).cumprod() - 1
    
    #Plot results
    plt.plot(cum_ret_perc, label = 'Cumulative Strategy Returns')
    plt.title('Mean-Reversion Backtest')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Percentage Cumulative Returns')
    plt.xticks(rotation=45, ha='right')
    plt.show()
    
    return positions, cum_ret
    
#ADF_test(tickers[0], tickers[1])
#Johansen()    
spread, weights = mean_reversion()
positions, cum_ret = mean_reversion_backtest(adj_close, weights)

print("Weights:", weights)
print("Spread stats:", spread.describe())
print(adj_close.shape)
    


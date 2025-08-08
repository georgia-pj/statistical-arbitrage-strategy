# Statistical Arbitrage & Cointegration Testing Guide

## 1️⃣ What is Statistical Arbitrage? (In Plain English)

Imagine two friends, Alice and Bob, who always walk together.  
Sometimes Alice walks a little ahead, sometimes Bob does, but over time they stay **roughly side-by-side**.

- If Alice gets *way* ahead, you could bet that Bob will catch up (or Alice will slow down).
- That bet — based on them historically sticking together — is **statistical arbitrage**.

In finance, Alice and Bob are **two stocks** whose prices move together over time due to shared fundamentals (e.g., same sector, market forces).  
We want to **find such pairs** and trade the temporary misalignments.

---

## 2️⃣ What is Cointegration?  

Two stocks are **cointegrated** if:
- Their prices individually might wander around randomly (like drunk walkers).
- But the **difference between them stays within a stable range** over time.

That “difference” is called the **spread**.

**Why care?**  
If two stocks are cointegrated:
- When the spread is unusually wide → expect it to narrow (mean reversion).
- You can **buy the cheaper one and short the expensive one**.

---

## 3️⃣ How to Test for Cointegration

We’ll use **historical data (2015–2025)** and two main tests:

### **A) Augmented Dickey-Fuller (ADF) Test**
- Purpose: Checks if a time series is **stationary** (has a stable mean/variance).
- How we use it:  
  1. Regress Stock A on Stock B.
  2. Get the residuals (spread).
  3. Run the ADF test on those residuals.
  4. If p-value < 0.05 → spread is stationary → stocks are cointegrated.

### **B) Johansen Test**
- Purpose: Tests for cointegration between **more than two time series at once**.
- How we use it:  
  1. Give it a set of price series (e.g., 3+ stocks).
  2. It finds if there are any cointegration relationships between them.
- Advantage: No need to pick one stock as “dependent” — it’s symmetric.

---

## 4️⃣ Step-by-Step in Python (Using `yfinance`)

```python
import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import statsmodels.api as sm

# 1. Download stock data (2015–2025)
tickers = ['XOM', 'CVX']  # Energy majors example
data = yf.download(tickers, start='2015-01-01', end='2025-01-01')['Adj Close']
data.dropna(inplace=True)

# 2. ADF Test for Cointegration
# Step 2.1: Regress XOM on CVX
x = sm.add_constant(data['CVX'])
model = sm.OLS(data['XOM'], x).fit()
spread = model.resid

# Step 2.2: ADF on residuals
adf_result = adfuller(spread)
print(f"ADF Statistic: {adf_result[0]}")
print(f"p-value: {adf_result[1]}")
if adf_result[1] < 0.05:
    print("✅ Likely cointegrated (spread is stationary)")
else:
    print("❌ Not cointegrated")

# 3. Johansen Test (for >2 stocks)
johansen_result = coint_johansen(data, det_order=0, k_ar_diff=1)
print("Johansen eigenvalues:", johansen_result.lr1)
print("Critical values:\n", johansen_result.cvt)
```

---

## 5️⃣ Interpreting the Results

- **ADF p-value < 0.05** → Reject “non-stationary” → Spread is stable → Cointegration likely.
- **Johansen Test** → Look at `lr1` vs `cvt` (critical values). If test statistic > critical value at 95% → Cointegration exists.

---

## 6️⃣ In a Nutshell Workflow

1. Pick stocks in the same sector (more likely cointegrated).
2. Pull historical prices from Yahoo Finance.
3. Run **ADF** on their spread (for pairs) or **Johansen** (for groups).
4. If cointegrated → consider building a **mean reversion strategy**.

---

**Tip:** Always use **Adjusted Close** prices, as they account for splits and dividends.


# Statistical Arbitrage & Cointegration Testing Guide

## 1. What is Statistical Arbitrage?

Imagine two friends, Alice and Bob, who always walk together.  
Sometimes Alice walks a little ahead, sometimes Bob does, but over time they stay **roughly side-by-side**.

- If Alice gets *way* ahead, you could bet that Bob will catch up (or Alice will slow down).
- That bet — based on them historically sticking together — is **statistical arbitrage**.

In finance, Alice and Bob are **two stocks** whose prices move together over time due to shared fundamentals (e.g., same sector, market forces).  
We want to **find such pairs** and trade the temporary misalignments.

---

## 2️. What is Cointegration?  

Two stocks are **cointegrated** if:
- Their prices individually might wander around randomly (like drunk walkers).
- But the **difference between them stays within a stable range** over time.

That “difference” is called the **spread**.

**Why care?**  
If two stocks are cointegrated:
- When the spread is unusually wide → expect it to narrow (mean reversion).
- You can **buy the cheaper one and short the expensive one**.

---

## 3. How to Test for Cointegration

I used **historical data (2011-2013)** and two main tests:

### **A) Augmented Dickey-Fuller (ADF) Test**
- Purpose: Checks if a time series is **stationary** (has a stable mean/variance).
- How it's used:  
  1. Regress Stock A on Stock B.
  2. Get the residuals (spread).
  3. Run the ADF test on those residuals.
  4. If p-value < 0.05 → spread is stationary → stocks are cointegrated.

### **B) Johansen Test**
- Purpose: Tests for cointegration between **more than two time series at once**.
- How it's used:  
  1. Give it a set of price series (e.g., 3+ stocks). I initially used 4 Oil & Energy stocks: XOM, CVX, BP, COP
  2. It finds if there are any cointegration relationships between them.
- Advantage of Johansen test over ADF is that you don't need to pick one stock as a "dependent" as it's symmetric
- See my ![python script](cointegration_and_backtesting.py) for how I did it.

---

## 4. Interpreting the Results

- **ADF p-value < 0.05** → Reject “non-stationary” → Spread is stable → Cointegration likely.
- **Johansen Test** → Important values are  the `lr1` vs `cvt` (critical values). lr1 is a NumPy array of test statistics for each rank, where rank is the number of cointegrating relationships. If the test statistic (lr1) > critical value (cvt) at 95% → Cointegration exists.

---

## 5. Final Overview / How To

1. Pick stocks in the same sector (more likely cointegrated).
2. Pull historical prices from Yahoo Finance.
3. Run **ADF** on their spread (for pairs) or **Johansen** (for groups).
4. If cointegrated → consider building a **mean reversion strategy**.

---

**Tip:** Always use **Adjusted Close** prices, as they account for splits and dividends.


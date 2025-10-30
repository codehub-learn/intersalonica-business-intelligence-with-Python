"""
Advent of Code - Day 7 - Exercise 2

This script implements the Black–Scholes model, Monte Carlo simulation, and computes Delta, Gamma, Vega, Theta, and Rho


"""

import numpy as np

# --- Step 1: Parameters ---
S0 = 100.0      # initial stock price
K = 105.0       # strike price
T = 1.0         # time to maturity (1 year)
r = 0.05        # risk-free interest rate
sigma = 0.2     # volatility
n_sim = 1_000_000  # Monte Carlo simulations

# --- Step 2: Monte Carlo pricing for a European Call ---
np.random.seed(42)
Z = np.random.standard_normal(n_sim)
ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
payoffs = np.maximum(ST - K, 0)
C0_MC = np.exp(-r * T) * np.mean(payoffs)

print(f"Monte Carlo European Call Price: {C0_MC:.4f}")

# --- Step 3: Analytical Black–Scholes formula for comparison ---
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    call_price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return call_price, d1, d2

C0_BS, d1, d2 = black_scholes_call(S0, K, T, r, sigma)
print(f"Black–Scholes Analytical Price: {C0_BS:.4f}")

# --- Step 4: Compute Greeks using NumPy (vectorized) ---
Delta = norm.cdf(d1)
Gamma = norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
Vega = S0 * norm.pdf(d1) * np.sqrt(T)
Theta = -(S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2)
Rho = K*T*np.exp(-r*T)*norm.cdf(d2)

print("\nOption Greeks:")
print(f"  Delta: {Delta:.4f}")
print(f"  Gamma: {Gamma:.6f}")
print(f"  Vega : {Vega:.4f}")
print(f"  Theta: {Theta:.4f}")
print(f"  Rho  : {Rho:.4f}")

# --- Step 5: Stress testing (sensitivity to volatility and rate) ---
vol_range = np.linspace(0.05, 0.6, 12)
price_vs_vol = np.array([black_scholes_call(S0, K, T, r, vol)[0] for vol in vol_range])

rate_range = np.linspace(0.0, 0.1, 12)
price_vs_rate = np.array([black_scholes_call(S0, K, T, rate, sigma)[0] for rate in rate_range])

# --- Step 6: Monte Carlo Delta estimation (finite difference) ---
eps = 0.01
S_up = S0 + eps
S_down = S0 - eps

ST_up = S_up * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
ST_down = S_down * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
payoffs_up = np.maximum(ST_up - K, 0)
payoffs_down = np.maximum(ST_down - K, 0)

Delta_MC = np.exp(-r*T) * (np.mean(payoffs_up - payoffs_down)) / (2*eps)
print(f"\nMonte Carlo Delta Estimate: {Delta_MC:.4f}")

# --- Step 7: Risk Simulation: P&L distribution at maturity ---
positions = 1000   # number of options held
portfolio_payoff = positions * np.maximum(ST - K, 0)
portfolio_value_today = positions * C0_BS
PnL = portfolio_payoff * np.exp(-r*T) - portfolio_value_today

VaR_99 = -np.percentile(PnL, 1)
CVaR_99 = -PnL[PnL < -VaR_99].mean()

print("\nPortfolio Risk (99% confidence):")
print(f"  Value-at-Risk (VaR): {VaR_99:,.2f}")
print(f"  Conditional VaR (CVaR): {CVaR_99:,.2f}")


import matplotlib.pyplot as plt

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(vol_range, price_vs_vol, 'o-')
plt.title("Option Price vs Volatility")
plt.xlabel("Volatility")
plt.ylabel("Call Price")

plt.subplot(1,2,2)
plt.plot(rate_range, price_vs_rate, 's-', color='purple')
plt.title("Option Price vs Interest Rate")
plt.xlabel("Interest Rate")
plt.ylabel("Call Price")

plt.tight_layout()
plt.show()

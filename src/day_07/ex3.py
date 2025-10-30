"""
Arithmetic Asian (path-dependent) call with Monte Carlo, antithetic variates,
 and control variate using the geometric Asian closed-form (we compute the normal CDF 
                                                            with np.erf so no scipy needed). 
 Also includes a pathwise Delta estimator and finite-difference Greeks.

Multi-asset Basket call (correlated assets) with Monte Carlo, antithetic variates, 
and a few variance-reduction tricks (moment-matching). Finite-difference Greeks for Delta.

"""


"""
Advanced NumPy-only examples:
A) Arithmetic Asian Call with control variate (geometric Asian closed form)
B) Multi-asset Basket Call (correlated assets)

Run as-is. Only dependency: numpy.
"""

"""
Advanced NumPy-only examples:
A) Arithmetic Asian Call with control variate (geometric Asian closed form)
B) Multi-asset Basket Call (correlated assets)

Run as-is. Only dependency: numpy.
"""


"""
Basket Option Monte Carlo — Risk–Return & Correlation Visualization
(using NumPy + SciPy + Matplotlib)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- reuse functions from previous code ---
def basket_call_mc(S0_vec, weights, K, r, Sigma, T=1.0, n_sim=100_000, antithetic=True, seed=123):
    rng = np.random.default_rng(seed)
    n_assets = len(S0_vec)
    sims = n_sim // (2 if antithetic else 1)
    L = np.linalg.cholesky(Sigma)
    Z = rng.standard_normal(size=(sims, n_assets))
    if antithetic:
        Z = np.vstack([Z, -Z])
    correlated = Z @ L.T
    drift = (r - 0.5 * np.diag(Sigma)) * T
    log_ST = np.log(S0_vec) + drift + correlated * np.sqrt(T)
    ST = np.exp(log_ST)
    basket = ST @ weights
    payoffs = np.maximum(basket - K, 0.0)
    disc = np.exp(-r * T) * payoffs
    return {
        "price": disc.mean(),
        "stderr": disc.std(ddof=1) / np.sqrt(disc.size),
        "basket_values": basket
    }

# --- Simulation parameters ---
S0_vec = np.array([100, 95, 110, 80])
weights = np.array([0.4, 0.3, 0.2, 0.1])
K = 100
r = 0.02
T = 1.0
vols = np.array([0.18, 0.22, 0.25, 0.20])

# --- correlation scenarios ---
corr_levels = [0.0, 0.25, 0.5, 0.75, 0.9]
results = []

for rho in corr_levels:
    corr = np.full((len(vols), len(vols)), rho)
    np.fill_diagonal(corr, 1.0)
    Sigma = np.outer(vols, vols) * corr
    res = basket_call_mc(S0_vec, weights, K, r, Sigma, T)
    results.append({
        "rho": rho,
        "price": res["price"],
        "risk": res["basket_values"].std(),
        "return": res["basket_values"].mean() - np.exp(r * T) * np.dot(S0_vec, weights)
    })

# --- Plot 1: Risk–Return curve ---
plt.figure(figsize=(8, 6))
risks = [r["risk"] for r in results]
returns = [r["return"] for r in results]
prices = [r["price"] for r in results]
labels = [f"ρ={r['rho']}" for r in results]

plt.plot(risks, returns, "o-", lw=2, markersize=8)
for x, y, lbl, p in zip(risks, returns, labels, prices):
    plt.text(x, y, f"{lbl}\nprice={p:.2f}", fontsize=9, ha='left', va='bottom')

plt.title("Basket Option Risk–Return Profile vs. Correlation", fontsize=14)
plt.xlabel("Basket Risk (σ of terminal value)")
plt.ylabel("Expected Excess Return")
plt.grid(True, alpha=0.3)
plt.show()

# --- Plot 2: Price vs. Correlation ---
plt.figure(figsize=(8, 5))
plt.plot(corr_levels, prices, "s-", lw=2)
plt.title("Basket Option Price vs. Correlation", fontsize=14)
plt.xlabel("Correlation ρ between assets")
plt.ylabel("Option Price")
plt.grid(True, alpha=0.3)
plt.show()

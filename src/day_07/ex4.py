"""
animated efficient-frontier plot built on top of the basket option Monte Carlo model
"""

"""
Animated Efficient Frontier:
Basket Option Monte Carlo + Dynamic Correlation Evolution
(using NumPy, SciPy, Matplotlib)
"""


"""
Animated Efficient Frontier:
Basket Option Monte Carlo + Dynamic Correlation Evolution
(using NumPy, SciPy, Matplotlib)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import norm

# ----------------------------
# Monte Carlo basket call pricing
# ----------------------------
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
        "risk": basket.std(),
        "return": basket.mean() - np.exp(r * T) * np.dot(S0_vec, weights)
    }

# ----------------------------
# Parameters
# ----------------------------
S0_vec = np.array([100, 95, 110, 80])
weights = np.array([0.4, 0.3, 0.2, 0.1])
K = 100
r = 0.02
T = 1.0
vols = np.array([0.18, 0.22, 0.25, 0.20])

# Range of correlation values (to animate)
corr_range = np.linspace(0.0, 0.95, 20)

# Precompute results
results = []
for rho in corr_range:
    corr = np.full((len(vols), len(vols)), rho)
    np.fill_diagonal(corr, 1.0)
    Sigma = np.outer(vols, vols) * corr
    res = basket_call_mc(S0_vec, weights, K, r, Sigma, T)
    res["rho"] = rho
    results.append(res)

# Extract arrays for plotting
risks = np.array([r["risk"] for r in results])
returns = np.array([r["return"] for r in results])
prices = np.array([r["price"] for r in results])
rhos = np.array([r["rho"] for r in results])

# ----------------------------
# Animation setup
# ----------------------------
fig, ax = plt.subplots(figsize=(8, 6))
line, = ax.plot([], [], "o-", lw=2, color="dodgerblue")
text = ax.text(0.05, 0.9, "", transform=ax.transAxes, fontsize=12, color="black")

ax.set_xlim(0.9 * risks.min(), 1.1 * risks.max())
ax.set_ylim(1.1 * returns.min(), 1.1 * returns.max())
ax.set_title("Animated Efficient Frontier — Basket Option vs Correlation", fontsize=14)
ax.set_xlabel("Basket Risk (σ of terminal value)")
ax.set_ylabel("Expected Excess Return")
ax.grid(alpha=0.3)

# Initialize animation frame
def init():
    line.set_data([], [])
    text.set_text("")
    return line, text

# Update function for each frame
def update(frame):
    i = frame
    line.set_data(risks[:i+1], returns[:i+1])
    current_rho = rhos[i]
    current_price = prices[i]
    text.set_text(f"ρ = {current_rho:.2f}\nOption Price = {current_price:.4f}")
    return line, text

anim = FuncAnimation(fig, update, frames=len(rhos),
                     init_func=init, interval=500, blit=False, repeat=False)

plt.show()


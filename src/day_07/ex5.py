import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Objective coefficients (note: linprog minimizes → use negative for maximization)
c = [-40, -30]  # maximize 40x1 + 30x2

# Constraint matrix (A_ub * x <= b_ub)
A = [
    [2, 1],   # labor
    [1, 1]    # material
]
b = [100, 80]

# Bounds for x1 and x2
x_bounds = (0, None)
bounds = [x_bounds, x_bounds]

# Solve linear program
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

print("Status:", res.message)
print(f"Optimal values: x1 = {res.x[0]:.2f}, x2 = {res.x[1]:.2f}")
print(f"Maximum profit: {(-res.fun):.2f}")

# --- Visualization of feasible region ---
x1 = np.linspace(0, 60, 200)
x2_1 = 100 - 2*x1        # 2x1 + x2 <= 100
x2_2 = 80 - x1           # x1 + x2 <= 80

plt.figure(figsize=(8, 6))
plt.plot(x1, x2_1, label=r'$2x_1 + x_2 <= 100$')
plt.plot(x1, x2_2, label=r'$x_1 + x_2 <= 80$')

# Feasible region shading
plt.fill_between(x1, np.minimum(x2_1, x2_2), 0, color='lightblue', alpha=0.5)

# Plot optimal point
plt.plot(res.x[0], res.x[1], 'ro', label='Optimal Solution')
plt.text(res.x[0]+0.5, res.x[1]+0.5,
         f"Opt: x1={res.x[0]:.1f}, x2={res.x[1]:.1f}\nProfit={-res.fun:.1f}",
         fontsize=10, color='red')

plt.xlim(0, 60)
plt.ylim(0, 80)
plt.xlabel(r'$x_1$ (Product A units)')
plt.ylabel(r'$x_2$ (Product B units)')
plt.title('Linear Programming Feasible Region and Optimum')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

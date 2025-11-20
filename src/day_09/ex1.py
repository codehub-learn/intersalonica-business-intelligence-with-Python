import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X**2 + Y**2) / (X**2 + Y**2)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True)
cont = ax.contour(X, Y, Z, 15, offset=-0.5, cmap='plasma')

ax.set_title("Advanced 3D Surface + Contour Projection")
fig.colorbar(surf)
plt.show()

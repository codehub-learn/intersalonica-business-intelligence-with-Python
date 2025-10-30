# mock data 4 categorical labels , 6 numeric range 0 -1 for 1000 rows
import random
random.seed(42)

categories = ['A', 'B', 'C', 'D']
data = []
for _ in range(1000):
    row = {
        'category': random.choice(categories),
        'value1': round(random.uniform(0, 1), 2),
        'value2': round(random.uniform(0, 1), 2),
        'value3': round(random.uniform(0, 1), 2),
        'value4': round(random.uniform(0, 1), 2),
        'value5': round(random.uniform(0, 1), 2),
        'value6': round(random.uniform(0, 1), 2),
    }
    data.append(row)    

for row in data[:5]:
    print(row)
print("Total rows generated:", len(data))

# plot histograms for numeric columns
import matplotlib.pyplot as plt
numeric_cols = ['value1', 'value2', 'value3', 'value4', 'value5', 'value6']
fig, axes = plt.subplots(2, 3, figsize=(15, 8)) 
for i, col in enumerate(numeric_cols):
    ax = axes[i//3, i%3]
    values = [row[col] for row in data]
    ax.hist(values, bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'Histogram of {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')  

plt.tight_layout()
plt.show()

#scatter plot for value1 vs value2
x = [row['value1'] for row in data]
y = [row['value2'] for row in data]
plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.5, color='green')
plt.title('Scatter Plot of value1 vs value2')
plt.xlabel('value1')
plt.ylabel('value2')
plt.grid(True)
plt.show()


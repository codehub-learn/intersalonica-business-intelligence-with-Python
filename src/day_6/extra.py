"""Create a pie chart of revenue share per product using data/sales.csv

Saves the image to output/exports_pie.png and prints the path.
"""
import csv
import os
from matplotlib import pyplot as plt


def main():
	# resolve paths
	base = os.path.dirname(__file__)
	data_path = os.path.normpath(os.path.join(base, "..", "..", "data", "sales.csv"))
	out_dir = os.path.normpath(os.path.join(base, "..", "..", "output"))
	out_path = os.path.join(out_dir, "exports_pie.png")

	# read data
	if not os.path.exists(data_path):
		print(f"Data file not found: {data_path}")
		return

	products = []
	revenues = []
	with open(data_path, newline='', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			try:
				rev = float(row.get('Revenue', 0) or 0)
			except ValueError:
				rev = 0.0
			prod = row.get('Product') or 'Unknown'
			products.append(prod)
			revenues.append(rev)

	if not products or sum(revenues) == 0:
		print('No revenue data found or all revenues are zero. Nothing to plot.')
		return

	# ensure output directory exists
	os.makedirs(out_dir, exist_ok=True)

	# create pie chart
	plt.figure(figsize=(8, 6))
	wedges, texts, autotexts = plt.pie(
		revenues,
		labels=products,
		autopct=lambda pct: _autopct(pct, revenues),
		startangle=140,
		textprops={'fontsize': 10}
	)
	plt.title('Revenue Share by Product')
	# make sure pie is drawn as a circle
	plt.axis('equal')

	plt.tight_layout()
	plt.savefig(out_path, dpi=150)
	plt.close()

	print(f'Pie chart saved to: {out_path}')


def _autopct(pct, allvals):
	"""Return absolute value and percentage for autopct label."""
	total = sum(allvals)
	val = int(round(pct * total / 100.0))
	return f"{pct:.1f}%\n({val})"


if __name__ == '__main__':
	main()

   
 

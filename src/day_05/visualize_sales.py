"""
Create an influential visualization using the transactions data.
Saves a combined bar + donut chart to the repository `output/` folder.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


# --- data (copied from tellStory.py) ---------------------------------
transactions = [
    {"txn_id": 1, "customer": "Alice", "amount": 120, "region": "North"},
    {"txn_id": 2, "customer": "Bob", "amount": 200, "region": "South"},
    {"txn_id": 3, "customer": "Alice", "amount": 150, "region": "North"},
    {"txn_id": 4, "customer": "Alice", "amount": 0, "region": "North"},
]


def prepare_aggregates(transactions):
    sales_by_customer = {}
    sales_by_region = {}
    for t in transactions:
        sales_by_customer[t["customer"]] = sales_by_customer.get(t["customer"], 0) + t["amount"]
        sales_by_region[t["region"]] = sales_by_region.get(t["region"], 0) + t["amount"]
    # sort customers descending
    cust_sorted = sorted(sales_by_customer.items(), key=lambda x: x[1], reverse=True)
    customers, cust_amounts = zip(*cust_sorted)
    regions = list(sales_by_region.keys())
    region_amounts = list(sales_by_region.values())
    return list(customers), list(cust_amounts), regions, region_amounts


def create_visualization(transactions, out_path: Path):
    sns.set(style="whitegrid")
    customers, cust_amounts, regions, region_amounts = prepare_aggregates(transactions)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [2, 1]})

    # Bar chart: Sales by customer
    ax = axes[0]
    palette = sns.color_palette("Blues_d", len(customers))
    sns.barplot(x=cust_amounts, y=customers, palette=palette, ax=ax)
    ax.set_title("Total Sales by Customer")
    ax.set_xlabel("Total Sales (currency units)")
    ax.set_ylabel("")
    # annotate bars with values
    for i, v in enumerate(cust_amounts):
        ax.text(v + max(cust_amounts) * 0.01, i, f"{v}", va="center")

    # Highlight zero or low contributors
    for i, v in enumerate(cust_amounts):
        if v == 0:
            ax.patches[i].set_edgecolor('red')
            ax.patches[i].set_linewidth(2)

    # Donut chart: Sales by region
    ax2 = axes[1]
    wedges, texts, autotexts = ax2.pie(
        region_amounts,
        labels=regions,
        autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*sum(region_amounts)))})",
        startangle=140,
        colors=sns.color_palette("pastel")
    )
    # draw circle for donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax2.set_title("Sales Distribution by Region")

    # overall subtitle with top customer
    total_sales = sum(t["amount"] for t in transactions)
    top_customer = customers[0] if customers else "-"
    top_amount = cust_amounts[0] if cust_amounts else 0
    fig.suptitle(f"Key insight: {top_customer} is top customer with {top_amount} of {total_sales} total sales", fontsize=12)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches='tight', dpi=150)
    print(f"Visualization saved to: {out_path}")


if __name__ == "__main__":
    out_file = Path(__file__).resolve().parents[1] / "output" / "sales_insight.png"
    create_visualization(transactions, out_file)

"""
Marketing Funnel — Conversion Drop-off Sankey Diagram

"""

import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=["Website Visit", "Add to Cart", "Checkout", "Purchase"],
        pad=20,
        thickness=20
    ),
    link=dict(
        source=[0, 1, 2],
        target=[1, 2, 3],
        value=[10000, 4500, 2200]
    )
)])

fig.update_layout(title_text="Marketing Funnel Conversion Flow")
fig.show()

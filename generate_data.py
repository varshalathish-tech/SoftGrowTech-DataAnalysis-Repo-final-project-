import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Config ----
start_date = "2025-01-01"
end_date = "2025-12-31"
dates = pd.date_range(start_date, end_date, freq="D")

regions = ["North", "South", "East", "West"]
region_weights = [0.30, 0.22, 0.26, 0.22]

categories = ["Electronics", "Apparel", "Home & Kitchen", "Beauty", "Sports & Outdoors"]
category_base_price = {
    "Electronics": 180,
    "Apparel": 45,
    "Home & Kitchen": 65,
    "Beauty": 28,
    "Sports & Outdoors": 55,
}
category_margin = {
    "Electronics": 0.18,
    "Apparel": 0.35,
    "Home & Kitchen": 0.28,
    "Beauty": 0.42,
    "Sports & Outdoors": 0.30,
}
category_weights = [0.28, 0.24, 0.20, 0.16, 0.12]

segments = ["New Customer", "Returning Customer", "VIP"]
segment_weights = [0.42, 0.40, 0.18]

rows = []
order_id = 100000

for d in dates:
    # seasonality: more orders in Nov-Dec (holiday), dip in Feb, summer bump for Sports
    month = d.month
    weekday = d.weekday()

    base_orders = 28
    if month in (11, 12):
        base_orders *= 1.9
    elif month == 2:
        base_orders *= 0.75
    elif month in (6, 7):
        base_orders *= 1.15

    # weekends slightly busier for retail
    if weekday >= 5:
        base_orders *= 1.2

    n_orders = np.random.poisson(base_orders)

    for _ in range(n_orders):
        order_id += 1
        region = np.random.choice(regions, p=region_weights)
        category = np.random.choice(categories, p=category_weights)

        # Sports & Outdoors gets a summer boost
        if category == "Sports & Outdoors" and month in (5, 6, 7, 8):
            qty = np.random.randint(1, 4)
        else:
            qty = np.random.randint(1, 3)

        base_price = category_base_price[category]
        price = max(5, np.random.normal(base_price, base_price * 0.25))
        sales = round(price * qty, 2)
        margin = category_margin[category] + np.random.normal(0, 0.03)
        margin = min(max(margin, 0.05), 0.55)
        profit = round(sales * margin, 2)
        segment = np.random.choice(segments, p=segment_weights)

        rows.append({
            "OrderID": order_id,
            "Date": d.strftime("%Y-%m-%d"),
            "Region": region,
            "Category": category,
            "Quantity": qty,
            "Sales": sales,
            "Profit": profit,
            "CustomerSegment": segment,
        })

df = pd.DataFrame(rows)
df.to_csv("ecommerce_sales_2025.csv", index=False)
print(f"Rows generated: {len(df)}")
print(df.head())
print(df["Sales"].sum(), df["Profit"].sum())

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json

plt.rcParams["font.family"] = "DejaVu Sans"

df = pd.read_csv("ecommerce_sales_2025.csv", parse_dates=["Date"])
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
df["MonthName"] = df["Date"].dt.strftime("%b")

COLOR_MAIN = "#2563EB"
COLOR_ACCENT = "#14B8A6"
PALETTE = ["#2563EB", "#14B8A6", "#F59E0B", "#EF4444", "#8B5CF6"]

insights = {}

# ---------------- 1. Monthly revenue trend ----------------
monthly = df.groupby("Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("OrderID", "count")).reset_index()

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly["Month"], monthly["Sales"], marker="o", color=COLOR_MAIN, linewidth=2.5, label="Revenue")
ax.fill_between(monthly["Month"], monthly["Sales"], color=COLOR_MAIN, alpha=0.08)
ax.set_title("Monthly Revenue Trend (2025)", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig("chart_monthly_trend.png", dpi=160)
plt.close()

peak_month = monthly.loc[monthly["Sales"].idxmax()]
low_month = monthly.loc[monthly["Sales"].idxmin()]
insights["peak_month"] = peak_month["Month"].strftime("%B")
insights["peak_month_sales"] = round(peak_month["Sales"], 2)
insights["low_month"] = low_month["Month"].strftime("%B")
insights["low_month_sales"] = round(low_month["Sales"], 2)
q4_sales = monthly[monthly["Month"].dt.month.isin([10, 11, 12])]["Sales"].sum()
h1_avg = monthly[monthly["Month"].dt.month <= 6]["Sales"].mean()
insights["q4_share_pct"] = round(100 * q4_sales / monthly["Sales"].sum(), 1)

# ---------------- 2. Category performance ----------------
cat = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("OrderID", "count")).reset_index()
cat["MarginPct"] = round(100 * cat["Profit"] / cat["Sales"], 1)
cat = cat.sort_values("Sales", ascending=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(cat["Category"], cat["Sales"], color=PALETTE)
ax.set_title("Revenue by Product Category", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
for b, v in zip(bars, cat["Sales"]):
    ax.text(b.get_x() + b.get_width()/2, v + 5000, f"${v/1000:.0f}K", ha="center", fontsize=9)
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig("chart_category_revenue.png", dpi=160)
plt.close()

top_cat = cat.iloc[0]
best_margin_cat = cat.loc[cat["MarginPct"].idxmax()]
insights["top_category"] = top_cat["Category"]
insights["top_category_sales"] = round(top_cat["Sales"], 2)
insights["top_category_share_pct"] = round(100 * top_cat["Sales"] / cat["Sales"].sum(), 1)
insights["best_margin_category"] = best_margin_cat["Category"]
insights["best_margin_pct"] = best_margin_cat["MarginPct"]

# ---------------- 3. Regional performance ----------------
reg = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("OrderID", "count")).reset_index()
reg["AvgOrderValue"] = round(reg["Sales"] / reg["Orders"], 2)
reg = reg.sort_values("Sales", ascending=False)

fig, ax = plt.subplots(figsize=(6.2, 6.2))
wedges, texts, autotexts = ax.pie(
    reg["Sales"], labels=reg["Region"], autopct="%1.1f%%", startangle=90,
    colors=PALETTE, wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 11}
)
ax.set_title("Revenue Share by Region", fontsize=13, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig("chart_region_share.png", dpi=160)
plt.close()

top_region = reg.iloc[0]
insights["top_region"] = top_region["Region"]
insights["top_region_share_pct"] = round(100 * top_region["Sales"] / reg["Sales"].sum(), 1)
insights["top_region_aov"] = top_region["AvgOrderValue"]

# ---------------- 4. Customer segment analysis ----------------
seg = df.groupby("CustomerSegment").agg(Sales=("Sales", "sum"), Orders=("OrderID", "count")).reset_index()
seg["AvgOrderValue"] = round(seg["Sales"] / seg["Orders"], 2)
seg = seg.sort_values("Sales", ascending=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
x = range(len(seg))
ax.bar([i - 0.2 for i in x], seg["Orders"], width=0.4, label="Orders", color=COLOR_MAIN)
ax2 = ax.twinx()
ax2.bar([i + 0.2 for i in x], seg["AvgOrderValue"], width=0.4, label="Avg Order Value ($)", color=COLOR_ACCENT)
ax.set_xticks(list(x))
ax.set_xticklabels(seg["CustomerSegment"])
ax.set_ylabel("Number of Orders")
ax2.set_ylabel("Avg Order Value ($)")
ax.set_title("Orders vs. Average Order Value by Customer Segment", fontsize=13, fontweight="bold", pad=12)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=9, frameon=False)
ax.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
plt.tight_layout()
plt.savefig("chart_segment_analysis.png", dpi=160)
plt.close()

vip = seg[seg["CustomerSegment"] == "VIP"].iloc[0]
newc = seg[seg["CustomerSegment"] == "New Customer"].iloc[0]
insights["vip_aov"] = vip["AvgOrderValue"]
insights["new_aov"] = newc["AvgOrderValue"]
insights["vip_aov_premium_pct"] = round(100 * (vip["AvgOrderValue"] - newc["AvgOrderValue"]) / newc["AvgOrderValue"], 1)
insights["vip_share_of_orders_pct"] = round(100 * vip["Orders"] / seg["Orders"].sum(), 1)

# ---------------- Totals ----------------
insights["total_sales"] = round(df["Sales"].sum(), 2)
insights["total_profit"] = round(df["Profit"].sum(), 2)
insights["total_orders"] = int(df["OrderID"].nunique())
insights["overall_margin_pct"] = round(100 * df["Profit"].sum() / df["Sales"].sum(), 1)
insights["avg_order_value"] = round(df["Sales"].sum() / df["OrderID"].nunique(), 2)

with open("insights.json", "w") as f:
    json.dump(insights, f, indent=2, default=str)

print(json.dumps(insights, indent=2, default=str))
print("\nCategory table:\n", cat)
print("\nRegion table:\n", reg)
print("\nSegment table:\n", seg)

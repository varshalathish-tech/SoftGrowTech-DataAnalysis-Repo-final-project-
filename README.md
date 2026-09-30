# Business Data Analysis Project — E-Commerce Sales (FY2025)

**Domain:** Data Analysis
**Submitted for:** SoftGrowTech Final Project (Project 1 — Business Data Analysis Project)

## Overview
This project analyzes one year of e-commerce sales data (12,534 orders) across
4 regions, 5 product categories, and 3 customer segments to uncover revenue
patterns, category/regional performance, and customer behavior trends.

## Project Structure
```
├── generate_data.py     # Generates the synthetic e-commerce dataset
├── analyze.py           # Runs the analysis and produces all charts + insights.json
├── data/
│   ├── ecommerce_sales_2025.csv   # Raw dataset (12,534 orders)
│   └── insights.json              # Key computed metrics/insights
├── charts/
│   ├── chart_monthly_trend.png
│   ├── chart_category_revenue.png
│   ├── chart_region_share.png
│   └── chart_segment_analysis.png
└── README.md
```

## How to Run
```bash
pip install pandas numpy matplotlib
python generate_data.py   # creates data/ecommerce_sales_2025.csv
python analyze.py         # creates charts/ and data/insights.json
```

## Key Findings
- **Total Revenue:** $1,607,545 | **Total Profit:** $386,754 | **Orders:** 12,534
- Q4 (Oct–Dec) drove **33.8%** of annual revenue — a strong holiday effect.
- **Electronics** leads revenue (57.7% share) but has the thinnest margin (18.0%).
- **Beauty** has the best margin (42.0%) despite lower revenue.
- **North** region leads with 30.7% of revenue; the other three regions are
  fairly evenly split (21–26%).
- Average order value is consistent (~$127–$129) across New, Returning, and
  VIP customer segments — loyalty value comes from repeat purchases, not
  bigger baskets.

Full written report with charts and recommendations: see the submitted
`FullName_DataAnalysis.docx` document.

## Author
_Add your name here before submitting._

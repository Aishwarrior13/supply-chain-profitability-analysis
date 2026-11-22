# Supply Chain Profitability Performance Analysis

**Customer, Product, and Profitability Performance Analysis in Supply Chain Operations**

An end-to-end analytics project using the APL Logistics dataset to examine financial performance, customer contribution, product profitability, and discount patterns. The project combines Python-based analysis with an interactive Streamlit dashboard.

## Live Dashboard

[Open the Supply Chain Profitability Dashboard](https://supply-chain-profitability-analysis-aishwarrior.streamlit.app/)

## Project Objectives

- Measure gross revenue, net revenue, discounts, profit, and profitability margins.
- Identify customer groups and individual customers contributing most to profit.
- Compare product and category performance using revenue and profit margins.
- Examine profitability and loss-making transaction rates across discount bands.
- Explore hypothetical discount changes through a sensitivity analysis.

## Dashboard Modules

1. **Revenue & Profit Overview** — gross and net revenue, discounts, profit, margin measures, transaction profitability, and market-level performance.
2. **Customer Value Dashboard** — customer-level revenue, profit, transaction frequency, Customer Value Index (CVI), value tiers, and profit rankings.
3. **Product & Category Performance** — category results, top products by net revenue, and products with above-median revenue but below-median profit margin.
4. **Discount Impact Analyzer** — profitability by discount band, loss-making transaction rates, and a discount sensitivity scenario.

## Key Findings

The following figures are based on the analyzed dataset before dashboard filtering:

| Metric | Result |
|---|---:|
| Order-item records | 180,519 |
| Unique customers | 20,652 |
| Products | 118 |
| Categories | 50 |
| Markets | 5 |
| Gross revenue (Sales) | 36,784,734.31 |
| Net revenue (Order Item Total) | 33,054,402.04 |
| Total recorded profit | 3,966,902.97 |
| Total discounts | 3,730,378.40 |
| Margin on gross revenue | 10.78% |
| Margin on net revenue | 12.00% |
| Loss-making records | 33,784 |

### Customer profitability

- The top 10% of customers by profit generated approximately **49.10%** of total recorded profit.
- Approximately **20.34%** of customers generated **80.01%** of total recorded profit.
- Customer Value Index (CVI) combines normalized net revenue, total profit, and transaction frequency with equal weights. It is a relative ranking measure, not customer lifetime value; actual customer profit should be reviewed separately.

### Product and discount performance

- Products classified as high-revenue, low-margin are above the product-level median net revenue and below the median profit margin. “Low margin” is relative to this dataset and does not necessarily mean a product is loss-making.
- Discount-band margins are not monotonic, and loss rates are broadly similar across bands. The observed comparisons do not establish that discounts cause lower profitability.
- The what-if analysis is a sensitivity scenario that assumes transaction volume, product mix, and costs remain unchanged. It is not a forecast.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Streamlit
- GitHub
- Streamlit Community Cloud

## Repository Contents

- supply_chain_profitability_dashboard.py — Streamlit dashboard application.
- APL_Logistics_Cleaned-ZIP.zip — compressed cleaned dataset used by the dashboard.
- requirements.txt — Python package dependencies.

## How to Run Locally

1. Clone this repository.
2. Install the dependencies:
   pip install -r requirements.txt
3. Run the dashboard:
   streamlit run supply_chain_profitability_dashboard.py

## Data and Methodology Notes

- The dataset contains 180,519 order-item records. Because a usable order timestamp and unique Order ID were not available, the analysis does not claim monthly or weekly trends or distinct order counts.
- Sales is treated as gross revenue; Order Item Total is treated as net revenue after discounts. The two are reported separately.
- No separate shipping-cost field was available, so shipping cost cannot be isolated as a driver of margin.
- Negative-profit and zero-profit records are retained in the analysis.
- The dataset's currency was not independently confirmed; financial values are shown in the dataset's recorded units.
- Customer CVI is a relative index, not customer lifetime value.
- Discount comparisons are descriptive, not causal. The what-if analysis is assumption-based and should not be interpreted as a forecast.

## Project Scope

This project focuses on profitability performance across customers, products, categories, discount bands, and markets. It does not estimate delivery performance, shipping cost, or time-based demand trends where the required fields are unavailable.

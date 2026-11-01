# Enterprise Analytics Architecture

A Power BI enterprise analytics dashboard that combines three business intelligence domains into one executive reporting environment.

## Business context

This project unifies:
- E-commerce sales performance
- Competitor pricing analysis
- Predictive churn risk monitoring

## Data model

- Dim_Customers
- Dim_Products
- Dim_Calendar
- Fact_Sales
- Fact_Competitor_Scraping
- Fact_Customer_Churn_ML

## Key relationships

- Dim_Customers -> Fact_Sales
- Dim_Customers -> Fact_Customer_Churn_ML
- Dim_Products -> Fact_Sales
- Dim_Products -> Fact_Competitor_Scraping
- Dim_Calendar -> Fact_Sales
- Dim_Calendar -> Fact_Competitor_Scraping
- Dim_Calendar -> Fact_Customer_Churn_ML

## DAX highlights

```DAX
Total Revenue =
SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price])

Total Cost =
SUMX(
    Fact_Sales,
    Fact_Sales[Quantity] * RELATED(Dim_Products[Unit_Cost])
)

Total Profit = [Total Revenue] - [Total Cost]

Profit Margin % =
DIVIDE([Total Profit], [Total Revenue], 0)

Price Gap % =
DIVIDE(
    [Avg Internal Price] - [Avg Competitor Price],
    [Avg Competitor Price],
    0
)
```

## Dashboard structure

1. C-Suite Financial Overview
2. Competitive Market Intelligence
3. Proactive Customer Retention CRM

## Generate sample data

```bash
python scripts/generate_sample_data.py
```

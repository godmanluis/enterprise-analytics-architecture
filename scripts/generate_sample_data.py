import pandas as pd
import numpy as np

np.random.seed(42)

customer_count = 250
customer_ids = [f"CUST-{i:04d}" for i in range(1, customer_count + 1)]
segments = np.random.choice(["Retail", "SMB", "Enterprise"], size=customer_count, p=[0.5, 0.35, 0.15])
regions = np.random.choice(["North", "South", "East", "West", "Central"], size=customer_count)
acquisition_dates = pd.date_range("2021-01-01", "2024-12-31").to_series().sample(customer_count, replace=True).values
monthly_charges = np.random.uniform(25, 450, customer_count)

customers = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Customer_Name": [f"Customer {i}" for i in range(1, customer_count + 1)],
    "Segment": segments,
    "Region": regions,
    "Acquisition_Date": acquisition_dates,
    "Monthly_Charges": monthly_charges.round(2),
})

products = [
    ("P1001", "Wireless Mouse", "Electronics", "Logitech", "TechHub", 18.5),
    ("P1002", "Mechanical Keyboard", "Electronics", "Corsair", "TechHub", 42.0),
    ("P1003", "4K Monitor", "Electronics", "Dell", "DisplayCo", 210.0),
    ("P1004", "Office Chair", "Furniture", "Herman Miller", "FurniMax", 120.0),
    ("P1005", "Standing Desk", "Furniture", "Steelcase", "FurniMax", 285.0),
    ("P1006", "Laptop Stand", "Accessories", "Anker", "TechHub", 22.0),
    ("P1007", "USB-C Hub", "Accessories", "Belkin", "TechHub", 35.0),
    ("P1008", "Noise Cancelling Headphones", "Electronics", "Sony", "AudioSource", 95.0),
    ("P1009", "Desk Lamp", "Furniture", "Philips", "LightWorks", 40.0),
    ("P1010", "Ergonomic Backpack", "Accessories", "North Face", "TravelGear", 55.0),
    ("P1011", "Webcam", "Electronics", "Logitech", "TechHub", 68.0),
    ("P1012", "Bluetooth Speaker", "Electronics", "JBL", "AudioSource", 48.0),
]

dim_products = pd.DataFrame(products, columns=[
    "Product_ID", "Product_Name", "Category", "Brand", "Supplier", "Unit_Cost"
])

start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2025-12-31")
calendar = pd.date_range(start=start_date, end=end_date, freq="D")

dim_calendar = pd.DataFrame({
    "Date": calendar,
    "Month": calendar.month,
    "Month_Year": calendar.strftime("%Y-%m"),
    "Quarter": (calendar.month - 1) // 3 + 1,
    "Year": calendar.year,
})

sales_rows = []
for _ in range(6000):
    date_val = pd.to_datetime(np.random.choice(calendar))
    customer_id = np.random.choice(customer_ids)
    product = np.random.choice(dim_products.to_dict("records"))
    quantity = np.random.randint(1, 9)
    unit_price = round(float(product["Unit_Cost"]) * np.random.uniform(1.25, 2.8), 2)

    sales_rows.append({
        "Sales_ID": f"SALE-{len(sales_rows) + 1:06d}",
        "Date": date_val,
        "Customer_ID": customer_id,
        "Product_ID": product["Product_ID"],
        "Quantity": quantity,
        "Unit_Price": unit_price,
    })

fact_sales = pd.DataFrame(sales_rows)
fact_sales["Revenue"] = (fact_sales["Quantity"] * fact_sales["Unit_Price"]).round(2)

scrape_rows = []
for _, row in dim_products.iterrows():
    for date_val in pd.date_range("2023-01-01", "2025-12-31", freq="D"):
        competitor_name = np.random.choice(["Amazon", "Walmart", "Target", "eBay", "BestBuy"])
        competitor_price = round(float(row["Unit_Cost"]) * np.random.uniform(1.05, 1.65), 2)
        scrape_rows.append({
            "Scrape_ID": f"SCRAPE-{len(scrape_rows) + 1:06d}",
            "Date": date_val,
            "Product_ID": row["Product_ID"],
            "Competitor_Name": competitor_name,
            "Competitor_Price": competitor_price,
        })

fact_competitor = pd.DataFrame(scrape_rows)

churn_rows = []
months = pd.date_range("2023-01-01", "2025-12-01", freq="MS")
for customer in customers.itertuples():
    for month_start in months:
        monthly_charge = round(float(customer.Monthly_Charges) * np.random.uniform(0.85, 1.25), 2)
        support_tickets = np.random.randint(0, 9)
        risk_probability = np.clip(
            (support_tickets * 7) + (100 - (monthly_charge / 5)) * 0.2 + np.random.uniform(-10, 15),
            0,
            100,
        )
        churn_rows.append({
            "Customer_ID": customer.Customer_ID,
            "Date": month_start,
            "Churn_Risk_Probability_%": round(float(risk_probability), 2),
            "Support_Tickets_Raised": support_tickets,
            "Monthly_Charges": monthly_charge,
        })

fact_churn = pd.DataFrame(churn_rows)

customers.to_csv("Dim_Customers.csv", index=False)
dim_products.to_csv("Dim_Products.csv", index=False)
dim_calendar.to_csv("Dim_Calendar.csv", index=False)
fact_sales.to_csv("Fact_Sales.csv", index=False)
fact_competitor.to_csv("Fact_Competitor_Scraping.csv", index=False)
fact_churn.to_csv("Fact_Customer_Churn_ML.csv", index=False)

print("Sample files generated successfully.")

# sales_analysis.py
import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\LENOVO\Downloads\SalesDashboard\superstore_data.csv", encoding="ISO-8859-1")

# Basic Cleaning
# 1. Handle missing values
df.dropna(inplace=True)

# 2. Remove duplicates
df.drop_duplicates(inplace=True)

# 3. Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 4. Create time-based columns
df['Month'] = df['Order Date'].dt.month_name()
df['Quarter'] = df['Order Date'].dt.quarter

# 5. Calculate Profit Margin
df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100

# Save cleaned data (optional)
df.to_csv("cleaned_superstore_data.csv", index=False)

df.head()

# Total Sales and Profit
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
avg_profit_margin = df['Profit Margin (%)'].mean()

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Average Profit Margin: {avg_profit_margin:.2f}%")

# Sales by Region
sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print("\nSales by Region:")
print(sales_by_region)

# Top 5 Products
top_products = df.groupby('Product Name')['Sales'].sum().nlargest(5)
print("\nTop 5 Products by Sales:")
print(top_products)

import matplotlib.pyplot as plt
import seaborn as sns

# Monthly Sales Trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Month', y='Sales', estimator='sum', errorbar=None)
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.show()

# Sales by Region
plt.figure(figsize=(10, 6))
sns.barplot(x=sales_by_region.index, y=sales_by_region.values)
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales ($)")
plt.show()




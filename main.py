import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

print(df.head())
print("\nShape of Dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nInformation:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())

# ==========================================
# DATA CLEANING
# ==========================================

# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# Remove extra spaces from text columns
df["Division"] = df["Division"].str.strip()
df["Product Name"] = df["Product Name"].str.strip()

# Remove rows with invalid values (if any)
df = df[df["Sales"] > 0]
df = df[df["Cost"] >= 0]
df = df[df["Units"] > 0]

print("\nData Cleaning Completed Successfully!")

# ==========================================
# KPI CALCULATIONS
# ==========================================

# Gross Margin %
df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

# Profit Per Unit
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# Revenue Contribution
total_sales = df["Sales"].sum()
df["Revenue Contribution (%)"] = (df["Sales"] / total_sales) * 100

# Profit Contribution
total_profit = df["Gross Profit"].sum()
df["Profit Contribution (%)"] = (df["Gross Profit"] / total_profit) * 100

print("\nKPI Columns Added Successfully!\n")

print(df[[
    "Product Name",
    "Sales",
    "Gross Profit",
    "Gross Margin %",
    "Profit per Unit",
    "Revenue Contribution (%)",
    "Profit Contribution (%)"
]].head())

# ==========================================
# SAVE CLEAN DATASET
# ==========================================

df.to_csv("Cleaned_Nassau_Candy.csv", index=False)

print("\nCleaned dataset saved as 'Cleaned_Nassau_Candy.csv'")

print("\nFinal Shape:", df.shape)
print("\nColumns:")
print(df.columns)

# ==========================================
# SALES DISTRIBUTION
# ==========================================

plt.figure(figsize=(8,5))

plt.hist(df["Sales"], bins=30)

plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.savefig("charts/sales_distribution.png")
plt.show()

# ==========================================
# GROSS PROFIT DISTRIBUTION
# ==========================================

plt.figure(figsize=(8,5))

plt.hist(df["Gross Profit"], bins=30)

plt.title("Gross Profit Distribution")
plt.xlabel("Gross Profit")
plt.ylabel("Frequency")

plt.savefig("charts/profit_distribution.png")
plt.show()

# ==========================================
# SALES BY DIVISION
# ==========================================

division_sales = df.groupby("Division")["Sales"].sum()

plt.figure(figsize=(7,5))

division_sales.plot(kind="bar")

plt.title("Sales by Division")
plt.xlabel("Division")
plt.ylabel("Total Sales")

plt.savefig("charts/sales_by_division.png")
plt.show()

# ==========================================
# PROFIT BY DIVISION
# ==========================================

division_profit = df.groupby("Division")["Gross Profit"].sum()

plt.figure(figsize=(7,5))

division_profit.plot(kind="bar")

plt.title("Profit by Division")
plt.xlabel("Division")
plt.ylabel("Gross Profit")

plt.savefig("charts/profit_by_division.png")
plt.show()

# ==========================================
# TOP PRODUCTS
# ==========================================

top_sales = df.groupby("Product Name")["Sales"].sum()

top_sales = top_sales.sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))

top_sales.plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")

plt.savefig("charts/top10_sales_products.png")
plt.show()

# ==========================================
# TOP PROFIT PRODUCTS
# ==========================================

top_profit = df.groupby("Product Name")["Gross Profit"].sum()

top_profit = top_profit.sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))

top_profit.plot(kind="barh")

plt.title("Top 10 Products by Gross Profit")
plt.xlabel("Gross Profit")

plt.savefig("charts/top10_profit_products.png")
plt.show()

# ==========================================
# COST VS SALES
# ==========================================

plt.figure(figsize=(8,6))

plt.scatter(df["Cost"], df["Sales"], alpha=0.5)

plt.title("Cost vs Sales")
plt.xlabel("Cost")
plt.ylabel("Sales")

plt.savefig("charts/cost_vs_sales.png")
plt.show()

# ==========================================
# PRODUCT ANALYSIS
# ==========================================

product = df.groupby("Product Name").agg({
    "Sales":"sum",
    "Gross Profit":"sum",
    "Units":"sum"
})

product["Gross Margin %"] = (
    product["Gross Profit"] /
    product["Sales"]
) * 100

product["Profit per Unit"] = (
    product["Gross Profit"] /
    product["Units"]
)

product = product.sort_values(
    by="Gross Profit",
    ascending=False
)

print("\nTop 10 Profitable Products\n")
print(product.head(10))

product.to_csv("Product_Analysis.csv")

# ==========================================
# PRODUCT PROFITABILITY ANALYSIS
# ==========================================

product = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Gross Profit": "sum",
    "Units": "sum",
    "Cost": "sum"
}).reset_index()

product["Gross Margin %"] = (
    product["Gross Profit"] / product["Sales"]
) * 100

product["Profit per Unit"] = (
    product["Gross Profit"] / product["Units"]
)

print("\n========== PRODUCT PROFITABILITY ==========\n")
print(product)

top_profit = product.sort_values(
    by="Gross Profit",
    ascending=False
)

print("\nTop 10 Most Profitable Products\n")

print(
top_profit[
[
"Product Name",
"Sales",
"Gross Profit",
"Gross Margin %"
]
].head(10)
)

top_margin = product.sort_values(
    by="Gross Margin %",
    ascending=False
)

print("\nTop 10 Highest Margin Products\n")

print(
top_margin[
[
"Product Name",
"Gross Margin %"
]
].head(10)
)

average_sales = product["Sales"].mean()
average_margin = product["Gross Margin %"].mean()

high_sales_low_margin = product[
(product["Sales"] > average_sales) &
(product["Gross Margin %"] < average_margin)
]

print("\nHigh Sales but Low Margin Products\n")
print(high_sales_low_margin)

average_profit = product["Gross Profit"].mean()

low_products = product[
(product["Sales"] < average_sales) &
(product["Gross Profit"] < average_profit)
]

print("\nLow Sales & Low Profit Products\n")

print(low_products)

product.to_csv(
"output/Product_Profitability.csv",
index=False
)

division = df.groupby("Division").agg({
    "Sales":"sum",
    "Gross Profit":"sum",
    "Cost":"sum",
    "Units":"sum"
}).reset_index()

division["Gross Margin %"] = (
division["Gross Profit"]/
division["Sales"]
)*100

print("\n========== DIVISION PERFORMANCE ==========\n")
print(division)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.bar(
division["Division"],
division["Sales"],
label="Sales"
)

plt.bar(
division["Division"],
division["Gross Profit"],
label="Profit"
)

plt.legend()

plt.title("Revenue vs Profit by Division")

plt.savefig("charts/revenue_vs_profit.png")

plt.show()

division = division.sort_values(
by="Gross Profit",
ascending=False
)

print("\nDivision Ranking\n")

print(division)

# ==========================================
# PARETO ANALYSIS
# ==========================================

pareto = product.sort_values(
    by="Gross Profit",
    ascending=False
).copy()

pareto["Cumulative Profit"] = pareto["Gross Profit"].cumsum()

total_profit = pareto["Gross Profit"].sum()

pareto["Cumulative %"] = (
    pareto["Cumulative Profit"] / total_profit
) * 100

print("\n========== PARETO ANALYSIS ==========\n")
print(pareto[[
    "Product Name",
    "Gross Profit",
    "Cumulative Profit",
    "Cumulative %"
]])

plt.figure(figsize=(10,6))

plt.bar(
    pareto["Product Name"],
    pareto["Gross Profit"],
    label="Gross Profit"
)

plt.plot(
    pareto["Product Name"],
    pareto["Cumulative %"],
    color="red",
    marker="o",
    label="Cumulative %"
)

plt.axhline(80, color="green", linestyle="--", label="80%")

plt.xticks(rotation=90)

plt.title("Pareto Analysis of Product Profit")

plt.legend()

plt.tight_layout()

plt.savefig("charts/pareto_analysis.png")

plt.show()

pareto.to_csv(
    "output/Pareto_Analysis.csv",
    index=False
)

# ==========================================
# COST STRUCTURE
# ==========================================

plt.figure(figsize=(8,6))

plt.scatter(
    product["Cost"],
    product["Gross Margin %"]
)

plt.xlabel("Total Cost")

plt.ylabel("Gross Margin %")

plt.title("Cost vs Gross Margin")

plt.savefig("charts/cost_margin_analysis.png")

plt.show()

margin_risk = product[
    product["Gross Margin %"] < 30
]

print("\n========== MARGIN RISK PRODUCTS ==========\n")

print(margin_risk)

margin_risk.to_csv(
    "output/Margin_Risk_Products.csv",
    index=False
)

division["Profit Ratio"] = (
    division["Gross Profit"] /
    division["Sales"]
) * 100

division = division.sort_values(
    by="Profit Ratio",
    ascending=False
)

print("\n========== DIVISION EFFICIENCY ==========\n")

print(division)

plt.figure(figsize=(8,5))

plt.bar(
    division["Division"],
    division["Profit Ratio"]
)

plt.title("Division Profit Margin")

plt.ylabel("Margin %")

plt.savefig("charts/division_margin.png")

plt.show()

print("\n========== EXECUTIVE SUMMARY ==========\n")

print("Total Sales : $", round(df["Sales"].sum(),2))

print("Total Profit : $", round(df["Gross Profit"].sum(),2))

print("Average Margin :",
      round(df["Gross Margin %"].mean(),2),
      "%")

print("Number of Products :",
      df["Product Name"].nunique())

print("Number of Divisions :",
      df["Division"].nunique())

print("Best Product :",
      product.loc[
          product["Gross Profit"].idxmax(),
          "Product Name"
      ])

print("Best Division :",
      division.loc[
          division["Profit Ratio"].idxmax(),
          "Division"
      ])
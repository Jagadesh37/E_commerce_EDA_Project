# E-Commerce_EDA_Project
# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load dataset
df = pd.read_csv("EDA_Ecommerce_dataset.csv")
# Data Cleaning
df.columns = df.columns.str.strip().str.lower()
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df.drop_duplicates(inplace=True)
df.loc[df['price'] < 0, 'price'] = None
df['price'] = df['price'].fillna(df['price'].median())
# Handle missing review_score
if 'review_score' in df.columns:
    df['review_score'] = df['review_score'].fillna(df['review_score'].median())
df['revenue'] = df['price'] * df['quantity']
df['order_month'] = df['order_date'].dt.to_period("M").astype(str)
df['order_weekday'] = df['order_date'].dt.day_name()
print("Dataset after cleaning")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())
print("\nSummary Stats:\n", df.describe(include='all'))
print("\nTotal Revenue: ", df['revenue'].sum())
print("Total Orders: ", df['order_id'].nunique())
print("Unique Customers: ", df['customer_id'].nunique())
print("Average Order Value (AOV): ", df.groupby('order_id')['revenue'].sum().mean())
# Visualizations
sns.set(style="whitegrid", palette="muted")
plt.figure(figsize=(8,5))
sns.barplot(x="category", y="revenue", data=df, estimator=sum, errorbar=None)
plt.title("Revenue by Category")
plt.xticks(rotation=45)
plt.show()
# Orders by Payment Method
plt.figure(figsize=(7,5))
sns.countplot(x="payment_method", data=df)
plt.title("Orders by Payment Method")
plt.xticks(rotation=45)
plt.show()
# Monthly Revenue Trend
monthly_revenue = df.groupby("order_month")["revenue"].sum().reset_index()
plt.figure(figsize=(10,5))
plt.plot(monthly_revenue["order_month"], monthly_revenue["revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.show()
# Revenue by Weekday
weekday_revenue = df.groupby("order_weekday")["revenue"].sum().reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
plt.figure(figsize=(8,5))
sns.barplot(x="order_weekday", y="revenue", data=weekday_revenue, errorbar=None)
plt.title("Revenue by Weekday")
plt.show()
# Distribution of Review Scores
plt.figure(figsize=(7,5))
sns.countplot(x="review_score", data=df)
plt.title("Distribution of Review Scores")
plt.show()
# Correlation Heatmap
plt.figure(figsize=(7,5))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

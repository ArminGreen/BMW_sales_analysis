
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, "data", "bmw_global_sales_dataset.csv")

df = pd.read_csv(file_path)

st.title("BMW Sales Dashboard")
st.x = ("Year")
st.y = ("Units Sold")

st.write("Bar Chart: BMW Sales Over Time")
st.bar_chart(df.groupby("year")["units_sold"].sum())


st.write("Line Chart: BMW Sales Over Time")
st.line_chart(df.groupby("year")["units_sold"].sum())


st.write("Bar Chart: Countries with Highest Marketing Spend")
st.bar_chart(df.groupby("country")["marketing_spend_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(8))






# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="BMW Sales Dashboard",
    layout="centered"
)

st.title("BMW Global Sales Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df['revenue'] = df['units_sold'] * df['price_usd']
    return df

df = load_data()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].unique(),
    default=df['country'].unique()
)

selected_year = st.sidebar.slider(
    "Select Year Range",
    int(df['year'].min()),
    int(df['year'].max()),
    (int(df['year'].min()), int(df['year'].max()))
)

# Apply filters
filtered_df = df[
    (df['country'].isin(selected_country)) &
    (df['year'].between(selected_year[0], selected_year[1]))
]

# ---------------------------
# KPI METRICS
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,}")
col2.metric("Total Revenue ($)", f"{filtered_df['revenue'].sum():,.0f}")
col3.metric("Avg Price ($)", f"{filtered_df['price_usd'].mean():,.0f}")

# ---------------------------
# SALES OVER TIME
# ---------------------------
st.subheader("📈 Sales Over Time")

sales_trend = filtered_df.groupby('year')['units_sold'].sum()

fig1, ax1 = plt.subplots()
sales_trend.plot(ax=ax1)
ax1.set_ylabel("Units Sold")
st.pyplot(fig1)

# ---------------------------
# TOP COUNTRIES (DUAL AXIS)
# ---------------------------
st.subheader("🌍 Top Countries: Sales vs Dealerships")

dealerships = filtered_df.groupby("country")["dealership_count"].sum().sort_values(ascending=False).head(8)
units_sold = filtered_df.groupby("country")["units_sold"].sum().sort_values(ascending=False).head(8)

countries = dealerships.index.tolist()
x = np.arange(len(countries))
width = 0.4

fig2, ax1 = plt.subplots(figsize=(10,5))

bars1 = ax1.bar(x - width/2, dealerships.values, width,color="#FF4E08", label='Dealerships')

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, units_sold.values, width,color="#4751E9", label='Units Sold')

ax1.set_xticks(x)
ax1.set_xticklabels(countries, rotation=30)
ax1.set_ylabel("Dealerships")
ax2.set_ylabel("Units Sold")

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2)

st.pyplot(fig2)

# ---------------------------
# TOP MODELS
# ---------------------------
st.subheader("🚘 Top Selling Models")

top_models = filtered_df.groupby('model')['units_sold'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
top_models.plot(kind='bar', ax=ax3)
st.pyplot(fig3)

# ---------------------------
# CORRELATION HEATMAP
# ---------------------------
st.subheader("🔥 Correlation Heatmap")

fig4, ax4 = plt.subplots(figsize=(8,5))
sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, ax=ax4)
st.pyplot(fig4)

# ---------------------------
# EFFICIENCY ANALYSIS
# ---------------------------
st.subheader("⚡ Sales Efficiency (Units per Dealership)")

efficiency = (filtered_df.groupby('country')['units_sold'].sum() /
              filtered_df.groupby('country')['dealership_count'].sum()).sort_values(ascending=False).head(10)

fig5, ax5 = plt.subplots()
efficiency.plot(kind='bar', ax=ax5)
st.pyplot(fig5)
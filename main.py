import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

# Set page configuration
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# 1. Load data
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    datetime_columns = ["order_purchase_timestamp"] 
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])
    return df

all_df = load_data()

# 2. Sidebar - Filter Rentang Waktu
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") # Opsional: Logo
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan input tanggal
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# 3. Header
st.header('E-Commerce Data Analysis Dashboard :sparkles:')

# --- PERTANYAAN 1: REVENUE PER KATEGORI ---
st.subheader("Performa Pendapatan Berdasarkan Kategori Produk")

col1, col2 = st.columns(2)

with col1:
    # Top 5 Revenue
    category_revenue_df = main_df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index().head(5)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="price", y="product_category_name_english", data=category_revenue_df, palette="viridis", ax=ax)
    ax.set_title("5 Kategori Produk Teratas (Revenue)", fontsize=15)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    # Bottom 5 Revenue
    bottom_category_revenue_df = main_df.groupby("product_category_name_english").price.sum().sort_values(ascending=True).reset_index().head(5)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="price", y="product_category_name_english", data=bottom_category_revenue_df, palette="magma", ax=ax)
    ax.set_title("5 Kategori Produk Terendah (Revenue)", fontsize=15)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    st.pyplot(fig)

# --- PERTANYAAN 2: RFM ANALYSIS ---
st.subheader("Best Customer Based on RFM Parameters")

# Menyiapkan RFM Data
recent_date = all_df["order_purchase_timestamp"].max() + dt.timedelta(days=1)
rfm_df = main_df.groupby(by="customer_unique_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]

col_r, col_f, col_m = st.columns(3)

with col_r:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Avg Recency (days)", value=avg_recency)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette="Blues", ax=ax)
    ax.set_title("By Recency (days)", fontsize=12)
    ax.set_xticks([])
    st.pyplot(fig)

with col_f:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Avg Frequency", value=avg_frequency)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette="Greens", ax=ax)
    ax.set_title("By Frequency", fontsize=12)
    ax.set_xticks([])
    st.pyplot(fig)

with col_m:
    avg_monetary = f"R$ {rfm_df.monetary.mean():,.2f}"
    st.metric("Avg Monetary", value=avg_monetary)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette="Oranges", ax=ax)
    ax.set_title("By Monetary", fontsize=12)
    ax.set_xticks([])
    st.pyplot(fig)

st.caption('Copyright (c) Dwiyan Achmad Assidiqie 2026')

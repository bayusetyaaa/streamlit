import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
from babel.numbers import format_currency

sns.set(style='dark')

def create_mountly_df(df):
    all_df["dteday_x"] = pd.to_datetime(all_df["dteday_x"])
    latest_year = all_df["dteday_x"].dt.year.max()
    filtered_df = all_df[all_df["dteday_x"].dt.year == latest_year]

    mountly_df = filtered_df.resample(rule='ME', on='dteday_x').agg({
        "instant": "nunique",
        "cnt_x": "sum"
    })

    mountly_df.index = mountly_df.index.strftime('%B')
    mountly_df = mountly_df.reset_index()
    mountly_df.rename(
        columns={"dteday_x": "bulan"}, 
        inplace=True)
    
    return mountly_df

def create_byseason_df(df):
    byseason_df = all_df.groupby(by="season_x").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)

    return byseason_df

def create_byweathersit_df(df):
    byweathersit_df= all_df.groupby(by="weathersit_x").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byweathersit_df

def create_byhr_df(df):
    byhr_df = all_df.groupby(by="hr").instant.nunique().reset_index()
    byhr_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byhr_df

# Load cleaned data
all_df = pd.read_csv("all_data.csv")

# Filter data
min_date = all_df["dteday_x"].min()
max_date = all_df["dteday_x"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday_x"] >= str(start_date)) & 
                (all_df["dteday_x"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
mountly_df = create_mountly_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)
byhr_df = create_byhr_df(main_df)

# plot number of daily orders
st.header('Bike Shararing')
st.subheader('Penggunaan Sepeda Berdasarkan Musim dan Cuaca')

col1 = st.columns(2)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    mountly_df["bulan"],
    mountly_df["cnt_x"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# customer demographic
st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = sns.color_palette("viridis", len(byseason_df))

    sns.barplot(
        y="customer_count", 
        x="season_x",
        data=byseason_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Saeson", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="customer_count", 
        x="weathersit_x",
        data=byweathersit_df.sort_values(by="weathersit_x", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by weathersit", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="hr",
    data=byhr_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by hourrs", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.caption('Bayu : Copyright © Dicoding 2025')
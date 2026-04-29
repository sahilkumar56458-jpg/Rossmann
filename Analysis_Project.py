from PIL import Image
import pandas as pd
import numpy as np 
# import seaborn as sns 
import matplotlib.pyplot as plt 
import streamlit as st

st.set_page_config(page_title="Competitors Analysis", page_icon="📊", layout="wide",)

img = Image.open("logo_ross.png")
st.sidebar.image(img)

# ✅ CHANGE BACKGROUND COLOR
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: lavender;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ✅ CHANGE TEXT COLOR
st.markdown(
    """
    <style>
    h1, h2, h3, p, span, label {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ CHANGE BUTTON COLOR
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊Competitors Analysis")
st.markdown("<style>.block-container {padding-top: 2rem;}</style>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Home", "About company"])
col1, col2 = st.columns(2)

with tab1:
    st.subheader("We Analyzing the sales behalf Multiple factors")
    store = pd.read_csv("store.csv")
    train= pd.read_csv("train.csv")
    df = pd.merge(store,train,on="Store",how="left")
    print(df.head())

       # ------------------------ Sales by year ------------------------------------- 
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    # st.write(df.head())


    #------------------------ Filter by Year -------------------------------------
    year  = st.sidebar.multiselect("Pick your Year", df["Year"].unique())
    if not year:
        df2 = df.copy()
    else:
        df2 = df[df["Year"].isin(year)]

    # ------------------------Filter by month-------------------------------------
    month = st.sidebar.multiselect("Pick your month",df["Month"].unique())
    if not month:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Month"].isin(month)]
# -------------------Combine year and month filters-----------------------
if not year and not month:
    filtered_df = df
elif year and not month:
    filtered_df = df[df["Year"].isin(year)]
elif month and not year:
    filtered_df = df[df["Month"].isin(month)]
else:
    filtered_df = df[df["Year"].isin(year) & df["Month"].isin(month)]

# ✅ CHARTS START HERE (NO INDENT)
    with col1:
        sales_by_year = filtered_df.groupby("Year")["Sales"].mean()

        fig,ax=plt.subplots()
        plt.bar(sales_by_year.index.astype(str),sales_by_year.values)
        plt.title("Sales by Year")
        plt.ylabel("Sales")
        plt.xlabel("year")
        st.pyplot(fig)

#------------------------------------------------------------------------------------------------- 
    with col2:
        month_order = [
"January","February","March","April","May","June",
    "July","August","September","October","November","December"]
        sales_by_month = filtered_df.groupby("Month")["Sales"].mean().reindex(month_order)
        fig,ax=plt.subplots()
        plt.bar(sales_by_month.index.astype(str),sales_by_month.values)
        plt.title("Sales by Month")
        plt.ylabel("Sales")
        plt.xlabel("Month")
        st.pyplot(fig)

        # ------------------------Sales by competition distance-------------------------
    with col1:
        month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"]
        customers_by_month = filtered_df.groupby("Month")["Customers"].mean().reindex(month_order)
        fig,ax=plt.subplots()
        plt.bar(customers_by_month.index.astype(str),customers_by_month.values)
        plt.xlabel("Month")
        plt.ylabel("Customers")
        plt.xticks(rotation=90)
        plt.title("Average Customers by Month")
        st.pyplot(fig)

        # ---------------------------customer Type-------------------------
    with col2:
        min_dist = int(filtered_df["CompetitionDistance"].min())
        max_dist = int(filtered_df["CompetitionDistance"].max())
        dist_range = st.sidebar.slider(
        "Select Competition Distance Range",
        min_value=min_dist,
        max_value=max_dist,
        value=(min_dist, max_dist))
        temp_df = filtered_df[
    (filtered_df["CompetitionDistance"] >= dist_range[0]) & (filtered_df["CompetitionDistance"] <= dist_range[1])]
        temp_df = temp_df.dropna(subset=["CompetitionDistance"])
        sales_by_comp = (
        temp_df.groupby("CompetitionDistance")["Sales"]
        .mean()
        .sort_index())
        fig,ax=plt.subplots()
        plt.plot(sales_by_comp)
        plt.title("Sales by competition")
        plt.ylabel("Sales")
        plt.xlabel("Competition Distance")
        st.pyplot(fig)


        # ------------------------customers by Month------------------------
    with col1:
        store = st.sidebar.multiselect("Pick Store Type",df["StoreType"].unique())
        if not store:
            df = filtered_df.copy()
        else:
            df = filtered_df[filtered_df["StoreType"].isin(store)]
        
        customer_by_storetype = df.groupby("StoreType")["Customers"].mean()
        fig,ax=plt.subplots()
        plt.bar(customer_by_storetype.index,customer_by_storetype.values)
        plt.title("Average Customer by storetype")
        plt.xlabel("StoreType")
        plt.ylabel("Customers")
        st.pyplot(fig)
    
 #        ------------------- Sales by store type ------------------------------------ 
    with col2:
            # sales = ['a', 'b', 'c', 'd']
            sales_by_storetype = df.groupby("StoreType")["Sales"].mean()
            fig,ax=plt.subplots()
            print(sales_by_storetype)
            plt.bar(sales_by_storetype.index,sales_by_storetype.values)
            plt.title("Sales by StoreType")
            plt.xlabel("StoreType")
            plt.ylabel("Sales")
            plt.xticks(rotation = 90)
            st.pyplot(fig)
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background-color: #D8BFD8;
    }
    </style>
    """,
    unsafe_allow_html=True
)





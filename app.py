import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Page Config
# =========================
st.set_page_config(page_title="FoodRescue Analytics Hub", layout="wide")

# =========================
# Load Data (Replace with your CSV paths)
# =========================
@st.cache_data
def load_data():
    providers = pd.read_csv("providers.csv")
    receivers = pd.read_csv("receivers.csv")
    listings = pd.read_csv("listings.csv")
    claims = pd.read_csv("claims.csv")
    return providers, receivers, listings, claims

provider_df, receiver_df, listings_df, claims_df = load_data()

# =========================
# Sidebar Controls
# =========================
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    st.subheader("📍 Location Filters")
    selected_cities = st.multiselect("Select Cities", provider_df["City"].unique())
    
    st.subheader("🎯 Data Filters")
    start_date = st.date_input("Start Date", pd.to_datetime("2024-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2024-12-31"))
    
    provider_types = st.multiselect("Provider Types", provider_df["Type"].unique())
    food_types = st.multiselect("Food Types", listings_df["Food_Type"].unique())
    
    st.subheader("📊 Analysis Mode")
    analysis_mode = st.radio("Select Mode", ["Dashboard Overview", "Detailed Query Analysis", "Predictive Analytics", "Comparative Analysis"])

# =========================
# Header
# =========================
st.markdown(
    """
    <div style="padding:20px; border-radius:15px; background: linear-gradient(90deg, #6a11cb, #2575fc); text-align:center;">
        <h1 style="color:white;">🍽️ FoodRescue Analytics Hub</h1>
        <h3 style="color:white;">Advanced Food Wastage Management & Analytics Platform</h3>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("## 🔍 Advanced Query Analysis")

# =========================
# Query Selection
# =========================
categories = {
    "Provider Analysis": [
        "Q1. Providers by City",
        "Q3. Top Provider Types",
        "Q7. Provider with Maximum Contribution",
        "Q12. Avg. Food per Provider Type",
        "Q21. Provider Contribution Distribution",
        "Q25. Top 10 Providers by Contribution"
    ],
    "Receiver Analysis": [
        "Q2. Receivers by City",
        "Q10. Receiver Claiming the Most Food",
        "Q14. Receiver Type Benefiting Most",
        "Q22. Receiver Claim Distribution"
    ],
    "Listings & Food Analysis": [
        "Q5. Cities with Highest Food Listings",
        "Q6. Most Common Food Type",
        "Q15. Monthly Trend of Food Listings",
        "Q19. Listings by Category per City",
        "Q23. Food Availability Heatmap"
    ],
    "Claims & Wastage": [
        "Q8. Number of Claims per City",
        "Q9. Success Rate of Claims",
        "Q11. City Wasting the Most Food",
        "Q13. City with Highest Claim Success Rate",
        "Q17. Provider Type Wasting the Least",
        "Q24. Wastage Reduction Trend"
    ],
    "Supply vs Demand": [
        "Q18. Demand vs Supply per City",
        "Q20. Most Balanced Supply-Demand City"
    ]
}

category = st.selectbox("Select Analysis Category", list(categories.keys()))
query_choice = st.selectbox("Select Specific Query", categories[category])

# =========================
# Query Execution
# =========================
st.markdown(f"### 📊 Analysis Results: {query_choice}")

if query_choice.startswith("Q1"):
    result = provider_df.groupby("City")["Name"].count().reset_index(name="Providers")
    top = result.sort_values("Providers", ascending=False).head(15)

    col1, col2 = st.columns([2,1])
    with col1:
        fig, ax = plt.subplots(figsize=(8,5))
        sns.barplot(data=top, x="City", y="Providers", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        st.dataframe(top)

elif query_choice.startswith("Q2"):
    result = receiver_df.groupby("City")["Name"].count().reset_index(name="Receivers")
    st.dataframe(result)

elif query_choice.startswith("Q10"):
    df = claims_df.merge(receiver_df, on="Receiver_ID", how="left")
    result = df.groupby("Name")["Claim_ID"].count().reset_index(name="Claims").sort_values("Claims", ascending=False).head(10)
    st.dataframe(result)
    st.bar_chart(result.set_index("Name"))

# ⚠️ # ---------------------------
# Q3 – Q25 (drop-in handlers)
# ---------------------------

elif query_choice.startswith("Q3"):
    # Which type of food provider contributes the most food?
    df = listings_df.merge(
        provider_df[["Provider_ID", "Type"]], on="Provider_ID", how="left"
    )
    result = df.groupby("Type")["Quantity"].sum().reset_index().sort_values(
        "Quantity", ascending=False
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Type", y="Quantity", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Total Quantity by Provider Type")
    st.pyplot(fig)

elif query_choice.startswith("Q4"):
    # Contact info of food providers in a city
    df = provider_df.copy()
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    view = df[["Name", "Type", "City", "Contact", "Address"]].sort_values(["City", "Name"])
    st.dataframe(view, use_container_width=True)

elif query_choice.startswith("Q5"):
    # Cities with highest number of food listings
    df = listings_df.merge(
        provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("City")["Food_ID"].count().reset_index(name="Listings")
        .sort_values("Listings", ascending=False)
        .head(15)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Listings", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Cities by Number of Listings")
    st.pyplot(fig)

elif query_choice.startswith("Q6"):
    # Most commonly listed food type
    df = listings_df.copy()
    result = (
        df["Food_Type"].value_counts().reset_index()
        .rename(columns={"index": "Food Type", "Food_Type": "Count"})
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Food Type", y="Count", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Most Commonly Listed Food Types")
    st.pyplot(fig)

elif query_choice.startswith("Q7"):
    # Provider with maximum food contribution
    df = listings_df.merge(
        provider_df[["Provider_ID", "Name", "City"]], on="Provider_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("Name")["Quantity"].sum().reset_index()
        .sort_values("Quantity", ascending=False)
        .head(10)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Name", y="Quantity", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Providers by Total Quantity")
    st.pyplot(fig)

elif query_choice.startswith("Q8"):
    # Number of claims in each city
    df = claims_df.merge(
        receiver_df[["Receiver_ID", "City"]], on="Receiver_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("City")["Claim_ID"].count().reset_index(name="Claims")
        .sort_values("Claims", ascending=False)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Claims", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Claims by City")
    st.pyplot(fig)

elif query_choice.startswith("Q9"):
    # Success rate of claims (Completed / total)
    result = (
        claims_df["Status"].value_counts(normalize=True)
        .reset_index()
        .rename(columns={"index": "Status", "Status": "Rate"})
    )
    result["Rate"] = (result["Rate"] * 100).round(2)
    st.dataframe(result)
    fig, ax = plt.subplots()
    ax.pie(result["Rate"], labels=result["Status"], autopct="%1.1f%%")
    ax.set_title("Claim Status Distribution")
    st.pyplot(fig)

elif query_choice.startswith("Q10"):
    # Receiver claiming the most food (by claim count)
    df = claims_df.merge(
        receiver_df[["Receiver_ID", "Name", "City"]], on="Receiver_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("Name")["Claim_ID"].count().reset_index(name="Claims")
        .sort_values("Claims", ascending=False)
        .head(10)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Name", y="Claims", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Receivers by Number of Claims")
    st.pyplot(fig)

elif query_choice.startswith("Q11"):
    # City wasting the most food (listings with zero claims)
    claims_per_listing = (
        claims_df.groupby("Food_ID")["Claim_ID"].count().rename("ClaimCount")
    )
    df = listings_df.merge(claims_per_listing, on="Food_ID", how="left")
    df["ClaimCount"] = df["ClaimCount"].fillna(0)
    df = df.merge(provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left")
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    df["Unclaimed_Item"] = (df["ClaimCount"] == 0).astype(int)
    result = df.groupby("City")["Unclaimed_Item"].sum().reset_index()
    result = result.rename(columns={"Unclaimed_Item": "Unclaimed Listings"}).sort_values(
        "Unclaimed Listings", ascending=False
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Unclaimed Listings", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Unclaimed Listings by City")
    st.pyplot(fig)

elif query_choice.startswith("Q12"):
    # Average food quantity provided per provider type
    df = listings_df.merge(
        provider_df[["Provider_ID", "Type"]], on="Provider_ID", how="left"
    )
    result = df.groupby("Type")["Quantity"].mean().reset_index().sort_values(
        "Quantity", ascending=False
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Type", y="Quantity", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Average Quantity per Provider Type")
    st.pyplot(fig)

elif query_choice.startswith("Q13"):
    # City with highest average claim success rate
    df = claims_df.merge(
        receiver_df[["Receiver_ID", "City"]], on="Receiver_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("City")["Status"]
        .apply(lambda s: (s == "Completed").mean())
        .reset_index(name="Success_Rate")
        .sort_values("Success_Rate", ascending=False)
    )
    result["Success_Rate"] = (result["Success_Rate"] * 100).round(2)
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Success_Rate", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Claim Success Rate by City (%)")
    st.pyplot(fig)

elif query_choice.startswith("Q14"):
    # Receiver type benefiting the most (by claim count)
    df = claims_df.merge(
        receiver_df[["Receiver_ID", "Type", "City"]], on="Receiver_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("Type")["Claim_ID"].count().reset_index(name="Claims")
        .sort_values("Claims", ascending=False)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Type", y="Claims", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Claims by Receiver Type")
    st.pyplot(fig)

elif query_choice.startswith("Q15"):
    # Monthly trend of food listings (by Expiry month as proxy)
    df = listings_df.copy()
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
    df = df.merge(provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left")
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    df["Month"] = df["Expiry_Date"].dt.to_period("M").astype(str)
    result = df.groupby("Month")["Food_ID"].count().reset_index(name="Listings")
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=result, x="Month", y="Listings", marker="o", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Trend of Food Listings (by Expiry Month)")
    st.pyplot(fig)

elif query_choice.startswith("Q16"):
    # Monthly trend of food claims
    df = claims_df.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.merge(receiver_df[["Receiver_ID", "City"]], on="Receiver_ID", how="left")
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    df["Month"] = df["Timestamp"].dt.to_period("M").astype(str)
    result = df.groupby("Month")["Claim_ID"].count().reset_index(name="Claims")
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=result, x="Month", y="Claims", marker="o", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Trend of Claims")
    st.pyplot(fig)

elif query_choice.startswith("Q17"):
    # Provider type wasting the least (lowest share of unclaimed listings)
    claims_per_listing = (
        claims_df.groupby("Food_ID")["Claim_ID"].count().rename("ClaimCount")
    )
    df = listings_df.merge(claims_per_listing, on="Food_ID", how="left")
    df["ClaimCount"] = df["ClaimCount"].fillna(0)
    df = df.merge(provider_df[["Provider_ID", "Type"]], on="Provider_ID", how="left")
    agg = df.groupby("Type").agg(
        total_listings=("Food_ID", "count"),
        unclaimed=("ClaimCount", lambda x: (x == 0).sum()),
    )
    agg["Unclaimed_Rate"] = (agg["unclaimed"] / agg["total_listings"] * 100).round(2)
    result = agg.reset_index().sort_values("Unclaimed_Rate", ascending=True)
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Type", y="Unclaimed_Rate", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Unclaimed Listings Rate by Provider Type (%) – Lower is Better")
    st.pyplot(fig)

elif query_choice.startswith("Q18"):
    # Demand vs provider supply per city (units differ; shown side-by-side)
    supply = (
        listings_df.merge(provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left")
        .groupby("City")["Quantity"].sum()
        .reset_index(name="Supply")
    )
    demand = (
        claims_df.merge(receiver_df[["Receiver_ID", "City"]], on="Receiver_ID", how="left")
        .groupby("City")["Claim_ID"].count()
        .reset_index(name="Demand")
    )
    result = pd.merge(supply, demand, on="City", how="outer").fillna(0)
    if selected_cities:
        result = result[result["City"].isin(selected_cities)]
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    result.set_index("City")[["Supply", "Demand"]].plot(kind="bar", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Supply (Quantity) vs Demand (Claims) per City")
    st.pyplot(fig)

elif query_choice.startswith("Q19"):
    # Listings by category (Food_Type) per city
    df = listings_df.merge(
        provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby(["City", "Food_Type"])["Food_ID"].count().reset_index(name="Listings")
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Listings", hue="Food_Type", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Listings by City & Food Type")
    st.pyplot(fig)

elif query_choice.startswith("Q20"):
    # Most balanced supply-demand city (min |normalized supply - normalized demand|)
    supply = (
        listings_df.merge(provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left")
        .groupby("City")["Quantity"].sum()
        .reset_index(name="Supply")
    )
    demand = (
        claims_df.merge(receiver_df[["Receiver_ID", "City"]], on="Receiver_ID", how="left")
        .groupby("City")["Claim_ID"].count()
        .reset_index(name="Demand")
    )
    tmp = pd.merge(supply, demand, on="City", how="outer").fillna(0)
    # Min-max normalize to 0–1
    for col in ["Supply", "Demand"]:
        col_min, col_max = tmp[col].min(), tmp[col].max()
        if col_max > col_min:
            tmp[col + "_norm"] = (tmp[col] - col_min) / (col_max - col_min)
        else:
            tmp[col + "_norm"] = 0.0
    tmp["Balance_Gap"] = (tmp["Supply_norm"] - tmp["Demand_norm"]).abs()
    result = tmp.sort_values("Balance_Gap").head(10)[["City", "Supply", "Demand", "Balance_Gap"]]
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="City", y="Balance_Gap", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Most Balanced Cities (Lower Gap = Better)")
    st.pyplot(fig)

elif query_choice.startswith("Q21"):
    # Provider contribution distribution by type
    df = listings_df.merge(
        provider_df[["Provider_ID", "Type"]], on="Provider_ID", how="left"
    )
    result = df.groupby("Type")["Quantity"].sum().reset_index()
    st.dataframe(result)
    fig, ax = plt.subplots()
    ax.pie(result["Quantity"], labels=result["Type"], autopct="%1.1f%%")
    ax.set_title("Provider Contribution Distribution")
    st.pyplot(fig)

elif query_choice.startswith("Q22"):
    # Receiver claim distribution by type
    df = claims_df.merge(
        receiver_df[["Receiver_ID", "Type"]], on="Receiver_ID", how="left"
    )
    result = df.groupby("Type")["Claim_ID"].count().reset_index(name="Claims")
    st.dataframe(result)
    fig, ax = plt.subplots()
    ax.pie(result["Claims"], labels=result["Type"], autopct="%1.1f%%")
    ax.set_title("Receiver Claim Distribution")
    st.pyplot(fig)

elif query_choice.startswith("Q23"):
    # Food availability heatmap by city (sum quantity)
    df = listings_df.merge(
        provider_df[["Provider_ID", "City"]], on="Provider_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    pivot = df.pivot_table(
        index="Food_Type", columns="City", values="Quantity", aggfunc="sum", fill_value=0
    )
    st.dataframe(pivot)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt="g", cmap="YlGnBu", ax=ax)
    plt.title("Food Availability (Quantity) Heatmap")
    st.pyplot(fig)

elif query_choice.startswith("Q24"):
    # Wastage reduction trend over time (share of listings that are unclaimed)
    claims_per_listing = (
        claims_df.groupby("Food_ID")["Claim_ID"].count().rename("ClaimCount")
    )
    df = listings_df.merge(claims_per_listing, on="Food_ID", how="left").copy()
    df["ClaimCount"] = df["ClaimCount"].fillna(0)
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
    df["Month"] = df["Expiry_Date"].dt.to_period("M").astype(str)
    monthly = df.groupby("Month").agg(
        listings=("Food_ID", "count"),
        unclaimed=("ClaimCount", lambda x: (x == 0).sum()),
    ).reset_index()
    monthly["Unclaimed_Rate_%"] = (monthly["unclaimed"] / monthly["listings"] * 100).round(2)
    st.dataframe(monthly[["Month", "listings", "unclaimed", "Unclaimed_Rate_%"]])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly, x="Month", y="Unclaimed_Rate_%", marker="o", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Unclaimed Listings Rate Over Time (%)")
    st.pyplot(fig)

elif query_choice.startswith("Q25"):
    # Top 10 providers by total food contribution
    df = listings_df.merge(
        provider_df[["Provider_ID", "Name", "City"]], on="Provider_ID", how="left"
    )
    if selected_cities:
        df = df[df["City"].isin(selected_cities)]
    result = (
        df.groupby("Name")["Quantity"].sum().reset_index()
        .sort_values("Quantity", ascending=False)
        .head(10)
    )
    st.dataframe(result)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=result, x="Name", y="Quantity", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Providers by Total Quantity")
    st.pyplot(fig)



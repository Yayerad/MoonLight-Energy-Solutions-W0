# Streamlit Solar Data Dashboard with Multi-Country Support
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from scipy.stats import zscore

# File Mapping
file_mapping = {
    "Benin (Malanville)": "data/benin-malanville.csv",
    "Sierra Leone (Bumbuna)": "data/sierraleone-bumbuna.csv",
    "Togo (Dapaong)": "data/togo-dapaong_qc.csv"
}

# Sidebar - Country Selector
st.sidebar.title("Navigation")
country = st.sidebar.selectbox("Select Country", list(file_mapping.keys()))

# Load Selected Dataset
df = pd.read_csv(file_mapping[country], parse_dates=["Timestamp"])

# Navigation Options
page = st.sidebar.radio("Go to", ["Summary Statistics", "Time Series Analysis", 
                                  "Impact of Cleaning", "Correlation Analysis", 
                                  "Wind Analysis", "Z-Score Analysis", 
                                  "Histograms", "Bubble Chart"])

# Summary Statistics
if page == "Summary Statistics":
    st.header(f"Summary Statistics - {country}")
    st.write(df.describe())
    median_values = df.median()
    st.write("Median Values:")
    st.write(median_values)

# Time Series Analysis
elif page == "Time Series Analysis":
    st.header(f"Time Series Analysis - {country}")
    plt.figure(figsize=(12, 6))
    plt.plot(df["Timestamp"], df["GHI"], label="GHI", marker="o")
    plt.plot(df["Timestamp"], df["DNI"], label="DNI", marker="s")
    plt.plot(df["Timestamp"], df["DHI"], label="DHI", marker="^")
    plt.plot(df["Timestamp"], df["Tamb"], label="Tamb (Temperature)", linestyle="--")
    plt.title("Time Series: Solar Irradiance and Temperature")
    plt.xlabel("Timestamp")
    plt.ylabel("Values")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

# Impact of Cleaning
elif page == "Impact of Cleaning":
    st.header(f"Impact of Cleaning on Module Readings - {country}")
    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["ModA"], label="ModA", marker="o")
    plt.plot(df["Timestamp"], df["ModB"], label="ModB", marker="^")
    plt.title("Module Readings Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Readings")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Correlation Analysis
elif page == "Correlation Analysis":
    st.header(f"Correlation Matrix - {country}")
    correlation_matrix = df[["GHI", "DNI", "DHI", "TModA", "TModB", "WS", "WSgust"]].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    st.pyplot(plt)

# Wind Analysis
elif page == "Wind Analysis":
    st.header(f"Wind Rose Analysis - {country}")
    ax = WindroseAxes.from_ax()
    ax.bar(df["WD"], df["WS"], normed=True, opening=0.8, edgecolor="white")
    ax.set_title("Wind Rose")
    st.pyplot(ax.figure)

# Z-Score Analysis
elif page == "Z-Score Analysis":
    st.header(f"Z-Score Analysis - {country}")
    z_scores = df[["GHI", "DNI", "DHI", "Tamb"]].apply(zscore)
    outliers = (z_scores.abs() > 3).any(axis=1)
    st.write("Outlier Rows:")
    st.write(df[outliers])

# Histograms
elif page == "Histograms":
    st.header(f"Histograms of Variables - {country}")
    df[["GHI", "DNI", "DHI", "WS"]].hist(figsize=(10, 8), bins=10)
    plt.suptitle("Histograms of Solar and Wind Data")
    plt.tight_layout()
    st.pyplot(plt)

# Bubble Chart
elif page == "Bubble Chart":
    st.header(f"Bubble Chart: GHI vs. Tamb vs. WS - {country}")
    plt.figure(figsize=(10, 6))
    plt.scatter(df["GHI"], df["Tamb"], s=df["RH"] * 10, alpha=0.5, c=df["WSgust"], cmap="viridis")
    plt.colorbar(label="Wind Gust (WSgust)")
    plt.title("Bubble Chart: GHI vs. Tamb vs. WS")
    plt.xlabel("GHI")
    plt.ylabel("Tamb")
    st.pyplot(plt)

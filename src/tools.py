import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json # Used for structuring output

# --- 1. Data Summary Tool ---

def data_summary(df):
    """
    Generates a structured dictionary summary of the DataFrame including
    shape, columns, data types, missing values, descriptive stats, and 
    a sample of unique values for low-cardinality columns.
    """
    if df is None or df.empty:
        return {"error": "DataFrame is None or empty."}

    summary = {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
    }
    
    numerical_stats = df.describe(include=['number', 'datetime']).T.to_dict()
    summary["numerical_descriptive_stats"] = numerical_stats
    
    categorical_samples = {}
    MAX_UNIQUE_SAMPLES = 50 
    
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            unique_count = df[col].nunique()
            if unique_count > 0 and unique_count <= MAX_UNIQUE_SAMPLES:
                categorical_samples[col] = {
                    "unique_count": unique_count,
                    "sample_values": list(df[col].unique())
                }
            elif unique_count > MAX_UNIQUE_SAMPLES:
                categorical_samples[col] = {
                    "unique_count": unique_count,
                    "note": f"Too many unique values ({unique_count}) to list."
                }
        
    summary["categorical_metadata"] = categorical_samples
    summary["head_sample_t"] = df.head().T.to_dict()

    return summary

# --- 2. Automated EDA Tool ---

def automated_eda(df):
    """
    Performs standard Exploratory Data Analysis (EDA) on key Superstore metrics 
    and saves the resulting visualizations to files.
    """
    required_cols = ["sales", "profit", "category", "segment", "discount"]
    if not all(col in df.columns for col in required_cols):
        return {"error": "Missing required columns for EDA."}

    results = {}
    
    # Chart 1: Sales Distribution Histogram
    plt.figure(figsize=(9,6))
    plt.hist(df["sales"], bins=30, color='#1f77b4', edgecolor='black')
    plt.title("1. Sales Distribution")
    plt.xlabel("Sales Amount (USD)")
    plt.ylabel("Frequency (Count of Orders)")
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.savefig("sales_distribution.png")
    plt.close()
    results["sales_distribution_plot"] = "sales_distribution.png"

    # Chart 2: Category-wise Performance (Bar Chart)
    category_summary = df.groupby("category")[["sales", "profit"]].sum().sort_values(by="sales", ascending=False)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    category_summary["sales"].plot(kind="bar", ax=axes[0], color='#2ca02c', rot=0)
    axes[0].set_title("Total Sales by Category")
    axes[0].set_ylabel("Total Sales (USD)")
    axes[0].set_xlabel("Category")
    category_summary["profit"].plot(kind="bar", ax=axes[1], color='#d62728', rot=0)
    axes[1].set_title("Total Profit by Category")
    axes[1].set_ylabel("Total Profit (USD)")
    axes[1].set_xlabel("Category")

    plt.suptitle("2. Category Performance: Sales vs. Profit", y=1.02)
    plt.tight_layout()
    plt.savefig("category_performance.png")
    plt.close(fig) 
    results["category_performance_plot"] = "category_performance.png"

    # Chart 3: Discount vs. Profit Analysis (Scatter Plot)
    plt.figure(figsize=(9, 6))
    plt.scatter(df["discount"], df["profit"], alpha=0.6, color='#9467bd')
    plt.title("3. Impact of Discount on Profit")
    plt.xlabel("Discount Rate")
    plt.ylabel("Profit (USD)")
    plt.axhline(0, color='grey', linestyle='--', linewidth=1) 
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("discount_profit_scatter.png")
    plt.close()
    results["discount_profit_scatter_plot"] = "discount_profit_scatter.png"

    return results

# --- 3. Outlier Detection Tool ---

def check_for_outliers(df, column_name):
    """
    Detects outliers in a specified numerical column using the Interquartile Range (IQR) method.
    """
    if column_name not in df.columns or not pd.api.types.is_numeric_dtype(df[column_name]):
        return {"error": f"Column '{column_name}' not found or is not numeric."}
    
    data = df[column_name].dropna() 
    if data.empty:
        return {"error": f"Column '{column_name}' is empty after dropping NaN values."}
        
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]
    outlier_count = len(outliers)
    total_count = len(df)
    outlier_percentage = (outlier_count / total_count) * 100
    
    # Prepare results dictionary
    return {
        "column": column_name,
        "Q1": round(Q1, 2),
        "Q3": round(Q3, 2),
        "IQR": round(IQR, 2),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "outlier_count": outlier_count,
        "outlier_percentage": round(outlier_percentage, 2),
        "note": "Outliers are defined by the 1.5 * IQR rule.",
    }

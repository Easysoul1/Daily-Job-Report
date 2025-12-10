import pandas as pd
import numpy as np

# Define the path to the dataset
file_path = 'D:\\newproject\\Python\\231_projects\\python-projects-for-beginners\\iris.csv'

# (1). Load the iris dataset and display the first 10 rows
print("--- 1. Load Iris Dataset and Display First 10 Rows ---")
try:
    df = pd.read_csv(file_path)
    print(df.head(10))
except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
    exit()

# (2). Identify missing values and handle them
print("\n--- 2. Identify and Handle Missing Values ---")

# To demonstrate handling missing values, we'll first introduce some.
# In a real scenario, you would just check for existing NaNs.
df_missing = df.copy()
for col in df_missing.columns[:-1]: # Don't add NaNs to the species column
    df_missing.loc[df_missing.sample(frac=0.1).index, col] = np.nan

print("\nDataFrame with missing values introduced:")
print(df_missing.head(10))

print("\nMissing values before handling:")
print(df_missing.isnull().sum())

# Handle missing values by filling with the mean of each column
for col in df_missing.columns[:-1]:
    if df_missing[col].isnull().any():
        mean_val = df_missing[col].mean()
        df_missing[col].fillna(mean_val, inplace=True)

print("\nMissing values after handling:")
print(df_missing.isnull().sum())

print("\nDataFrame after filling missing values:")
print(df_missing.head(10))


# (3). Calculate mean, median, mode and variance of numeric columns
# We will use the original, unmodified dataframe (df) for this.
print("\n--- 3. Calculate Statistics for Numeric Columns (from original data) ---")

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    print(f"\n--- Statistics for {col} ---")
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode()[0] # Mode can return multiple values
    variance_val = df[col].var()
    
    print(f"Mean: {mean_val:.2f}")
    print(f"Median: {median_val}")
    print(f"Mode: {mode_val}")
    print(f"Variance: {variance_val:.2f}")

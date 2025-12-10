import pandas as pd
import numpy as np
import io

# 1. Load student data into pandas dataframe and display summary statistics

# Sample data with missing values
student_data = """
Name,Age,Score
Alice,20,85
Bob,22,92
Charlie,21,68
David,23,
Emily,20,75
Frank,22,95
Grace,21,
"""

# Load data into a pandas DataFrame
df = pd.read_csv(io.StringIO(student_data))

print("--- Original DataFrame ---")
print(df)

print("\n--- Summary Statistics ---")
print(df.describe())

# 2. Perform filtering to select students with scores above 70
print("\n--- Students with Scores Above 70 ---")
above_70 = df[df['Score'] > 70]
print(above_70)

# 3. Handle missing values by replacing them with the column mean

# Calculate the mean of the 'Score' column
mean_score = df['Score'].mean()

# Replace missing values with the mean
df['Score'].fillna(mean_score, inplace=True)

print("\n--- DataFrame After Handling Missing Values ---")
print(df)

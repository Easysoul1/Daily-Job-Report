import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# (1). Plot a line graph showing the growth of a savings account over 12 months
print("--- Plot 1: Savings Account Growth ---")
months = np.arange(1, 13)
savings = np.cumsum(np.random.randint(50, 200, size=12)) # Monthly savings
initial_balance = 1000
savings = initial_balance + savings

plt.figure(figsize=(10, 5))
plt.plot(months, savings, marker='o', linestyle='-')
plt.title('Savings Account Growth Over 12 Months')
plt.xlabel('Month')
plt.ylabel('Balance ($)')
plt.grid(True)
plt.xticks(months)
plt.show()

# (2). Use seaborn to plot a histogram of student exam scores
print("\n--- Plot 2: Histogram of Student Exam Scores ---")
np.random.seed(42) # for reproducibility
exam_scores = np.random.randint(50, 101, size=100)

plt.figure(figsize=(10, 6))
sns.histplot(exam_scores, bins=10, kde=True)
plt.title('Histogram of Student Exam Scores')
plt.xlabel('Score')
plt.ylabel('Number of Students')
plt.show()

# (3). Generate a heatmap of correlations in a dataset
print("\n--- Plot 3: Heatmap of Correlations ---")
# Create a sample dataset
data = {
    'Math_Score': np.random.randint(60, 100, 50),
    'Science_Score': np.random.randint(55, 95, 50),
    'Hours_Studied': np.random.randint(1, 10, 50),
    'IQ': np.random.randint(90, 140, 50)
}
df = pd.DataFrame(data)

# Add some correlation
df['Math_Score'] = df['Math_Score'] + df['Hours_Studied'] * 2
df['Science_Score'] = df['Science_Score'] + df['Hours_Studied'] * 1.5

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Generate the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap of Correlations in a Dataset')
plt.show()

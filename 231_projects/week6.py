import numpy as np

# Question 1
# Create 1D and 2D Numpy arrays and display their shape, ndim, dtype.
print("--- Question 1 ---")
# 1D Array
arr_1d = np.array([1, 2, 3, 4, 5])
print("1D Array:")
print(arr_1d)
print(f"Shape: {arr_1d.shape}")
print(f"Number of dimensions: {arr_1d.ndim}")
print(f"Data type: {arr_1d.dtype}")

print("\n" + "="*20 + "\n")

# 2D Array
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("2D Array:")
print(arr_2d)
print(f"Shape: {arr_2d.shape}")
print(f"Number of dimensions: {arr_2d.ndim}")
print(f"Data type: {arr_2d.dtype}")

# Question 2
# Perform element-wise addition and multiplication of two matrices
print("\n--- Question 2 ---")
matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

print("Matrix 1:")
print(matrix1)
print("\nMatrix 2:")
print(matrix2)

# Element-wise addition
print("\nElement-wise addition:")
print(matrix1 + matrix2)

# Element-wise multiplication
print("\nElement-wise multiplication:")
print(matrix1 * matrix2)

# Question 3
# Use numpy to generate 10 random integers between 1 and 100
print("\n--- Question 3 ---")
random_integers = np.random.randint(1, 101, 10)
print("10 random integers between 1 and 100:")
print(random_integers)

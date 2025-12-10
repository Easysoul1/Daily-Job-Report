# WEEK 2
#  Question 1
print('Question 1...')
name = input('Enter your name : ')
age = input('Enter your age : ')
print(f'Hello {name}, {age} years old. \nYou\'re welcome to CSC 231 class ')


# Question 2

print('Simple calculator...')
def num(a, b):
       operator = input('Enter the operator, + for addition, - for substraction, / for division, * for multiplication : ')
       if operator == "+":
              result = a + b
       elif operator == "-":
              result = a - b
       elif operator == "*":
              result = a * b
       elif operator == "/":
              result = a / b
       else:
              print('Invalid Operator')
       print(result)
a = int(input('Enter the first value :'))
b = int(input('Enter the second value :'))
num(a, b)


# Question 3

# Temperature conversion
print("Conversion of temperature from degreee Celsius to degree Fahrenheit and Vice versa")
temp = input("Enter your temperature \'F\' for Fahrenheit and \'C\' for Celsius : ")
if temp.upper() == "F":
       fahrenheit = float(input("Enter your Temperature in degree Fahrenheit to convert to Celsius : "))
       celsius = (fahrenheit - 32) * (5/9)
       print(f'{fahrenheit}°F = {celsius}°C')

elif temp.upper() == "C":
       celsius = float(input("Enter your Temperature in degree Celsius to convert to Fahrenheit : "))
       fahrenheit = (celsius * (9/5)) + 32
       print(f'{celsius}°C = {fahrenheit}°F')

else:
       print("Please input a valid value")
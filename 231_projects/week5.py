# Pratice Exercises
# Question 1 Week 5
# Factorial calculation using recursive function
def factorial(number):
       if number == 0 or number == 1:
              return 1
       elif number < 0:
              return "Enter a valid input greater than 1 !"
       else:
              return number * factorial(number - 1)

print(factorial(5))
print(factorial(-5))
print(factorial(1))


# Question 2
# Squared root number 
def number(s):
       print([x**2 for x in s])
number_squared = [1,2,3,4,5,6]
number(number_squared)

# Question 3

import csv

def add_student():
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    grade = input("Enter student grade: ")

    with open('students.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, grade])
    print("Student record saved successfully!")

def view_students():
    try:
        with open('students.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"Name: {row[0]}, Age: {row[1]}, Grade: {row[2]}")
    except FileNotFoundError:
        print("No student records found.")

def main():
    while True:
        print("\nStudent Record Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
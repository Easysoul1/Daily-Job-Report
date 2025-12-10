# Pratice Exercises
# Question 1 Week 3

# Number checker
num =int( input("Enter the number you want to check : "))
if num < 0:
       print(f'{num} is a Negative number')
elif num > 0 :
       print(f'{num} is a Positive number')
elif num == 0:
       print(f'{num} is Zero')
else:
       print("Please enter a number ")



# Question 2
# Grade assigning
score = int(input("Enter your score : "))
grade = ""
if score > 100 :
       print("The highest score should'nt be more than 100")
elif score >= 70:
       grade = "A"
       print(f'You got {grade}, You really tried, Keep it up!')
elif score >= 60:
       grade = "B"
       print(f'You got {grade}, Very good performance, You\'re on the right track !')
elif score >= 50:
       grade = "C"
       print(f'You got {grade}, Fair performance, You can do better')
elif score >= 45:
       grade = "D"
       print(f'You got {grade}, This grade is not good at all, Try harder')
elif score >= 40:
       grade = 'E'
       print(f'You got {grade}, Poor performance, You are at risk of failing')
elif score >= 0:
       grade = 'F'
       print(f'You got {grade}, You Failed woefully')
else:
       print('Please input a valid score')


       
# Question 3 Password Strength Checker
print("HINT: A strong password must contsains a special character,at least a number and must be at least 8 characters long ")
password = input("Enter your password : ")
password_strength = ""
special_character_checking = ",./';""][}{|~`!@#$%^&*()_+?"
number_checking = "1234567890"
contain_special_character = False
contain_number = False

for special in password:
       if special in special_character_checking:
              contain_special_character = True
              break

for number in password :
       if number in number_checking:
              contain_number = True
              break

length_checking = len(password) >= 8

if contain_number and contain_special_character and length_checking :
       password_strength = "Strong"
elif contain_special_character and contain_number or contain_number and length_checking or contain_special_character and length_checking:
       password_strength = "Medium"
else:
       password_strength = "Weak"

print(f'Password Strength {password_strength}')
if not contain_number:
       print("Suggestion: Add at least a number")
if not contain_special_character :
       print("Suggestion: Add some special character")
if not length_checking :
       print("Suggestion: Improve the length of the password")












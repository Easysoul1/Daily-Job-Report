# Question 1 Week 3
# Even number checker
import math
range_check = 50
for i in range(2, range_check + 1):
       if i % 2 == 0:
              print(i)


# Question 2
# Multiplication Table
print('This is mulyiplication table 1 - 12')
for i in range(1, 13):
       for j in range(1, 13):
              print(f'{i} * {j} = {i * j}\n')


# Question 3
# Number guess game
import random
guess_limit = 10
random_number = random.randint(1, 30)
for i in range(guess_limit + 1):
       print(f'You have {guess_limit} guesses left')
       guess = int(input('Enter the guess number from 1 to 30: '))
       if guess == random_number:
              print('You Won !')
              break
       else:
              print('Try again !')
              guess_limit -= 1
              if guess > random_number:
                     print(f'{guess} too high, try reducing it')
              elif guess < random_number :
                     print(f'{guess} too low, try increasing it')
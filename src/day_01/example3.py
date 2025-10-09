#Squares of numbers
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

#Filtering even numbers
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

#Flatten a 2D list
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6]

# Set Comprehension
# Unique first letters
words = ["apple", "banana", "apricot", "cherry"]
first_letters = {w[0] for w in words}
print(first_letters)  # {'a', 'b', 'c'}

# Dict Comprehension
# Mapping numbers to their squares
squares_dict = {x: x**2 for x in range(1, 6)}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Word lengths
words = ["apple", "banana", "cherry"]
lengths = {w: len(w) for w in words}
print(lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# Generator Expression
# Lazy evaluation (like list comprehension but with ())
gen = (x**2 for x in range(5))
print(next(gen))  # 0
print(next(gen))  # 1



# Extract emails ending with "@gmail.com"
emails = ["user1@gmail.com", "user2@yahoo.com", "admin@gmail.com"]
gmail_users = [e for e in emails if e.endswith("@gmail.com")]
print(gmail_users)  # ['user1@gmail.com', 'admin@gmail.com']
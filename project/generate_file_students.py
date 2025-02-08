import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker for random names
fake = Faker()

# Define the columns
columns = ["Student_id", "firstname", "lastname", "date_of_birth", "sex", "level", "section", "group"]

# Initialize an empty list to store student data
students = []

# Generate 100 students
for i in range(1, 101):
    student_id = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    firstname = fake.first_name()
    lastname = fake.last_name()
    date_of_birth = fake.date_of_birth(minimum_age=15, maximum_age=18).strftime('%Y-%m-%d')
    sex = random.choice(["Male", "Female"])
    level = random.choice([1, 2, 3])
    
    # Define sections based on level
    if level == 1:
        section = random.choice(["Common trunk literature", "Common trunk science and technology"])
        group = random.randint(1, 3)  # Random group from 1 to 5
    else:
        section = random.choice([
            "Experimental science", "Literature and philosophy", "Management and economy",
            "Foreign languages", "Mathematics", "Science Technology"
        ])
        group = random.randint(1, 2)  # Random group from 1 to 5
    
    
    
    # Append the student data to the list
    students.append([student_id, firstname, lastname, date_of_birth, sex, level, section, group])

# Create a DataFrame
df = pd.DataFrame(students, columns=columns)

# Save the DataFrame to an Excel file
df.to_excel("students.xlsx", index=False)

print("Excel file 'students.xlsx' has been generated successfully!")
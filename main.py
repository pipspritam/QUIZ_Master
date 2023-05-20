import sqlite3
import os

# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Retrieve the quiz data from the database
quiz_data = cursor.execute("SELECT question, option1, option2, option3, option4, correct_answer FROM quiz_table").fetchall()

# Close the database connection


# Implement the spaced repetition algorithm
score_dict = {}  # dictionary to store question scores

for question_data in quiz_data:
    question, option1, option2, option3, option4, correct_answer = question_data
    score = score_dict.get(question, 0)  # retrieve the score for the question

    # Present the question to the user and collect their response
    print(question)
    print("Options:")
    print(f"1. {option1}")
    print(f"2. {option2}")
    print(f"3. {option3}")
    print(f"4. {option4}")
    user_answer = input("Enter your answer (1-4): ")
    

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        print("Correct answer!")
        # Increment the score if the answer is correct
    else:
        print(f"Incorrect! The correct answer is {correct_answer}.")
        

    print("\n")
    # Update the score for the question in the score_dict
    score_dict[question] = score

# Print the final scores for each question
print("Question scores:")
for question, score in score_dict.items():
    print(f"{question}: {score}")

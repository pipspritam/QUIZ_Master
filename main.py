import sqlite3
import datetime
import random
import os
import platform

MAX_QUESTIONS = 5

def clear_terminal():
    # Check the operating system
    system = platform.system()

    # Clear the terminal screen based on the operating system
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")

clear_terminal()


# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


# Retrieving the quiz data from the database

time_questions = cursor.execute(
    "SELECT serial_number, question, option1, option2, option3, option4, correct_answer, time, priority FROM quiz_table ORDER BY time ASC LIMIT 13"
).fetchall()

priority_questions = cursor.execute(
    "SELECT serial_number, question, option1, option2, option3, option4, correct_answer, time, priority FROM quiz_table ORDER BY priority DESC LIMIT 12"
).fetchall()

quiz_question = ()
# Set of 10 questions based on intersection
intersection_questions = set(time_questions) & set(priority_questions)

# Select the first 5 questions from the intersection
intersection_questions = list(intersection_questions)[:5]

# Set of 3 questions based on oldest time, Sort by time and select the first 3 questions
oldest_time_questions = sorted(time_questions, key=lambda x: x[7])[:3]

# Set of 2 questions based on highest priority, Sort by priority and select the first 2 questions
highest_priority_questions = sorted(
    priority_questions, key=lambda x: x[8], reverse=True
)[:2]

# Combine the question sets
quiz_question = (
    intersection_questions + oldest_time_questions + highest_priority_questions
)


for question_data in quiz_question:
    (
        serial_number,
        question,
        correct_answer,
        option1,
        option2,
        option3,
        option4,
        time,
        priority,
    ) = question_data
    print(f"Serial Number: {serial_number}")
    print(f"Question: {question}")
    print(f"Options:")
    # print(f"1. {option1}")
    # print(f"2. {option2}")
    # print(f"3. {option3}")
    # print(f"4. {option4}")
    print(f"Correct Answer: {correct_answer}")
    print(f"Time: {time}")
    print(f"Priority: {priority}")
    print("-----------------------")

random_questions = random.sample(quiz_question, 5)

for question_data in random_questions:
    (
        serial_number,
        question,
        option1,
        option2,
        option3,
        option4,
        correct_answer,
        time,
        priority,
    ) = question_data

    # score = score_dict.get(question, 0)  # retrieve the score for the question

    # Present the question to the user and collect their response
    print(serial_number, " ", question)
    print("Options:")
    print(f"1. {option1}")
    print(f"2. {option2}")
    print(f"3. {option3}")
    print(f"4. {option4}")
    user_answer = input("Enter your answer: ")

    # Update the time for the question in the database
    updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE quiz_table SET time = ? WHERE serial_number = ?",
        (updated_time, serial_number),
    )
    connection.commit()

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        print("Correct answer!")
        # set priority to 0 once the answer is correct
        cursor.execute(
            "UPDATE quiz_table SET priority = ? WHERE serial_number = ?",
            (0, serial_number),
        )
    else:
        print(f"Incorrect! The correct answer is {correct_answer}.")
        cursor.execute(
            "UPDATE quiz_table SET priority = ? WHERE serial_number = ?",
            (priority + 1, serial_number),
        )
        connection.commit()

    print("\n")


# Close the database connection
connection.close()
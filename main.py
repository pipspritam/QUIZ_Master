import sqlite3
import datetime
import random

# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
MAX_QUESTIONS = 5
# Retrieve the quiz data from the database
quiz_data = cursor.execute(
    "SELECT serial_number, question, option1, option2, option3, option4, correct_answer, time, priority FROM quiz_table ORDER BY time ASC LIMIT 10"
).fetchall()

for question_data in quiz_data:
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

random_questions = random.sample(quiz_data, 5)
# print(random_questions)


# Implement the spaced repetition algorithm

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
        # Increment the score if the answer is correct

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

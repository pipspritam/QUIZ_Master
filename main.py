import sqlite3
import datetime
import random

# MAX_QUESTIONS = 5

# def clear_terminal():
#     # Check the operating system
#     system = platform.system()

#     # Clear the terminal screen based on the operating system
#     if system == "Windows":
#         os.system("cls")
#     else:
#         os.system("clear")

# clear_terminal()


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

oldest_time_questions = (list(time_questions)[:3])
highest_priority_questions = (list(priority_questions)[:2])

# Set of 10 questions based on intersection
intersection_questions = set((list(time_questions)[3:13])) & set(list(priority_questions)[2:12])

#select 5 random questions 
if len(intersection_questions)>=5:
    random_questions = random.sample(list(intersection_questions), 5)
else:
    intersection_questions = set((list(time_questions)[3:13])) | set(list(priority_questions)[2:12])
    random_questions = random.sample(list(intersection_questions), 5)


# Combine the question sets
quiz_question = set(
    list(random_questions) + oldest_time_questions + highest_priority_questions
)

count = 1
    
#display questions 
for question_data in quiz_question:
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

    # Present the question to the user and collect their response
    print("---------------------Question ",count, "-----------------------")
    count+=1
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
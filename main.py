import sqlite3
import datetime


# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Retrieve the quiz data from the database
quiz_data = cursor.execute("SELECT serial_number,question, option1, option2, option3, option4, correct_answer, time, priority FROM quiz_table").fetchall()


# Implement the spaced repetition algorithm
# score_dict = {}  # dictionary to store question scores

for question_data in quiz_data:
    serial_number,question, option1, option2, option3, option4, correct_answer, time,priority = question_data
    
    # score = score_dict.get(question, 0)  # retrieve the score for the question

    # Present the question to the user and collect their response
    print(question)
    print("Options:")
    print(f"1. {option1}")
    print(f"2. {option2}")
    print(f"3. {option3}")
    print(f"4. {option4}")
    user_answer = input("Enter your answer: ")
    
    # Update the time for the question in the database
    updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE quiz_table SET time = ? WHERE serial_number = ?", (updated_time, serial_number))
    connection.commit()

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        print("Correct answer!")
        # Increment the score if the answer is correct
        
    else:
        print(f"Incorrect! The correct answer is {correct_answer}.")
        cursor.execute("UPDATE quiz_table SET priority = ? WHERE serial_number = ?", (priority+1, serial_number))
        connection.commit()
        

    print("\n")
    # Update the score for the question in the score_dict
    # score_dict[question] = score

# Print the final scores for each question
    # print("Question scores:")
# for question, score in score_dict.items():
    # print(f"{question}: {score}")


# Close the database connection
connection.close()

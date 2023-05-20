from quiz_master import QuizMaster

# Create an instance of QuizMaster with the database filename
quiz_master = QuizMaster("database.db")

# Retrieve the questions
questions = quiz_master.get_questions()

# Process and display the questions
count = 1
for question_data in questions:
    quiz_master.display_question(question_data, count)
    count += 1

    user_answer = input("Enter your answer: ")

    serial_number, _, _, _, _, _, correct_answer, _, priority = question_data
    quiz_master.update_question(quiz_master.connection, serial_number, user_answer, correct_answer, priority)

    print("\n")

# Close the connection to the database
quiz_master.close_connection()

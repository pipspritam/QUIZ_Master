import sqlite3
import datetime
import random


class QuizMaster:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_questions(self):
        # Retrieve the quiz data from the database
        query = "SELECT serial_number, question, option1, option2, option3, option4, correct_answer, time, priority FROM quiz_table ORDER BY time ASC, priority DESC"
        all_questions = self.cursor.execute(query).fetchall()

        # Select 5 random questions
        selected_questions = random.sample(all_questions, 5)

        return selected_questions

    def update_question(self, serial_number, user_answer, correct_answer, priority):
        # Update the time for the question in the database
        updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "UPDATE quiz_table SET time = ? WHERE serial_number = ?",
            (updated_time, serial_number),
        )

        # Check if the user's answer is correct
        if user_answer == correct_answer:
            print("Correct answer!")
            # Set priority to 0 once the answer is correct
            self.cursor.execute(
                "UPDATE quiz_table SET priority = ? WHERE serial_number = ?",
                (0, serial_number),
            )
        else:
            print(f"Incorrect! The correct answer is {correct_answer}.")
            self.cursor.execute(
                "UPDATE quiz_table SET priority = ? WHERE serial_number = ?",
                ((priority + 1), serial_number),
            )

        self.connection.commit()

    def close_connection(self):
        self.connection.close()


def display_question(question_data, count):
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

    print("---------------------Question ", count, "-----------------------")
    count += 1
    print(serial_number, " ", question)
    print("Options:")
    print(f"1. {option1}")
    print(f"2. {option2}")
    print(f"3. {option3}")
    print(f"4. {option4}")


def main():
    database = "questions.db"
    quiz_master = QuizMaster(database)
    questions = quiz_master.get_questions()

    count = 1
    for question in questions:
        display_question(question, count)
        user_answer = input("Your answer (1/2/3/4): ").strip().lower()
        (
            serial_number,
            _,
            _,
            _,
            _,
            _,
            correct_answer,
            _,
            priority,
        ) = question
        quiz_master.update_question(serial_number, user_answer, correct_answer, priority)
        count += 1

    quiz_master.close_connection()


if __name__ == "__main__":
    main()

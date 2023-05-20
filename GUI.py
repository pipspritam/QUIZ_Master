import sqlite3
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QRadioButton,
    QMessageBox,
    QButtonGroup,
)
import datetime
from quiz_master import QuizMaster

class QuizMasterGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QuizMaster")

        # Create a central widget and set it as the main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a horizontal layout for the central widget
        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Create a vertical layout for the left side
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # Create a label for the instruction
        self.instruction_label = QLabel("Press 'Start Quiz' to begin.")
        left_layout.addWidget(self.instruction_label)

        # Create a button for starting the quiz
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)
        left_layout.addWidget(self.start_button)

        # Create a question label
        self.question_label = QLabel("")
        left_layout.addWidget(self.question_label)

        # Create radio buttons for options
        self.option1_button = QRadioButton()
        left_layout.addWidget(self.option1_button)
        self.option1_button.hide()

        self.option2_button = QRadioButton()
        left_layout.addWidget(self.option2_button)
        self.option2_button.hide()

        self.option3_button = QRadioButton()
        left_layout.addWidget(self.option3_button)
        self.option3_button.hide()

        self.option4_button = QRadioButton()
        left_layout.addWidget(self.option4_button)
        self.option4_button.hide()

        # Create a next button
        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.hide()
        left_layout.addWidget(self.next_button)

        # Create a button group to group the radio buttons
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.option1_button)
        self.button_group.addButton(self.option2_button)
        self.button_group.addButton(self.option3_button)
        self.button_group.addButton(self.option4_button)

        # Dictionary to store the question, options, and answer
        self.quiz_data = {
            "question": "",
            "options": [],
            "answer": "",
        }
        
        # Create an instance of QuizMaster with the database filename
        quiz_master = QuizMaster("database.db")

        # Retrieve the questions
        self.questions = quiz_master.get_questions()
        print(self.questions)

        # Variable to keep track of the current question index
        self.current_question_index = 0

        self.quiz_questions = []
        for question in self.questions:
            self.quiz_data["serial_number"] = question[0]
            self.quiz_data["question"] = str(question[0])+ ". "+question[1]
            self.quiz_data["options"] = [question[2], question[3], question[4], question[5]]
            self.quiz_data["answer"] = question[6]
            self.quiz_data["priority"] = question[8]

            self.quiz_questions.append(self.quiz_data.copy())
        
        # Close the connection to the database
        quiz_master.close_connection()

    def start_quiz(self):
        # Set the instruction and hide the start button
        self.instruction_label.setText("Answer the question:")
        self.start_button.hide()

        # Display the first question
        self.display_question(0)

    def display_question(self, index):
                # Set the question label and options
        self.question_label.setText(self.quiz_questions[index]["question"])
        self.option1_button.setText(self.quiz_questions[index]["options"][0])
        self.option2_button.setText(self.quiz_questions[index]["options"][1])
        self.option3_button.setText(self.quiz_questions[index]["options"][2])
        self.option4_button.setText(self.quiz_questions[index]["options"][3])

        # Clear the selection of radio buttons
        self.button_group.setExclusive(False)
        self.option1_button.setChecked(False)
        self.option2_button.setChecked(False)
        self.option3_button.setChecked(False)
        self.option4_button.setChecked(False)
        self.button_group.setExclusive(True)

        # Show the options and next button
        self.option1_button.show()
        self.option2_button.show()
        self.option3_button.show()
        self.option4_button.show()
        self.next_button.show()

    def next_question(self):
        # Check the user's answer
        selected_option = self.button_group.checkedButton()
        quiz_master = QuizMaster("database.db")
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        if selected_option is not None:
            serial_number = self.quiz_questions[self.current_question_index]["serial_number"]
            user_answer = selected_option.text()
            correct_answer = self.quiz_questions[self.current_question_index]["answer"]
            priority = self.quiz_questions[self.current_question_index]["priority"]
            # quiz_master.update_question(quiz_master.connection, serial_number, user_answer, correct_answer, priority)
            updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
            "UPDATE quiz_table SET time = ? WHERE serial_number = ?",(updated_time, serial_number))
            self.connection.commit()

        # Check if the user's answer is correct
        if user_answer == correct_answer:
            print("Correct answer!")
            # Set priority to 0 once the answer is correct
            self.cursor.execute("UPDATE quiz_table SET priority = ? WHERE serial_number = ?",(0, serial_number))
            self.connection.commit()
        else:
            print(f"Incorrect! The correct answer is {correct_answer}.")
            self.cursor.execute("UPDATE quiz_table SET priority = ? WHERE serial_number = ?",((priority + 1), serial_number))
            self.connection.commit()
            # quiz_master.close_connection()
            if selected_option.text() == self.quiz_questions[self.current_question_index]["answer"]:

                # serial_number, _, _, _, _, _, correct_answer, _, priority = question_data
                
                QMessageBox.information(self, "QuizMaster", "Correct answer!")
            else:
                QMessageBox.warning(self, "QuizMaster", "Wrong answer!")
        self.connection.close()

        # Increase the question index
        self.current_question_index += 1

        # Check if all questions have been answered
        if self.current_question_index < len(self.quiz_questions):
            # Display the next question
            self.display_question(self.current_question_index)
        else:
            # All questions answered, show quiz completion message
            QMessageBox.information(self, "QuizMaster", "Quiz completed!")

            # Reset the quiz state
            self.start_button.show()
            self.current_question_index = 0
            self.instruction_label.setText("Press 'Start Quiz' to begin.")
            self.question_label.setText("")
            self.option1_button.hide()
            self.option2_button.hide()
            self.option3_button.hide()
            self.option4_button.hide()
            self.next_button.hide()


if __name__ == "__main__":
    app = QApplication([])
    quiz_master = QuizMasterGUI()
    quiz_master.show()
    app.exec()

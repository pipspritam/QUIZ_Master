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
from QuizMasterCLI import QuizMaster


class QuizMasterGUI(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.quiz_database = QuizMaster(database)

        self.setWindowTitle("QuizMaster")
        self.create_gui_elements()
        self.load_quiz_data()

    def create_gui_elements(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.instruction_label = QLabel("Press 'Start Quiz' to begin.")
        left_layout.addWidget(self.instruction_label)

        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)
        left_layout.addWidget(self.start_button)

        self.question_label = QLabel("")
        left_layout.addWidget(self.question_label)

        self.option_buttons = []
        for i in range(4):
            option_button = QRadioButton()
            left_layout.addWidget(option_button)
            self.option_buttons.append(option_button)
            option_button.hide()

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.hide()
        left_layout.addWidget(self.next_button)

        self.button_group = QButtonGroup()
        for option_button in self.option_buttons:
            self.button_group.addButton(option_button)

    def load_quiz_data(self):
        self.quiz_questions = []
        for question in self.quiz_database.get_questions():
            serial_number, question_text, option1, option2, option3, option4, correct_answer, _, priority = question
            question_data = {
                "serial_number": serial_number,
                "question": f"{serial_number}. {question_text}",
                "options": [option1, option2, option3, option4],
                "answer": correct_answer,
                "priority": priority,
            }
            self.quiz_questions.append(question_data)

    def start_quiz(self):
        self.instruction_label.setText("Answer the question:")
        self.start_button.hide()
        self.current_question_index = 0
        self.display_question(self.current_question_index)

    def display_question(self, index):
        question_data = self.quiz_questions[index]

        self.question_label.setText(question_data["question"])

        for i, option_button in enumerate(self.option_buttons):
            option_button.setText(question_data["options"][i])

        self.clear_option_selection()
        self.show_option_buttons()
        self.show_next_button()

    def clear_option_selection(self):
        for option_button in self.option_buttons:
            option_button.setChecked(False)

    def show_option_buttons(self):
        for option_button in self.option_buttons:
            option_button.show()

    def show_next_button(self):
        self.next_button.show()

    def next_question(self):
        selected_option = self.button_group.checkedButton()

        if selected_option is not None:
            question_data = self.quiz_questions[self.current_question_index]
            serial_number = question_data["serial_number"]
            user_answer = selected_option.text()
            correct_answer = question_data["answer"]
            priority = question_data["priority"]

            self.quiz_database.update_question(
                serial_number, user_answer, correct_answer, priority
            )

            if user_answer == correct_answer:
                QMessageBox.information(self, "QuizMaster", "Correct answer!")
            else:
                QMessageBox.warning(
                    self,
                    "QuizMaster",
                    f"Wrong answer!\nCorrect answer is {correct_answer}.",
                )

        self.current_question_index += 1

        if self.current_question_index < len(self.quiz_questions):
            self.display_question(self.current_question_index)
        else:
            QMessageBox.information(self, "QuizMaster", "Quiz completed!")
            self.start_button.show()
            self.instruction_label.setText("Press 'Start Quiz' to begin.")
            self.question_label.setText("")
            self.hide_option_buttons()
            self.hide_next_button()

    def hide_option_buttons(self):
        for option_button in self.option_buttons:
            option_button.hide()

    def hide_next_button(self):
        self.next_button.hide()

    def close_connection(self):
        self.quiz_database.close_connection()


if __name__ == "__main__":
    app = QApplication([])
    database = input("Enter the name of the database (without extension): ").strip()
    quiz_gui = QuizMasterGUI(database + ".db")
    quiz_gui.show()
    app.exec()
    print("Done....")
    quiz_gui.close_connection()
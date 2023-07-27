# QuizMaster App

The QuizMaster App is an interactive quiz application developed using Python with PySide6 for the graphical user interface (GUI) and SQLite for the backend database. This app incorporates a question sorting mechanism based on question priority, which is determined by the number of times a question has been attempted incorrectly, as well as the timestamp of the last occurrence of that particular question. Additionally, the app shuffles a subset of questions based on priority, another subset based on the timestamp, and includes a set of unique questions derived from the shuffling of both sets.

<img width="441" alt="Screenshot 2023-07-27 at 11 29 12 AM" src="https://github.com/rishavnathpati/QUIZ_Master/assets/40483229/a743b4b2-4c6f-486c-888d-a559d8d89dd3">
<img width="612" alt="Screenshot 2023-07-27 at 11 30 05 AM" src="https://github.com/rishavnathpati/QUIZ_Master/assets/40483229/ede6227e-7192-407a-bcc1-dce77c22d242">
<img width="664" alt="Screenshot 2023-07-27 at 11 31 02 AM" src="https://github.com/rishavnathpati/QUIZ_Master/assets/40483229/d84b4d33-4ffe-43a5-89e8-ed91b807f112">


## Features

- User-friendly graphical user interface (GUI) developed using PySide6.
- Backend database powered by SQLite for storing and retrieving questions.
- Sorting mechanism based on question priority, determined by the number of incorrect attempts.
- Timestamp-based sorting to prioritize questions based on the last occurrence.
- Shuffling of questions based on priority, timestamp, and a combination of both.
- Unique set of questions derived from the shuffling process.

## Prerequisites

Before running the QuizMaster App, ensure you have the following:

- Python 3.8 or above installed on your system.
- PySide6 library installed. You can install it using pip:
    ```
    pip install pyside6
    ```
- SQLite database management system installed.

## Getting Started

1. Clone this repository to your local machine or download the source code as a ZIP file.
2. Open a terminal or command prompt and navigate to the project directory.
3. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Run the `GUI.py` file:
    ```
    python GUI.py
    ```
6. The QuizMaster App GUI will launch, allowing you to start using the application.

## Usage

1. Upon launching the QuizMaster App, you will be presented with the main interface.
2. Click on the "Start Quiz" button to begin the quiz.
3. The app will shuffle the questions based on their priority and timestamp.
4. Questions with higher priority indicate that the user has attempted them incorrectly more times.
5. The timestamp shuffling ensures that questions that haven't been encountered recently are included in the quiz.
6. Answer each question and click the "Next" button to proceed to the next question.
7. Once you have completed the quiz, you will receive a score and have the option to restart or exit the app.
## Customization

- You can customize the questions by modifying the SQLite database. Use any SQLite client or command-line tool to access the database file (`questions.db`) and update/add questions as needed.
- Adjust the shuffling mechanism and sorting algorithm in the code (`quizmaster.py`) based on your specific requirements.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [PySide6](https://wiki.qt.io/Qt_for_Python)
- [SQLite](https://www.sqlite.org/index.html)

Feel free to contribute, report issues, or suggest improvements. Happy quizzing!

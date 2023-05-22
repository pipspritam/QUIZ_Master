import openai
import sqlite3


class QuizQuestionGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def read_text_from_file(self, file_path):
        with open(file_path, "r") as file:
            text = file.read()
        return text

    def generate_questions(self, text):
        openai.api_key = self.api_key

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=500,
            n=10,
            stop=None,
            temperature=0.6,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        questions = []
        for choice in response.choices:
            question = {
                "question": choice["text"].strip(),
                "answer": "",
            }
            questions.append(question)

        return questions


class QuizDatabase:
    def __init__(self, dbname):
        self.dbname = dbname

    def create_table(self):
        connection = sqlite3.connect(self.dbname + ".db")
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_table (
                serial_number INTEGER PRIMARY KEY,
                question TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                option4 TEXT,
                correct_answer TEXT,
                time timestamp DEFAULT CURRENT_TIMESTAMP,
                priority INTEGER
            )
        """
        )

        connection.close()

    def insert_questions(self, questions):
        connection = sqlite3.connect(self.dbname + ".db")
        cursor = connection.cursor()

        numbering = 1
        for question in questions:
            stripped_question = question.strip()
            question_parts = stripped_question.strip("()").split(",")
            question_parts[0] = str(numbering)
            modified_question_string = "(" + ",".join(question_parts)
            cursor.execute(
                "INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority) VALUES "
                + modified_question_string.strip()
            )
            connection.commit()

            numbering += 1

        connection.close()


# Example usage
def main():
    api_key = "YOUR_OPENAI_API_KEY"
    information_file = (
        "Information.txt"
    )
    dbname = input("Enter the name of the database: ")

    generator = QuizQuestionGenerator(api_key)
    text = generator.read_text_from_file(information_file)
    prompt = """ 
    Now Create quiz questions based on the previous information and following the format below:
    The first line is the question number, followed by the question, 4 answer choices, the correct answer, and 0.
    (1, 'What is the capital of France?', 'Paris', 'London', 'Berlin', 'Madrid', 'Paris', 0);
    (2, 'Who wrote the novel "Pride and Prejudice"?', 'Jane Austen', 'Charles Dickens', 'Mark Twain', 'Leo Tolstoy', 'Jane Austen', 0);
    (3, 'What is the chemical symbol for gold?', 'Ag', 'Hg', 'Au', 'Pb', 'Au', 0);
    (4, 'What is the tallest mountain in the world?', 'Mount Kilimanjaro', 'Mount Everest', 'Mount McKinley', 'Mount Fuji', 'Mount Everest', 0);
    (5, 'What is the largest country in the world?', 'Russia', 'Canada', 'China', 'United States', 'Russia', 0);
    Do not repeat given example questions in the generated questions. Start question numbering from 1, and increment by 1 for each question like this 1, 2, 3, 4, 5 and keep going for all 10 questions.
    Give me questions with proper serial number and format. 
    """
    
    text=text+prompt
    questions = generator.generate_questions(text)

    with open("questions.txt", "w") as file:
        for i, question in enumerate(questions):
            file.write(f"{question['question']}\n")

    for i, question in enumerate(questions):
        print(f"{question['question']}")

    database = QuizDatabase(dbname)
    database.create_table()
    with open("questions.txt", "r") as file:
        questions = file.readlines()

    database.insert_questions(questions)


if __name__ == "__main__":
    main()

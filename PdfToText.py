import openai


# Function to read text from a local file
def read_text_from_file(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return text


# Function to generate questions using GPT-3
def generate_questions(text):
    openai.api_key = "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"  # Replace with your OpenAI API key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=50,
        n=15,  # Number of questions to generate
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


# Example usage
txt_file = "/Users/rishav/Developer/Python/Hackathon/QUIZ_Master/Information.txt"
prompt="  \nGive me 10 questions so that I can use them in a table with the following schema. Questions should come with 4 options and the correct option following this format: INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority)VALUES (1, 'What is the capital of France?', 'Paris', 'London', 'Berlin', 'Madrid', 'Paris',0)  "
text = read_text_from_file(txt_file)
questions = generate_questions(text+prompt)

# print(text)

# Print generated questions
for i, question in enumerate(questions):
    print(f"Question {i+1}: {question['question']}")

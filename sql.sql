-- CREATE TABLE quiz_table (
--     serial_number INTEGER PRIMARY KEY,
--     question TEXT,
--     option1 TEXT,
--     option2 TEXT,
--     option3 TEXT,
--     option4 TEXT,
--     correct_answer TEXT,
--     time timestamp DEFAULT CURRENT_TIMESTAMP,
--     priority INTEGER
-- );

-- INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority)
-- VALUES (1, 'What is the capital of France?', 'Paris', 'London', 'Berlin', 'Madrid', 'Paris', 0);

-- INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority)
-- VALUES (2, 'Who wrote the novel "Pride and Prejudice"?', 'Jane Austen', 'Charles Dickens', 'Mark Twain', 'Leo Tolstoy', 'Jane Austen', 0);

-- INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority)
-- VALUES (3, 'What is the chemical symbol for gold?', 'Ag', 'Hg', 'Au', 'Pb', 'Au', 0);

-- INSERT INTO quiz_table (serial_number, question, option1, option2, option3, option4, correct_answer, priority)
-- VALUES (4, 'What is the tallest mountain in the world?', 'Mount Kilimanjaro', 'Mount Everest', 'Mount McKinley', 'Mount Fuji', 'Mount Everest', 0);

-- -- Continue inserting the remaining 6 questions in a similar manner

SELECT * FROM quiz_table;
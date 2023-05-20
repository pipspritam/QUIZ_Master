CREATE TABLE quiz_table (
    serial_number INTEGER PRIMARY KEY,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer TEXT,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    priority INTEGER
);
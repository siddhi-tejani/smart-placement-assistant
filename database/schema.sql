CREATE DATABASE IF NOT EXISTS placement_assistant;
USE placement_assistant;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    branch VARCHAR(60),
    study_year INT
);

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(60) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'Beginner',
    description TEXT NOT NULL,
    sample_input TEXT,
    expected_output TEXT
);

CREATE TABLE attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    question_id INT NOT NULL,
    submitted_answer TEXT,
    score DECIMAL(5,2) DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);
USE placement_assistant;

INSERT INTO students (full_name, branch, study_year)
VALUES ('Demo Student', 'Computer Science', 3);

INSERT INTO questions (title, category, difficulty, description, sample_input, expected_output) VALUES
('Reverse a string', 'Strings', 'Beginner', 'Write a function that returns the reverse of a given string.', 'hello', 'olleh'),
('Palindrome check', 'Strings', 'Beginner', 'Check whether a string reads the same forwards and backwards.', 'madam', 'True'),
('Count vowels', 'Strings', 'Beginner', 'Count the number of vowels (a, e, i, o, u) in a string.', 'education', '5'),
('Largest in list', 'Lists', 'Beginner', 'Return the largest number in a list without using max().', '[3, 9, 2, 7]', '9'),
('Remove duplicates', 'Lists', 'Intermediate', 'Remove duplicate items from a list while keeping the original order.', '[1, 2, 2, 3, 1]', '[1, 2, 3]'),
('Word frequency', 'Dictionaries', 'Intermediate', 'Count how many times each word appears in a sentence.', 'the cat the dog', '{"the": 2, "cat": 1, "dog": 1}'),
('Merge dictionaries', 'Dictionaries', 'Beginner', 'Merge two dictionaries into one.', '{"a": 1}, {"b": 2}', '{"a": 1, "b": 2}'),
('Factorial function', 'Functions', 'Beginner', 'Write a function that returns the factorial of n.', '5', '120'),
('Prime number check', 'Numbers', 'Intermediate', 'Check whether a number is prime.', '17', 'True'),
('Fibonacci series', 'Numbers', 'Intermediate', 'Print the first n numbers of the Fibonacci series.', '6', '0 1 1 2 3 5');
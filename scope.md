Project Scope: Smart Placement Preparation Assistant
Task A: Minimum features
Show a list of Python questions with category and difficulty
Open one question and show its description, sample input and expected output
Let a student submit an answer or mark a question as completed
Save attempts and scores in MySQL
Progress page showing questions attempted and scores
Chatbot page that answers a fixed set of technical questions (rule-based, no paid AI)
Frontend gets all data from FastAPI using fetch(), with nothing hard-coded
Friendly messages for empty input, failed requests and missing records

Out of scope for now (optional extensions, only if time remains): admin page, timed quiz, login.

Known limitation to mention in your README: no login, so a seeded demo student (ID 1) is used.

Task B: The 10 questions
#	Title	Category	Difficulty
1	Reverse a string	Strings	Beginner
2	Palindrome check	Strings	Beginner
3	Count vowels	Strings	Beginner
4	Largest in list	Lists	Beginner
5	Remove duplicates	Lists	Intermediate
6	Word frequency	Dictionaries	Intermediate
7	Merge dictionaries	Dictionaries	Beginner
8	Factorial function	Functions	Beginner
9	Prime number check	Numbers	Intermediate
10	Fibonacci series	Numbers	Intermediate

These cover all five required categories: strings, lists, dictionaries, functions and numbers. They match the seed.sql data you’ll use in Step 3.

Task C: Screen sketches

1. Question list (questions.html)

+--------------------------------------------+
|  Smart Placement Assistant   [Home][Progress][Chatbot] |
+--------------------------------------------+
|  Python Questions                          |
|  ------------------------------------------|
|  1. Reverse a string   | Strings | Beginner |
|  2. Palindrome check   | Strings | Beginner |
|  3. Count vowels       | Strings | Beginner |
|  ...                                       |
|  (click a row to open the question)        |
+--------------------------------------------+

2. Question detail

+--------------------------------------------+
|  Reverse a string        [Strings][Beginner]|
|  Description: Write a function that ...     |
|  Sample input:    hello                     |
|  Expected output: olleh                     |
|  ------------------------------------------|
|  Your answer:                               |
|  +--------------------------------------+   |
|  |                                      |   |
|  +--------------------------------------+   |
|  [Submit Answer]  [Mark as Completed]       |
|  (message area: "Attempt saved!")           |
+--------------------------------------------+

3. Progress

+--------------------------------------------+
|  My Progress                                |
|  Questions attempted: 4                     |
|  Completed: 3                               |
|  Average score: 75                          |
|  ------------------------------------------|
|  Question          | Score | Date           |
|  Reverse a string  |  100  | 06-11-2026     |
|  Count vowels      |   50  | 06-11-2026     |
+--------------------------------------------+

4. Chatbot

+--------------------------------------------+
|  Chatbot                                    |
|  ------------------------------------------|
|  Bot: Hi! Ask me about Python, FastAPI...   |
|  You: what is fastapi?                      |
|  Bot: FastAPI is a Python framework ...     |
|  ------------------------------------------|
|  [ type your message...        ] [Send]     |
+--------------------------------------------+

Home page (index.html): a title and four links leading to Questions, Progress and Chatbot.
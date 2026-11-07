# Testing Checklist (Step 10)

Run the backend (`uvicorn main:app --reload`) and the frontend (`python -m http.server 5501`) first.
Tick each box and write what you observed. Take a screenshot for the items marked (S).

## Backend (use http://127.0.0.1:8000/docs)
- [ ] Backend starts without errors and /docs opens
- [ ] GET /questions returns 10 questions
- [ ] GET /questions?category=Strings returns 3 questions
- [ ] GET /questions/1 returns "Reverse a string"
- [ ] GET /questions/999 returns 404 "Question not found" (S)
- [ ] GET /questions/abc returns 422
- [ ] POST /attempts with {"student_id":1,"question_id":1,"submitted_answer":"olleh"} returns 201, score 100 (S)
- [ ] POST /attempts with a wrong answer returns 201, score 0
- [ ] POST /attempts with {"student_id":1,"question_id":3,"mark_completed":true} returns completed true
- [ ] POST /attempts with an empty answer returns 400
- [ ] POST /attempts with question_id 999 returns 404
- [ ] POST /attempts with student_id 99 returns 404
- [ ] GET /students/1/progress shows the right counts (S)
- [ ] GET /students/99/progress returns 404
- [ ] POST /chat {"message":"hello"} returns a greeting
- [ ] POST /chat {"message":"what is the weather"} says it has no predefined answer
- [ ] POST /chat {"message":""} returns 422

## Database (MySQL Workbench)
- [ ] `SELECT * FROM attempts;` shows the attempts you just saved
- [ ] Attempts are still there after restarting the backend

## Frontend (http://127.0.0.1:5501/index.html)
- [ ] Home page shows "Backend status: Backend is running"
- [ ] Question list loads real data from the database (S)
- [ ] Category and difficulty filters work
- [ ] Clicking a title opens the question detail page (S)
- [ ] Submitting an empty answer shows "Please type an answer"
- [ ] A correct answer shows "Correct!" and 100/100
- [ ] A wrong answer shows the attempt was saved with 0/100
- [ ] "Mark as Completed" works
- [ ] Progress page shows the new attempts (S)
- [ ] Refresh the browser: the progress is still there (data persists)
- [ ] Chatbot answers: hello, python, rest api, fastapi, mysql, interview, help (S)
- [ ] Chatbot says it has no predefined answer for an unknown question
- [ ] Empty chat input shows "Please type a message first"
- [ ] http://127.0.0.1:5501/question.html?id=999 shows "Question not found"

## Failure scenarios
- [ ] Stop the backend (Ctrl+C), refresh the question list: error "Cannot reach the server" appears (S)
- [ ] Stop the MySQL service, call GET /questions: "Database error" message, no crash
- [ ] Start everything again and confirm it recovers

## Security
- [ ] `.env` is not on GitHub and not visible in any screenshot
- [ ] No password or API key anywhere in the code
- [ ] SQL queries use %s parameters (check main.py)

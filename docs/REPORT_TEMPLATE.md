# Project Report - Smart Placement Preparation Assistant
(Short report required for submission. Fill in each section; keep it to 3-5 pages.)

## 1. Introduction
What problem does the project solve, and who is it for? (3-4 lines)

## 2. Architecture
Paste the diagram and explain each layer in one or two lines:
```
Browser (HTML + CSS + JavaScript)
   |  Fetch API: HTTP + JSON
   v
FastAPI backend (Pydantic validation, question/attempt logic, rule-based chatbot)
   |  SQL queries
   v
MySQL database
```

## 3. Database Design
Describe the tables students, questions and attempts, their columns, and the foreign keys. Explain why you added or kept each field.

## 4. API Design
List the endpoints (copy the table from README.md) and explain the status codes you used (200, 201, 400, 404, 422, 500).

## 5. Chatbot: rule-based vs Generative AI
Explain how `get_reply()` works. Explain how an LLM could replace it later, why the API key must stay on the backend, and that API use can cost money.

## 6. Testing
Summarise the checklist in docs/TESTING_CHECKLIST.md. Include 3-4 screenshots (success, 404, backend-down error).

## 7. Security
Parameterised queries, backend validation, `.env` kept out of Git, no unnecessary personal data.

## 8. Limitations and Future Work
No login, text-based answer checking, fixed chatbot topics. Future: login with hashed passwords, safe code runner, admin page, LLM chatbot.

## 9. Team Contributions
| Member | Contribution |
|--------|-------------|

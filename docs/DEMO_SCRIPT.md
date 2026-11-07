# Demonstration Script (Step 12) - about 5 minutes

## Before the demo
1. Start MySQL (check `services.msc` if needed).
2. Terminal 1: `cd backend`, activate venv, `uvicorn main:app --reload`
3. Terminal 2: `cd frontend`, `python -m http.server 5501`
4. Open http://127.0.0.1:5501/index.html
5. (Optional) clear old attempts so the demo is clean: in Workbench run `DELETE FROM attempts;`
6. Keep `.env` closed and MySQL Workbench ready in another window.

## Live walkthrough
1. **Home** - "The status line shows the frontend reached FastAPI."
2. **Questions** - "This list comes from MySQL through GET /questions." Use the Strings filter.
3. **Question detail** - open "Reverse a string". Show description and sample input/output.
4. **Submit a wrong answer, then a correct one** - "POST /attempts validates the data, checks the answer and saves it."
5. **Progress** - open the progress page: attempts, completed count, average score.
6. **Workbench** - run `SELECT * FROM attempts;` to show the rows really are in MySQL.
7. **Chatbot** - ask "hello", "What is FastAPI?", then something unknown like "weather".
8. **/docs** - show http://127.0.0.1:8000/docs and the 404 for /questions/999.

## Explain how the three layers talk (every member should be able to say this)
"The browser runs JavaScript. When I click, `fetch()` sends an HTTP request with JSON to FastAPI.
FastAPI validates the data with Pydantic, runs a parameterised SQL query on MySQL, and returns JSON.
JavaScript turns that JSON into what you see on the page."

## Questions your teacher may ask
- **Why Pydantic?** It validates request data and defines response shapes, so bad input gets a clear 422.
- **Why parameterised queries?** The `%s` placeholders keep user input separate from SQL, which prevents SQL injection.
- **Why is `.env` not on GitHub?** It holds the database password; `.gitignore` excludes it.
- **What does a foreign key do?** An attempt can only point to a student and question that exist.
- **Is the chatbot AI?** No. It is rule-based keyword matching. An LLM would generate answers; we could replace `get_reply()` with an LLM API call later.
- **What are the limitations?** No login (demo student 1), answers compared as text, fixed chatbot topics.
- **What does CORS do?** It lets the browser page on port 5501 call the API on port 8000.

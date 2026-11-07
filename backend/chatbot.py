"""Rule-based chatbot.

This is NOT Generative AI. It looks for known keywords in the message and
returns a predefined answer. To use a real LLM later, replace the body of
get_reply() with a call to an AI API (keep the API key on the backend only).
"""
import re

SUPPORTED_TOPICS = "Python, REST API, FastAPI, MySQL / database, interview"

HELP_REPLY = (
    "I can answer basic questions about: " + SUPPORTED_TOPICS + ". "
    "Try asking: 'What is FastAPI?', 'What is a REST API?', 'What is MySQL?' "
    "or 'How do I practise for an interview?'"
)

# Each rule: (keywords, reply). The FIRST rule that matches wins,
# so more specific topics are listed before general ones.
RULES = [
    (["help", "topics", "what can you do"], HELP_REPLY),
    (
        ["fastapi"],
        "FastAPI is a modern Python framework for building APIs. It is fast, "
        "uses Python type hints, validates data with Pydantic, and creates "
        "interactive documentation automatically at /docs.",
    ),
    (
        ["mysql", "database", "sql"],
        "MySQL is a relational database. Data is stored in tables made of rows "
        "and columns, and tables can be linked using primary and foreign keys. "
        "You read and write data with SQL queries such as SELECT and INSERT.",
    ),
    (
        ["rest api", "api", "rest", "http"],
        "A REST API lets programs talk to each other over HTTP, usually "
        "exchanging JSON. Common methods: GET (read data), POST (create data), "
        "PUT (update data) and DELETE (remove data).",
    ),
    (
        ["python"],
        "Python is a beginner-friendly, general-purpose programming language. "
        "It is used for web development, data science, automation and AI. "
        "It is very popular in technical interviews.",
    ),
    (
        ["interview", "placement"],
        "To practise for technical interviews: solve a few questions daily, "
        "start with strings, lists and dictionaries, explain your solution "
        "out loud, and review the questions you got wrong. Use the Questions "
        "page of this app to practise.",
    ),
    (
        ["hello", "hi", "hey"],
        "Hello! I'm the placement preparation assistant. Ask me about "
        "Python, REST APIs, FastAPI, MySQL or interview preparation. "
        "Type 'help' to see everything I can answer.",
    ),
]

FALLBACK_REPLY = (
    "Sorry, I don't have a predefined answer for that. "
    "I can help with: " + SUPPORTED_TOPICS + ". Type 'help' for examples."
)


def _contains(text: str, keyword: str) -> bool:
    # Match whole words/phrases only, so "hi" does not match inside "this".
    return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None


def get_reply(message: str) -> str:
    text = message.lower().strip()
    for keywords, reply in RULES:
        if any(_contains(text, k) for k in keywords):
            return reply
    return FALLBACK_REPLY

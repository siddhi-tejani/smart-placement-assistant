import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # reads your .env file


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@contextmanager
def db_cursor(commit=False):
    """Open a connection + cursor, and always close them afterwards.

    Usage:
        with db_cursor() as cursor:
            cursor.execute("SELECT ...", (value,))
            rows = cursor.fetchall()

    Pass commit=True for INSERT/UPDATE/DELETE so the change is saved.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            yield cursor
            if commit:
                conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()

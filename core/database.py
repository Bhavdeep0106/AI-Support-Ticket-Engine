import sqlite3
from datetime import datetime
import pytz
import os

DATABASE_PATH = "data/tickets.db"

os.makedirs("data", exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_name TEXT NOT NULL,
            customer_email TEXT,

            ticket_text TEXT NOT NULL,
            previous_contacts INTEGER DEFAULT 0,

            category TEXT,
            subcategory TEXT,
            sentiment TEXT,
            urgency TEXT,
            summary TEXT,

            priority TEXT,
            assigned_team TEXT,
            action TEXT,
            escalated INTEGER,
            decision_reason TEXT,

            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_ticket(
    customer_name,
    customer_email,
    ticket_text,
    previous_contacts,
    analysis,
    decision
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tickets (
            customer_name,
            customer_email,
            ticket_text,
            previous_contacts,

            category,
            subcategory,
            sentiment,
            urgency,
            summary,

            priority,
            assigned_team,
            action,
            escalated,
            decision_reason,

            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            customer_email,
            ticket_text,
            previous_contacts,

            analysis["category"],
            analysis["subcategory"],
            analysis["sentiment"],
            analysis["urgency"],
            analysis["summary"],

            decision["priority"],
            decision["team"],
            decision["action"],
            int(decision["escalated"]),
            decision["reason"],

            datetime.now(pytz.timezone("Asia/Kolkata")).isoformat()
        )
    )

    connection.commit()

    ticket_id = cursor.lastrowid

    connection.close()

    return ticket_id


def get_all_tickets():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        ORDER BY created_at DESC
        """
    )

    tickets = cursor.fetchall()

    connection.close()

    return tickets
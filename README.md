# AI Support Ticket Decision Engine

An AI-powered support ticket automation system that combines LLM-based ticket classification with deterministic business rules for prioritization, routing, escalation, and operational analytics.

## Problem

Support teams often spend significant time manually:

* Categorizing customer tickets
* Determining urgency
* Assigning tickets to teams
* Identifying tickets requiring escalation
* Reviewing repeated customer contacts

This project demonstrates how these decisions can be partially automated using AI and deterministic business logic.

## Architecture

```text
Customer Support Ticket
          |
          v
    Streamlit UI
          |
          v
      Groq LLM
          |
          v
  AI Classification
  - Category
  - Subcategory
  - Sentiment
  - Urgency
  - Summary
          |
          v
   Deterministic Rules
  - Priority
  - Team Assignment
  - Action
  - Escalation
          |
          v
       SQLite
          |
          v
 Operations Dashboard
```

## Features

### AI Classification

The system uses an LLM to extract structured information from unstructured customer support tickets.

It identifies:

* Category
* Subcategory
* Sentiment
* Urgency
* Summary

### Deterministic Decision Engine

Business rules convert the AI output into operational decisions.

Examples:

* High urgency + negative sentiment → Critical priority
* Multiple previous contacts → Higher priority
* Billing issue → Payments Team
* Technical issue → Technical Support
* Critical tickets → Immediate senior review
* High-priority negative tickets → Escalation

### Persistence

Analyzed tickets are stored in SQLite with:

* Customer information
* Original ticket
* AI classification
* Previous support contacts
* Priority
* Assigned team
* Recommended action
* Escalation status
* Decision reasoning
* Timestamp

### Operations Dashboard

The dashboard provides:

* Total ticket count
* Critical ticket count
* High-priority ticket count
* Escalated ticket count
* Tickets by category
* Tickets by priority
* Recent ticket history

### AI Usage Protection

The application tracks token consumption locally and applies an application-level safety threshold to prevent uncontrolled API usage.

## Tech Stack

* Python
* Streamlit
* Groq API
* LLM
* SQLite
* Deterministic Rules Engine
* REST API integration

## Project Structure

```text
ai-support-ticket-engine/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── core/
│   ├── __init__.py
│   ├── llm.py
│   ├── rules.py
│   ├── database.py
│   └── usage.py
│
└── data/
    └── tickets.db
```

## Running Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

## Example

Input:

```text
I was charged twice for my subscription and nobody has helped me.
I contacted support three times already. This is extremely frustrating.
```

The system can classify the ticket as:

```text
Category: Billing
Sentiment: Negative
Urgency: High
```

The rules engine can then determine:

```text
Priority: Critical
Team: Payments Team
Action: Immediate senior review
Escalated: Yes
```

## Future Improvements

Potential extensions include:

* Automated email notifications
* CRM integration
* SLA monitoring
* Human approval workflows
* Webhook-based ticket ingestion
* Authentication
* PostgreSQL persistence
* Advanced analytics
* Rule configuration through a UI
* Audit logs

import json
import os

from dotenv import load_dotenv
from groq import Groq

from core.usage import (
    can_make_request,
    record_usage
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are a customer support ticket classification system.

Analyze the customer's support ticket and return ONLY valid JSON.

The JSON must contain exactly these fields:

{
    "category": "...",
    "subcategory": "...",
    "sentiment": "...",
    "urgency": "...",
    "summary": "..."
}

Allowed category values:
- Billing
- Technical
- Account
- Shipping
- Product
- Other

Allowed sentiment values:
- Positive
- Neutral
- Negative

Allowed urgency values:
- Low
- Medium
- High

Keep the summary concise and factual.

Do not include markdown.
Do not include explanations outside the JSON.
"""


def analyze_ticket(ticket_text: str) -> dict:

    # Application-level safety check
    if not can_make_request():
        raise RuntimeError(
            "AI usage limit reached. "
            "Please try again later."
        )

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": ticket_text
                }
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }
        )

    except Exception as e:

        # Catch API/rate-limit/network errors
        error_message = str(e)

        if "429" in error_message:
            raise RuntimeError(
                "AI service rate limit reached. "
                "Please try again later."
            )

        raise RuntimeError(
            f"AI service error: {error_message}"
        )

    # Track actual token usage
    usage = response.usage

    if usage:
        total_tokens = usage.total_tokens
        record_usage(total_tokens)

    content = response.choices[0].message.content

    try:
        result = json.loads(content)

    except json.JSONDecodeError:
        raise RuntimeError(
            "AI returned an invalid response format."
        )

    return result
import json
import os

USAGE_FILE = "usage.json"

TOKEN_LIMIT = 1_000_000
WARNING_THRESHOLD = 0.80
BLOCK_THRESHOLD = 0.95


def load_usage():
    if not os.path.exists(USAGE_FILE):
        return {
            "total_tokens": 0,
            "total_requests": 0
        }

    with open(USAGE_FILE, "r") as file:
        return json.load(file)


def save_usage(usage):
    with open(USAGE_FILE, "w") as file:
        json.dump(usage, file, indent=2)


def can_make_request():
    usage = load_usage()

    return usage["total_tokens"] < (
        TOKEN_LIMIT * BLOCK_THRESHOLD
    )


def record_usage(tokens):
    usage = load_usage()

    usage["total_tokens"] += tokens
    usage["total_requests"] += 1

    save_usage(usage)

    return usage


def get_usage_status():
    usage = load_usage()

    tokens = usage["total_tokens"]
    percentage = (tokens / TOKEN_LIMIT) * 100

    if percentage >= BLOCK_THRESHOLD * 100:
        status = "blocked"
    elif percentage >= WARNING_THRESHOLD * 100:
        status = "warning"
    else:
        status = "normal"

    return {
        "total_tokens": tokens,
        "total_requests": usage["total_requests"],
        "percentage": percentage,
        "status": status
    }
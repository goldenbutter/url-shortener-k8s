"""
storage.py (Hybrid Version)
---------------------------
This module supports TWO storage backends:

1. In-memory dictionary (default for local testing)
2. Redis database (for Docker + Kubernetes)

You can switch between them by toggling ONE variable:
    USE_REDIS = False   # In-memory mode
    USE_REDIS = True    # Redis mode

This makes development smooth and avoids blocking you
when Redis is not installed on Windows.
"""

import os
import string
import random
from typing import Optional

# ---------------------------------------------------------
# MODE SWITCH
# ---------------------------------------------------------
# Set this to True ONLY when Redis is available (Docker/K8s)
# For now, keep it False so you can test locally.
# ---------------------------------------------------------
USE_REDIS = False


# ---------------------------------------------------------
# IN-MEMORY STORAGE (used when USE_REDIS = False)
# ---------------------------------------------------------
_url_store = {}  # simple Python dictionary


# ---------------------------------------------------------
# REDIS SETUP (used when USE_REDIS = True)
# ---------------------------------------------------------
if USE_REDIS:
    import redis  # Only import Redis if needed

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )


# ---------------------------------------------------------
# Generate a short alphanumeric code
# ---------------------------------------------------------
def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# ---------------------------------------------------------
# Save URL (works for both in-memory and Redis)
# ---------------------------------------------------------
def save_url(original_url: str) -> str:
    """
    Save the original URL and return a short code.

    Behavior:
        • If USE_REDIS = False → store in Python dictionary
        • If USE_REDIS = True  → store in Redis
    """
    short_code = generate_short_code()

    if USE_REDIS:
        # Redis storage
        redis_client.set(f"short:{short_code}", original_url)
    else:
        # In-memory storage
        _url_store[short_code] = original_url

    return short_code


# ---------------------------------------------------------
# Get URL (works for both in-memory and Redis)
# ---------------------------------------------------------
def get_url(short_code: str) -> Optional[str]:
    """
    Retrieve the original URL for a given short code.

    Behavior:
        • If USE_REDIS = False → read from dictionary
        • If USE_REDIS = True  → read from Redis
    """
    if USE_REDIS:
        return redis_client.get(f"short:{short_code}")
    else:
        return _url_store.get(short_code)
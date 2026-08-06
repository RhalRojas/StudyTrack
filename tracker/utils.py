from datetime import date, timedelta
import json
import redis
from django.conf import settings
from django.db.models import Sum


def calculate_priority_score(task):
    days_left = (task.deadline - date.today()).days

    if days_left <= 0:
        return 100 + task.estimated_effort  # overdue/due today: max urgency

    score = (task.estimated_effort * 10) / days_left
    return round(score, 2)


def calculate_streak(subject):
    session_dates = set(subject.sessions.values_list("date", flat=True))

    if not session_dates:
        return 0

    streak = 0
    current_day = date.today()

    if current_day not in session_dates:
        current_day -= timedelta(days=1)

    while current_day in session_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak
_redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)

CACHE_TTL_SECONDS = 60  # how long a cached result is considered "fresh"


def get_subject_stats(subject):
    cache_key = f"subject_stats:{subject.id}"
    cached = _redis_client.get(cache_key)

    if cached:
        data = json.loads(cached)
        data["from_cache"] = True
        return data

    total_hours = subject.sessions.aggregate(total=Sum("hours"))["total"] or 0
    streak = calculate_streak(subject)

    data = {
        "total_hours": float(total_hours),
        "streak": streak,
    }

    _redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(data))

    data["from_cache"] = False
    return data


def invalidate_subject_stats(subject):
    _redis_client.delete(f"subject_stats:{subject.id}")
    _redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)

CACHE_TTL_SECONDS = 60  # how long a cached result is considered "fresh"


def get_subject_stats(subject):
    cache_key = f"subject_stats:{subject.id}"
    cached = _redis_client.get(cache_key)

    if cached:
        data = json.loads(cached)
        data["from_cache"] = True
        return data

    total_hours = subject.sessions.aggregate(total=Sum("hours"))["total"] or 0
    streak = calculate_streak(subject)

    data = {
        "total_hours": float(total_hours),
        "streak": streak,
    }

    _redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(data))

    data["from_cache"] = False
    return data


def invalidate_subject_stats(subject):
    _redis_client.delete(f"subject_stats:{subject.id}")

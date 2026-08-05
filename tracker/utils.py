from datetime import date, timedelta


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

from datetime import datetime, time


def time_to_seconds(t: datetime | time, cutoff_hour: int = 8):
    hour = t.hour
    if hour < cutoff_hour:
        hour += 24

    return 60 * (60 * hour + t.minute) + t.second


def hour_to_seconds(hour: int, cutoff_hour: int = 8):
    if hour < cutoff_hour:
        hour += 24

    return 60 * 60 * hour

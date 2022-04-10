from datetime import datetime, timedelta, timezone


def get_time():
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    time = utc_time.astimezone(
        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    return time

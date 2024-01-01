from datetime import datetime, timezone

from src.config import DATE_TIME_FORMAT


def date_time_to_str_gmt(value: datetime) -> str:
    if not value.tzinfo:
        value = value.replace(tzinfo=timezone.utc)
    return value.strftime(DATE_TIME_FORMAT)


def str_to_date_time_gmt(value) -> datetime:
    try:
        parsed_date = datetime.strptime(value, DATE_TIME_FORMAT)
        return parsed_date
    except ValueError as e:
        raise ValueError(f"Invalid datetime format. Expected format: {DATE_TIME_FORMAT}. Error: {e}")

from datetime import datetime,timedelta
import math

def calculate_days_between(date_str1:str, date_str2:str)-> int:
    try:
        date1 = datetime.fromisoformat(date_str1)
        date2 = datetime.fromisoformat(date_str2)
    except ValueError as error:
        print(f"Please provide a valid date string.{error}")
        return None
    delta = date2 - date1
    return delta.days



print(calculate_days_between("2026-071", "2026-07-25"))


def calculate_circle_area(radius: float) -> float:
    if radius <= 0:
        raise ValueError(f"Radius must be a positive number. radius is: {radius}")

    return math.pi * (radius ** 2)



print(calculate_circle_area(-5))        